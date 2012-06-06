from django.db import models
from django.utils.encoding import force_unicode
from categories.base import CategoryBase

class ProductCategoryBase(CategoryBase):
    
    path = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
        
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