from django.shortcuts import redirect,render
from booking.models import ArtistProfile, Review, Location
# redirect to booking/index
def page_redirect(request):
    artists = ArtistProfile.objects.distinct('firstname').order_by('firstname')
    reviews = Review.objects.all()
    locations = Location.objects.distinct('name').order_by('name')
    args = {'artists': artists, 'reviews': reviews, 'locations': locations}
    return render(request, 'booking/index.html', args)

def error404(request):
    return render(request, 'booking/404_page.html')