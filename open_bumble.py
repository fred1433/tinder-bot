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
                facebook_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continuer avec Facebook')]"))
                )
            except Exception as e:
                print(f"Could not find 'Continuer avec Facebook' button: {e}")
                # If not found, try finding the button in English
                try:
                    facebook_button = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continue with Facebook')]"))
                    )
                except Exception as e:
                    print(f"Could not find 'Continue with Facebook' button: {e}")
                    raise e
                
            print(f"Facebook login button found at {time.time() - start_time:.2f} seconds")
            facebook_button.click()
            print(f"Clicked on Facebook login button at {time.time() - start_time:.2f} seconds")
            
            print(f"Number of windows before switch: {len(driver.window_handles)}")
            print("Switching to Facebook login popup...")
            
            # Wait for the new window handle directly
            WebDriverWait(driver, 20).until(lambda d: len(d.window_handles) > 1)
            new_window_handles = driver.window_handles
            if len(new_window_handles) > 1:
                driver.switch_to.window(new_window_handles[1])
                print(f"New window detected and switched to: {new_window_handles[1]}")
            else:
                print("No new window detected.")
                raise Exception("New window not detected.")
            
            time.sleep(5)  # Adding additional wait time to ensure the popup is fully loaded
            print(f"Number of windows after switch: {len(driver.window_handles)}")
            print(f"Switched to Facebook login popup at {time.time() - start_time:.2f} seconds")
            
            # Ensure the popup window is active
            driver.switch_to.window(driver.window_handles[1])
            print("Popup window is active.")
            
            print("Waiting for email input field...")
            try:
                email_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
            except Exception as e:
                print(f"Could not find email input field: {e}")
                raise e
            
            print(f"Email input field found at {time.time() - start_time:.2f} seconds")
            email_input.send_keys("frederic.de.choulot@gmail.com")
            print(f"Entered email at {time.time() - start_time:.2f} seconds")

            print("Entering password...")
            try:
                password_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "pass"))
                )
            except Exception as e:
                print(f"Could not find password input field: {e}")
                raise e
            
            password_input.send_keys("1875Miamik@")
            print(f"Entered password at {time.time() - start_time:.2f} seconds")

            print("Clicking login button...")
            try:
                login_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.NAME, "login"))
                )
            except Exception as e:
                print(f"Could not find login button: {e}")
                raise e
            
            login_button.click()
            print(f"Clicked login button at {time.time() - start_time:.2f} seconds")
            
            print("Switching back to Bumble window...")
            try:
                WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(1))
            except Exception as e:
                print(f"Could not switch back to Bumble window: {e}")
                raise e
            
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
