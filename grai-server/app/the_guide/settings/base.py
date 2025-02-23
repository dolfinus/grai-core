import logging
import os
import subprocess
import warnings
from pathlib import Path

import openai
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


def clean_hosts(val):
    if isinstance(val, list):
        return [item.strip() for item in val]
    elif isinstance(val, str):
        return [s.strip() for s in val.strip("'\"").split(",")]
    else:
        raise TypeError(f"hosts must be a list or comma separated string not {type(val)}")


def get_server_version():
    if not (ver := config("GRAI_SERVER_VERSION", False)):
        try:
            result = subprocess.run(["poetry", "version", "-s"], stdout=subprocess.PIPE)
            ver = result.stdout.decode("utf-8").strip()
        except:
            ver = "unknown"
    return ver


def cast_string_to_bool(default: bool = True):
    yes_values = {"true", "yes", "y"}
    no_values = {"false", "no", "n"}

    def inner(value: str | bool) -> bool:
        if isinstance(value, bool):
            return value
        elif value.lower() in yes_values:
            return True
        elif value.lower() in no_values:
            warnings.warn(f"Unrecognized boolean value `{value}`, defaulting to `{default}`")
            return default

    return inner


SERVER_VERSION = get_server_version()
DEBUG = config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = config("TEMPLATE_DEBUG", default=DEBUG, cast=bool)

SERVER_HOST = config("SERVER_HOST", default="localhost", cast=str)
SERVER_PORT = config("SERVER_PORT", default="8000", cast=str)
SERVER_URL = config("SERVER_URL", default=f"http://{SERVER_HOST}:{SERVER_PORT}", cast=str)

FRONTEND_HOST = config("FRONTEND_HOST", default=SERVER_HOST, cast=str)
FRONTEND_PORT = config("SERVER_PORT", default="3000", cast=str)
FRONTEND_URL = config("FRONTEND_URL", default=f"http://{FRONTEND_HOST}:{FRONTEND_PORT}", cast=str)

DISABLE_HTTP = config("DISABLE_HTTP", default=False)

POSTHOG_HOST = config("POSTHOG_HOST", default="https://app.posthog.com")
POSTHOG_PROJECT_API_KEY = config("POSTHOG_PROJECT_API_KEY", default="phc_Q8OCDm0JpCwt4Akk3pMybuBWniWPfOsJzRrdxWjAnjE")
DISABLE_POSTHOG = config("DISABLE_POSTHOG", default=False, cast=cast_string_to_bool(False))

SENTRY_DSN = config(
    "SENTRY_DSN",
    default="https://3ef0d6800e084eae8b3a8f4ee4be1d3d@o4503978528407552.ingest.sentry.io/4503978529456128",
)
SENTRY_SAMPLE_RATE = config("SENTRY_SAMPLE_RATE", default=0.2, cast=float)

schemes = ["https"] if DISABLE_HTTP else ["http", "https"]
hosts = {SERVER_HOST, FRONTEND_HOST}
if DEBUG:
    default_allowed_hosts = ["*"]
    default_csrf_trusted_origins = [f"{scheme}://*" for scheme in schemes]
    default_cors_allowed_origins = [
        f"{scheme}://{host}" for scheme in schemes for host in [FRONTEND_HOST, f"{FRONTEND_HOST}:{FRONTEND_PORT}"]
    ]
    default_allow_all_origins = True
else:
    default_allowed_hosts = [SERVER_HOST, "127.0.0.1", "[::1]"]
    default_csrf_trusted_origins = [f"{scheme}://{host}" for scheme in schemes for host in hosts]
    default_cors_allowed_origins = [
        f"{scheme}://{host}" for scheme in schemes for host in [FRONTEND_HOST, f"{FRONTEND_HOST}:{FRONTEND_PORT}"]
    ]
    default_allow_all_origins = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=default_allowed_hosts, cast=clean_hosts)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default=default_cors_allowed_origins, cast=clean_hosts)
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default=default_csrf_trusted_origins, cast=clean_hosts)
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=default_allow_all_origins, cast=bool)


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="psqlextra.backend"),
        "NAME": config("DB_NAME", default="grai"),
        "USER": config("DB_USER", default="grai"),
        "PASSWORD": config("DB_PASSWORD", default="grai"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}


DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "whitenoise.runserver_nostatic",
    "strawberry.django",
    "rest_framework",
    "phonenumber_field",
    "corsheaders",
    "social_django",
    "rest_framework_simplejwt",
    "django_extensions",
    "rest_framework_api_key",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "django_celery_beat",
    "storages",
    "email_log",
    "djcelery_email",
    "drf_spectacular",
    "django.contrib.postgres",
    "psqlextra",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
]

ALGOLIA_APPLICATION_ID = config("ALGOLIA_APPLICATION_ID", None)
ALGOLIA_ADMIN_KEY = config("ALGOLIA_ADMIN_KEY", None)
ALGOLIA_SEARCH_KEY = config("ALGOLIA_SEARCH_KEY", None)

ALGOLIA = {"APPLICATION_ID": ALGOLIA_APPLICATION_ID, "API_KEY": ALGOLIA_ADMIN_KEY}

if ALGOLIA_APPLICATION_ID is not None:
    THIRD_PARTY_APPS += ["algoliasearch_django"]

THE_GUIDE_APPS = [
    "lineage",
    "connections",
    "installations",
    "notifications",
    "workspaces",
    "users",
    "search",
    "telemetry",
    "grAI",
]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + THE_GUIDE_APPS

MIDDLEWARE = [
    "middleware.HealthCheckMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "middleware.MultitenantMiddleware",
]


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "pagination.standard_pagination.StandardResultsPagination",
}

ROOT_URLCONF = "the_guide.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


REDIS_HOST = config("REDIS_HOST", "localhost")
REDIS_PORT = config("REDIS_PORT", 6379)

WSGI_APPLICATION = "the_guide.wsgi.application"

REDIS_CHANNEL_HOST = config("REDIS_CHANNEL_HOST", REDIS_HOST)
REDIS_CHANNEL_PORT = config("REDIS_CHANNEL_PORT", REDIS_PORT)

ASGI_APPLICATION = "the_guide.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (REDIS_CHANNEL_HOST, REDIS_CHANNEL_PORT),
            ],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

PHONENUMBER_DEFAULT_REGION = "US"

