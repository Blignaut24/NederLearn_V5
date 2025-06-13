"""
Custom widgets for the blog application.

This module contains custom widget implementations that fix issues
with third-party packages while maintaining functionality.
"""

from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django_summernote.utils import get_config
from django import forms
import json


class FixedSummernoteInplaceWidget(SummernoteInplaceWidget):
    """
    Custom Summernote widget that fixes the HTML5 validation error
    with the 'hidden' attribute implementation.
    
    The original django-summernote package incorrectly sets hidden="true"
    which violates HTML5 standards. This widget corrects the implementation
    to use proper boolean attribute syntax.
    
    Bug Fix: Changes hidden="true" to hidden="" for HTML5 compliance
    """
    
    def render(self, name, value, attrs=None, **kwargs):
        """
        Render the widget with corrected hidden attribute implementation.
        
        Args:
            name (str): The field name
            value (str): The field value
            attrs (dict): HTML attributes for the widget
            **kwargs: Additional keyword arguments
            
        Returns:
            str: Rendered HTML with proper hidden attribute
        """
        # Initialize attrs if None
        if attrs is None:
            attrs = {}
            
        # Create a copy to avoid modifying the original
        attrs_for_textarea = attrs.copy()
        
        # Fix: Use empty string for boolean hidden attribute (HTML5 compliant)
        # Instead of hidden="true" (non-compliant)
        attrs_for_textarea['hidden'] = ''
        
        # Get summernote settings
        summernote_settings = self.summernote_settings()
        summernote_settings.update(attrs.get('summernote', {}))
        
        # Render the textarea with corrected attributes
        # Call the grandparent's render method to bypass the buggy implementation
        html = forms.Textarea.render(
            self, name, value, attrs=attrs_for_textarea, **kwargs
        )
        
        # Add the summernote JavaScript and styling
        context = {
            'id': attrs.get('id', f'id_{name}'),
            'id_safe': attrs.get('id', f'id_{name}').replace('-', '_'),
            'attrs': self.final_attr(attrs),
            'config': get_config(),
            'settings': json.dumps(summernote_settings),
            'CSRF_COOKIE_NAME': getattr(__import__('django.conf', fromlist=['settings']).settings, 'CSRF_COOKIE_NAME', 'csrftoken'),
        }
        
        html += render_to_string('django_summernote/widget_inplace.html', context)
        return mark_safe(html)
    
    def final_attr(self, attrs):
        """
        Process final attributes for the widget.
        
        Args:
            attrs (dict): Original attributes
            
        Returns:
            dict: Processed attributes
        """
        attrs_for_final = attrs.copy()
        attrs_for_final.update(self.attrs)
        attrs_for_final.pop('id', None)
        
        # Remove form-control class that can interfere with crispy forms
        if 'class' in attrs_for_final:
            attrs_for_final['class'] = attrs_for_final['class'].replace(' form-control', '')
            
        return attrs_for_final


class StandardTextareaWidget(forms.Textarea):
    """
    Standard textarea widget with enhanced styling options.
    
    This widget provides a fallback option for cases where
    rich text editing is not needed but consistent styling is desired.
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'rows': 4,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


# Widget choices for easy switching between rich text and plain text
CONTENT_WIDGET_CHOICES = {
    'summernote': FixedSummernoteInplaceWidget,
    'textarea': StandardTextareaWidget,
}


def get_content_widget(widget_type='summernote', **widget_attrs):
    """
    Factory function to get the appropriate content widget.
    
    Args:
        widget_type (str): Type of widget ('summernote' or 'textarea')
        **widget_attrs: Additional attributes for the widget
        
    Returns:
        Widget instance configured with the provided attributes
        
    Example:
        # Get a Summernote widget
        widget = get_content_widget('summernote', maxlength="10000")
        
        # Get a standard textarea
        widget = get_content_widget('textarea', rows=6)
    """
    widget_class = CONTENT_WIDGET_CHOICES.get(widget_type, FixedSummernoteInplaceWidget)
    
    default_attrs = {
        'placeholder': 'Write your content here...',
        'class': 'form-control',
    }
    default_attrs.update(widget_attrs)
    
    return widget_class(attrs=default_attrs)
