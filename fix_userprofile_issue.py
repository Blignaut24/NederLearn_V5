#!/usr/bin/env python
"""
Script to fix the UserProfile RelatedObjectDoesNotExist error.

This script will:
1. Check for users without UserProfile instances
2. Create missing UserProfile instances
3. Verify the fix

Run this script from your Django project root directory.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nederlearn.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile


def check_missing_profiles():
    """Check for users without UserProfile instances."""
    users_without_profiles = User.objects.filter(userprofile__isnull=True)
    return users_without_profiles


def create_missing_profiles():
    """Create UserProfile instances for users that don't have one."""
    users_without_profiles = check_missing_profiles()
    
    if not users_without_profiles.exists():
        print("✅ All users already have UserProfile instances.")
        return 0
    
    count = users_without_profiles.count()
    print(f"🔍 Found {count} users without UserProfile instances:")
    
    for user in users_without_profiles:
        print(f"   - User: {user.username} (ID: {user.id})")
    
    print("\n🔧 Creating missing UserProfile instances...")
    
    created_count = 0
    for user in users_without_profiles:
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            created_count += 1
            print(f"   ✅ Created UserProfile for user: {user.username}")
    
    print(f"\n🎉 Successfully created {created_count} UserProfile instances!")
    return created_count


def verify_fix():
    """Verify that all users now have UserProfile instances."""
    users_without_profiles = check_missing_profiles()
    
    if users_without_profiles.exists():
        print(f"❌ Still {users_without_profiles.count()} users without profiles!")
        return False
    else:
        print("✅ All users now have UserProfile instances!")
        return True


def main():
    """Main function to run the fix."""
    print("🚀 UserProfile Fix Script")
    print("=" * 50)
    
    # Check current state
    print("1. Checking for missing UserProfile instances...")
    missing_count = check_missing_profiles().count()
    
    if missing_count == 0:
        print("✅ No missing UserProfile instances found. Nothing to fix!")
        return
    
    print(f"⚠️  Found {missing_count} users without UserProfile instances.")
    
    # Ask for confirmation
    response = input("\nDo you want to create missing UserProfile instances? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    # Create missing profiles
    print("\n2. Creating missing UserProfile instances...")
    created_count = create_missing_profiles()
    
    # Verify the fix
    print("\n3. Verifying the fix...")
    if verify_fix():
        print("\n🎉 UserProfile issue has been fixed!")
        print("You should now be able to log in without the RelatedObjectDoesNotExist error.")
    else:
        print("\n❌ Something went wrong. Please check the error messages above.")


if __name__ == "__main__":
    main()
