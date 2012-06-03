from django.conf.urls.defaults import patterns, url

from shop.views import ShopListView
from shop.views.product import ProductDetailView
from shop.models.productmodel import Product

class CategoryShopListView(ShopListView):
    
    def get_queryset(self):
        queryset = super(CategoryShopListView, self).get_queryset()
        return queryset.filter(additional_categories__path=self.kwargs['path'])

class CategoryProductDetailView(ProductDetailView):
    def get_queryset(self):
        queryset = super(CategoryProductDetailView, self).get_queryset()
        return queryset.filter(additional_categories__path=self.kwargs['path'])

urlpatterns = patterns('',
    url(r'^(?P<path>.+)/product/(?P<slug>[0-9A-Za-z-_.//]+)/$',
        CategoryProductDetailView.as_view(),
        name='product_detail'
        ),
    url(r'^(?P<path>.+)/$',
        CategoryShopListView.as_view(model=Product),
        name='product_list'
        ),
    )