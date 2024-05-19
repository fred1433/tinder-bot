#open_tinder.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pickle

def open_tinder():
    print("Opening Tinder...")
    driver_path = "/opt/homebrew/bin/chromedriver"
    service = Service(driver_path)

    user_data_dir = "/Users/frederic/Library/Application Support/Google/Chrome"
    profile_directory = "Default"

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://tinder.com/app/recs")
    time.sleep(8)
    print("Tinder page opened...")

    session_id = driver.session_id
    executor_url = driver.command_executor._url

    with open('/Users/frederic/tinder-bot/session.pkl', 'wb') as file:
        pickle.dump(session_id, file)
        pickle.dump(executor_url, file)

    print(f"Session saved: {session_id}, {executor_url}")

    with open('/Users/frederic/tinder-bot/session_ready.txt', 'w') as file:
        file.write("session ready")

    return driver

if __name__ == "__main__":
    driver = open_tinder()
    print("Tinder is open and session is saved.")
    while True:
        time.sleep(1)
