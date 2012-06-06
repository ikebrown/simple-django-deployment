from haystack import indexes
from django.utils.encoding import force_unicode
from django.utils.html import strip_tags
from cms_facetsearch.indexes import IndexBase, Indexable, HTMLEntitiesToUnicode
from shop.models import Product

class ProductIndex(IndexBase, Indexable):
    
    url = indexes.CharField(stored=True, indexed=False)
    title = indexes.CharField(stored=True, indexed=False, model_attr='name')
    text = indexes.CharField(document=True, use_template=False)

    def get_model(self):
       return Product

    def prepare(self, obj):
        data = super(ProductIndex, self).prepare(obj)
        data['url'] = obj.get_absolute_url()
        data['text'] = u'%s %s' % (obj.name, HTMLEntitiesToUnicode(force_unicode(strip_tags(obj.body))))
        return data
        
    def index_queryset(self):
        return Product.objects.all()