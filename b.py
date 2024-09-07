from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

# List of bot IDs to skip (kept from the original code)
bots_to_skip = [
    "777000",
    "1629538930",
    "928179081",
    "1754165189",
    "2141959380",
    "745228470",
    "1449679485",
    "5912830138",
    "5912830138",
    "1289979382",
    "1477356653",
    "866058111",
    "1049044284",
    "1456692404",
    "5296612492",
    "1050954529",
    "705978189",
    "6261948851",
    "986852438",
    "986852438",
    "1173591906",
    "5750894615",
    "208056682",
    "1629538930",
]


def extract_peer_ids(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    avatar_divs = soup.find_all("div", class_="Avatar")
    peer_ids = [
        div.get("data-peer-id")
        for div in avatar_divs
        if div.get("data-peer-id") and "no-photo" not in div.get("class", [])
    ]
    peer_ids = set(
        pid for pid in peer_ids if not pid.startswith("-") and pid not in bots_to_skip
    )
    return peer_ids


def load_logged_in_state():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storageState.json")
        page = context.new_page()
        page.goto("https://web.telegram.org/a/#-1001271340650")
        page.wait_for_timeout(10000)

        chat_selector = "#MiddleColumn > div.messages-layout > div.Transition > div > div.MessageList.custom-scroll.with-default-bg.scrolled"
        scroll_duration = 60
        scroll_pause_time = 0.0
        start_time = time.time()

        peer_ids = set()

        while time.time() - start_time < scroll_duration:
            page.evaluate(
                f"""
                const chatContainer = document.querySelector("{chat_selector}");
                if (chatContainer) {{
                    const yPosition = chatContainer.scrollTop - chatContainer.clientHeight / 2;
                    chatContainer.scrollTo(0, yPosition);
                }}
            """
            )
            time.sleep(scroll_pause_time)

            # Extract peer IDs from the current page content
            html_content = page.content()
            new_peer_ids = extract_peer_ids(html_content)
            peer_ids.update(new_peer_ids)

        browser.close()

        # Write the extracted peer IDs to the output file
        with open("output.txt", "w", encoding="utf-8") as output_file:
            for peer_id in peer_ids:
                output_file.write(f"https://web.telegram.org/a/#{peer_id}\n")


load_logged_in_state()
