# Django settings for gametome project.
from os.path import abspath, dirname, normpath, join

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = dirname(normpath(abspath(__file__ + '/../../')))

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(PROJECT_ROOT, 'gametome/static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wl!f=vhzxgop8#ct&!&yj$ioo8zzg4ii)d4xu7@9w++w((qk)*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pybb.middleware.PybbMiddleware',
)

ROOT_URLCONF = 'gametome.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(PROJECT_ROOT, 'gametome/templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    # 3rd Party apps
    'haystack',
    'taggit',
    
    'pybb',
    #'pytils',
    #'sorl.thumbnail',
    'pure_pagination',
    'galeria',
    
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.stackexchange',
    #'allauth.socialaccount.providers.twitter',
    
    # Bespoke apps
    'gtdb',
    'gallery',
    #'gtdb2',
    
)

AUTH_PROFILE_MODULE = 'pybb.Profile'

RESULTS_PER_PAGE = 20
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
}

#HAYSTACK_SITECONF = 'gametome.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'whoosh'
#HAYSTACK_WHOOSH_PATH = normpath(join(PROJECT_ROOT, 'whoosh_index'))
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': normpath(join(PROJECT_ROOT, 'whoosh_index')),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = RESULTS_PER_PAGE

from imagekit.processors import Anchor, ResizeToFill, ResizeToFit, Transpose, SmartResize
GALERIA_THUMBNAIL_IMAGE_PROCESSORS = [
    Transpose(Transpose.AUTO),
    SmartResize(width=100, height=75)
]
GALERIA_DISPLAY_IMAGE_PROCESSORS = [
    Transpose(Transpose.AUTO),
    ResizeToFit(width=800, height=600)
]
GALERIA_COVER_IMAGE_PROCESSORS = [
    Transpose(Transpose.AUTO),
    ResizeToFit(width=256, height=256)
]

PYBB_MARKUP = 'markdown'        
PYBB_SMILES = {
    'X|': 'angry.png',
    ':.(': 'cry.png',
    'o.O': 'eyes.png',
    '8)': 'glasses.png',
    'B)': 'geek.png',
    ':D': 'lol.png',
    ':(': 'sad.png',
    ':O': 'shok.png',
    ':|': 'shy.png',
    ':)': 'smile.png',
    ':P': 'tongue.png',
    ';)': 'wink.png'
}

ALL_SMILES = {
    '&gt;_&lt;': 'angry.png',
    'X|': 'angry.png',
    'X-|': 'angry.png',
    ':.(': 'cry.png',
    ':\'(': 'cry.png',
    'o_O': 'eyes.png',
    'o.O': 'eyes.png',
    '8)': 'glasses.png',
    '8-)': 'glasses.png',
    'B)': 'geek.png',
    'B-)': 'geek.png',
    ':D': 'lol.png',
    ':(': 'sad.png',
    ':-(': 'sad.png',
    ':O': 'shok.png',
    ':-O': 'shok.png',
    ':|': 'shy.png',
    ':-|': 'shy.png',
    ':)': 'smile.png',
    ':-)': 'smile.png',
    '(-:': 'smile.png',
    ':P': 'tongue.png',
    ':-P': 'tongue.png',
    ';)': 'wink.png',
    ';-)': 'wink.png',
}


CKEDITOR_UPLOAD_PATH = "/tmp"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', '-', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor' ],
            ['Image', 'Table', 'HorizontalRule', '-', 'Smiley', 'SpecialChar'],
            ['TextColor', 'BGColor'],
            ['Source'],
        ],
    },
}

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = False
LOGIN_REDIRECT_URL = 'index'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'pybb.context_processors.processor',
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
