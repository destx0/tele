from playwright.sync_api import sync_playwright
import time


def send_messages_to_peers():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storageState.json")

        # Read peer IDs from the output file
        with open("output.txt", "r") as file:
            peer_ids = [line.strip() for line in file]

        for peer_id in peer_ids:
            # Open a new page for each peer
            page = context.new_page()
            url = f"https://web.telegram.org/a/#7312991196"
            page.goto(url)

            # Wait for the page to load
            # page.wait_for_selector('#message-input-text', state='visible', timeout=100000)

            # Find the input box and type the message
            # input_box = page.locator('#message-input-text div[contenteditable="true"]')
            # input_box.fill("hi")

            # # Send the message
            # page.keyboard.press("Enter")

            # # Wait for 2 seconds
            time.sleep(60)

            # # Close the tab
            page.close()

        # Close the browser
        browser.close()


send_messages_to_peers()
