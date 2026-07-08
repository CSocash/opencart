import time
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.data_reader_util import read_json_data, read_csv_data, read_excel_data
import csv, openpyxl, json

from config import Config  # Configuration file holding credentials


# Load/read the data from teh test data files

# csv
# data_csv = []  # we ultimately need the data in a list format
# with open ("testdata/logindata.csv", "r") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         data_csv.append((row["username", row["password"]]))     # not needed

csv_data = read_csv_data("testdata/logindata.csv")
json_data = read_json_data("testdata/logindata.json")
excel_data = read_excel_data("testdata/logindata.xlsx")



@pytest.mark.datadriven
@pytest.mark.parametrize("testname, email, password, expected", csv_data)
def test_invalid_user_login_data_driven_csv(page, testname, email, password, expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # login_page.set_email(email)
    # login_page.set_password(password)
    # login_page.click_login()
    login_page.login(email, password)
    time.sleep(3)
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=6000)

    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)


@pytest.mark.datadriven
@pytest.mark.parametrize("testname, email, password, expected", json_data)
def test_invalid_user_login_data_driven_json(page, testname, email, password, expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # login_page.set_email(email)
    # login_page.set_password(password)
    # login_page.click_login()
    login_page.login(email, password)
    time.sleep(3)
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=6000)

    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)



@pytest.mark.parametrize("testname, email, password, expected", excel_data)
def test_invalid_user_login_data_driven_excel(page, testname, email, password, expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    # login_page.set_email(email)
    # login_page.set_password(password)
    # login_page.click_login()
    login_page.login(email, password)
    time.sleep(3)
    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=6000)

    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=3000)