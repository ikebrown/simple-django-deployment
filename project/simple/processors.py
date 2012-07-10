import os
import operator, itertools
from PIL import Image
from django.conf import settings

TRANSPARENCY = os.path.join(settings.STATIC_ROOT, 'simple', 'images', 'white_top.png')
    
def bend_transparancy(image, bend=False, **kwargs):

    if bend:
        transparency = Image.open(TRANSPARENCY)
        transparency.load()
        r,g,b,alpha = transparency.split()
        mask = Image.new('L', image.size, '#ffffff')
        mask.paste(alpha, (-20, 0))
        image.putalpha(mask)
    return image