import datetime
import time

from django.urls import reverse
from languages.fields import LanguageField
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


def artist_profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'artist_image/{0}{1}/profile.{2}'.format(instance.firstname, instance.surname, filename.split('.')[-1])


def artist_cover_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'artist_image/{0}{1}/cover.{2}'.format(instance.firstname, instance.surname, filename.split('.')[-1])


def artist_folio_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'artist_image/{0}{1}/folioImages/folio.{2}'.format(instance.firstname, instance.surname,
                                                              filename.split('.')[-1])

def artist_video_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'artist_image/{0}{1}/video/{2}'.format(instance.firstname, instance.surname,
                                                              filename.split('.')[-1])


def service_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'artist_image/{0}{1}/services/{2}.{3}'.format(instance.artist.firstname, instance.artist.surname,
                                                         instance.service_name, filename.split('.')[-1])


def blog_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'blog_image/{0}/{1}'.format(instance.creator_name, filename)

def location_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'location_image/{0}/{1}'.format(instance.name, filename)

def skill_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'skill_image/{0}/{1}'.format(instance.name, filename)

def review_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'review_image/{0}/{1}'.format(instance.reviewer_name, filename)



class Location(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=2000)
    cover_picture = models.ImageField(upload_to=location_directory_path, blank=False)
    slug = models.SlugField(max_length=100, blank=True)
    def get_absolute_url(self):
        return reverse("search_location", kwargs={"slug": self.slug})

    def __str__(self):
        return '%s' % (self.name)

class Skill(models.Model):
    name = models.CharField(max_length=30)
    cover_picture = models.ImageField(upload_to=skill_directory_path, blank=False)

    def __str__(self):
        return '%s' % (self.name)


# This model is a dummy model for artist
class ArtistProfile(models.Model):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    genderChoice = (('Male', 'Male'), ('Female', 'Female'))
    yearChoice = []
    for r in range(1950, (datetime.datetime.now().year + 1)):
        yearChoice.append((r, r))

    difficultyChoice = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('Extreme', 'Extreme'))

    firstname = models.CharField(max_length=30, blank=False)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=genderChoice, blank=False, default='Male')
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=False, default='+855')
    home_address_URL = models.CharField(max_length=25, blank=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, default="")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default="")
    experience_since = models.IntegerField(('year'), choices=yearChoice, default=2010, blank=False)
    work_at = models.CharField(max_length=25, blank=True)
    exp_name = models.CharField(max_length=100,blank=True)
    slug = models.SlugField(max_length=100,blank=True)
    hour = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    blocked_day = models.IntegerField(blank=False)
    available_time = ArrayField(ArrayField(models.CharField(max_length=20, blank=False)))
    amenities = ArrayField(ArrayField(models.TextField(blank=True, default='Kid Friendly (Age 2+)')))
    highlights = ArrayField(ArrayField(models.TextField(max_length=500, blank=True)))
    item_prepare = ArrayField(ArrayField(models.TextField(max_length=500, blank=True,null=True),blank=True),null=True,blank=True)
    timeline = ArrayField(ArrayField(models.TextField(max_length=500, blank=True,null=True),blank=True),null=True,blank=True)
    max_guest = models.IntegerField(blank=False)
    difficulty = models.CharField(max_length=15, choices=difficultyChoice, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    exclude_amenities = ArrayField(ArrayField(models.TextField(blank=True, default='Internet Connection', null=True)))
    transportation_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    star = models.IntegerField(default=1,
                               validators=[
                                   MaxValueValidator(5),
                                   MinValueValidator(1)
                               ]
                               )
    no_book = models.IntegerField(blank=True)
    profile_picture = models.ImageField(upload_to=artist_profile_directory_path, blank=False)
    video = models.FileField(upload_to=artist_video_directory_path,blank=True)
    cover_picture1 = models.ImageField(upload_to=artist_cover_directory_path, blank=False)
    cover_picture2 = models.ImageField(upload_to=artist_cover_directory_path, blank=False)
    cover_picture3 = models.ImageField(upload_to=artist_cover_directory_path, blank=False)
    cover_picture4 = models.ImageField(upload_to=artist_cover_directory_path, blank=False)
    story = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    description = models.TextField(blank=True)
    folioImg1 = models.ImageField(upload_to=artist_folio_directory_path, blank=False)
    folioImg2 = models.ImageField(upload_to=artist_folio_directory_path, blank=False)
    folioImg3 = models.ImageField(upload_to=artist_folio_directory_path, blank=False)
    folioImg4 = models.ImageField(upload_to=artist_folio_directory_path, blank=False)
    folioImg5 = models.ImageField(upload_to=artist_folio_directory_path, blank=True)
    folioImg6 = models.ImageField(upload_to=artist_folio_directory_path, blank=True)
    folioImg7 = models.ImageField(upload_to=artist_folio_directory_path, blank=True)
    folioImg8 = models.ImageField(upload_to=artist_folio_directory_path, blank=True)
    keywords = models.CharField(max_length=300, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % (self.fullname())

    def get_absolute_url(self):
        return reverse("detail_with_slug", kwargs={"slug": self.slug})

    def artist_id(self):
        return self.id

    def fullname(self):
        return self.firstname + ' ' + self.surname

    def get_exp_name(self):
        return self.exp_name

    def top_book(self):
        artistProfiles = ArtistProfile.objects.order_by('-no_book')[:3]
        print(artistProfiles)
        return artistProfiles

    def get_service_obj(self):
        a = service.objects.all().get(artist_id=self.id)
        return a

    def similar_exp(self):
        artistProfiles = ArtistProfile.objects.order_by('-no_book')[:3]
        return artistProfiles

    def skill_search(skill):
        artistProfiles = ArtistProfile.objects.all().filter(skill__icontains=skill)
        return artistProfiles

    def experience(self):
        return int(time.strftime("%Y")) - self.experience_since

    def booking_time(self):
        array_bookingtime = []
        for t in self.available_time:
            dataset_list = ''.join(t)
            array_bookingtime.append(dataset_list)
        return array_bookingtime

    def amenities_list(self):
        array_amenities = []
        for amenity in self.amenities:
            dataset_list = ''.join(amenity)
            array_amenities.append(dataset_list)
        return array_amenities

    def exclude_amenities_list(self):
        array_exclude_amenities = []
        for amenity in self.exclude_amenities:
            dataset_list = ''.join(amenity)
            array_exclude_amenities.append(dataset_list)
        return array_exclude_amenities

    def highlights_list(self):
        array_hightlights = []
        for hightlight in self.highlights:
            dataset_list = ''.join(hightlight)
            array_hightlights.append(dataset_list)
        return array_hightlights

    def item_prepare_list(self):
        array_item_prepare = []
        for item in self.item_prepare:
            dataset_list = ''.join(item)
            array_item_prepare.append(dataset_list)
        return array_item_prepare

    def timeline_list(self):
        array_timeline = []
        for time in self.timeline:
            dataset_list = ''.join(time)
            array_timeline.append(dataset_list)
        return array_timeline

    def guest_number(self):
        array_guestnumber = []
        for each_num in range(self.max_guest + 1):
            if each_num != 0:
                array_guestnumber.append(each_num)
        return array_guestnumber


class BlogProfile(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, blank=True)
    creator_name = models.CharField(max_length=2000, blank=False)
    image = models.ImageField(upload_to=blog_directory_path, default='')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=1000, blank=False, default='')
    content = models.TextField(max_length=20000, blank=False)
    source = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(blank=True,default=False)
    keywords = models.CharField(max_length=300,blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % (self.name)

    def get_absolute_url(self):
        return reverse('blogdetail_with_slug', kwargs={"slug": self.slug})

    def recent_blog():
        blogProfiles = BlogProfile.objects.filter(status=True).order_by('-created_time')[:3]
        return blogProfiles

class Review(models.Model):
    reviewer_name = models.CharField(max_length=30, blank=False)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=review_directory_path, default='')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=30, blank=False)
    content = models.TextField(max_length=20000, blank=False)
    star = models.IntegerField(default=1,
                               validators=[
                                   MaxValueValidator(5),
                                   MinValueValidator(1)
                               ]
                               )

    def __str__(self):
        return '%s' % (self.reviewer_name)

    def recent_review():
        review = Review.objects.order_by('-created_time')[:3]
        return review


