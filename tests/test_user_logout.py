
"""
Test Case: User Logout Functionality

=====================
Test Steps
=====================

1. Open teh application in the browser.
2. Navigate to the "Muy Account" menu and click "Login"/
3. Enter valid user credentials (email oand password).
4. Click the "Login" button.
5. Verify that the "My Account" page is displayed.
6. Click the "Logout" link or button.
7. Verify that the Logout confirmation page is displayed.
8. Click the "Continue" button to return to the Home page.
9. Verify that the Home page is displayed by checking its title.

Expected Result:

After logging out, the user shoudl ve redirected to the Logout confirmation page.  
Clicking "Continue" should navigate back to the HOme page successfully.

"""

import time
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.logout_page import LogoutPage
from utils.data_reader_util import read_json_data, read_csv_data, read_excel_data
import csv, openpyxl, json

from config import Config  # Configuration file holding credentials



# csv_data = read_csv_data("testdata/logindata.csv")
# json_data = read_json_data("testdata/logindata.json")
# excel_data = read_excel_data("testdata/logindata.xlsx")

fixed_data = [("lunatuna", "lunatuna@yopmail.com", "luna123abc", "success")]
from config import Config


@pytest.mark.regression
@pytest.mark.parametrize("testname, email, password, expected", fixed_data)
def test_invalid_user_login_data_driven_json(page, testname, email, password, expected):

    # --- Step 1: Create Page Object Instances ---
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    # --- Step 2: Navigate to Login Page ---
    home_page.click_my_account()
    home_page.click_login()

    # --- Step 3: Enter Valid Credentials and Login ---
    #login_page.login(email, password)
    login_page.login(Config.email, Config.password)
    time.sleep(3)

    # --- Step 4: Verify 'My Account' Page is Displayed ---
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=6000)

    # --- Step 5: Perform Logout Action ---
    home_page.click_my_account()
    logout_page = my_account_page.click_logout()

    # --- Step 16: Verify Logout Page is Displayed ---
    # --- Cheks whether the 'Continue' button is visible on the Logout page ---
    expect(logout_page.msg_account_logout).to_be_visible(timeout=3000)

    # --- Step 7: Click 'Continue' to Return to Home Page---
    logout_page.click_continue()

    # --- Step 1: Verify Navigation to HOme Page by CHecking Page Title ---
    expect(page).to_have_title("Your Store")

