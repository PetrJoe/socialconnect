import os
from pathlib import Path
# import cloudinary #type: ignore
# import cloudinary.uploader #type: ignore
# import cloudinary.api #type: ignore


# cloudinary.config(
#   cloud_name = "",
#   api_key = "",
#   api_secret = "",
#   secure = True
# )

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure---b7%l+49f774%21m!nj^o%(j5g6qkak*!a_7hg0y_!k4kp4pw'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
DEBUG = True

ALLOWED_HOSTS = ["*", ".onrender.com",".vercel.app"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'chat',
    'crispy_forms',
    'crispy_tailwind',
    'whitenoise',
    # 'cloudinary',
    # 'cloudinary_storage',
]

SITE_ID=1

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'login'

LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'


CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'socialapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'socialapp.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.json',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Change to PostgreSQL backend
        'NAME': 'socialconnect_circlefind',  # PostgreSQL database name
        'USER': 'socialconnect_circlefind',      # Database username
        'PASSWORD': '46941e1cdcef3d49ad66ca68336b8f5f83f75b53',       # Database password
        'HOST': '50dzg.h.filess.io',  # Database host
        'PORT': '5433',         # Database port        
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
