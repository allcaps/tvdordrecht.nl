# -*- coding: utf-8 -*-
import os
from PIL import Image
from django.template import Library
from django.conf import settings

register = Library()

def crop(file, size='200x200'):
    """
    Crops an image to w x h.
    Usage: {{ image|crop:"144x144" }}
    """
    try:
        # defining the size
        w, h = [int(x) for x in size.split('x')]
        # defining the filename and the miniature filename
        file = str(file).replace('\\', '/') # windows fix
        basename, format = file.rsplit('.', 1)
        cropped = basename + '_c_' + size + '.' +  format
        cropped_filename = os.path.join(settings.MEDIA_ROOT, cropped)
        cropped_url = os.path.join(settings.MEDIA_URL, cropped)
        # if the image wasn't already resized, resize it
        if not os.path.exists(cropped_filename):
            filename = os.path.join(settings.MEDIA_ROOT, file)
            image = Image.open(filename).convert("RGBA")
            width, height = image.size
            if width < w or height < h:
                print basename, 'is to small. Minimum canvas size is ', size 
            else:
                if 1. * width / w > 1. * height / h:
                    image.thumbnail([width, h], Image.ANTIALIAS) 
                    width, height = image.size
                    x1 = (width - w) / 2
                    x2 = x1 + w
                    box = (x1, 0, x2, h)
                else:
                    image.thumbnail([w, height], Image.ANTIALIAS) 
                    width, height = image.size
                    y1 = (height - h) / 2
                    y2 = y1 + h
                    box = (0, y1, w, y2)
    
                image = image.crop(box)
                image.save(cropped_filename, image.format, quality=100)
        return cropped_url
    except:
        return ""

register.filter(crop)