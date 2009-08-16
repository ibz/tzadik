import re

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Count
from django import http
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django import template

from photoblog import models

import settings

def extra_context():
    return {'settings': settings,
            'pages': models.Page.objects.all()}

def render(template_file, request, context=None):
    if not context:
        context = {}
    context.update(extra_context())
    return render_to_response(template_file, context, context_instance=template.RequestContext(request))

def index(request):
    try:
        photo = models.Photo.objects.all()[0]
    except IndexError:
        photo = None
    return render("photo_view.html", request, {'photo': photo})

def properties(request, id):
    photo = get_object_or_404(models.Photo, id=id)
    return render("photo_properties.html", request, {'photo': photo})

def comments(request, id):
    photo = get_object_or_404(models.Photo, id=id)
    if request.method == 'GET':
        return render("photo_comments.html", request, {'photo': photo})
    elif request.method == 'POST':
        if request.POST['human'].strip().lower() == "yes":
            name = request.POST['name'].strip()
            email = request.POST['email'].strip()
            url = request.POST['url'].strip()
            text = request.POST['text'].strip()
            if not text:
                return http.HttpResponseBadRequest()
            if not name:
                name = "Anonymous"
            if not re.match(r"^.*@.*\..*$", email):
                email = ""
            if not re.match(r"^(http://)?.*\..*$", url):
                url = ""
            elif not url.startswith("http://"):
                url = "http://" + url
            comment = models.Comment(photo=photo, name=name, email=email, url=url, text=text)
            comment.save()
        return http.HttpResponse()

def browse(request, filter_keyword=None, filter=None):
    photos = models.Photo.objects

    if filter_keyword == 'category':
        photos = photos.filter(categories__slug=filter)
    elif filter_keyword == 'location':
        photos = photos.filter(location__slug=filter)

    photos = photos.all()

    paginator = Paginator(photos, 15)

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    try:
        photos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        photos = paginator.page(paginator.num_pages)

    return render("photo_browse.html", request, {'photos': photos})

def categories(request):
    categories = models.Category.objects.annotate(Count('photo'))

    return render("photo_filters.html", request, {'title': "Categories", 'filter_keyword': 'category',
                                                  'filters': categories})

def locations(request):
    locations = models.Location.objects.annotate(Count('photo'))

    return render("photo_filters.html", request, {'title': "Locations", 'filter_keyword': 'location',
                                                  'filters': locations})

def feed(request):
    photos = models.Photo.objects.all()[:20]

    return render("photo_feed.xml", request, {'photos': photos})
