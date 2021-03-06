import os
from configurations import Configuration, values

class Base(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.Value("youneverguess")

    VK_SECRET_KEY = values.Value("vkkey")

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'corsheaders',
        "rest_framework",

        'inventories',
        'accounts',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware', # cors
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # CSRF_COOKIE_NAME = "XSRF-TOKEN"

    AUTHENTICATION_BACKENDS = [
        'accounts.backends.VkBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

    ROOT_URLCONF = 'vkpsytest.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'vkpsytest.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'vkpsytest',
            'USER' : 'vkpsytest',
            'PASSWORD' : 'vkpsytest',
            'HOST' : 'localhost',
            'PORT' : '5432',
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'accounts.backends.VkBackendREST',
        ]
    }

    CORS_ORIGIN_ALLOW_ALL = True
    # CORS_ORIGIN_WHITELIST = [
    #     'http://localhost:10888'
    # ]

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    DEFAULT_USER_PASSWORD_LENGTH = 16

    # business settings
    MIN_SAMPLE = 10



class Dev(Base):

    DEBUG = True

    TEMPLATE_DEBUG = DEBUG



class Prod(Base):

    DEBUG = False

    TIME_ZONE = 'America/New_York'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'accounts.backends.VkBackendREST',
            # 'rest_framework.authentication.BasicAuthentication',
            # 'rest_framework.authentication.SessionAuthentication',
        ]
    }
