from django.contrib import admin
from shop.models import Product
from categories.base import CategoryBaseAdmin
from category_product.models import ProductCategory
from category_product.admin import ProductCategoryAdmin

class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(ProductCategory, ProductCategoryAdmin)    
admin.site.register(Product, CategoryProductAdmin)