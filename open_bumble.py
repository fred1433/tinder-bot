#open_bumble.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

def open_bumble():
    print("Opening Bumble...")
    start_time = time.time()
    
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

    driver.get("https://bumble.com/app")
    print(f"Bumble page requested at {time.time() - start_time:.2f} seconds")
    time.sleep(8)
    print(f"Bumble page opened at {time.time() - start_time:.2f} seconds")

    try:
        # Check if already logged in by looking for an element that is only present after login
        if driver.find_elements(By.XPATH, "//div[contains(@class, 'logged-in')]"):
            print("Already logged in to Bumble.")
        else:
            print("Waiting for Facebook login button...")
            try:
                # Try finding the button in French
                facebook_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continuer avec Facebook')]"))
                )
            except:
                # If not found, try finding the button in English
                facebook_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continue with Facebook')]"))
                )
                
            print(f"Facebook login button found at {time.time() - start_time:.2f} seconds")
            facebook_button.click()
            print(f"Clicked on Facebook login button at {time.time() - start_time:.2f} seconds")
            
            print(f"Number of windows before switch: {len(driver.window_handles)}")
            print("Switching to Facebook login popup...")
            WebDriverWait(driver, 20).until(EC.new_window_is_opened(driver.window_handles))
            driver.switch_to.window(driver.window_handles[1])
            print(f"Number of windows after switch: {len(driver.window_handles)}")
            print(f"Switched to Facebook login popup at {time.time() - start_time:.2f} seconds")
            
            print("Waiting for email input field...")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            print(f"Email input field found at {time.time() - start_time:.2f} seconds")
            email_input.send_keys("frederic.de.choulot@gmail.com")
            print(f"Entered email at {time.time() - start_time:.2f} seconds")

            print("Entering password...")
            password_input = driver.find_element(By.ID, "pass")
            password_input.send_keys("1875Miamik@")
            print(f"Entered password at {time.time() - start_time:.2f} seconds")

            print("Clicking login button...")
            login_button = driver.find_element(By.NAME, "login")
            login_button.click()
            print(f"Clicked login button at {time.time() - start_time:.2f} seconds")
            
            print("Switching back to Bumble window...")
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
            driver.switch_to.window(driver.window_handles[0])
            print(f"Switched back to Bumble window at {time.time() - start_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred at {time.time() - start_time:.2f} seconds: {e}")
    
    session_id = driver.session_id
    executor_url = driver.command_executor._url

    with open('/Users/frederic/tinder-bot/session_bumble.pkl', 'wb') as file:
        pickle.dump(session_id, file)
        pickle.dump(executor_url, file)

    print(f"Session saved at {time.time() - start_time:.2f} seconds: {session_id}, {executor_url}")

    with open('/Users/frederic/tinder-bot/session_ready_bumble.txt', 'w') as file:
        file.write("session ready")

    return driver, start_time

if __name__ == "__main__":
    driver, start_time = open_bumble()
    print(f"Bumble is open and session is saved at {time.time() - start_time:.2f} seconds.")
    while True:
        time.sleep(1)
