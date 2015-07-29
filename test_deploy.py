import os
import unittest
import getpass

from splinter import Browser


class RollbackTest(unittest.TestCase):
    def setUp(self):
        self.dashboard = os.environ.get("TSURU_DASHBOARD_URL")
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def test_oauth_login(self):
        self.browser.visit(self.dashboard)
        self.browser.find_by_css(".btn").click()

        email = os.environ.get("EMAIL")

        password = os.environ.get("PASSWORD")
        if not password:
            password = getpass.getpass()

        self.browser.fill("email", email)
        self.browser.fill("password", password)
        self.browser.find_by_css(".enabled").click()
