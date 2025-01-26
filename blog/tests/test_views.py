"""
Django Test Suite for NederLearn Blog Application
------------------------------------------------
This test suite covers views for blog posts, user profiles, and error handling.
Author: Johann-Jurgens Blignaut
Date: 2025-01-26
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Blogpost, MediaCategory, Comment, UserProfile
import datetime


class TestViews(TestCase):
    """
    Test suite for all view functionalities in the Culture Club blog application.
    Includes tests for blog posts, user profiles, and error handling.
    """

    def setUp(self):
        """
        Initialize test environment with required objects:
        - Test client
        - Two users (owner and other)
        - Media category
        - Sample blog posts
        - Sample comment
        """
        self.client = Client()

        # Create test users
        self.owner_user = User.objects.create_user(
            username="owneruser", password="123password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="123password"
        )

        # Create test category
        self.category = MediaCategory.objects.create(media_name="Test Category")

        # Create test blog posts
        self.owner_blogpost = Blogpost.objects.create(
            blog_title="Owner's Post",
            content="Test Content",
            author=self.owner_user,
            media_category=self.category,
            release_year=2021,
            status=1,
        )

        self.other_blogpost = Blogpost.objects.create(
            blog_title="Other's Post",
            content="Test Content",
            author=self.other_user,
            media_category=self.category,
            release_year=2021,
            status=1,
        )

        # Create test comment
        self.comment = Comment.objects.create(
            body="Test Comment",
            blogpost=self.owner_blogpost,
            user=self.owner_user,
            approved=True,
        )

        # Set up authentication
        self.client.login(username="owneruser", password="123password")

    ###################
    # BLOG POST TESTS #
    ###################

    def test_BlogPostList_GET(self):
        """
        Verify blog post list view:
        - Returns 200 status code
        - Uses correct template
        - Contains blogposts in context
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("blogposts", response.context)

    def test_BlogpostCreateView_GET(self):
        """
        Verify blog post creation view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("blogpost_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_create.html")

    def test_create_blogpost(self):
        """
        Verify blog post creation functionality:
        - Creates new post
        - Redirects to detail view
        """
        self.client.login(username="owneruser", password="123password")
        post_data = {
            "blog_title": "New Post",
            "content": "Content for new post",
            "excerpt": "Short excerpt",
            "media_category": self.category.id,
            "release_year": datetime.datetime.now().year,
            "media_link": "http://www.example.com",
        }
        response = self.client.post(reverse("blogpost_create"), post_data)
        self.assertEqual(response.status_code, 302)
        new_post = Blogpost.objects.get(blog_title="New Post")
        self.assertRedirects(response, reverse("blogpost_detail", args=[new_post.slug]))

    def test_BlogpostUpdateView_GET(self):
        """
        Verify blog post update view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("blogpost_update", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_update.html")

    def test_update_blogpost(self):
        """
        Verify blog post update functionality:
        - Updates existing post
        - Redirects to detail view
        - Content is updated correctly
        """
        self.client.login(username="owneruser", password="123password")
        update_data = {
            "blog_title": "Updated Post",
            "content": "Updated content",
            "excerpt": "Updated excerpt",
            "media_category": self.category.id,
            "release_year": datetime.datetime.now().year,
            "media_link": "http://www.updated.com",
        }
        response = self.client.post(
            reverse("blogpost_update", args=[self.owner_blogpost.slug]), update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("blogpost_detail", args=[self.owner_blogpost.slug])
        )
        self.owner_blogpost.refresh_from_db()
        self.assertEqual(self.owner_blogpost.content, "Updated content")

    def test_BlogpostDeleteView_GET(self):
        """
        Verify blog post delete view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("blogpost_delete", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_delete.html")

    def test_delete_blogpost(self):
        """
        Verify blog post deletion:
        - Post is removed from database
        - Redirects correctly
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("blogpost_delete", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Blogpost.objects.filter(slug=self.owner_blogpost.slug).exists()
        )

    def test_MyBlogPostsView_GET(self):
        """
        Verify user's blog posts view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_posts.html")

    def test_MyBlogPostsView_access(self):
        """
        Verify access to user's blog posts by different user:
        - Returns 200 status code
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("my_posts"))
        self.assertEqual(response.status_code, 200)

    def test_BlogPostDetail_GET(self):
        """
        Verify blog post detail view:
        - Returns 200 status code
        - Uses correct template
        """
        response = self.client.get(
            reverse("blogpost_detail", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_detail.html")

    def test_submit_comment(self):
        """
        Verify comment submission:
        - Comment is created
        - Content is correct
        """
        self.client.login(username="owneruser", password="123password")
        comment_data = {"body": "This is a test comment."}
        response = self.client.post(
            reverse("blogpost_detail", args=[self.owner_blogpost.slug]), comment_data
        )
        self.assertEqual(response.status_code, 200)
        new_comment = Comment.objects.filter(
            blogpost=self.owner_blogpost, user=self.owner_user
        ).last()
        self.assertIsNotNone(new_comment)
        self.assertEqual(new_comment.body, "This is a test comment.")

    def test_LikeUnlike_POST(self):
        """
        Verify like/unlike functionality:
        - Returns correct redirect status
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("like_unlike", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 302)

    def test_bookmarked_GET(self):
        """
        Verify bookmarked posts view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("bookmarked"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookmarked.html")

    def test_BookmarkUnbookmark_POST(self):
        """
        Verify bookmark/unbookmark functionality:
        - Returns correct redirect status
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("bookmark_unbookmark", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 302)

    ##################
    # PROFILE TESTS #
    ##################

    def test_ProfileView_GET(self):
        """
        Verify profile view:
        - Returns 200 status code
        - Uses correct template
        - Contains profile in context
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertIn("profile", response.context)

    def test_OtherUserProfileView_GET(self):
        """
        Verify other user's profile view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("other_user_profile", args=[self.other_user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_ProfileEditView_GET(self):
        """
        Verify profile edit view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_edit.html")

    def test_ProfileEditView_access(self):
        """
        Verify profile edit access by different user:
        - Returns 200 status code
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_profile(self):
        """
        Verify profile update functionality:
        - Updates profile data
        - Content is updated correctly
        """
        self.client.login(username="owneruser", password="123password")
        update_data = {
            "bio": "Updated bio",
            "country": "Updated country",
            "top_movies": "Updated movies",
            "top_series": "Updated series",
            "top_music_albums": "Updated music albums",
            "top_books": "Updated books",
            "top_podcasts": "Updated podcasts",
            "top_miscellaneous": "Updated miscellaneous",
        }
        response = self.client.post(reverse("profile_edit"), update_data)
        self.assertEqual(response.status_code, 302)
        updated_profile = UserProfile.objects.get(user__username="owneruser")
        self.assertEqual(updated_profile.bio, "Updated bio")
        self.assertEqual(updated_profile.country, "Updated country")

    def test_ProfileDeleteView_GET(self):
        """
        Verify profile delete view:
        - Returns 200 status code
        - Uses correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("account_delete", args=[self.owner_user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_manage.html")

    def test_ProfileDeleteView_access(self):
        """
        Verify profile delete access by different user:
        - Returns 200 status code
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("account_delete", args=[self.other_user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_profile(self):
        """
        Verify profile deletion:
        - User is removed from database
        - Returns correct redirect status
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("account_delete", args=[self.owner_user.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="owneruser").exists())

    #######################
    # ERROR HANDLER TESTS #
    #######################

    def test_BlogpostUpdateView_unauthorized_access(self):
        """
        Verify unauthorized access handling for update view:
        - Returns 404 status code
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(
            reverse("blogpost_update", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_BlogpostDeleteView_unauthorized_access(self):
        """
        Verify unauthorized access handling for delete view:
        - Returns 404 status code
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(
            reverse("blogpost_delete", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_BlogPostList_method_not_allowed(self):
        """
        Verify method not allowed handling:
        - Returns 405 status code for POST request to GET-only view
        """
        response = self.client.post(reverse("home"))
        self.assertEqual(response.status_code, 405)
