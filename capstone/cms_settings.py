from .settings import *

# Add any CMS-specific settings here

ROOT_URLCONF = 'cms.urls'
ALLOWED_HOSTS = ['*'] 

# Authentication settings
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/' 