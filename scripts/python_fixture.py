# coding=utf-8
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from category_product.models import Category
from shop.models import Product
from cms import api
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from decimal import Decimal
import random

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
                [ ['RC Car'], ['Legos'] ]
            ]
        ]
    ]
]

Category.objects.all().delete()
Product.objects.all().delete()

def loopit(what, below):
    for item in what:
        obj = Category(name=item[0], slug=slugify(item[0]), active=True)
        if below:
            obj.parent=below
        obj.save()
        
        if len(item) == 2:
            loopit(item[1], obj)

loopit(tree, None)
Category.tree.rebuild()

ipsum = '''
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi mattis massa rhoncus dolor imperdiet feugiat. Etiam felis enim, interdum pulvinar pharetra ut, blandit sit amet neque. Aliquam semper, nunc nec fermentum dapibus, magna risus posuere quam, vitae tincidunt neque neque eu turpis. Donec convallis posuere mi, non venenatis felis tincidunt vitae. Morbi viverra elementum felis vitae blandit. Aliquam ut elit libero. Proin a dui magna. Morbi non lobortis sapien. Aliquam felis mi, sagittis vel fringilla sed, pellentesque a neque.</p>

	<p>Suspendisse sit amet nulla ut turpis rhoncus congue eget non justo. Sed dignissim ultricies porta. Nam euismod nisi vitae nisi porttitor in pretium risus lacinia. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas eu consequat eros. Etiam ipsum metus, sollicitudin id blandit ut, placerat eget metus. Nunc mi nisi, ultricies in sodales nec, lacinia sed neque. Nulla sodales justo et sapien volutpat nec mattis sapien tristique.</p>

	<p>Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas sed arcu odio, eu sagittis risus. Vestibulum vitae lectus eu nisi imperdiet bibendum vitae ac mauris. Ut a ante eu lorem bibendum gravida quis nec elit. Suspendisse nec tellus velit. Sed at volutpat mi. Duis posuere faucibus venenatis. Proin ante diam, pharetra a vehicula vitae, tempus ac ipsum. Morbi nulla lectus, dapibus vitae sodales non, faucibus eget eros.</p>

	<p>Aenean metus mauris, mollis id ornare quis, facilisis vitae nunc. Aenean rutrum eleifend accumsan. Nulla facilisi. Suspendisse at odio nunc, mollis aliquet justo. Proin consequat condimentum nisl, tincidunt pretium mi egestas consectetur. In porta lorem ut neque rutrum tincidunt. Mauris arcu nibh, lobortis non rutrum id, tempor at massa. Nullam at faucibus ante. Integer tellus lorem, sagittis at gravida ac, pretium semper metus. Mauris sit amet justo lectus, nec convallis metus. Curabitur scelerisque nulla luctus ipsum pulvinar pharetra. Mauris semper nulla vel mauris tempor et ultrices est volutpat. Duis nibh tortor, facilisis at lobortis nec, rutrum vitae enim. Aenean tempor mi et est blandit vel vulputate erat tristique. Ut sed ligula sed nibh accumsan placerat a eget neque. Aliquam vulputate sodales congue.</p>

	<p>Nulla aliquam faucibus dictum. Donec a lectus at nisl rhoncus tincidunt ut sit amet nulla. Morbi eget dui orci, non adipiscing sapien. Suspendisse pharetra vulputate auctor. Aliquam accumsan, justo id interdum mattis, orci mi pretium est, id feugiat nisi nunc vel ante. Duis tincidunt, arcu sit amet imperdiet semper, sem elit pharetra neque, ut consectetur tortor est quis eros. Nulla eget libero non elit gravida auctor. Integer vehicula ullamcorper porta. Donec eleifend facilisis lacus nec condimentum. Pellentesque imperdiet, elit eget bibendum volutpat, neque tortor consectetur mi, a pharetra velit arcu quis purus. Nam consectetur urna felis. Suspendisse condimentum ligula eu mauris laoreet in consequat turpis imperdiet.</p>

	<p>Curabitur sagittis tellus at lectus rutrum tristique. Maecenas viverra, orci ut pulvinar placerat, elit ante suscipit odio, sit amet tempus dui risus vel justo. Quisque eget tellus lacus. Mauris sit amet neque sed nunc malesuada tempor. Aenean malesuada odio non risus interdum eu ultrices metus ornare. Morbi eleifend, diam quis bibendum porttitor, nibh mauris varius erat, ultricies luctus est enim sed diam. Proin pretium porta ornare. Fusce enim nibh, volutpat non vulputate in, dapibus vitae diam. Nulla luctus augue mattis augue ultricies tempus dictum metus malesuada. Fusce velit sem, porttitor eget vehicula in, sagittis at odio. Nullam vitae sapien non quam eleifend dapibus nec sit amet elit. Donec dapibus ultricies odio bibendum aliquet. Vivamus interdum dui in mauris pellentesque elementum. Praesent at nibh et augue facilisis consequat in sit amet libero. Maecenas id felis vel nibh pharetra cursus at sit amet nulla.</p>

	<p>Donec mattis egestas enim eu accumsan. Curabitur posuere purus mollis massa ullamcorper ac tempus mauris blandit. Sed nunc nisi, pharetra et fringilla a, vestibulum cursus metus. Etiam porttitor, purus in tempor imperdiet, ligula purus mollis felis, id tincidunt enim tellus quis nibh. Vestibulum nec mi ante. Nam dapibus nisi sed justo dignissim in euismod eros consectetur. Suspendisse tincidunt orci et eros dapibus eu ornare metus tempor. Quisque nec iaculis ligula. Quisque in vehicula turpis. Integer vehicula, dui ac lobortis vestibulum, erat augue volutpat turpis, nec tristique leo leo eget neque.</p>

	<p>Mauris vitae lectus et velit imperdiet scelerisque at id metus. Etiam viverra convallis neque, at sollicitudin orci interdum nec. Nulla purus odio, tempor non pellentesque nec, luctus eget magna. Suspendisse non erat augue, sit amet porttitor ligula. Quisque at orci ante. Aliquam vitae ligula dui. Praesent aliquam, eros nec commodo dignissim, nisi ipsum rutrum sapien, vel tincidunt tortor tellus sed velit. Quisque laoreet ipsum at risus tempus at rhoncus erat mattis. Praesent nec viverra diam. Quisque ut nisi cursus sem scelerisque rhoncus non non massa. Nunc eu leo augue, quis tristique libero. Vivamus a eros ut libero dapibus ultrices id sit amet magna. Suspendisse commodo congue mi, et varius dui vehicula sit amet. Aliquam dignissim gravida sapien, ut laoreet nibh rutrum sed.</p>

	<p>Aenean vitae adipiscing leo. Pellentesque ligula mi, scelerisque at molestie eget, lobortis porta ante. Maecenas sapien mauris, tempor et ornare nec, viverra rhoncus dui. Etiam neque lacus, hendrerit et blandit sit amet, imperdiet et turpis. Nunc elementum convallis libero in faucibus. Sed ullamcorper turpis sit amet ipsum tristique sed pretium lacus fermentum. Nunc tempus sagittis tortor, sed varius nibh sollicitudin ut. Nulla ac suscipit mauris. Fusce in sapien purus. Integer mauris est, auctor ac ultrices at, vehicula mollis justo. Duis venenatis facilisis mollis.</p>

	<p>In congue euismod nulla, id commodo odio hendrerit a. Aliquam feugiat cursus convallis. Nulla nec elit consectetur metus aliquam egestas. Pellentesque laoreet velit sed nunc posuere eget gravida magna condimentum. Duis at metus tortor, eu vestibulum dui. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In volutpat lorem vel mi interdum pretium molestie justo pulvinar. Fusce laoreet adipiscing quam, quis fermentum ante lacinia eu. Vivamus eleifend auctor turpis a dictum. Nam in purus quis diam blandit suscipit vitae in erat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Quisque eu nulla et nunc porta mollis lobortis et quam.</p>'''

lorem = ipsum.split('</p>')
for i in lorem:
    category = Category.objects.order_by('?')[0]
    name = strip_tags(i).strip()[:20]
    slug = slugify(name)
    product = Product(name=name, slug=slug, active=True, body=i, unit_price=Decimal(random.randint(50, 1000)), main_category=category, weigth_in_grams=250)
    product.save()
    product.additional_categories.add(category)