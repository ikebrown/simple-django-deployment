from django.contrib import admin
from category_product.models import ProductCategory, CategoryProduct
from categories.base import CategoryBaseAdmin

class ProductCategoryAdmin(CategoryBaseAdmin):
    exclude = ('path',)
    list_display = ('name', 'active', 'path')

class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(ProductCategory, ProductCategoryAdmin)    
admin.site.register(CategoryProduct, CategoryProductAdmin)