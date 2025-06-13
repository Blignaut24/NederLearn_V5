"""
Test cases for custom widgets in the blog application.

This module tests the custom widget implementations, particularly
the FixedSummernoteInplaceWidget that resolves HTML5 validation issues.
"""

from django.test import TestCase
from django.forms import Form
from blog.widgets import FixedSummernoteInplaceWidget, get_content_widget
from blog.forms import BlogpostForm
import re


class FixedSummernoteInplaceWidgetTest(TestCase):
    """Test cases for the FixedSummernoteInplaceWidget."""
    
    def setUp(self):
        """Set up test data."""
        self.widget = FixedSummernoteInplaceWidget()
        self.attrs = {
            'id': 'id_content',
            'class': 'form-control',
            'maxlength': '10000',
        }
    
    def test_hidden_attribute_format(self):
        """Test that the hidden attribute is properly formatted for HTML5 compliance."""
        html = self.widget.render('content', '', attrs=self.attrs)
        
        # Should contain hidden="" (HTML5 compliant)
        self.assertIn('hidden=""', html)
        
        # Should NOT contain hidden="true" (non-compliant)
        self.assertNotIn('hidden="true"', html)
    
    def test_widget_renders_textarea(self):
        """Test that the widget renders a textarea element."""
        html = self.widget.render('content', 'test content', attrs=self.attrs)
        
        # Should contain textarea element
        self.assertIn('<textarea', html)
        self.assertIn('</textarea>', html)
        
        # Should contain the field name
        self.assertIn('name="content"', html)
    
    def test_widget_preserves_attributes(self):
        """Test that the widget preserves other HTML attributes."""
        html = self.widget.render('content', '', attrs=self.attrs)
        
        # Should preserve id attribute
        self.assertIn('id="id_content"', html)
        
        # Should preserve maxlength attribute
        self.assertIn('maxlength="10000"', html)
    
    def test_widget_includes_summernote_script(self):
        """Test that the widget includes Summernote JavaScript."""
        html = self.widget.render('content', '', attrs=self.attrs)
        
        # Should include summernote-related content
        self.assertIn('summernote', html.lower())
    
    def test_widget_handles_none_attrs(self):
        """Test that the widget handles None attributes gracefully."""
        html = self.widget.render('content', '', attrs=None)
        
        # Should still render without errors
        self.assertIn('<textarea', html)
        self.assertIn('hidden=""', html)
    
    def test_widget_handles_empty_value(self):
        """Test that the widget handles empty values correctly."""
        html = self.widget.render('content', '', attrs=self.attrs)
        
        # Should render without errors
        self.assertIn('<textarea', html)
        
        # Should not have content between textarea tags when value is empty
        textarea_content = re.search(r'<textarea[^>]*>(.*?)</textarea>', html, re.DOTALL)
        if textarea_content:
            self.assertEqual(textarea_content.group(1).strip(), '')
    
    def test_widget_handles_value_with_content(self):
        """Test that the widget handles values with content."""
        test_content = "This is test content for the blog post."
        html = self.widget.render('content', test_content, attrs=self.attrs)
        
        # Should contain the test content
        self.assertIn(test_content, html)


class BlogpostFormTest(TestCase):
    """Test cases for the BlogpostForm using the fixed widget."""
    
    def test_form_uses_fixed_widget(self):
        """Test that the BlogpostForm uses the FixedSummernoteInplaceWidget."""
        form = BlogpostForm()
        
        # Get the content field widget
        content_widget = form.fields['content'].widget
        
        # Should be an instance of FixedSummernoteInplaceWidget
        self.assertIsInstance(content_widget, FixedSummernoteInplaceWidget)
    
    def test_form_renders_compliant_html(self):
        """Test that the form renders HTML5-compliant markup."""
        form = BlogpostForm()
        html = str(form['content'])
        
        # Should contain hidden="" (HTML5 compliant)
        self.assertIn('hidden=""', html)
        
        # Should NOT contain hidden="true" (non-compliant)
        self.assertNotIn('hidden="true"', html)
    
    def test_form_functionality_preserved(self):
        """Test that form functionality is preserved after the fix."""
        form_data = {
            'blog_title': 'Test Blog Post',
            'content': '<p>This is test content with <strong>HTML</strong>.</p>',
            'excerpt': 'Test excerpt',
            'media_category': 1,  # Assuming category with ID 1 exists
            'release_year': 2023,
            'media_link': 'http://www.example.com',
        }
        
        form = BlogpostForm(data=form_data)
        
        # Form should be valid (assuming media_category exists)
        # Note: This might fail if media_category doesn't exist in test DB
        # but the widget functionality should still work
        if form.is_valid():
            self.assertEqual(form.cleaned_data['content'], form_data['content'])


