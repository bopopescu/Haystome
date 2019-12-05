from django import forms
from .models import BookingRequest, Review,ArtistProfile


class BookingForm(forms.ModelForm):
    class Meta:
        CHOICES = (('0', 'Number Of Guest'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)
        model = BookingRequest
        widgets = {'booking_date': forms.DateInput(
            attrs={'class': 'form-control datepicker', 'placeholder': 'Date', 'onchange': 'changeOption()'}),
            'guest_no': forms.Select(attrs={'class': 'form-control selectpicker guest_selecter_section',
                                            'onchange': 'changeOption()'}, choices=CHOICES),
            'service_type': forms.TextInput(),
            'total_price': forms.NumberInput()}
        exclude = ['artist']

    def __init__(self, artistProfile, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        global artistg
        artistg = artistProfile

    def save(self, commit=True):
        bookingRequest = super(BookingForm, self).save(commit=False)
        bookingRequest.service_fees = self.cleaned_data['service_fees']
        bookingRequest.transportation_fees = self.cleaned_data['transportation_fees']
        bookingRequest.booking_date = self.cleaned_data['booking_date']
        bookingRequest.booking_time = self.cleaned_data['booking_time']
        bookingRequest.guest_no = self.cleaned_data['guest_no']
        bookingRequest.subtotal_price = self.cleaned_data['subtotal_price']
        bookingRequest.total_price = self.cleaned_data['total_price']
        bookingRequest.payer_name = self.cleaned_data['payer_name']
        bookingRequest.email = self.cleaned_data['email']
        bookingRequest.phone_number = self.cleaned_data['phone_number']
        bookingRequest.language = self.cleaned_data['language']
        bookingRequest.question = self.cleaned_data['question']
        bookingRequest.pickup_location = self.cleaned_data['pickup_location']
        bookingRequest.gender = self.cleaned_data['gender']
        bookingRequest.promo_code = self.cleaned_data['promo_code']
        bookingRequest.passport_id = self.cleaned_data['passport_id']
        bookingRequest.passport_exp_date = self.cleaned_data['passport_exp_date']
        bookingRequest.artist = artistg

        if commit:
            bookingRequest.save()

        return bookingRequest

class ReviewForm(forms.ModelForm):
    class Meta:
        CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)
        LOCATION = (('PHNOM PENH', 'PHNOM PENH'), ('SIEM REAP', 'SIEM REAP'),)
        model = Review
        fields = ('reviewer_name','location','image','content','artist','star')
        widgets = {'star': forms.Select(attrs={'class': 'form-control selectpicker guest_selecter_section',
                                            'onchange': 'changeOption()'}, choices=CHOICES),
                   'reviewer_name': forms.TextInput(attrs={'class': 'form-control '}),
                   'location': forms.Select(attrs={'class': 'form-control '}, choices=LOCATION),
                   'content': forms.TextInput(attrs={'class': 'form-control '}),
                   'image': forms.FileInput(attrs={'class': 'form-control','style':'display: inline-block;width: 100%;padding: 60px 0 0 0;overflow: hidden;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;background: url("https://cdn1.iconfinder.com/data/icons/hawcons/32/698394-icon-130-cloud-upload-512.png") center center no-repeat #fff;border-radius: 20px;background-size: 60px 60px;'}),
                   }

        def save(self, commit=True):
            if commit:
                Review.save()

            return Review
