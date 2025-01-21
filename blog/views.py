# Django imports for rendering views and handling HTTP responses
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Blogpost, Comment, MediaCategory
from .forms import CommentForm

# Import models from current directory
from .models import Blogpost, Comment, MediaCategory


def index(request):
    return render(request, "index.html")


# List View for Blog Posts
class BlogpostPostList(generic.ListView):
    """
    Shows a list of blog posts with 6 posts per page, using the Blogpost model to get only published posts.
    """

    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by("created_on")
    context_object_name = "blogposts"
    template_name = "index.html"
    paginate_by = 6


# Blog post detail view
class BlogPostDetail(View):
    """
    Displays blog posts with comments and user like status.
    """

    def get(self, request, slug, *args, **kwargs):
        # Get published post or 404
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        # Get approved comments
        comments = blogpost.comments.filter(approved=True).order_by("created_on")
        # Check if user has liked post
        liked = False
        if blogpost.likes.filter(id=self.request.user.id).exists():
            liked = True
        # Render template with context
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
        queryset = Blogpost.objects.filter(status=1)
        blogpost = get_object_or_404(queryset, slug=slug)
        comments = blogpost.comments.filter(approved=True).order_by("created_on")
        liked = blogpost.likes.filter(id=request.user.id).exists()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blogpost = blogpost
            comment.user = request.user  # Assign the current user to the comment
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