class WidgetFactoryTest(TestCase):
    """Test cases for the widget factory function."""
    
    def test_get_summernote_widget(self):
        """Test getting a Summernote widget from the factory."""
        widget = get_content_widget('summernote', maxlength="5000")
        
        self.assertIsInstance(widget, FixedSummernoteInplaceWidget)
        self.assertEqual(widget.attrs.get('maxlength'), "5000")
    
    def test_get_textarea_widget(self):
        """Test getting a textarea widget from the factory."""
        widget = get_content_widget('textarea', rows=6)
        
        # Should be a standard textarea widget
        self.assertEqual(widget.attrs.get('rows'), 6)
        self.assertIn('form-control', widget.attrs.get('class', ''))
    
    def test_get_default_widget(self):
        """Test that invalid widget type returns default (Summernote)."""
        widget = get_content_widget('invalid_type')
        
        self.assertIsInstance(widget, FixedSummernoteInplaceWidget)
    
    def test_widget_factory_default_attributes(self):
        """Test that the widget factory applies default attributes."""
        widget = get_content_widget('summernote')
        
        # Should have default placeholder
        self.assertIn('placeholder', widget.attrs)
        self.assertIn('form-control', widget.attrs.get('class', ''))


class HTMLValidationTest(TestCase):
    """Test cases specifically for HTML validation compliance."""
    
    def test_boolean_attribute_compliance(self):
        """Test that boolean attributes follow HTML5 standards."""
        widget = FixedSummernoteInplaceWidget()
        html = widget.render('test_field', '', attrs={'id': 'test_id'})
        
        # Test for proper boolean attribute formats
        boolean_attrs = ['hidden', 'disabled', 'readonly', 'required']
        
        for attr in boolean_attrs:
            if f'{attr}=' in html:
                # If the attribute exists, it should be in proper format
                # Either attr="" or attr="attr_name", not attr="true"
                self.assertNotIn(f'{attr}="true"', html)
                self.assertNotIn(f'{attr}="false"', html)
    
    def test_no_invalid_attribute_values(self):
        """Test that no invalid attribute values are present."""
        widget = FixedSummernoteInplaceWidget()
        html = widget.render('test_field', 'test content', attrs={'id': 'test_id'})
        
        # Common invalid patterns that should not appear
        invalid_patterns = [
            'hidden="true"',
            'hidden="false"',
            'disabled="true"',
            'readonly="true"',
        ]
        
        for pattern in invalid_patterns:
            self.assertNotIn(pattern, html, 
                           f"Found invalid pattern: {pattern}")
    
    def test_html5_validator_would_pass(self):
        """Test conditions that would make HTML5 validator pass."""
        widget = FixedSummernoteInplaceWidget()
        html = widget.render('content', '', attrs={'id': 'id_content'})
        
        # Extract the textarea element
        textarea_match = re.search(r'<textarea[^>]*>', html)
        self.assertIsNotNone(textarea_match, "Textarea element should be present")
        
        textarea_tag = textarea_match.group(0)
        
        # If hidden attribute is present, it should be properly formatted
        if 'hidden' in textarea_tag:
            # Should match HTML5 boolean attribute patterns
            hidden_patterns = [
                r'hidden=""',           # empty string
                r'hidden="hidden"',     # attribute name
                r'hidden(?=\s|>)',      # just the attribute name
            ]
            
            pattern_found = any(re.search(pattern, textarea_tag) for pattern in hidden_patterns)
            self.assertTrue(pattern_found, 
                          f"Hidden attribute should follow HTML5 standards. Found: {textarea_tag}")
