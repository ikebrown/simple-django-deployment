from django.db import models
from django.utils.encoding import force_unicode
from categories.base import CategoryBase    
from mptt.fields import TreeForeignKey, TreeManyToManyField
from mptt.managers import TreeManager
from shop.models.defaults.managers import ProductManager
from shop.models.defaults.product import Product

class CategoryProductManager(ProductManager, TreeManager):
    pass
    
class Category(CategoryBase):
    
    path = models.CharField(max_length=255)
    
    def get_path(self):
        ancestors = list(self.get_ancestors()) + [self,]
        return '/'.join([force_unicode(i.slug) for i in ancestors])
    
    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        self.path = self.get_path()
        super(Category, self).save(*args, **kwargs)
        descendants = list(self.get_descendants())
        for descendant in descendants:
            descendant.save()
            
    @models.permalink    
    def get_absolute_url(self):
        return('product_list', (), {'path': self.path})
                
class CategoryProduct(Product):
    main_category = TreeForeignKey(Category)
    additional_categories = TreeManyToManyField(Category, related_name='extra_product_categories')

    objects = CategoryProductManager()

    class Meta:
        pass
        
    @models.permalink    
    def get_absolute_url(self):
        return('product_detail', (), {'slug':self.slug, 'path': self.main_category.path})
    