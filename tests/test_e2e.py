import os

import pytest
from docx import Document
from docx.shared import Inches
from playwright.sync_api import Playwright
from playwright.sync_api import Page
from configparser import ConfigParser
from docx.shared import Pt
import utils.utils_actions_test
import time

from utils.json_utils import load_test_data
from utils.screenshot_utils import capture_element_region
from utils.word_utils import word_doc_utilty




os.makedirs("screenshots", exist_ok=True)
os.makedirs("videos", exist_ok=True)

document = Document()
document.add_heading("AODD Dates Capture Report", level=1)
@pytest.mark.parametrize("test_data",load_test_data())
def test_capture_dates(playwright:Playwright,test_data):

    brand = test_data["Brand"]
    item = test_data["item"]

    print(f"===== Running dataset for {brand} - {item} =====")
    output_dir = f"screenshots/{brand}_{item}"
    os.makedirs(output_dir, exist_ok=True)

    browser = None

    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir="videos/")  # Enable video recording
        page = context.new_page()

        utils.utils_actions_test.launchURL(page, brand)
        time.sleep(15)

        utils.utils_actions_test.closeDialog(page, brand)
        print("Dialog is closed")

        utils.utils_actions_test.enterProduct(page, item)
        print("Product is entered")

        utils.utils_actions_test.enterPostalCode(page)
        print("Postal code is entered")

        time.sleep(10)
        dates_pip = utils.utils_actions_test.getAODDDatesOnPipPage(page)
        print(dates_pip)
        pip_screenshot = f"{output_dir}/pip_page.png"
        pip_screenshot = capture_element_region(page, pip_screenshot)

        utils.utils_actions_test.addItemToCart(page)
        cart_dates = utils.utils_actions_test.getAODDDatesonCartPage(page)
        print("AODD Dates on Cart Page:", cart_dates)
        cart_screenshot = f"{output_dir}/cart_page.png"
        cart_screenshot = capture_element_region(page, cart_screenshot)

        checkout_dates = utils.utils_actions_test.addProductToCheckOut(page, brand)
        print("Checkout Dates:", checkout_dates)
        checkout_screenshot = f"{output_dir}/checkout_page.png"
        checkout_screenshot = capture_element_region(page, checkout_screenshot)

        time.sleep(10)
        video_path = context.pages[0].video.path() if context.pages[0].video else "No video"

        # Add results to Word document
        word_doc_utilty(document, brand, item, dates_pip, pip_screenshot, cart_screenshot, checkout_dates,
                        checkout_screenshot, cart_dates, video_path)

    except Exception as e:
        print(f"Error for dataset {brand} - {item}: {e}")

    finally:
        # Always close context and browser
        try:
            context.close()
        except Exception:
            pass
        if browser:
            browser.close()
        print(f"Browser closed for {brand} - {item}")

    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"AODD_Date_Report_{timestamp}.docx")

    document.save(report_path)
    print(f"\n Report saved successfully: {report_path}")








