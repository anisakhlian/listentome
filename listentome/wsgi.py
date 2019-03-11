import os

import dotenv
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

settings_file = 'production'
if os.environ.get('IS_LOCAL') == 'True':
    settings_file = 'local'
elif os.environ.get('IS_DEVELOPMENT') == 'True':
    settings_file = 'development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listentome.settings.' + settings_file)
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
