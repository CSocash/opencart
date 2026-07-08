"""
Test Case: Add Product to Cart

============================
Manual Test Steps
============================

1. Open the application in th browser.
2. Locate the search box on the homepage.
3. Enter a valid product name (e.g., "iPhone") and click the Search button.
4. Verify that the search results page displayes products matching the entered name.
5. Select the desired product from the list.
6. On the product page, updat eh product quanity (e.g., 2).
7. Click the "Add to Cart" button.
8. Verify tha a success confirmation message is displayed indicating 
that the product has been successfully aded to the cart.

Expected Result:
----------------------
The product shoudl be successfullly added to the shopping card,
and a visible confirmation message should appear.

"""



import time
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.logout_page import LogoutPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.data_reader_util import read_json_data, read_csv_data, read_excel_data
import csv, openpyxl, json

from config import Config  # Configuration file holding credentials

@pytest.mark.regression
def test_product_search(page):

    product_name = Config.product_name
    quantity = Config.product_quantity

    # 1. Open the application in th browser.
    # 2. Locate the search box on the homepage.
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    #3. Enter a valid product name (e.g., "iPhone") and click the Search button.
    home_page.enter_product_name(product_name)
    home_page.click_search()


    # 4. Verify that the search results page displayes products matching the entered name.
    expect(search_results_page.get_search_results_page_header()).to_be_visible(timeout=3000)
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(timeout=3000)

    # 5. Select the desired product from the list.
    search_results_page.select_product(product_name)

    # 6. On the product page, update the product quanity (e.g., 2).
    product_page.set_quantity(quantity)

    # 7. Click the "Add to Cart" button.
    product_page.add_to_cart()

    # 8. Verify tha a success confirmation message is displayed indicating
    # that the product has been successfully aded to the cart.
    confirmation_message = product_page.get_confirmation_message()
    expect(product_page.cnf_msg).to_contain_text("Success: You have added MacBook to your shopping cart!")
    expect(confirmation_message).to_contain_text("Success: You have added MacBook to your shopping cart!")