class BookingRequest(models.Model):
    stateChoice = (('Draft', 'Draft'), ('Confirmed', 'Confirmed'), ('Cancel', 'Cancel'), ('Done', 'Done'))
    genderChoice = (('Male', 'Male'), ('Female', 'Female'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE, default="")
    service_type = models.CharField(max_length=150, blank=False)
    booking_date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
    booking_time = models.CharField(max_length=150, blank=False)
    service_fees = models.DecimalField(blank=False, decimal_places=2, max_digits=9)
    transportation_fees = models.DecimalField(blank=False, decimal_places=2, max_digits=9)
    subtotal_price = models.DecimalField(blank=False, decimal_places=2, max_digits=9)
    guest_no = models.IntegerField(blank=False)
    total_price = models.DecimalField(blank=False, decimal_places=2, max_digits=9)
    payer_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=150, blank=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, default='+855')
    language = models.CharField(max_length=100,blank=False)
    question = models.TextField(max_length=150,blank=True)
    pickup_location = models.CharField(max_length=100,blank=False)
    gender = models.CharField(max_length=6, blank=False, default='Male')
    passport_id = models.CharField(blank=False, max_length=100)
    passport_exp_date = models.CharField(max_length=11, blank=False)
    promo_code = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=15, choices=stateChoice, blank=True, default='Draft')
    remark = models.TextField(max_length=250, blank=True)
    facilitator = models.ForeignKey(User, to_field="username", db_column="username",limit_choices_to={'is_superuser': False}, on_delete=models.CASCADE,blank=True,null=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % (self.id)

    def artist_fullname(self):
        return self.artist.fullname()




class service(models.Model):
    service_name = models.CharField(max_length=30, blank=False)
    size = models.CharField(max_length=30, blank=False, default="100cm x 200cm")
    hour = models.IntegerField(blank=False)
    image = models.ImageField(upload_to=service_directory_path, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.service_name)

    def artist_fullname(self):
        return self.artist.fullname()

class subscriber_email(models.Model):
    email = models.CharField(max_length=50,blank=False)

    def __str__(self):
        return '%s' % (self.email)

