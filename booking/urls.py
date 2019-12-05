from django.conf.urls import url
from booking import views


urlpatterns = [
    url('^$', views.index,name="index"),
    url('^search/$', views.search,name="search"),
    url('^detail/$', views.detail, name='detail'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.detail, name='detail_with_slug'),
    url('^checkout/$', views.checkout, name='checkout'),
    url('^blog/$', views.blog, name='blog'),
    url('^blog/blogdetail/(?P<slug>[\w-]+)/$', views.blog_detail, name='blogdetail_with_slug'),
    url('^checkout/confirm/$', views.confirm_page, name='confirm_page'),
    url('^about_us/$', views.about_us, name='about_us'),
    url('^subscribe/$', views.subscribe, name='subscribe'),
    url('^get_locations/$', views.get_locations, name='get_locations'),
    url('^review/$', views.submitReview, name='submit_review'),
    url('^(?P<slug>[\w-]+)/$',views.search_location,name="search_location")
]
