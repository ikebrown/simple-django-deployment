from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from simple.models import TopPicture

class TopPicturePlugin(CMSPluginBase):

    model = TopPicture
    name = _('TopPicture')
    render_template = "simple/toppicture_plugin.html"
        
    def render(self, context, instance, placeholder):

        context.update({
            'instance': instance,
            'placeholder': placeholder
        })
        return context
        
plugin_pool.register_plugin(TopPicturePlugin)
