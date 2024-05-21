#navigate_bumble.py

import time
import random
import sys
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

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

        # Vérifiez si un match a été trouvé
        try:
            match_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Voir d'autres profils']"))
            )
            match_button.click()
            logger.info("Match found. Clicked 'Voir d'autres profils'.")
            return
        except Exception as e:
            logger.info("No match found or error occurred: ", e)

        # Sinon, continuez la navigation normale
        body = driver.find_element(By.TAG_NAME, 'body')
        if is_beautiful:
            body.send_keys(Keys.ARROW_RIGHT)
            logger.info("Pressed Right Arrow Key.")
        else:
            body.send_keys(Keys.ARROW_LEFT)
            logger.info("Pressed Left Arrow Key.")
    except Exception as e:
        logger.error(f"Erreur : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python navigate_bumble.py <is_beautiful>")
        sys.exit(1)

    is_beautiful = sys.argv[1].lower() == 'true'
    logger.info(f"is_beautiful: {is_beautiful}")

    logger.info("Loading session...")
    with open('/Users/frederic/tinder-bot/session_bumble.pkl', 'rb') as file:
        session_id = pickle.load(file)
        executor_url = pickle.load(file)

    logger.info(f"Restoring session: {session_id}, {executor_url}")
    driver = attach_to_session(executor_url, session_id)

    navigate(driver, is_beautiful)
