# -*- coding: UTF-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Menu, Page

class BaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return ['/',]
    
    def location(self, obj):
        return obj 


class MenuSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Menu.objects.all().exclude(slug="home")

    def lastmod(self, obj):
        return obj.last_modified


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Page.objects.filter(publish=True)
    
    def lastmod(self, obj):
        return obj.last_modified
