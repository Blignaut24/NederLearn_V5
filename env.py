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
    "postgresql://neondb_owner:RmJGSXldUY69@ep-lively-frost-a250gi75.eu-central-1.aws.neon.tech/coral_raid_tiara_871589",
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

os.environ.setdefault(
    "CLOUDINARY_URL",
    "cloudinary://651583882481459:oVB9sTCGPjJCl05vx3bjBNEZ0Eg@dki11spup",
)

#CLOUDINARY_URL = "cloudinary://#651583882481459:oVB9sTCGPjJCl05vx3bjBNEZ0Eg@dki11spup"
