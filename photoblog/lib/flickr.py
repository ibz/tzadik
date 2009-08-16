from datetime import datetime
import urllib
import urllib2
from xml.dom import minidom

from photoblog import utils

import settings

def call(method, **params):
    response = urllib2.urlopen("http://flickr.com/services/rest?api_key=%s&method=%s&%s"
                               % (settings.FLICKR_KEY, method, urllib.urlencode(params)))
    try:
        return minidom.parse(response)
    finally:
        response.close()

def flickr_photos_getInfo(photo_id):
    dom = call('flickr.photos.getInfo', photo_id=photo_id)
    node = dom.getElementsByTagName('photo')[0]
    return {'url': utils.find(node.getElementsByTagName('url'), lambda n: n.getAttribute('type') == 'photopage').childNodes[0].nodeValue}

def flickr_photos_getSizes(photo_id):
    dom = call('flickr.photos.getSizes', photo_id=photo_id)
    return dict((node.getAttribute('label'), node.getAttribute('source')) for node in dom.getElementsByTagName('size'))

def flickr_photos_getExif(photo_id):
    def tag_name(exif_node):
        return exif_node.attributes['tag'].value
    def tag_value(exif_node):
        try:
            return exif_node.getElementsByTagName('raw')[0].childNodes[0].wholeText
        except IndexError:
            return None
    dom = call('flickr.photos.getExif', photo_id=photo_id)
    return dict((tag_name(exif), tag_value(exif)) for exif in dom.getElementsByTagName('exif'))

def get_photopage_url(photo_id):
    return flickr_photos_getInfo(photo_id)['url']

def get_urls(photo_id):
    sizes = flickr_photos_getSizes(photo_id)
    return sizes['Large'], sizes['Thumbnail']

def get_exif_properties(photo_id):
    exif = flickr_photos_getExif(photo_id)
    return {"Camera": "%s, %s" % (exif.get('Make', ""), exif.get('Model', "")),
            "Exposure time": exif.get('ExposureTime'),
            "F number": exif.get('FNumber'),
            "Focal length": exif.get('FocalLength'),
            "ISO": exif.get('ISOSpeedRatings'),
            "Flash": exif.get('Flash'),
            "Date taken": exif.get('DateTimeOriginal')}
