# -----------------------------------------------------------------------------
# DJANGO TEST SUITE: NEDERLEARN APP MODELS
# -----------------------------------------------------------------------------
# Purpose: Validates the core functionality of all models in the Culture Club app
# -----------------------------------------------------------------------------

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import UserProfile, MediaCategory, Blogpost, Comment


class TestModels(TestCase):
    """
    Test suite for validating model functionality in the Culture Club app.
    Covers: User Profiles, Media Categories, Blog Posts, and Comments
    """

    def setUp(self):
        """
        Initialize test data:
        1. Create test user (triggers automatic UserProfile creation)
        2. Create media category
        3. Create sample blog post
        4. Create associated comment
        """
        # Test user setup
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Media category setup
        self.test_category = MediaCategory.objects.create(media_name="Test Category")

        # Blog post setup with required fields
        self.test_blogpost = Blogpost.objects.create(
            blog_title="Test Title",
            content="Test Content",
            author=self.test_user,
            media_category=self.test_category,
            release_year=2021,
        )

        # Comment setup with all fields
        self.test_comment = Comment.objects.create(
            body="Test Comment Body",
            blogpost=self.test_blogpost,
            user=self.test_user,
            approved=True,
        )

    def test_user_profile_creation(self):
        """
        Verify: UserProfile auto-creation on new user registration
        Expected: UserProfile instance exists for test user
        """
        self.assertTrue(
            UserProfile.objects.filter(user=self.test_user).exists()
        )

    def test_media_category_creation(self):
        """
        Verify: MediaCategory creation and field accuracy
        Expected: Category name matches input
        """
        self.assertEqual(self.test_category.media_name, "Test Category")

    def test_blogpost_creation(self):
        """
        Verify: Blogpost creation and relationship integrity
        Expected: All fields match input values and relationships are maintained
        """
        self.assertEqual(self.test_blogpost.blog_title, "Test Title")
        self.assertEqual(self.test_blogpost.author, self.test_user)
        self.assertEqual(
            self.test_blogpost.media_category, self.test_category
        )

    def test_comment_creation(self):
        """
        Verify: Comment creation and relationship integrity
        Expected: Comment body matches input and relationships are properly established
        """
        self.assertEqual(self.test_comment.body, "Test Comment Body")
        self.assertEqual(self.test_comment.blogpost, self.test_blogpost)
        self.assertEqual(self.test_comment.user, self.test_user)
        self.assertTrue(self.test_comment.approved)
