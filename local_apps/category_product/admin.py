from mptt.admin import FeinCMSModelAdmin

class ProductCategoryAdmin(FeinCMSModelAdmin):
    exclude = ('path',)
    list_display = ('name', 'active', 'path')
