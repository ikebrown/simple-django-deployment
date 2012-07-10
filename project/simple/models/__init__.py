from cms.models import CMSPlugin
from filer.fields.image import FilerImageField

class TopPicture(CMSPlugin):
    image = FilerImageField()