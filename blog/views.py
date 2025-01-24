# =============================================================================
# 1. IMPORTS & SETUP
# =============================================================================

# Standard Django imports for core functionality
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# User authentication and permissions
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

# Local application imports
from .models import Blogpost, UserProfile
from .forms import CommentForm, UserProfileForm, BlogpostForm


# =============================================================================
# 2. BLOG POST MANAGEMENT (CRUD)
# =============================================================================
"""
Core blog functionality implementing Create, Read, Update, Delete operations
All views require user authentication via LoginRequiredMixin
"""


class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Creates new blog posts
    - Assigns current user as author
    - Handles form validation
    - Redirects to post detail on success
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Updates existing blog posts
    - Validates form data
    - Maintains author attribution
    - Redirects to updated post
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_update.html"
    success_url = reverse_lazy("blogpost_detail")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost_detail", kwargs={"slug": self.object.slug})


class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Handles post deletion
    - Requires confirmation
    - Redirects to home page after deletion
    """

    model = Blogpost
    template_name = "blogpost_confirm_delete.html"
    success_url = reverse_lazy("home")


# =============================================================================
# 3. CORE VIEWS
# =============================================================================
"""
Basic application views and navigation endpoints
"""


def index(request):
    """Landing page view"""
    return render(request, "index.html")


# =============================================================================
# 4. BLOG CONTENT DISPLAY
# =============================================================================
"""
Views for displaying blog content:
- List view with pagination
- Detailed post view with comments
"""


class BlogpostPostList(generic.ListView):
    """
    Main blog listing page
    Features:
    - Pagination (6 posts per page)
    - Status filtering (active only)
    - Reverse chronological order
    - Authentication required
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """Authentication check before access"""
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)


class BlogPostDetail(View):
    """
    Individual blog post display
    Features:
    - Post content
    - Comments section
    - Like status
    - Comment submission
    """

    def get(self, request, slug, *args, **kwargs):
        """
        GET: Display post and related content
        - Fetches post details
        - Shows approved comments
        - Checks like status
        """
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = blogpost.likes.filter(id=self.request.user.id).exists()

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        POST: Handle comment submission
        - Validates comment form
        - Associates comment with post and user
        - Updates view context
        """
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by("created_on")
        liked = blogpost.likes.filter(id=request.user.id).exists()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": comment_form,
            },
        )


# =============================================================================
# 5. USER INTERACTIONS
# =============================================================================
"""
Handles user engagement features (likes, etc.)
"""


class LikeUnlike(View):
    """
    Toggle post likes
    - Checks current like status
    - Updates accordingly
    - Redirects back to post
    """

    def post(self, request, slug, *args, **kwargs):
        """Toggle like status for current user"""
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# =============================================================================
# 6. USER PROFILE SYSTEM
# =============================================================================
"""
Profile management system:
- View own profile
- View other profiles
- Edit profile
"""


class ProfileView(View):
    """Display user's own profile"""

    def get(self, request):
        """Fetch and show current user's profile"""
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """View other users' profiles"""

    def get(self, request, username):
        """Fetch and display requested user's profile"""
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        context = {
            "profile": user_profile,
            "is_own_profile": request.user == user,
        }
        return render(request, "profile.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    Handle profile updates
    Features:
    - Form display
    - Image upload
    - Profile data updates
    """

    def get(self, request):
        """Display profile edit form"""
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        """Process profile updates"""
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})
