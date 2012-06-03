from django.contrib import admin
from category_product.models import Category, CategoryProduct
from categories.base import CategoryBaseAdmin

class CategoryAdmin(CategoryBaseAdmin):
    exclude = ('path',)
    list_display = ('name', 'active', 'path')

class CategoryProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Category, CategoryAdmin)    
admin.site.register(CategoryProduct, CategoryProductAdmin)