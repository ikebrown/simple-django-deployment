# coding=utf-8
# Django settings for cms project.
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

CACHE_BACKEND = 'locmem:///'

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_URL = '/media/media/'
CMS_MEDIA_URL= '/media/cms/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
TINYMCE_JS_URL = '/media/tiny_mce/tiny_mce.js'
JQUERY_JS = 'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'
JQUERY_UI_JS = 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js'
JQUERY_UI_CSS = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/smoothness/jquery-ui.css'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*xq7m@)*f2awoj!spa0(jibsrz9%c0d=e(g)v*!17y(vx0ue_3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "sekizai.context_processors.sekizai",
    "cms.context_processors.media",
)

INTERNAL_IPS = ('127.0.0.1', )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'simple.urls'

INSTALLED_APPS = (
    'simple',
    'haystack',
    'djangocms_utils',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'cms',
    'menus',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.twitter',
    'mptt',
    'reversion',
    'pagination',
    'tinymce',
    # 'cmsplugin_blog',
    # 'cmsplugin_blog_search',
    'simple_translation',
    'tagging',
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'easy_thumbnails',
    'south',
    'cms_facetsearch',
    'rosetta',
    'sekizai',
    'djcelery',
    'celery_haystack',
    'shop',
    'category_product',
    'treeadmin'
)

SHOP_PRODUCT_MODEL = 'simple.models.product.Product'
SHOP_ADDRESS_MODEL =  'simple.models.address.Address'

SHOP_PAYMENT_BACKENDS = [
    'shop.payment.backends.pay_on_delivery.PayOnDeliveryBackend',
]
SHOP_SHIPPING_BACKENDS = ['shop.shipping.backends.flat_rate.FlatRateShipping']
CATEGORYPRODUCT_CATEGORY_MODEL = 'simple.models.category.Category'

gettext = lambda s: s

LANGUAGE_CODE = "nb"

CMS_LANGUAGES = (
    ('nb', gettext('Norwegian Bokmal')),
    ('en', gettext('English')),
)

LANGUAGES = CMS_LANGUAGES

CMS_TEMPLATES = (
    ('base_templates/default.html', gettext('default')),
    ('base_templates/main_split.html', gettext('split')),
    ('base_templates/front.html', gettext('front'))

)

CMS_SOFTROOT = True
CMS_REDIRECTS = True

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    "height": "880",
    "plugins": "table,paste,searchreplace",
"theme_advanced_buttons1": "bold,italic,underline,strikethrough,|,sub,sup,|,charmap,|,formatselect,|,link,unlink,anchor,|,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,outdent,indent,blockquote",
"theme_advanced_buttons2": ",cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,cleanup,help,code,|,insertdate,inserttime",
"theme_advanced_buttons3": "tablecontrols,|,hr,removeformat,visualaid",
"theme_advanced_toolbar_location": "top",
"theme_advanced_toolbar_align": "left",
"theme_advanced_statusbar_location": "bottom",
"theme_advanced_resizing": "true",
"extended_valid_elements" : "a[href|onclick|target|class]"
}   

FORCE_LOWERCASE_TAGS = True

from easy_thumbnails import defaults

THUMBNAIL_PROCESSORS = defaults.PROCESSORS + (
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
)
THUMBNAIL_DEBUG = True

# netaxept 
NETAXEPT_PAYMENT_METHOD_LIST='Visa,MasterCard,Paypal'
NETAXEPT_MERCHANTID = '*snip*'
NETAXEPT_TOKEN = '*snip*'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'stdout': {                # define and name a handler
            'level': 'DEBUG',
            'class': 'logging.StreamHandler', # set the logging class to log to a file
            'formatter': 'simple',         # define the formatter to associate
            'stream': sys.stdout
        },

    },
    'loggers': {
        'djnetaxept.utils': {              # define a logger - give it a name
            'handlers': ['stdout'], # specify what handler to associate
            'level': 'DEBUG',                 # specify the logging level
            'propagate': True
        }       
    }       
}

try:
    from local_settings import *
except ImportError:
    pass

import djcelery
djcelery.setup_loader()