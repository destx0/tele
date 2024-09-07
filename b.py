from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import re

# Convert the list of bot IDs to a set to remove duplicates
bots_to_skip = {
    "777000", "1629538930", "928179081", "1754165189", "2141959380",
    "745228470", "1449679485", "5912830138", "1289979382", "1477356653",
    "866058111", "1049044284", "1456692404", "5296612492", "1050954529",
    "705978189", "6261948851", "986852438", "1173591906", "5750894615",
    "208056682"
}


def extract_peer_ids(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    avatar_divs = soup.find_all("div", class_="Avatar")
    peer_ids = [
        div.get("data-peer-id") for div in avatar_divs if div.get("data-peer-id")
    ]
    peer_ids = set(
        pid for pid in peer_ids if not pid.startswith("-") and pid not in bots_to_skip
    )
    return peer_ids


def extract_user_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    message_divs = soup.find_all("div", class_="Message")
    user_info = {}
    
    for div in message_divs:
        avatar_div = div.find("div", class_="Avatar")
        if avatar_div and avatar_div.get("data-peer-id"):
            user_id = avatar_div.get("data-peer-id")
            username_span = div.find("span", class_="message-title-name")
            username = username_span.text.strip() if username_span else ""
            
            if not user_id.startswith("-") and user_id not in bots_to_skip:
                if user_id not in user_info or (username and not user_info[user_id]):
                    user_info[user_id] = username
    
    return user_info


def load_logged_in_state():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storageState.json")
        page = context.new_page()
        page.goto("https://web.telegram.org/a/#-1001271340650")
        page.wait_for_timeout(10000)

        chat_selector = "#MiddleColumn > div.messages-layout > div.Transition > div > div.MessageList.custom-scroll.with-default-bg.scrolled"
        scroll_duration = 6
        scroll_pause_time = 0.0
        start_time = time.time()

        user_info = {}
        unknown_users = set()
        found_users = set()

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

            # Extract user info from the current page content
            html_content = page.content()
            new_user_info = extract_user_info(html_content)
            
            # Update user_info dictionary and output files
            with open("users_found.txt", "a", encoding="utf-8") as found_file, \
                 open("users_not_found.txt", "a", encoding="utf-8") as not_found_file:
                for user_id, username in new_user_info.items():
                    if user_id not in user_info:
                        if username and user_id not in found_users:
                            user_info[user_id] = username
                            found_file.write(f"{user_id},{username}\n")
                            found_users.add(user_id)
                            if user_id in unknown_users:
                                unknown_users.remove(user_id)
                                update_not_found_file(user_id)
                        elif not username and user_id not in unknown_users and user_id not in found_users:
                            unknown_users.add(user_id)
                            not_found_file.write(f"{user_id}\n")
                    elif not user_info[user_id] and username and user_id not in found_users:
                        user_info[user_id] = username
                        found_file.write(f"{user_id},{username}\n")
                        found_users.add(user_id)
                        if user_id in unknown_users:
                            unknown_users.remove(user_id)
                            update_not_found_file(user_id)

        browser.close()


def update_not_found_file(user_id_to_remove):
    with open("users_not_found.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open("users_not_found.txt", "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip() != user_id_to_remove:
                file.write(line)


load_logged_in_state()
