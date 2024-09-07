from playwright.sync_api import sync_playwright
import time


def load_logged_in_state():
    with sync_playwright() as playwright:
        # Launch browser with headless mode off
        browser = playwright.chromium.launch(headless=False)

        # Load the previously saved session (cookies, local storage)
        context = browser.new_context(storage_state="storageState.json")

        # Create a new page with the saved context
        page = context.new_page()

        # Navigate to Telegram Web
        page.goto("https://web.telegram.org/a/#-1001271340650")

        # Wait for 10 seconds to allow elements to load
        page.wait_for_timeout(10000)

        # Scroll within the Telegram chat container (upwards)
        chat_selector = "#MiddleColumn > div.messages-layout > div.Transition > div > div.MessageList.custom-scroll.with-default-bg.scrolled"

        scroll_duration = 1800  # Scroll for 30 minutes (1800 seconds)
        scroll_pause_time = 0.1  # Pause for 1 second between scrolls
        start_time = time.time()

        while time.time() - start_time < scroll_duration:
            # Scroll up from the current position
            page.evaluate(
                f"""
                const chatContainer = document.querySelector("{chat_selector}");
                if (chatContainer) {{
                    const yPosition = chatContainer.scrollTop - chatContainer.clientHeight / 2;  // Scroll up by half of the visible height
                    chatContainer.scrollTo(0, yPosition);  // Scroll vertically, keeping x-axis the same
                }}
            """
            )
            time.sleep(scroll_pause_time)  # Wait for 1 second between scrolls

        # Close the browser
        browser.close()


load_logged_in_state()
