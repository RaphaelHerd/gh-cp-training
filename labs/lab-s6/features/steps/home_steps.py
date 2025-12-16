from behave import given, then
from assertpy import assert_that


@given('I open the home page')
def step_open_home(context):
    # use the page object if available
    if hasattr(context, 'home_page'):
        context.home_page.visit()
    else:
        # fallback: use browser directly
        from config.base import Config
        context.browser.get(Config.URL)


@then('the page title should contain "{expected}"')
def step_title_contains(context, expected):
    assert_that(context.browser.title).contains(expected)


@then('the left navigation should contain "{link_text}"')
def step_left_nav_contains(context, link_text):
    # try using page object locator if present
    if hasattr(context, 'home_page'):
        # check known locators
        found = False
        try:
            if hasattr(context.home_page, 'link_form3') and context.home_page.link_form3.text:
                if link_text in context.home_page.link_form3.text:
                    found = True
        except Exception:
            pass
        try:
            if hasattr(context.home_page, 'link_form6') and context.home_page.link_form6.text:
                if link_text in context.home_page.link_form6.text:
                    found = True
        except Exception:
            pass

        assert_that(found).is_true()
    else:
        # fallback: search anchors inside .left
        anchors = context.browser.find_elements_by_css_selector('.left a')
        texts = [a.text for a in anchors]
        assert_that(any(link_text in t for t in texts)).is_true()
