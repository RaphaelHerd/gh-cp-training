from seleniumpagefactory.Pagefactory import PageFactory
from config.base import Config


class HomePage(PageFactory):
    """Home page for the Test Site."""

    locators = {
        'link_form3': ('CSS', '.left a[href*="action=form3"]'),
        'link_form6': ('CSS', '.left a[href*="action=form6"]'),
        'link_childwindow': ('CSS', '.left a[href*="childWindow"]'),
    }

    def __init__(self, driver):
        super().__init__()
        self.url = Config.URL
        self.driver = driver

    def visit(self):
        self.driver.get(self.url)
