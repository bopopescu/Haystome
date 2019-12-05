from audioop import reverse

from django import forms
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect

from booking.models import ArtistProfile, Review, Location, Skill, BlogProfile,subscriber_email
import json
from django.shortcuts import render, HttpResponse, redirect
from .forms import BookingForm,ReviewForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    artists = ArtistProfile.objects.distinct('firstname').order_by('firstname')
    reviews = Review.objects.all()
    locations = Location.objects.distinct('name').order_by('name')
    args = {'artists': artists, 'reviews': reviews,'locations':locations}
    return render(request, 'booking/index.html', args)


def get_locations(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        locations = Location.objects.order_by('name').filter(name__istartswith=q)
        results = []
        for location in locations:
            location_json = {}
            location_json = location.name
            results.append(location_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search(request):
    if request.method == 'GET':
        location_name = request.GET.get('location', False)
        if not Location.objects.filter(name__iexact=location_name).exists():
            return index(request)
        skill = request.GET.get('skill', False)
        #if skill == 'All Skill':
        #    skill=False
        page = request.GET.get('page', False)
        if page == False:
            page = 1
        location = Location.objects.all().filter(name__iexact=location_name)
        if skill:
            artists = ArtistProfile.objects.all().filter(location__name__iexact=location_name).order_by('no_book')
            artists = artists.filter(skill__name__iexact=skill)
            paginator = Paginator(artists, 9)
            artists = paginator.get_page(page)
        else:
            artists = ArtistProfile.objects.all().filter(location__name__iexact=location_name).order_by('no_book')
            paginator = Paginator(artists, 9)
            artists = paginator.get_page(page)
        skills = Skill.objects.all().order_by('name')
        recent_reviews = Review.recent_review()
        reviews = Review.objects.all()
        if skill:
            args = {'artists': artists, 'reviews': reviews, 'location': location, 'skills': skills, 'skill': skill,
                    'recent_reviews': recent_reviews}
        else:
            args = {'artists': artists, 'reviews': reviews, 'location': location, 'skills': skills,
                    'recent_reviews': recent_reviews}
        return render(request, 'booking/search result.html', args)

def search_location(request,slug=None):
    if slug:
        page = 1
        if Location.objects.filter(slug=slug).exists():
            location = Location.objects.all().filter(slug=slug)
            artists = ArtistProfile.objects.all().filter(location__slug=slug).order_by('no_book')
            paginator = Paginator(artists, 9)
            artists = paginator.get_page(page)
            skills = Skill.objects.all().order_by('name')
            recent_reviews = Review.recent_review()
            reviews = Review.objects.all()
            args = {'artists': artists, 'reviews': reviews, 'location': location, 'skills':skills,'recent_reviews':recent_reviews}
            return render(request,'booking/search result.html',args)
        else:
            return index(request)

def detail(request, slug=None):
    if slug:
        artistProfile = ArtistProfile.objects.get(slug=slug)
        services = artistProfile.service_set.all().order_by('price')
        artists = ArtistProfile.objects.all().exclude(slug=slug).order_by('no_book')
        reviews = Review.objects.all().filter(artist__exp_name__iexact=artistProfile.exp_name).order_by('created_time')
        if request.method == 'POST':
            form = BookingForm(artistProfile=artistProfile, data=request.POST)
            if form.is_valid():
                BookingRequest = form.save(commit=False)
                if request.POST.get('options') == "on":
                    artistProfile.no_book += BookingRequest.guest_no
                    artistProfile.save()
                    BookingRequest.save()
                    send_mail(BookingRequest)
                    return redirect('/booking/checkout/confirm/')
                else:
                    args = {'BookingRequest': BookingRequest}
                    return render(request, 'booking/checkout.html', args)
            else:
                print(form.errors)
                return 0;
        else:
            form = BookingForm(artistProfile=artistProfile)
        args = {'artistProfile': artistProfile, 'services': services, 'form': form,'artists':artists,'reviews':reviews}
        return render(request, 'booking/detail.html', args)

def blog(request):
    blogProfiles = BlogProfile.objects.filter(status=True).order_by('-created_time')
    recentBlogProfiles = BlogProfile.recent_blog()
    args = {'blogProfiles': blogProfiles, 'recentBlogProfiles': recentBlogProfiles}
    return render(request, 'booking/blog_list.html', args)


def blog_detail(request, slug=None):
    if slug:
        blogProfile = BlogProfile.objects.get(slug=slug)
        recentBlogProfiles = BlogProfile.recent_blog()
        args = {'blogProfile': blogProfile, 'recentBlogProfiles': recentBlogProfiles}
    return render(request, 'booking/blog_single.html', args)


def send_mail(BookingRequest):
    subject = 'Requested Experience#' + str(BookingRequest.id)
    text_content, company_email, to, admin_email = 'Text Content', 'haystomeasia@gmail.com', BookingRequest.email, 'haystomeasia@gmail.com'
    context = {"username": BookingRequest.payer_name,
               "booking_id": BookingRequest.id,
               "booking_date": BookingRequest.booking_date,
               "booking_time": BookingRequest.booking_time,
               "artist_name": BookingRequest.artist.firstname + ' ' + BookingRequest.artist.surname,
               "exp_skill": BookingRequest.artist.skill,
               "service_type": BookingRequest.service_type,
               "total_guest": BookingRequest.guest_no,
               "cus_email": BookingRequest.email,
               "cus_lang": BookingRequest.language,
               "passport_id": BookingRequest.passport_id,
               "passport_expr": BookingRequest.passport_exp_date,
               "total_fee": BookingRequest.total_price,
               "meet_up_location":BookingRequest.pickup_location}

    html_content_admin = get_template('booking/adminEmail.html').render(context)
    msg_admin = EmailMultiAlternatives(subject, text_content, company_email, [admin_email])
    msg_admin.attach_alternative(html_content_admin, "text/html")
    msg_admin.content_subtype = "html"
    msg_admin.send()

    html_content_customer = get_template('booking/recieptMail.html').render(context)
    msg_customer = EmailMultiAlternatives(subject, text_content, company_email, [to])
    msg_customer.attach_alternative(html_content_customer, "text/html")
    msg_customer.content_subtype = "html"
    msg_customer.send()

def checkout(request):
    return render(request, 'booking/checkout.html')

def confirm_page(request):
    return render(request, 'booking/confirm.html')

def about_us(request):
    return render(request, 'booking/about_us.html')

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        subscriber_email.objects.create(
            email = email
        )
        return HttpResponse('')

def submitReview(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return index(request)
    form = ReviewForm()
    form.fields['artist'] = ArtistModelChoiceField(queryset=ArtistProfile.objects.all(),initial=2,empty_label=None,widget=forms.Select(attrs={'class':'form-control'}))
    return render(request, 'booking/review.html', {'form': form})

class ArtistModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_exp_name()