# OpenApi
# https://drf-spectacular.readthedocs.io/en/latest/settings.html

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "db-console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": f"debug.log",
#         },
#     },
#     "loggers": {
#         'health_check': {  # replace 'your_app' with the name of your application
#             'handlers': ['console'],
#             'level': 'WARNING',
#             'propagate': False,
#         },
#     },
# }

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = "email_log.backends.EmailBackend"
EMAIL_LOG_BACKEND = config("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_FROM = config("EMAIL_FROM", None)
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", None)
AWS_SES_REGION_NAME = config("AWS_SES_REGION", None)
AWS_SES_REGION_ENDPOINT = config("AWS_SES_REGION_ENDPOINT", "email.us-west-2.amazonaws.com")

# Celery settings

CELERY_BROKER_URL = config("CELERY_BROKER", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
CELERY_RESULT_BACKEND = config("CELERY_BACKEND", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_TASK_SERIALIZER = "json"

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", 1209600)

STORAGES = {
    "default": {
        "BACKEND": config("DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", None)

GITHUB_APP_ID = config("GITHUB_APP_ID", None)
GITHUB_PRIVATE_KEY = config("GITHUB_PRIVATE_KEY", None)

REDIS_GRAPH_CACHE_HOST = config("REDIS_GRAPH_CACHE_HOST", REDIS_HOST)
REDIS_GRAPH_CACHE_PORT = config("REDIS_GRAPH_CACHE_PORT", REDIS_PORT)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_GRAPH_CACHE_HOST}:{REDIS_GRAPH_CACHE_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

OTP_TOTP_ISSUER = "Grai Cloud"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# OpenAI

OPENAI_API_KEY = config("OPENAI_API_KEY", None)
OPENAI_ORG_ID = config("OPENAI_ORG_ID", None)
OPENAI_PREFERRED_MODEL = config("OPENAI_PREFERRED_MODEL", default="", cast=lambda x: "gpt-3.5-turbo" if x == "" else x)

openai.organization = OPENAI_ORG_ID
openai.api_key = OPENAI_API_KEY

if OPENAI_API_KEY is not None and OPENAI_ORG_ID is not None:
    try:
        client = openai.Client(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)
        models = [item.id for item in client.models.list().data]
    except openai.AuthenticationError as e:
        warnings.warn("Could not authenticate with OpenAI API key and organization id.")
        HAS_OPENAI = False
    else:
        if len(models) == 0:
            message = f"Provided OpenAI API key does not have access to any models as a result we've disabled OpenAI."
            warnings.warn(message)

            HAS_OPENAI = False
            OPENAI_PREFERRED_MODEL = ""
        elif OPENAI_PREFERRED_MODEL not in models:
            default_model = models[0]
            message = (
                f"Provided OpenAI API key does not have access to the preferred model {OPENAI_PREFERRED_MODEL}. "
                f"If you wish to use {OPENAI_PREFERRED_MODEL} please provide an API key with appropriate permissions. "
                f"In the mean time we've defaulted to {default_model}."
            )
            warnings.warn(message)

            HAS_OPENAI = True
            OPENAI_PREFERRED_MODEL = default_model
        else:
            HAS_OPENAI = True
else:
    HAS_OPENAI = False


if HAS_OPENAI:
    pass
    # TODO: Need to bake the encodings into the docker image otherwise it gets fetched every time
    TIKTOKEN_CACHE_DIR = "/TIKTOKEN_CACHE_DIR"
    # if not os.path.exists(TIKTOKEN_CACHE_DIR):
    #     os.makedirs(TIKTOKEN_CACHE_DIR)

    # os.environ["TIKTOKEN_CACHE_DIR"] = TIKTOKEN_CACHE_DIR
    # import tiktoken
    # # download the OpenAI preferred model encoder
    # try:
    #     tiktoken.encoding_for_model(OPENAI_PREFERRED_MODEL)
    # except:
    #     logging.error("Could not download OpenAI preferred model encoder with tiktoken")

SPECTACULAR_SETTINGS = {
    "TITLE": "Grai Server",
    "DESCRIPTION": "Grai Server API",
    "VERSION": config("GRAI_SERVER_VERSION", "0.0.0"),
    "SERVE_INCLUDE_SCHEMA": False,
    "EXTERNAL_DOCS": {"url": "https://docs.grai.io"},
    "SWAGGER_UI_FAVICON_HREF": f"{STATIC_URL}icons/favicon.svg",
    # OTHER SETTINGS
}

SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=0, cast=int)

# Content Security Policy
CSP_IMG_SRC = "'self' data: https://cdn.redoc.ly"
CSP_STYLE_SRC = "'self' 'unsafe-inline' https://unpkg.com https://fonts.googleapis.com"
CSP_SCRIPT_SRC = "'self' blob: https://unpkg.com https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js 'sha256-Ri7Dq6kn4d1SzxucogauP62ISolkcXZOaUT8I/xEVGg=' 'sha256-J8pGp/Y6gm05ag6P7dPEm65mUl5R2czgNxQwp+oKbgY='"
CSP_FONT_SRC = "'self' data: https://fonts.gstatic.com"
CSP_OBJECT_SRC = "'none'"
CSP_REPORT_ONLY = config("CSP_REPORT_ONLY", default=False, cast=bool)
CSP_REPORT_URI = config("CSP_REPORT_URI", default=None)

PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
