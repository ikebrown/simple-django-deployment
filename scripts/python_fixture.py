# coding=utf-8
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from category_product.models import ProductCategory
from cms import api

User.objects.create_superuser('%(db_user)s', '%(db_user)s@%(servername)s', '%(db_password)s')

try:
   site = Site.objects.get(pk=1)   
except Site.DoesNotExist:
   site = Site()

site.domain='%(servername)s'
site.name='%(project_name)s'
site.save()

user = User.objects.get(pk=1)
home_page = api.create_page('Home', 'base_templates/default.html', 'en', menu_title='Home', created_by=user, in_navigation=True, published=True)
api.create_title('nb', 'Hjem', home_page, menu_title='Hjem')
search_page = api.create_page('Search', 'base_templates/default.html', 'en', menu_title='Search', apphook='DjangoCmsFacetedSearchApphook', created_by=user, in_navigation=True, published=True, reverse_id='search')
api.create_title('nb', 'Søk', search_page, menu_title='Søk', slug='sok', apphook='DjangoCmsFacetedSearchApphook')

tree = [
    [ 'Transportation', 
        [   [ 'Bicycle'], 
            [ 'Car',
                [
                   ['Van'], ['SUV']
                ]
            ]
        ]
    ],
    [ 'Gifts', 
        [   [ 'For him',
                [ ['Stereo'], ['Big screen TV'] ]
            ],
            [ 'For her',
                [ ['Jewlery'], ['Lingerie'] ]
            ],
            [ 'For kids',
                [ ['RC Car'], ['Legos'] ] # wrong place, why beats me..
            ]
        ]
    ]
]

def loopit(what, below):
    for item in what:
        obj = ProductCategory(name=item[0], slug=slugify(item[0]), active=True)
        if below:
            obj.parent=below
        obj.save()
        
        if len(item) == 2:
            loopit(item[1], obj)

loopit(tree, None)
ProductCategory.tree.rebuild()