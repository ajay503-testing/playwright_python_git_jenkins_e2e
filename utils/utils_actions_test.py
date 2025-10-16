import os
from configparser import ConfigParser
from locators import BrandPageLocators, WSPageLocators  # Import the locators


def getBrand(brand):
    config = ConfigParser()
    ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'properties.ini'))
    config.read(ini_path)
    return config['ECOM'][brand]


def launchURL(page, brand):
    if brand == "PB":
        page.goto(getBrand(brand), wait_until="domcontentloaded", timeout=60000)
        if page.locator(BrandPageLocators.NO_THANKS_US_SITE).is_visible():
            page.locator(BrandPageLocators.NO_THANKS_US_SITE).click()
    else:
        page.goto(getBrand(brand), wait_until="domcontentloaded", timeout=60000)


def closeDialog(page, brand):
    if brand == "PB":
        page.locator(BrandPageLocators.CLOSE_EMAIL_MODAL).first.click()
    else:
        page.locator(WSPageLocators.CLOSE_GLOBAL_MODAL).click()


def enterProduct(page, item):
    page.locator("#search-field").first.click()
    page.locator("#search-field").first.fill(item)
    page.get_by_role("button", name="search").click()


def enterPostalCode(page):
    postal_input = page.locator(BrandPageLocators.SHIPPING_ZIP_CODE_INPUT)
    postal_input.clear()
    postal_input.first.fill("94111")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")


def getAODDDatesOnPipPage(page):
    aoddDatesOnPIPPage = page.locator(BrandPageLocators.DELIVERY_DATE_TEXT).first.text_content()
    return aoddDatesOnPIPPage


def getAODDDatesOnPipPageElement(page):
    return page.locator(BrandPageLocators.DELIVERY_DATE_TEXT).first


def addItemToCart(page):
    page.locator(BrandPageLocators.ADD_TO_CART_BUTTON).first.click()
    page.locator(BrandPageLocators.CHECKOUT_BUTTON).click()


def getAODDDatesonCartPage(page):
    aoddDatesOnCartPage = page.locator("#deliveryPrefixMessage").text_content()
    return aoddDatesOnCartPage


def addProductToCheckOut(page, brand):
    page.locator(BrandPageLocators.CHECKOUT_BUTTON).click()

    if "app/signin.html" not in page.url:
        element = page.locator(BrandPageLocators.GUEST_CHECKOUT_BUTTON)
        element.click()
        page.goto(getBrand(brand) + "/checkout/app/shipping.html")
    else:
        page.locator(
            "xpath=//checkout-text-ui//error-label-ui[@id='smart-login-email-email-error']//following::input").first.fill(
            "test@wsgc.com")
        page.locator(BrandPageLocators.CONTINUE_BUTTON).click()
        page.locator(BrandPageLocators.GUEST_CHECKOUT_BUTTON).click()

    page.locator(BrandPageLocators.FULL_NAME_INPUT).first.fill("ajay kumar")
    page.locator(BrandPageLocators.ADDRESS_LINE_1_INPUT).first.fill("141 area")
    page.locator(BrandPageLocators.CITY_INPUT).first.fill("San fransico")
    page.select_option(BrandPageLocators.STATE_PROVINCE_SELECT, value="CA")
    page.locator(BrandPageLocators.POSTAL_CODE_INPUT).first.type("94111")
    page.locator(BrandPageLocators.PHONE_INPUT).first.fill("9876123456")
    page.locator(BrandPageLocators.CONTINUE_BUTTON).first.click()
    page.locator(BrandPageLocators.USE_AS_ENTERED_BUTTON).first.click()

    ecdd_dates_on_checkout = page.locator(BrandPageLocators.ESTIMATED_DELIVERY_DATE).text_content()
    return ecdd_dates_on_checkout