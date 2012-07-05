from django.db import models
from tinymce import models as tinymce_models
from category_product.models.defaults.product.base import CategoryProductBase

class Product(CategoryProductBase):
    
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    body = tinymce_models.HTMLField()
    
    weigth_in_grams = models.PositiveIntegerField(null=True, blank=True)
    lenght_in_centimeters =  models.PositiveIntegerField(null=True, blank=True)
    width_in_centimeters = models.PositiveIntegerField(null=True, blank=True)  
    height_in_centimeters = models.PositiveIntegerField(null=True, blank=True)
    
    @property
    def dimensions(self):
        if self.lenght_in_centimeters and self.width_in_centimeters and self.height_in_centimeters:
            return {
                'length': self.lenght_in_centimeters,
                'width': self.width_in_centimeters,
                'height': self.height_in_centimeters
            }
        return None
        
    @property
    def weight(self):
        return self.weigth_in_grams 
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not ((self.lenght_in_centimeters and self.width_in_centimeters and self.height_in_centimeters) \
            or self.weigth_in_grams):
            raise ValidationError('Dimensions or weight required.')
    
    class Meta:
        abstract = False
        app_label = 'simple'