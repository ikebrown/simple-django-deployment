# coding=utf-8
from django.contrib.sites.models import Site

try:
   site = Site.objects.get(pk=1)   
except Site.DoesNotExist:
   site = Site()

site.domain='%(servername)s'
site.name='%(project_name)s'

site.save()

from django.contrib.auth.models import User
from cms import api
user = User.objects.get(pk=1)
home_page = api.create_page('Home', 'base_templates/front.html', 'en', menu_title='Home', created_by=user, in_navigation=True, published=True)
api.create_title('nb', 'Hjem', home_page, menu_title='Hjem')
search_page = api.create_page('Search', 'base_templates/default.html', 'en', menu_title='Search', apphook='DjangoCmsFacetedSearchApphook', created_by=user, in_navigation=True, published=True, reverse_id='search')
api.create_title('nb', 'Søk', search_page, menu_title='Søk', slug='sok', apphook='DjangoCmsFacetedSearchApphook')