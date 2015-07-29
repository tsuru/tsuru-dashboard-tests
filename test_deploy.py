import os
import unittest
import getpass
import time

from splinter import Browser


class RollbackTest(unittest.TestCase):
    def setUp(self):
        self.dashboard = os.environ.get("TSURU_DASHBOARD_URL")
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def oauth_login(self):
        self.browser.visit(self.dashboard)
        self.browser.find_by_css(".btn").click()

        email = os.environ.get("EMAIL")

        password = os.environ.get("PASSWORD")
        if not password:
            password = getpass.getpass()

        self.browser.fill("email", email)
        self.browser.fill("password", password)
        self.browser.find_by_css(".enabled").click()

    def create_app(self):
        self.oauth_login()

        url = "{}/apps/create/".format(self.dashboard)
        self.browser.visit(url)

        pool = os.environ.get("POOL")
        team = os.environ.get("TEAM")
        self.browser.fill("name", "tsuru-dashboard-automate-app")
        self.browser.select("platform", "python")
        self.browser.select("pool", pool)
        self.browser.select("teamOwner", team)
        self.browser.find_by_css(".btn").click()
        self.browser.is_text_present("App was successfully created")

    def remove_app(self):
        app_name = "tsuru-dashboard-automate-app"

        url = "{}/apps/{}/settings/".format(self.dashboard, app_name)
        self.browser.visit(url)

        self.browser.find_by_css(".btn-danger")[0].click()

        time.sleep(1)
        self.browser.find_by_css(".remove-confirmation").fill(app_name)
        self.browser.find_by_css(".btn-remove").click()
