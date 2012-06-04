# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from mptt.managers import TreeManager
from category_product.models.defaults.productcategorybase import ProductCategoryBase

class ProductCategory(ProductCategoryBase):
    tree = TreeManager()
    
    class Meta:
        abstract = False
        app_label = 'category_product'
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categorys')  