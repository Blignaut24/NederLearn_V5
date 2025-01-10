# =======================================
# DATABASE CONFIGURATION
# =======================================
# Sets up connection to PostgreSQL database hosted on Neon

import os

# Configure database connection URL
# -------------------------------
# Format: postgresql://{username}:{password}@{host}/{database_name}
# WARNING: Never commit credentials to version control!
os.environ.setdefault(
    "DATABASE_URL", 
    "postgresql://neondb_owner:RmJGSXldUY69@ep-lively-frost-a250gi75.eu-central-1.aws.neon.tech/coral_raid_tiara_871589"
)
os.environ.setdefault("SECRET_KEY", "LQm8KztTWpBz3D-")