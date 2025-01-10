"""
# =======================================
# Django Settings Configuration
# =======================================
# Main configuration file for nederlearn Django project
# Created with Django 5.1.4

# For detailed information:
# Settings guide: https://docs.djangoproject.com/en/5.1/topics/settings/
# Settings reference: https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# =======================================
# Core Imports and Setup
# =======================================
from pathlib import Path
import os
import dj_database_url
from django.contrib.messages import constants as messages

# Load environment variables if env.py exists
if os.path.isfile("env.py"):
    import env

# =======================================
# Path Configuration
# =======================================
# BASE_DIR: Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent
# TEMPLATES_DIR: Directory containing HTML templates
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# =======================================
# Security Settings
# =======================================
# WARNING: These are development settings
# Do NOT use in production without modification

SECRET_KEY = "django-insecure-&m%gu-ez==#b@$+_t99xi_wgv()$4vr7#$-og^=x4rdhx6lh6j"
DEBUG = False  # Enable debugging mode

# Host Configuration
# -----------------
# Defines which hosts can serve this application
ALLOWED_HOSTS = [
    "nederlearn-v4.herokuapp.com",  # Production server
    "localhost",  # Local development
    "8000-blignaut24-nederlearnv5-cxy96i1lj06.ws-eu117.gitpod.io",
    "nederlearn-v5-c628536a9899.herokuapp.com",
]

# =======================================
# Application Configuration
# =======================================
# List of installed Django apps
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",  # Admin interface
    "django.contrib.auth",  # Authentication
    "django.contrib.contenttypes",
    "django.contrib.sessions",  # Session handling
    "django.contrib.messages",  # User messages
    # Third-party apps
    "cloudinary_storage",  # Cloud storage
    "django.contrib.staticfiles",
    "cloudinary",
    # Local apps
    "blog",  # Blog functionality
]

# =======================================
# Middleware Configuration
# =======================================
# Request/response modification chain
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security
    "django.contrib.sessions.middleware.SessionMiddleware",  # Sessions
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =======================================
# URL and Template Configuration
# =======================================
ROOT_URLCONF = "nederlearn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "nederlearn.wsgi.application"

# ====================================
# Database Configuration (SQLite3)
# ====================================
# Default Django database settings using SQLite
# Currently commented out as we're using PostgreSQL
# Uncomment if switching back to local development
# DATABASES = {
#    "default": {                           # Main database connection
#        "ENGINE": "django.db.backends.sqlite3",  # Database engine
#        "NAME": BASE_DIR / "db.sqlite3",   # File location relative to BASE_DIR
#    }
# }

# =======================================
# Database Configuration
# =======================================
# Using environment variable for database URL
# Supports easy switching between development/production
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}

# =======================================
# Password Validation
# =======================================
# Rules for password strength and validation
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

# =======================================
# Internationalization
# =======================================
LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = "UTC"  # Timezone setting
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

# =======================================
# Static Files Configuration
# =======================================
# Configuration for CSS, JavaScript, Images
STATIC_URL = "/static/"

# =======================================
# Model Configuration
# =======================================
# Default field type for primary keys
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
