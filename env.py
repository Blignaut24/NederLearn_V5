# =================================================================
# DATABASE AND CLOUD SERVICES CONFIGURATION
# =================================================================

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# -----------------------------
# PostgreSQL Database Settings
# -----------------------------
# Database hosted on Neon Cloud Platform
# Connection string format: postgresql://<username>:<password>@<host>/<database>

os.environ.setdefault(
    "DATABASE_URL", 
    "postgresql://neondb_owner:RmJGSXldUY69@ep-lively-frost-a250gi75.eu-central-1.aws.neon.tech/coral_raid_tiara_871589"
)

# -----------------------------
# Security Configuration
# -----------------------------
os.environ.setdefault("SECRET_KEY", "LQm8KztTWpBz3D-")

# -----------------------------
# Environment Variables
# -----------------------------
if os.path.exists("env.py"):
    import env

# -----------------------------
# Cloudinary Media Storage
# -----------------------------
# Handles media file storage and delivery
# Configure cloud name, API key, and secret for Cloudinary service
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'dki11spup'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', '651583882481459'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'oVB9sTCGPjJCl05vx3bjBNEZ0Eg')
)