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
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables if env.py exists
if os.path.isfile("env.py"):
    import env

# =======================================
# Path Configuration
# =======================================
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# =======================================
# Security Settings
# =======================================
# WARNING: These are development settings
# Do NOT use in production without modification

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

# Host Configuration
# -----------------
ALLOWED_HOSTS = [
    # Production Environments
    "nederlearn-v4.herokuapp.com",  # Legacy production server
    "nederlearn-v5-c628536a9899.herokuapp.com",  # Current production server
    # Development Environments
    "localhost",  # Local development server
    "8000-blignaut24-nederlearnv5-rg2cno7yf87.ws-eu117.gitpod.io",
]

# =======================================
# Application Configuration
# =======================================
# List of installed Django apps
INSTALLED_APPS = [
    ###########################
    # 1. Django Core Apps     #
    ###########################
    "django.contrib.admin",  # Admin interface and functionality
    "django.contrib.auth",  # Authentication framework
    "django.contrib.contenttypes",  # Content type system
    "django.contrib.sessions",  # Session handling
    "django.contrib.messages",  # User messaging system
    ###########################
    # 2. File Management      #
    ###########################
    "django.contrib.staticfiles",  # Static assets (CSS, JS, images)
    "cloudinary_storage",  # Cloud storage integration
    "cloudinary",  # Media file handling
    "django.contrib.sites",  # Multi-site support
    ###########################
    # 3. Authentication       #
    ###########################
    "allauth",  # Main auth framework
    "allauth.account",  # User account management
    "allauth.socialaccount",  # Social media login support
    ###########################
    # 4. UI Enhancement       #
    ###########################
    "django_summernote",  # Rich text editor
    "crispy_forms",  # Form styling and layout
    ###########################
    # 5. Custom Applications  #
    ###########################
    "blog.apps.BlogConfig",  # Blog functionality
]

# ============================================================================
# Authentication Configuration
# ============================================================================
# Adapted from: Code Institute's "I Think Therefore I Blog" tutorial
#              Authentication/Django AllAuth section

# Site Configuration
# -----------------
SITE_ID = 1  # Unique identifier for multi-site setups

# Authentication Redirects
# ----------------------
# Post-login redirect destination
LOGIN_REDIRECT_URL = "/"

# Post-logout redirect destination
LOGOUT_REDIRECT_URL = "/accounts/login"

# Form Styling
# -----------
# Bootstrap 4 styling for Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# =================================================================
# MESSAGE TAGS CONFIGURATION
# =================================================================
# Define message tags for different alert types in the application
# These tags map Django message levels to Bootstrap alert classes
# -----------------------------------------------------------------
# DEBUG:   Information for developers (blue)
# INFO:    General information messages (blue)
# SUCCESS: Positive feedback messages (green)
# WARNING: Advisory messages (yellow)
# ERROR:   Critical problem messages (red)
# -----------------------------------------------------------------

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",  # Developer debugging info
    messages.INFO: "alert-info",  # User information
    messages.SUCCESS: "alert-success",  # Positive feedback
    messages.WARNING: "alert-warning",  # Cautionary messages
    messages.ERROR: "alert-danger",  # Error notifications
}

# ===========================================
# Summernote Editor Configuration
# ===========================================
#
# Purpose: Configure the Summernote WYSIWYG editor
# settings to ensure proper display and functionality
#
# Main Settings:
# - Editor width: Set to full width (100%) for
#   responsive design and better user experience

SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",  # Makes editor span full container width
    },
}

# =================================================================
# MIDDLEWARE CONFIGURATION
# =================================================================

MIDDLEWARE = [
    # -------------
    # Security Layer
    # -------------
    "django.middleware.security.SecurityMiddleware",
    # Handles security features
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Serves static files efficiently
    # -------------
    # Session & Authentication Layer
    # -------------
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Manages user sessions
    "django.middleware.common.CommonMiddleware",
    # Common request/response processing
    "django.middleware.csrf.CsrfViewMiddleware",
    # Protects against CSRF attacks
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Handles user authentication
    # -------------
    # User Interface Layer
    # -------------
    "django.contrib.messages.middleware.MessageMiddleware",
    # Flash messages system
    "allauth.account.middleware.AccountMiddleware",  # Handles auth accounts
]

# =======================================
# URL and Template Configuration
# =======================================
ROOT_URLCONF = "nederlearn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # BASE_DIR / 'templates' points to project root templates folder
        "DIRS": [BASE_DIR / "templates"],
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

# =======================================
# Database Configuration
# =======================================
# Using environment variable for database URL
# Supports easy switching between development/production
DATABASES = {"default": dj_database_url.parse(os.environ.get("DATABASE_URL"))}


CSRF_TRUSTED_ORIGINS = ["https://*.gitpod.io/", "https://*.herokuapp.com"]

# =================================================================
# Password Validation Configuration
# =================================================================
# This section configures Django's built-in password validation system
# to enforce password security requirements for user accounts.

AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks if password is too similar to username/email
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        # Ensures password meets minimum length requirement
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        # Prevents use of commonly used/easily guessed passwords
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        # Checks if password is not entirely numeric
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]


# ==============================================
# Email Verification Configuration
# ==============================================
# Disable email verification for development
# ----------------------------------------------
ACCOUNT_EMAIL_VERIFICATION = "none"

# =======================================
# Internationalization
# =======================================
LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = "UTC"  # Timezone setting
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

# ===================================
# Media Storage Configuration
# ===================================

# Define the URL path for media files
MEDIA_URL = "/media/"

# Configure Cloudinary as media file storage backend
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# =======================================
# Static Files Configuration
# =======================================
# Configuration for CSS, JavaScript, Images
STATIC_URL = "/static/"
STATICFILES_STORAGE = (
    "cloudinary_storage.storage."
    "StaticHashedCloudinaryStorage"
)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Cloudinary - Django intergration
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME", "dki11spup"),
    api_key=os.environ.get("CLOUDINARY_API_KEY", "651583882481459"),
    api_secret=os.environ.get(
        "CLOUDINARY_API_SECRET", "oVB9sTCGPjJCl05vx3bjBNEZ0Eg"),
)

# =======================================
# Model Configuration
# =======================================
# Default field type for primary keys
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =======================================
# Authentication Settings
# =======================================
# Disables email verification requirement
# for account registration/management

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# Close the session when the user closes the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
