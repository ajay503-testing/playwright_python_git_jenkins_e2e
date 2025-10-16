import os
import re
import time
from configparser import ConfigParser


def getBrand(brand):
    config=ConfigParser()
    ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'properties.ini'))
    config.read(ini_path)
    return config['ECOM'][brand]

def launchURL(page,brand):
    if brand=="PB":
        page.goto(getBrand(brand),wait_until="domcontentloaded", timeout=60000)
        if page.get_by_text("No thanks, I'd like to proceed to the US site").is_visible():
            page.get_by_text("No thanks, I'd like to proceed to the US site").click()
    else:
        page.goto(getBrand(brand),wait_until="domcontentloaded", timeout=60000)

def closeDialog(page,brand):
    if brand=="PB":
        page.locator("xpath=//div[@class='sticky-join-email-minimize']//a[@href='#']").first.click()
    else:
        page.locator("xpath=//dialog//button[@aria-label='close-global-modal']").click()


def enterProduct(page,item):
    page.locator("#search-field").first.click()
    page.locator("#search-field").first.fill(item)
    page.get_by_role("button",name="search").click()

def enterPostalCode(page):
    postal_input = page.locator("#shipping_zip_code")
    postal_input.clear()
    postal_input.first.fill("94111")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")

def getAODDDatesOnPipPage(page):
    aoddDatesOnPIPPage=page.locator("xpath=//p[@data-test-id='ship-to-customer-delivery-date-estimate-text']").first.text_content()
    return aoddDatesOnPIPPage

def getAODDDatesOnPipPageElement(page):
    return page.locator("xpath=//p[@data-test-id='ship-to-customer-delivery-date-estimate-text']").first



def addItemToCart(page):
    page.get_by_role("button",name="Add To Cart").first.click()
    page.locator('[title="Checkout"]').click()

def getAODDDatesonCartPage(page):
    aoddDatesOnCartPage=page.locator("#deliveryPrefixMessage").text_content()
    return aoddDatesOnCartPage

def addProductToCheckOut(page,brand):
    page.get_by_role("button",name="Checkout").click()

    #element = page.locator("xpath=//button[normalize-space(text())='Guest Checkout']")

    #if page.url=="https://www.williams-sonoma.com/checkout/signin.html":
    if "signin.html" in page.url:
        print("Element found and visible — clicking it.")
        if page.locator("xpath=//button[normalize-space(text())='Guest Checkout']").is_visible():
            element = page.locator("xpath=//button[normalize-space(text())='Guest Checkout']")
            element.click()
            #page.goto("https://www.williams-sonoma.com/checkout/app/shipping.html")
            page.goto(getBrand(brand)+"/checkout/app/shipping.html")
        else:
            page.locator(
                "xpath=//checkout-text-ui//error-label-ui[@id='smart-login-email-email-error']//following::input").first.fill(
                "test@wsgc.com")
            page.get_by_role("button", name="Continue").click()
            page.get_by_role("button", name="Guest Checkout").click()
    else:
        page.locator("xpath=//checkout-text-ui//error-label-ui[@id='smart-login-email-email-error']//following::input").first.fill("test@wsgc.com")
        page.get_by_role("button",name="Continue").click()
        page.get_by_role("button",name="Guest Checkout").click()
    page.locator("#fullName").first.fill("ajay kumar")
    page.locator("#line1").first.fill("141 area")
    page.locator("#city").first.fill("San fransico")
    #state_dropdown = page.locator("#stateProvince").nth(0)
    #state_dropdown.select_option("California")
    page.select_option("select#stateProvince",value="CA")
    page.locator("xpath=//input[@name='postalCode']").first.type("94111")
    page.locator("#phone").first.fill("9876123456")
    page.get_by_role("button",name="Continue").first.click()
    page.get_by_role("button",name="Use as entered").first.click()
    ecdd_dates_on_checkout=page.locator(".estimated-delivery-date").text_content()
    return ecdd_dates_on_checkout





