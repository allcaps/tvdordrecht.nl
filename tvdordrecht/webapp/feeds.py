# -*- coding: utf-8 -*-
# from django.contrib.syndication.views import Feed
#
# from .models import Page, Image
#
#
# class PageEntries(Feed):
#     title = "Pagina's"
#     link = "/"
#     description = "Pagina's"
#
#     def items(self):
#         return Page.objects.filter(publish=True).order_by('-pub_date')[:30]
#
#
# class ProjectEntries(Feed):
#     title = "DordrechtDordrecht projecten"
#     link ="/projecten/"
#     description = "Project-items"
#
#     def items(self):
#         return Page.objects.filter(publish=True).order_by('-pub_date')[:30]
#
#
# def items():
#     return Image.objects.all()
#
#
# class ImageEntries(Feed):
#     title = "DordrechtDordrecht afbeeldingen"
#     link ="/"
#     description = "Afbeeldingen"
#
#     def item_link(self, obj):
#         return "http://www.dordrecht-dordrecht.nl/static/%s" %obj.image
#
#     def item_description(self, obj):
#         f, ext = str(obj).rsplit('.', 1)
#         return "<a href=http://www.dordrecht-dordrecht.nl/static/%s_t_800x2000.%s><img border='0' alt='' src='http://www.dordrechtdordrecht.nl/static/%s_t_800x2000.%s'></a>" %(f, ext, f, ext)
