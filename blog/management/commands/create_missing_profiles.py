"""
Django management command to create missing UserProfile instances.

This command finds all User instances that don't have a corresponding
UserProfile and creates them with default values.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import UserProfile


class Command(BaseCommand):
    help = 'Create UserProfile instances for users that don\'t have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating profiles',
        )

    def handle(self, *args, **options):
        """
        Main command execution logic.
        """
        dry_run = options['dry_run']
        
        # Find users without profiles
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        
        if not users_without_profiles.exists():
            self.stdout.write(
                self.style.SUCCESS('All users already have UserProfile instances.')
            )
            return
        
        count = users_without_profiles.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would create {count} UserProfile instances for:'
                )
            )
            for user in users_without_profiles:
                self.stdout.write(f'  - User: {user.username} (ID: {user.id})')
            return
        
        # Create missing profiles
        created_profiles = []
        for user in users_without_profiles:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_profiles.append(profile)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created UserProfile for user: {user.username}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_profiles)} UserProfile instances.'
            )
        )
