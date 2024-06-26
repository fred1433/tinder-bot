# navigate_tinder.py
import time
import random
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pickle
from selenium import webdriver

def attach_to_session(executor_url, session_id):
    original_execute = webdriver.Remote.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'value': {'sessionId': session_id, 'capabilities': {}}}
        return original_execute(self, command, params)
    webdriver.Remote.execute = new_command_execute
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=executor_url, options=options)
    driver.session_id = session_id
    webdriver.Remote.execute = original_execute
    return driver

def navigate(driver, is_beautiful):
    try:
        delay = random.uniform(0.1, 0.4)
        time.sleep(delay)

        body = driver.find_element(By.TAG_NAME, 'body')
        if is_beautiful:
            body.send_keys(Keys.ARROW_RIGHT)
            print("Pressed Right Arrow Key.")
        else:
            body.send_keys(Keys.ARROW_LEFT)
            print("Pressed Left Arrow Key.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    print("Loading session...")
    with open('/Users/frederic/tinder-bot/session.pkl', 'rb') as file:
        session_id = pickle.load(file)
        executor_url = pickle.load(file)

    print(f"Restoring session: {session_id}, {executor_url}")
    driver = attach_to_session(executor_url, session_id)

    if len(sys.argv) < 2:
        print("Missing argument: is_beautiful (true/false)")
        sys.exit(1)

    is_beautiful = sys.argv[1].lower() == 'true'
    print(f"Navigating with is_beautiful={is_beautiful}")

    navigate(driver, is_beautiful)
