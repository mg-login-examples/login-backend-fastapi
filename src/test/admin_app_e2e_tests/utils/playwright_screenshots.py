from playwright.sync_api import Page

def save_screenshot(page: Page, screenshot_name: str):
    if not (screenshot_name.encode(".png")):
        screenshot_name = f"{screenshot_name}.png"
    page.screenshot(path=screenshot_name, full_page=True)
    return f"test-results/{screenshot_name}"
