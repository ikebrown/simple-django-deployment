from django.db import models
from django.db.models import signals

from django.utils.encoding import force_unicode
from categories.base import CategoryBase    
from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.managers import TreeManager
from shop.models.defaults.managers import ProductManager
from shop.models.defaults.product import Product

class CategoryProductManager(ProductManager, TreeManager):
    pass
    
class ProductCategoryBase(CategoryBase):
    
    path = models.CharField(max_length=255)
    
    class Meta:
        abstract= True
        
    def get_path(self):
        ancestors = []
        if self.parent:
            ancestors = list(self.parent.get_ancestors(include_self=True))
        ancestors = ancestors + [self,]    
        return '/'.join([force_unicode(i.slug) for i in ancestors])
    
    def save(self, *args, **kwargs):
        self.path = self.get_path()
        update_descendants = bool(self.pk)
        super(ProductCategoryBase, self).save(*args, **kwargs)
        if update_descendants:
            descendants = list(self.get_descendants())
            for descendant in descendants:
                descendant.save()
                
    @models.permalink    
    def get_absolute_url(self):
        return('product_list', (), {'path': self.path})            

class ProductCategory(ProductCategoryBase):
    pass
                
class CategoryProduct(Product):
    main_category = TreeForeignKey(ProductCategory)
    additional_categories = TreeManyToManyField(ProductCategory, related_name='extra_product_categories')

    objects = CategoryProductManager()

    class Meta:
        pass
        
    @models.permalink    
    def get_absolute_url(self):
        return('product_detail', (), {'slug':self.slug, 'path': self.main_category.path})
        
    def save(self, *args, **kwargs):
        super(CategoryProduct, self).save(*args, **kwargs)
        self.additional_categories.add(self.main_category)

def add_main_category_to_additional(sender, **kwargs):
    if kwargs['action'] not in ('post_clear', 'post_remove'):
        return
    product = kwargs['instance']
    reloaded = CategoryProduct.objects.get(pk=product.pk)
    product.additional_categories.add(reloaded.main_category)
        
signals.m2m_changed.connect(add_main_category_to_additional,
                    sender=CategoryProduct.additional_categories.through)    