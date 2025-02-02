# NederLearn Testing Report

This document outlines the comprehensive testing process for the NederLearn Blog application. Testing is crucial to ensure our application works reliably and provides a great experience for all users.

## Key Testing Areas

1. **Code Validation**
   - Ensuring HTML, CSS, and Python code meets quality standards
2. **Accessibility**
   - Making sure the website is usable by everyone
3. **Performance**
   - Testing how the website runs on both desktop and mobile devices
4. **Device Compatibility**
   - Verifying functionality across different devices
5. **Browser Compatibility**
   - Ensuring consistent performance across different web browsers
6. **Automated Testing**
   - Using systematic tests for views, models, and URLs
7. **Manual Testing**
   - Including security checks, user story verification, and user experience testing

The testing process helps us identify and fix potential issues before they affect users, ensuring a stable and reliable platform.

Return to [**README.md**](README.md)

## Content
- [NederLearn Testing Report](#nederlearn-testing-report)
  - [Key Testing Areas](#key-testing-areas)
  - [Content](#content)
  - [Code Validation](#code-validation)
    - [HTML Validation](#html-validation)
    - [CSS](#css)
    - [Python Validation](#python-validation)
- [Accessibility](#accessibility)
- [Automated Testing](#automated-testing)
  - [Test Setup](#test-setup)
    - [File Structure](#file-structure)
    - [Running Tests](#running-tests)
    - [My Testing Strategy](#my-testing-strategy)
    - [What Do My Tests Do?](#what-do-my-tests-do)
    - [Main Things I Test](#main-things-i-test)
    - [What I Tested](#what-i-tested)
    - [Configuration](#configuration)
  - [Code Coverage](#code-coverage)
    - [1. Installation](#1-installation)
    - [2. Running Coverage Tests](#2-running-coverage-tests)
    - [3. Generating a Report](#3-generating-a-report)
    - [4. Reading the Report](#4-reading-the-report)

## Code Validation

This section explains how we checked the code quality of the NederLearn Blog app. We focused on checking three main parts: HTML, CSS, and Python code.

We used these tools to check the HTML code:

- [W3C Markup Validator](https://validator.w3.org/) - A tool that checks if HTML code follows web standards
- Chrome Developer Tools - Used to look at and copy HTML from our website pages
- Summernote - A tool that helps create formatted text
- Django's |safe filter - Makes sure HTML content displays safely on the website
- Django's MessageMiddleware - Turned off temporarily during testing to get accurate results

<p align="right">(<a href="#content">back to top</a>)</p><br>

### HTML Validation

The [W3C Markup Validator](https://validator.w3.org/) was used to check our HTML code for compliance with web standards. Each page of the NederLearn app was validated to ensure proper markup structure and accessibility.

| **Nr** | **Tested**           | **Result** | **View Result**                                                                                        | **Pass** |
| ------ | -------------------- | ---------- | ------------------------------------------------------------------------------------------------------ | :------: |
| 1      | login.html           | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/login_w3c.webp)</details>      |    ✅    |
| 2      | about_us.html        | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/about_w3c.webp)</details>      |    ✅    |
| 3      | signup.html          | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/sign_w3c.webp)</details>       |    ✅    |
| 4      | index.html           | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/index_w3c.webp)</details>      |    ✅    |
| 5      | blogpost_detail.html | No errors  | <details><summary>Screenshot of result</summary>![Result]()</details>                                  |    ✅    |
| 6      | blogpost_create.html | No errors  | <details><summary>Screenshot of result</summary>![Result]()</details>                                  |    ✅    |
| 7      | blogpost_update.html | No errors  | <details><summary>Screenshot of result</summary>![Result]()</details>                                  |    ✅    |
| 8      | blogpost_delete.html | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/delete_w3c.webp)</details>
| 9      | profile.html         | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/profile_w3c.webp)</details>                                  |    ✅    |
| 10     | profile_edit.html    | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/edit_w3c.webp)</details>                                  |    ✅    |
| 11     | account_manage.html  | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/manage_w3c.webp)</details>                                  |    ✅    |
| 12     | my_posts.html        | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/my_w3c.webp)</details>                                  |    ✅    |
| 13     | bookmarked.html      | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/bookmarked_w3c.webp)</details> |    ✅    |
| 14     | logout.html          | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/logout_w3c.webp)</details>     |    ✅    |

<p align="right">(<a href="#content">back to top</a>)</p><br>

### CSS

[**W3C Jigsaw**](https://jigsaw.w3.org/css-validator/)  is a tool that checks if your website's styling code (CSS) is correct.

| **Nr** | **Tested** | **Result** | **View Result**                                                                                 | **Pass** |
| ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------------- | :------: |
| 1      | CSS File   | No errors  | <details><summary>Screenshot of result</summary>![Result](static/images/css_w3c.webp)</details> |    ✅    |

<p align="right">(<a href="#content">back to top</a>)</p><br>

### Python Validation

[**PEP 8**](https://pep8ci.herokuapp.com/) is a style guide for Python programming that provides guidelines for code formatting and naming conventions. It helps developers write more readable and maintainable code.

| **Nr** | **Tested**                | **Result**                 | **View Result**                                                       | **Pass** |
| ------ | ------------------------- | -------------------------- | --------------------------------------------------------------------- | :------: |
| 1      | nederlearn/settings.py    | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/settings_py.webp)</details>|✅
| 2      | nederlearn/urls.py        | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/nederlearn_url.webp)</details> |    ✅    |
| 3      | blog/models.py            | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/blog_models.webp)</details> |    ✅    |
| 3      | blog/views.py             | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/blog_views.webp)</details> |    ✅    |
| 4      | blog/forms.py             | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/blog_forms.webp)</details> |    ✅    |
| 5      | blog/urls.py              | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/blog_urls.webp)</details> |    ✅    |
| 6      | blog/admin.py             | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/blog_admin.webp)</details> |    ✅    |
| 7      | blog/tests/test_views.py  | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/test_views.webp)</details> |    ✅    |
| 8      | blog/tests/test_models.py | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/test_models.webp)</details> |    ✅    |
| 9      | blog/tests/test_urls.py   | All clear, no errors found | <details><summary>Screenshot of result</summary>![Result](static/images/test_urls.webp)</details> |    ✅    |

<p align="right">(<a href="#content">back to top</a>)</p><br>

# Accessibility

For my accessibility testing, I used **WAVE** [Web Accessibility Evaluation Tool](https://wave.webaim.org/) to evaluate the website. WAVE helps me check if my site meets web accessibility standards and can be used by all visitors. The tool helped me examine important features like:

- Screen reader compatibility
- Color contrast ratios
- Text alternatives for images
- Proper heading structure

Below are the results of my WAVE accessibility tests for each page:

| Page | Accessibility Check | Screenshot | Status |
| ---- | ------------------- | ---------- | ------ |
| About Us | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅  |
| Create New Post | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Edit Profile | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Latest Posts | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Log Out | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Login Landing Page | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Manage Account | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Sign Up | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| User Profile | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |
| Bookmarked | no errors found | <details><summary>Screenshot of result</summary>![Result]()</details> | ✅ |

<p align="right">(<a href="#content">back to top</a>)</p><br>

# Automated Testing

In my automated testing process, I focused on catching bugs and ensuring everything works correctly. I tested basic operations including:

- Creating new items
- Reading existing data
- Updating information
- Deleting items

## Test Setup
Let me explain how I set up my tests:

### File Structure

I keep all my tests organized in a special folder inside my blog app:

```
blog/
tests/
**init**.py
test_models.py
test_urls.py
test_views.py
```

### Running Tests

To run my tests, I use this simple command in the terminal:

```bash
python manage.py test <app name>.<file_name>
```

### My Testing Strategy

I like to follow a simple "TEST" approach:

- T - Try to keep tests organized and neat
- E - Each test looks at just one thing
- S - Structure my test files in a clear way
- T - Test everything from the main project folder

I use Django's TestCase for reliability and split my tests into three files - models, views, and URLs.

<details>
<summary>Test Views</summary>

<br>

![Test_Result!](/static/images/unit_test_views.webp "Unit Test Views Result")

<br>
The test_views.py file contains a comprehensive set of automated tests that verify our URL routing system. These tests make sure that when users click links or navigate to different pages, they end up in the right place. Using Django's SimpleTestCase, we test various URL patterns including:

- Main blog features (home page, creating/editing/deleting posts)
- User-specific pages (profile views, personal blog posts)
- Interactive features (like/unlike, bookmarks)

Each test follows a simple pattern: it creates a URL, then checks if that URL connects to the correct view function. For example, when testing the home page, we verify that the URL 'home' properly connects to our BlogPostList view. This helps catch routing problems early and ensures our navigation system works reliably.

The tests are well-organized with clear comments and documentation, making them easy to understand and maintain. They cover all major features of our blog application, from basic page navigation to more complex user interactions.
</details>

<details>
<summary>Test Models</summary>

<br>

![Test_Result!](/static/images/unit_test_models.webp "Unit Test Models Result")

<br>

I created tests to make sure my database models work correctly. These tests check if I can create and work with different parts of my app like user profiles, blog posts, and comments.

### What Do My Tests Do?

I organized my tests in a simple way:

- I create test data (like a fake user and blog post)
- I check if everything saves correctly in the database
- I verify that all connections between different parts work (like linking comments to posts)

### Main Things I Test

My tests focus on four main areas:

- User Profiles: Making sure new users get their profiles automatically
- Media Categories: Checking if I can create different categories for content
- Blog Posts: Verifying that posts save with the right title, content, and author
- Comments: Ensuring comments connect to the right posts and users

I wrote each test to be clear and simple, making it easy for other developers to understand what I'm testing and why. This helps me catch problems early and keeps my app running smoothly.

</details>

<details>
<summary>
Test URLs
</summary>

<br>

![Test_Result!](/static/images/unit_test_urls.webp "Unit Test URL Result")
<br>

I focused on testing all the URL patterns in our blog application to make sure they work correctly. The test_urls.py file contains a series of tests that check if each URL connects to the right view function. For example, when someone clicks on the home page link, I verify it goes to our BlogPostList view, and when they want to create a new post, it properly connects to BlogpostCreateView.

### What I Tested

I organized the tests into clear categories including:

- Main blog features (home, create, update posts)
- User-specific pages (profile views)
- Interactive features (like/unlike, bookmarks)

I used Django's SimpleTestCase and kept the code simple and well-documented with comments, making it easy for other developers to understand what each test does.

</details>

### Configuration

```python
# Use SQLite for testing, different database for production
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

Note: These settings are only used during testing, not in production.

<p align="right">(<a href="#content">back to top</a>)</p><br>

## Code Coverage

I've found code coverage to be super helpful in understanding how well my tests cover my code. Let me walk you through how to set it up:

### 1. Installation

First, we need to install `Coverage.py` . Just run this in your terminal:

```bash
pip install coverage
```

### 2. Running Coverage Tests

To check your code coverage, use this command:

```bash
coverage run --source='blog' manage.py test blog
```

This creates a `.coverage` file that works like a report card for your code.

### 3. Generating a Report

To create a nice visual report:

1. Open VS Code's terminal
2. Make sure you're in the project's root directory
3. Run: `coverage html`


### 4. Reading the Report

The report shows you:

- Green lines: Code that's been tested
- Red lines: Code that still needs testing

<p align="right">(<a href="#content">back to top</a>)</p><br>