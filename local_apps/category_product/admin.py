from categories.base import CategoryBaseAdmin

class ProductCategoryAdmin(CategoryBaseAdmin):
    exclude = ('path',)
    list_display = ('name', 'active', 'path')
