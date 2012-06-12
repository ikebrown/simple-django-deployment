from django.conf import settings

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
    
urlpatterns += patterns('',
    (r'^checkout/$', include('shop_singlestep.urls')),
)
    
urlpatterns += patterns('',
    (r'^pay/', include('shop.payment.urls')),
    (r'^ship/', include('shop.shipping.urls')),
    (r'^orders/', include('shop.urls.order')),
    (r'^checkout/', include('shop.urls.checkout')),
    (r'^cart/', include('shop.urls.cart')),
)

urlpatterns += patterns('',
    url(r'^catalog/', include('category_product.urls')),
)   

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)







    


