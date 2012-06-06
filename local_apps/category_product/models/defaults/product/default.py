# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from category_product.models.defaults.categoryproductbase import CategoryProductBase
        
class CategoryProduct(CategoryProductBase):     
    
    class Meta:
        abstract = False
        app_label = 'category_product'
        verbose_name = _('Category Product')
        verbose_name_plural = _('Category Products')        
        