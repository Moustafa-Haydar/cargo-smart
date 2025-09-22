from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z5m*zre34viycts)b=6)t!q5)r77vm@6y+*5u=hqsri=biq&)c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', 
    'rest_framework',
    'rest_framework.authtoken',  # For token authentication
    'drf_yasg',  # Swagger documentation

    # apps
    'apps.accounts',
    'apps.geo',
    'apps.rbac',
    'apps.routes',
    'apps.shipments',
    'apps.vehicles',
    'apps.alerts',
    'apps.agent_reroute',
]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "apps.accounts.middleware.RequireAdminGroupMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

RBAC_ADMIN_GROUPS = ["Admin"]   # who counts as admin
RBAC_ADMIN_PROTECTED = [        # which endpoints to protect
    "accounts:users",
    "accounts:user",
    "accounts:create_user",
    "accounts:update_user",
    "accounts:delete_user",
    "rbac:*"
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # sessions + CSRF
        "apps.accounts.authentication.BearerTokenAuthentication",  # Bearer token auth for mobile
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",           # default
    ],
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.56.1:3000",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://10.0.2.2:8000"
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # username/password
]

ROOT_URLCONF = 'cargosmart.urls'

# ---- Cookie/Session options ----
SESSION_COOKIE_NAME = "cargosmart_sessionid"   # cookie that stores the session key
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7          # 7 days
SESSION_SAVE_EVERY_REQUEST = False

# CSRF cookie lets clients (like Postman or your SPA) send X-CSRFToken on writes
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# When you deploy behind HTTPS, uncomment these:
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = "Lax"   # or "None" if a different top-level site must send cookies

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.56.1:3000",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://10.0.2.2:8000",
]
ALLOWED_HOSTS = [
    "localhost", 
    "127.0.0.1",
    "host.docker.internal",
    "10.0.2.2"
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROUTE_AI = {
    "P_DELAY_THRESHOLD": 0.3,  # Lowered from 0.65 to be more sensitive to delays
    "SCORE_WEIGHTS": {
        "eta_minutes": 0.6,
        "p_delay": 0.3,
        "toll_cost_usd": 0.1,
    },
    "IMPROVEMENT_EPS": 0.05,
    "MAX_ALTERNATIVES": 3,
    "MODEL_PATH": BASE_DIR / "models" / "delay_classifier.joblib",
}


WSGI_APPLICATION = 'cargosmart.wsgi.application'

import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Swagger/OpenAPI Configuration
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT token. Example: "Bearer {token}"'
        },
        'Session': {
            'type': 'apiKey',
            'name': 'csrftoken',
            'in': 'header',
            'description': 'CSRF token for session authentication'
        }
    },
    'USE_SESSION_AUTH': True,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': True,
    'SHOW_EXTENSIONS': True,
    'SHOW_COMMON_EXTENSIONS': True,
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}
