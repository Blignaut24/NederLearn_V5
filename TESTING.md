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

1. [**Code Validation**](#code-validation)
   1. [HTML Validation](#html-validation)
   2. [CSS Validation](#css-validation)
   3. [Python Validation](#python-validation)
2. **Accessibility**
   1. Wave
3. **Performance**
   1. Desktop Performance
   2. Mobile Performance
4. Performance Test on Various Devices
5. **Browser Compatibility**
6. **Automated Testing**
   1. test_views.py
   2. test_models.py
   3. test_urls.py
7. **Manual Testing**
   1. Security Testing
   2. Testing User Stories
   3. User Experience and Improvements
   4. Full Testing
8. **Summary**

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

I have conducted accessibility testing to evaluate our website's usability for all users. Using **WAVE** [Web Accessibility Evaluation Tool](https://wave.webaim.org/) (Web Accessibility Evaluation Tool), we assessed compliance with accessibility standards and identified one key area requiring improvement:

<p align="right">(<a href="#content">back to top</a>)</p><br>
