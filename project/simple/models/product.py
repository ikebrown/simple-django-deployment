from django.db import models
from tinymce import models as tinymce_models
from category_product.models.defaults.product.base import CategoryProductBase

class Product(CategoryProductBase):
    
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    body = tinymce_models.HTMLField()
    
    class Meta:
        abstract = False
        app_label = 'simple'