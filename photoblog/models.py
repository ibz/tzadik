from django.db import models
from django.utils import simplejson

from photoblog.lib import flickr

class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/browse/location/%s/" % self.slug

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/browse/category/%s/" % self.slug

class Photo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    date_posted = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    description = models.TextField(blank=True)
    flickr_id = models.CharField(max_length=30)

    # we get the following properties from Flickr when the photo is saved and cache them here
    url = models.CharField(max_length=100, null=True, editable=False)
    exif_properties = models.TextField(null=True, editable=False)
    file_url = models.CharField(max_length=200, null=True, editable=False)
    thumbnail_url = models.CharField(max_length=200, null=True, editable=False)

    class Meta:
        ordering = ('-date_posted',)

    def __unicode__(self):
        return "%s %s" % (self.date_posted.strftime("%Y-%m-%d"), self.title)

    def get_absolute_url(self):
        return "/photo/%s/%s/" % (self.date_posted.strftime("%Y/%m/%d"), self.slug)

    def get_date_posted_rfc3339(self):
        return self.date_posted.strftime("%Y-%m-%dT%H:%M:%SZ")

    def get_exif_properties(self):
        return simplejson.loads(self.exif_properties)

    def save(self):
        self.url = flickr.get_photopage_url(self.flickr_id)
        self.exif_properties = simplejson.dumps(flickr.get_exif_properties(self.flickr_id))
        self.file_url, self.thumbnail_url = flickr.get_urls(self.flickr_id)
        super(Photo, self).save()

class Comment(models.Model):
    photo = models.ForeignKey(Photo, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return "%s on %s" % (self.name, self.photo)

class Page(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    content = models.TextField()
    order_rank = models.IntegerField()

    def __unicode__(self):
        return self.title

