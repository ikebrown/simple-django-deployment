from django.db import models
from tinymce import models as tinymce_models
from category_product.models.defaults.category.base import ProductCategoryBase
        
class Category(ProductCategoryBase):
    
    def get_image(self):
        if self.image:
            return self.image
        else:
            try:
                return self.get_ancestors().exclude(image='')[-1]
            except IndexError:
                return None
    
    image = models.ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        abstract = False
        app_label = 'simple'