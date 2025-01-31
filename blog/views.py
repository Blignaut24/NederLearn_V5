# ------------------------------
# SECTION 1: IMPORTS
# ------------------------------

# Standard Django imports
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils.decorators import method_decorator

# View and authentication imports
from django.views import generic, View
from django.views.generic import DeleteView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Application-specific imports
from .models import Blogpost, UserProfile, MediaCategory
from .forms import CommentForm, UserProfileForm, BlogpostForm


# ------------------------------
# SECTION 2: POST MANAGEMENT
# ------------------------------


class BlogpostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Handle creation of new blog posts

    Features:
    - User authentication required
    - Auto-assigns current user as author
    - Success message display
    - Redirect to post details
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, "Your blog post has been created successfully."
        )
        return response

    def get_success_url(self):
        return reverse_lazy(
            "blogpost_detail", kwargs={"slug": self.object.slug}
        )


class BlogpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Handle updates to existing blog posts

    Features:
    - User authentication required
    - Author preservation
    - Success message display
    - Redirect to post details
    """

    model = Blogpost
    form_class = BlogpostForm
    template_name = "blogpost_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, "Your blog post has been updated successfully."
        )
        return response

    def get_success_url(self):
        return reverse_lazy(
            "blogpost_detail", kwargs={"slug": self.object.slug}
        )


class BlogpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Handle deletion of blog posts

    Features:
    - User authentication required
    - Success message display
    - Redirect to user's post list
    """

    model = Blogpost
    template_name = "blogpost_delete.html"
    success_url = reverse_lazy("my_posts")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request, "Your blog post has been deleted successfully."
        )
        return response


# ------------------------------
# SECTION 3: POST LISTING
# ------------------------------


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """
    Display user's personal posts

    Features:
    - User-specific filtering
    - Reverse chronological order
    - Pagination (6 per page)
    """

    model = Blogpost
    template_name = "my_posts.html"
    context_object_name = "my_blogposts"
    paginate_by = 6

    def get_queryset(self):
        return Blogpost.objects.filter(author=self.request.user).order_by(
            "-created_on"
        )


class BlogPostList(generic.ListView):
    """
    Display all published posts

    Features:
    - Authentication check
    - Category filtering
    - Chronological ordering
    - Pagination (6 per page)
    """

    model = Blogpost
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        """Verify user authentication"""
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Blogpost.objects.filter(status=1).order_by("-created_on")
        media_category = self.request.GET.get("category")
        if media_category:
            queryset = queryset.filter(
                media_category__media_name=media_category
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = MediaCategory.objects.all()
        return context


# ------------------------------
# SECTION 4: POST INTERACTION
# ------------------------------


class BlogPostDetail(View):
    """
    Handle individual post display and comments

    Features:
    - Post detail display
    - Comment management
    - Like status tracking
    - Form handling
    """

    def get(self, request, slug, *args, **kwargs):
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by(
            "created_on"
        )
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
        """Process comment submissions"""
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=False).order_by(
            "created_on"
        )
        liked = blogpost.likes.filter(id=request.user.id).exists()

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user
            comment.save()
            comment_form = CommentForm()

        return render(
            request,
            "blogpost_detail.html",
            {
                "blogpost": blogpost,
                "comments": comments,
                "commented": comment_form.is_valid(),
                "liked": liked,
                "comment_form": comment_form,
            },
        )


class LikeUnlike(View):
    """
    Handle post like toggling

    Features:
    - Like/unlike functionality
    - User verification
    - Redirect to post
    """

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.likes.filter(id=request.user.id).exists():
            blogpost.likes.remove(request.user)
        else:
            blogpost.likes.add(request.user)

        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# ------------------------------
# SECTION 5: USER PROFILES
# ------------------------------


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    """
    Display user profile page

    Features:
    - Authentication required
    - Personal profile display
    """

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"profile": user_profile, "is_own_profile": True}
        return render(request, "profile.html", context)


class OtherUserProfileView(View):
    """
    Display other users' profiles

    Features:
    - Profile lookup
    - Owner verification
    """

    def get(self, request, username):
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
    - Form processing
    - Success messages
    - Redirect handling
    """

    def get(self, request):
        form = UserProfileForm(instance=request.user.userprofile)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully."
            )
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handle account deletion

    Features:
    - Account removal
    - Auto logout
    - Login redirect
    """

    model = User
    template_name = "account_manage.html"
    success_url = reverse_lazy("account_login")

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)
        return response


# ------------------------------
# SECTION 6: BOOKMARKS
# ------------------------------


def bookmarked(request):
    """
    Display bookmarked posts

    Features:
    - Authentication check
    - Bookmark filtering
    """
    if request.user.is_authenticated:
        bookmarked_posts = Blogpost.objects.filter(bookmarks=request.user)
    else:
        bookmarked_posts = []

    return render(
        request, "bookmarked.html", {"bookmarked_posts": bookmarked_posts}
    )


class BookmarkUnbookmark(View):
    """
    Handle bookmark toggling

    Features:
    - Add/remove bookmarks
    - Success messages
    - Post redirect
    """

    def post(self, request, slug, *args, **kwargs):
        blogpost = get_object_or_404(Blogpost, slug=slug)
        if blogpost.bookmarks.filter(id=request.user.id).exists():
            blogpost.bookmarks.remove(request.user)
            messages.success(request, "Removed from 'Bookmarked'.")
        else:
            blogpost.bookmarks.add(request.user)
            messages.success(request, "Added to 'Bookmarked'.")
        return HttpResponseRedirect(reverse("blogpost_detail", args=[slug]))


# ------------------------------
# SECTION 7: ERROR HANDLING
# ------------------------------


def custom_403_error(request, exception):
    """Handle forbidden access errors"""
    return HttpResponseForbidden(render(request, "403.html"))


def custom_405_error(request, exception):
    """Handle method not allowed errors"""
    return HttpResponseNotAllowed(render(request, "405.html"))
