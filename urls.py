from django.conf.urls.defaults import *
from django.contrib import admin

from photoblog import models
from photoblog import views

import settings

admin.autodiscover()

urlpatterns = patterns('',
                       (r"^$", 'photoblog.views.index'),
                       (r"^photo/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[0-9a-z-]+)/$", 'django.views.generic.date_based.object_detail',
                        {'queryset': models.Photo.objects,
                         'template_name': "photo_view.html",
                         'template_object_name': "photo",
                         'extra_context': views.extra_context(),
                         'month_format': "%m",
                         'date_field': 'date_posted',
                         'slug_field': 'slug'}),
                       (r"^photo/(?P<id>\d+)/properties/$", 'photoblog.views.properties'),
                       (r"^photo/(?P<id>\d+)/comments/$", 'photoblog.views.comments'),
                       (r"^browse/((?P<filter_keyword>[a-z]+)/(?P<filter>[0-9a-z-]+)/)?$", 'photoblog.views.browse'),
                       (r"^categories/$", 'photoblog.views.categories'),
                       (r"^locations/$", 'photoblog.views.locations'),
                       (r"^photo/feed/$", 'photoblog.views.feed'),
                       (r"^_admin/", include(admin.site.urls)),
                       (r"^(?P<slug>.*)/$", 'django.views.generic.list_detail.object_detail',
                        {'queryset': models.Page.objects,
                         'template_name': "page_view.html",
                         'template_object_name': "page",
                         'extra_context': views.extra_context(),
                         'slug_field': 'slug'}),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r"^media/(?P<path>.*)$", 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
