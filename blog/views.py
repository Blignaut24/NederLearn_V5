# Django imports for rendering views and handling HTTP responses
from django.shortcuts import render, HttpResponse
from django.views import generic

# Import models from current directory
from .models import Blogpost, Comment, MediaCategory


# Basic view function to test server connectivity
def index(request):
    return HttpResponse("Hello, World!")


# List View for Blog Posts
class PostList(generic.ListView):
    """
    Shows a list of blog posts with 6 posts per page, using the Blogpost model to get only published posts.
    """
    model = Blogpost
    queryset = Blogpost.objects.filter(status=1).order_by('created_on')
    template_name = 'index.html'
    paginate_by = 6