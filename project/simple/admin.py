from django.contrib import admin
from shop.models import Product
from categories.base import CategoryBaseAdmin
from category_product.models import Category
from category_product.admin import ProductCategoryAdmin

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'active', 'unit_price', 'image', 'body', 'main_category', 'additional_categories')
    
admin.site.register(Category, ProductCategoryAdmin)    
admin.site.register(Product, ProductAdmin)
