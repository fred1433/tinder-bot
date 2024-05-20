from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pickle
import time

def export_cookies():
    driver_path = "/opt/homebrew/bin/chromedriver"
    service = Service(driver_path)

    user_data_dir = "/Users/frederic/Library/Application Support/Google/Chrome"
    profile_directory = "Default"

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://tinder.com")
    time.sleep(10)  # Time to manually log in if needed

    cookies = driver.get_cookies()
    with open('/Users/frederic/tinder-bot/cookies.pkl', 'wb') as file:
        pickle.dump(cookies, file)

    driver.quit()

if __name__ == "__main__":
    export_cookies()
