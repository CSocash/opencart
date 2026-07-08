import time
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage

from config import Config  # Configuration file holding credentials

@pytest.mark.sanity
def test_invalid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.invalid_email)
    login_page.set_password(Config.invalid_password)
    login_page.click_login()
    time.sleep(3)

    expect(login_page.get_login_error()).to_be_visible(timeout=3000)

@pytest.mark.sanity
def test_valid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.email)
    login_page.set_password(Config.password)
    login_page.click_login()
    time.sleep(3)
    # expect(login_page.get_login_error()).not_to_be_visible(timeout=3000)

    my_account_page = MyAccountPage(page)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=3000)