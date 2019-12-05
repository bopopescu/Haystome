from email.mime.image import MIMEImage

from django.contrib.admin.utils import flatten_fieldsets
from django.utils.text import slugify
from django.conf.urls import url
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import format_html
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from django.contrib.admin.models import LogEntry
from simple_history.admin import SimpleHistoryAdmin

from booking.models import ArtistProfile, BlogProfile, service, BookingRequest, Review, Location, Skill, subscriber_email,User
# Register your models here.
class ArtistProfileAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('id', 'fullname', 'gender', 'skill', 'location', 'work_at', 'phone_number','get_slug')

    def get_slug(self, obj):
        obj.slug = slugify(obj.exp_name)
        obj.slug = obj.slug +"-"+str(obj.pk)
        obj.save()
        return obj.slug


class BlogProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator_name','get_slug','history')
    exclude = ('slug',)

    def get_slug(self, obj):
        obj.slug = slugify(obj.name)
        obj.slug = obj.slug +"-"+str(obj.pk)
        obj.save()
        return obj.slug


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'artist_fullname', 'service_name', 'price')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name','created_time')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name','get_slug')

    def get_slug(self, obj):
        obj.slug = slugify(obj.name)
        obj.slug = obj.slug.replace("-","")
        obj.save()
        return obj.slug

class BlogProfileAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('status','keywords',)
        form = super(BlogProfileAdmin, self).get_form(request, obj, **kwargs)
        return form


class BookingRequestAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False



    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('state',)
            return list_filter
        return self.list_filter

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name='Ambassador').exists():
            fields = ('facilitator',)
            return fields
        if self.fields:
            return self.fields
        # _get_form_for_get_fields() is implemented in subclasses.
        form = self._get_form_for_get_fields(request, obj)
        return [*form.base_fields, *self.get_readonly_fields(request, obj)]




    def render_change_form(self, request, context, *args, **kwargs):
        if request.user.groups.filter(name='Ambassadorsr').exists():
            context['adminform'].form.fields['facilitator'].queryset = User.objects.filter(groups=2)
        elif request.user.groups.filter(name='Ambassadorpp').exists():
            context['adminform'].form.fields['facilitator'].queryset = User.objects.filter(groups=3)
        return super(BookingRequestAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('artist','booking_date','service_type','booking_time','service_fees','transportation_fees','subtotal_price','guest_no','total_price',
                            'payer_name','email','phone_number','language','question','pickup_location','gender','passport_id','passport_exp_date','state','remark','promo_code','keywords',)
        form = super(BookingRequestAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_list_display(self, request):
        if request.user.is_superuser:
            list_display = (
                'id', 'booking_date', 'booking_time', 'artist_fullname', 'service_type', 'guest_no', 'total_price',
                'get_artist_phone', 'promo_code',
                'remark', 'booking_actions', 'facilitator',)
            self.list_display_links = ('id',)
        elif request.user.groups.filter(name__icontains='Ambassador').exists():
            list_display = (
                'id', 'booking_date', 'booking_time', 'artist_fullname', 'service_type', 'guest_no', 'total_price',
                'pickup_location', 'language','payer_name','gender',
                'question', 'facilitator',)
            self.list_display_links = ('id',)
        else:
            list_display = (
                'booking_date', 'booking_time', 'artist_fullname', 'service_type', 'guest_no', 'total_price',
                'pickup_location', 'language', 'payer_name', 'gender',
                'question', 'facilitator',)
            self.list_display_links = (None,)
        return list_display

    def get_queryset(self, request):
        if request.user.is_superuser:
            return BookingRequest.objects.all()
        elif request.user.groups.filter(name='Ambassadorpp').exists():
            return BookingRequest.objects.filter(state='Confirmed',artist__location=2)
        elif request.user.groups.filter(name='Ambassadorsr').exists():
            return BookingRequest.objects.filter(state='Confirmed',artist__location=1)
        else:
            return BookingRequest.objects.filter(facilitator=request.user)


    def get_artist_phone(self, obj):
        return obj.artist.phone_number




    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<obj>.+)/confirm/$',
                self.admin_site.admin_view(self.process_confirm),
                name='booking-confirm',
            ),
            url(
                r'^(?P<obj>.+)/done/$',
                self.admin_site.admin_view(self.process_done),
                name='booking-done',
            ),
            url(
                r'^(?P<obj>.+)/cancel/$',
                self.admin_site.admin_view(self.process_cancel),
                name='booking-cancel',
            ),
        ]
        return custom_urls + urls

    def booking_actions(self, obj):
        booking = BookingRequest.objects.filter(pk=obj.pk)[:1].get()
        if booking.state != 'Draft':
            if booking.state == 'Confirmed':
                return format_html(
                    '<a class="button" href="{}">Done</a>&nbsp;',
                    reverse('admin:booking-done', args=[obj.pk]),
                )
            if booking.state == 'Cancel':
                return format_html(
                    '<p>Cancelled</p>'
                )
            if booking.state == 'Done':
                return format_html(
                    '<p>Done</p>'
                )

        return format_html(
            '<a class="button" href="{}">Confirm</a>&nbsp;'
            '<a class="button" href="{}">Cancel</a>',
            reverse('admin:booking-confirm', args=[obj.pk]),
            reverse('admin:booking-cancel', args=[obj.pk]),
        )

    def process_confirm(self, request, obj, *args, **kwargs):
        booking = BookingRequest.objects.filter(pk=obj)[:1].get()
        subject = 'Confirmed Experienced#' + str(booking.id)
        text_content, company_email, to, admin_email = 'Text Content', 'haystomeasia@gmail.com', booking.email, 'sopheareachte@gmail.com'
        artist_name = booking.artist.firstname + " " + booking.artist.surname
        #image = get_image(booking.artist.meet_up_location_image) get image
        context = {"username": booking.payer_name,
                   "artist_name": artist_name,
                   "hour_spend": booking.artist.hour,
                   "exp_skill": booking.artist.skill,
                   "amentities": booking.artist.amenities,
                   "booking_time": booking.booking_time,
                   "meet_up_location": booking.pickup_location,
                   "passport_id": booking.passport_id,
                   "total_fee": booking.total_price,
                   "service_type": booking.service_type,
                   "total_guest": booking.guest_no,
                   "booking_date": booking.booking_date,
                   "booking_time": booking.booking_time,
                   "booking_id": booking.id
                   }
        html_content = get_template('booking/confirmMail.html').render(context)
        msg_customer = EmailMultiAlternatives(subject, text_content, company_email, [to], [admin_email])
        msg_customer.attach_alternative(html_content, "text/html")
        msg_customer.content_subtype = "html"
        #msg_customer.attach(image) attach image
        msg_customer.send()
        booking.state = 'Confirmed'
        booking.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def process_done(self, request, obj, *args, **kwargs):
        booking = BookingRequest.objects.filter(pk=obj)[:1].get()
        subject = 'Thank You For Experienced With US'
        from_email, to, company_email = 'sopheareachte@gmail.com', booking.email, 'haystomeasia@gmail.com'
        text_content = 'Text Content'
        context = {"username": booking.payer_name}
        html_content = get_template('booking/doneMail.html').render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg1 = EmailMultiAlternatives(subject, text_content, from_email, [company_email])
        msg.attach_alternative(html_content, "text/html")
        msg1.attach_alternative(html_content, "text/html")
        print(msg)
        msg.send()
        msg1.send()
        booking.state = 'Done'
        booking.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def process_cancel(self, request, obj, *args, **kwargs):
        booking = BookingRequest.objects.filter(pk=obj)[:1].get()
        subject, from_email, to, company_email = 'Sorry For The Unavailability', 'sopheareachte@gmail.com', booking.email, 'haystomeasia@gmail.com'
        text_content = 'Text Content'
        context = {"username": booking.payer_name}
        html_content = get_template('booking/cancelMail.html').render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg1 = EmailMultiAlternatives(subject, text_content, from_email, [company_email])
        msg.attach_alternative(html_content, "text/html")
        msg1.attach_alternative(html_content, "text/html")
        print(msg)
        msg.send()
        msg1.send()
        booking.state = 'Cancel'
        booking.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    booking_actions.short_description = 'Actions'
    booking_actions.allow_tags = True
    get_artist_phone.short_description = 'artist_phone'
    get_artist_phone.admin_order_field = 'artist_phone'




def get_image(image):
    mime_image = MIMEImage(image.read())
    mime_image.add_header('Content-ID', '<image>')
    return mime_image

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message',
    )




admin.site.site_header ="Haystome Admin"
admin.site.site_title ="Haystome Admin"
admin.site.index_title = "Haystome Admin"
admin.site.register(ArtistProfile, ArtistProfileAdmin)
admin.site.register(BlogProfile, BlogProfileAdmin)
admin.site.register(service, ServiceAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Skill)
admin.site.register(subscriber_email)
admin.site.register(BookingRequest,BookingRequestAdmin)
admin.site.register(LogEntry,LogEntryAdmin)
