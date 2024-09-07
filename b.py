from playwright.sync_api import sync_playwright


def save_logged_in_state():
    with sync_playwright() as playwright:
        # Launch browser in headless mode off
        browser = playwright.chromium.launch(headless=False)

        # Create a new browser context and page
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Telegram Web
        page.goto("https://web.telegram.org/")

        # Wait for user to manually log in to Telegram (or use cookies for auto-login if already logged in)
        print("Please log in to Telegram. The session will be saved.")

        # Wait for 60 seconds to give enough time for login
        page.wait_for_timeout(
            60000
        )  # Adjust this time based on how long the login takes

        # Save storage state (cookies, local storage, etc.) after login
        context.storage_state(path="storageState.json")

        # Close browser
        browser.close()


save_logged_in_state()
