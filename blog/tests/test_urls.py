# ===================================
# URL Testing Configuration
# ===================================
# Import required Django testing and view modules
from django.test import SimpleTestCase
from django.views.generic.base import TemplateView
from django.urls import reverse, resolve

# Import all blog-related views for testing
from blog.views import (BlogPostList, BlogpostCreateView, BlogPostDetail, 
                        BlogpostUpdateView, BlogpostDeleteView, MyBlogPostsView,
                        LikeUnlike, ProfileView, OtherUserProfileView, 
                        ProfileEditView, BookmarkUnbookmark, bookmarked)

# ===================================
# URL Resolution Test Cases
# ===================================
class TestUrls(SimpleTestCase):
    """Test suite to verify URL pattern resolution for blog application"""

    # --- Main Blog Views ---
    def test_home_url_resolves(self):
        """Verify home page URL resolves to BlogPostList view"""
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, BlogPostList)

    def test_blogpost_create_url_resolves(self):
        """Verify blog post creation URL resolves to BlogpostCreateView"""
        url = reverse('blogpost_create')
        self.assertEqual(resolve(url).func.view_class, BlogpostCreateView)

    def test_blogpost_detail_url_resolves(self):
        """Verify blog post detail URL resolves to BlogPostDetail view"""
        url = reverse('blogpost_detail', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BlogPostDetail)

    def test_blogpost_update_url_resolves(self):
        """Verify blog post update URL resolves to BlogpostUpdateView"""
        url = reverse('blogpost_update', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BlogpostUpdateView)

    def test_blogpost_delete_url_resolves(self):
        """Verify blog post deletion URL resolves to BlogpostDeleteView"""
        url = reverse('blogpost_delete', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BlogpostDeleteView)

    # --- User-Specific Views ---
    def test_my_blog_posts_url_resolves(self):
        """Verify user's posts URL resolves to MyBlogPostsView"""
        url = reverse('my_posts')
        self.assertEqual(resolve(url).func.view_class, MyBlogPostsView)

    # --- Interaction Views ---
    def test_like_unlike_url_resolves(self):
        """Verify like/unlike functionality URL resolves to LikeUnlike view"""
        url = reverse('like_unlike', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, LikeUnlike)

    # --- Profile Management Views ---
    def test_profile_url_resolves(self):
        """Verify profile URL resolves to ProfileView"""
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_other_user_profile_url_resolves(self):
        """Verify other user's profile URL resolves to OtherUserProfileView"""
        url = reverse('other_user_profile', args=['some-username'])
        self.assertEqual(resolve(url).func.view_class, OtherUserProfileView)

    def test_profile_edit_url_resolves(self):
        """Verify profile edit URL resolves to ProfileEditView"""
        url = reverse('profile_edit')
        self.assertEqual(resolve(url).func.view_class, ProfileEditView)

    # --- Bookmark Features ---
    def test_bookmark_unbookmark_url_resolves(self):
        """Verify bookmark toggle URL resolves to BookmarkUnbookmark view"""
        url = reverse('bookmark_unbookmark', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BookmarkUnbookmark)

    def test_bookmarked_url_resolves(self):
        """Verify bookmarked posts URL resolves to bookmarked view function"""
        url = reverse('bookmarked')
        self.assertEqual(resolve(url).func, bookmarked)

    # --- Static Pages ---
    def test_about_us_url_resolves(self):
        """Verify about us URL resolves to TemplateView"""
        url = reverse('about_us')
        self.assertTrue(resolve(url).func.view_class, TemplateView)