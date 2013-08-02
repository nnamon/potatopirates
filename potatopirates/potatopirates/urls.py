from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'potatopirates.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^popular/$', 'velocity.views.popular'),
    url(r'^product/(?P<pid>\d+)/othersbought/$', 'velocity.views.productothersbought'),
    url(r'^(?P<rid>[A-F0-9]+)/$', 'velocity.views.login'),
    url(r'^(?P<rid>[A-F0-9]+)/purchases/$', 'velocity.views.purchases'),
    url(r'^(?P<rid>[A-F0-9]+)/recommended/$', 'velocity.views.recommended'),
    url(r'^(?P<rid>[A-F0-9]+)/stats/$', 'velocity.views.statistics'),
    url(r'^(?P<rid>[A-F0-9]+)/purchased/$', 'velocity.views.purchased'),
)
