def capture_element_region(page,screenshot_path):
    page.screenshot(path=screenshot_path, full_page=True)
    return screenshot_path
