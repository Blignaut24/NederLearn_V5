# ------------------------------------------------------------------------
# Django Test Suite for NederLearn Blog Views
# Purpose: Comprehensive testing of blog functionality and user interactions
#------------------------------------------------------------------------

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Blogpost, MediaCategory, Comment, UserProfile
import datetime


class TestViews(TestCase):

    def setUp(self):
        """
        Initialize test environment with mock data:
        - Creates test users (owner and other user)
        - Sets up test blog posts
        - Creates test categories and comments
        """
        self.client = Client()

        # Test Users Setup
        self.owner_user = User.objects.create_user(
            username="owneruser", password="123password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="123password"
        )

        # Test Category Setup
        self.category = MediaCategory.objects.create(media_name="Test Category")

        # Test Blog Posts Setup
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

        # Test Comment Setup
        self.comment = Comment.objects.create(
            body="Test Comment",
            blogpost=self.owner_blogpost,
            user=self.owner_user,
            approved=True,
        )

        # Authentication Setup
        self.client.login(username="owneruser", password="123password")

    # ==========================================================================
    # BLOG POST TESTS
    # ==========================================================================

    def test_BlogPostList_GET(self):
        """
        GIVEN: A request to view the blog post list
        WHEN: A GET request is made to the home page
        THEN: Verify correct response, template, and context
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("blogposts", response.context)

    def test_BlogpostCreateView_GET(self):
        """
        GIVEN: An authenticated user
        WHEN: User attempts to access blog post creation page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("blogpost_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_create.html")

    def test_create_blogpost(self):
        """
        GIVEN: An authenticated user with valid blog post data
        WHEN: User submits new blog post
        THEN: Verify successful creation and redirect
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
        GIVEN: An authenticated post owner
        WHEN: User attempts to access post update page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("blogpost_update", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_update.html")

    def test_update_blogpost(self):
        """
        GIVEN: An authenticated post owner with valid update data
        WHEN: User submits post update
        THEN: Verify successful update and redirect
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
        GIVEN: An authenticated post owner
        WHEN: User attempts to access post deletion page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("blogpost_delete", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_delete.html")

    def test_delete_blogpost(self):
        """
        GIVEN: An authenticated post owner
        WHEN: User confirms post deletion
        THEN: Verify successful deletion
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
        GIVEN: An authenticated user
        WHEN: User accesses their posts page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_posts.html")

    def test_MyBlogPostsView_access(self):
        """
        GIVEN: A different authenticated user
        WHEN: User accesses posts page
        THEN: Verify successful access
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("my_posts"))
        self.assertEqual(response.status_code, 200)

    def test_BlogPostDetail_GET(self):
        """
        GIVEN: A specific blog post
        WHEN: User accesses post detail page
        THEN: Verify successful access and correct template
        """
        response = self.client.get(
            reverse("blogpost_detail", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blogpost_detail.html")

    def test_submit_comment(self):
        """
        GIVEN: An authenticated user with valid comment data
        WHEN: User submits a comment on a post
        THEN: Verify successful comment creation
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
        GIVEN: An authenticated user
        WHEN: User likes/unlikes a post
        THEN: Verify successful response
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("like_unlike", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 302)

    def test_bookmarked_GET(self):
        """
        GIVEN: An authenticated user
        WHEN: User accesses bookmarked posts
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("bookmarked"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookmarked.html")

    def test_BookmarkUnbookmark_POST(self):
        """
        GIVEN: An authenticated user
        WHEN: User bookmarks/unbookmarks a post
        THEN: Verify successful response
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("bookmark_unbookmark", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 302)

    # ==========================================================================
    # USER PROFILE TESTS
    # ==========================================================================

    def test_ProfileView_GET(self):
        """
        GIVEN: An authenticated user
        WHEN: User accesses their profile
        THEN: Verify successful access and correct template/context
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertIn("profile", response.context)

    def test_OtherUserProfileView_GET(self):
        """
        GIVEN: An authenticated user
        WHEN: User views another user's profile
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(
            reverse("other_user_profile", args=[self.other_user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_ProfileEditView_GET(self):
        """
        GIVEN: An authenticated user
        WHEN: User accesses profile edit page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_edit.html")

    def test_ProfileEditView_access(self):
        """
        GIVEN: A different authenticated user
        WHEN: User accesses profile edit page
        THEN: Verify successful access
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("profile_edit"))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_profile(self):
        """
        GIVEN: An authenticated user with valid profile update data
        WHEN: User submits profile updates
        THEN: Verify successful update
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
        GIVEN: An authenticated user
        WHEN: User accesses account deletion page
        THEN: Verify successful access and correct template
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.get(reverse("account_delete", args=[self.owner_user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_manage.html")

    def test_ProfileDeleteView_access(self):
        """
        GIVEN: A different authenticated user
        WHEN: User accesses account deletion page
        THEN: Verify successful access
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(reverse("account_delete", args=[self.other_user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_profile(self):
        """
        GIVEN: An authenticated user
        WHEN: User confirms account deletion
        THEN: Verify successful deletion
        """
        self.client.login(username="owneruser", password="123password")
        response = self.client.post(
            reverse("account_delete", args=[self.owner_user.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="owneruser").exists())

    # ==========================================================================
    # ERROR HANDLING TESTS
    # ==========================================================================

    def test_BlogpostUpdateView_unauthorized_access(self):
        """
        GIVEN: An authenticated user who doesn't own the post
        WHEN: User attempts to update another's post
        THEN: Verify access denied (404)
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(
            reverse("blogpost_update", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_BlogpostDeleteView_unauthorized_access(self):
        """
        GIVEN: An authenticated user who doesn't own the post
        WHEN: User attempts to delete another's post
        THEN: Verify access denied (404)
        """
        self.client.login(username="otheruser", password="123password")
        response = self.client.get(
            reverse("blogpost_delete", args=[self.owner_blogpost.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_BlogPostList_method_not_allowed(self):
        """
        GIVEN: A POST request to a GET-only endpoint
        WHEN: POST request is made to home page
        THEN: Verify method not allowed (405)
        """
        response = self.client.post(reverse("home"))
        self.assertEqual(response.status_code, 405)
