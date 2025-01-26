# Django imports
from django.apps import AppConfig


# Main configuration class for Blog application
class BlogConfig(AppConfig):
    """
    Sets up the basic settings for the Blog app and manages how it starts up
    """

    #  Uses a unique ID number that can handle very large values as the main identifier for each item
    default_auto_field = "django.db.models.BigAutoField"
    # Application name identifier
    name = "blog"
    verbose_name = 'Blog'

    def ready(self):
        """
        Runs at Django startup to initialize signal handlers.
        """
        import blog.signals
