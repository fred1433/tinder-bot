import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pickle
from PIL import Image
import io

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

def extract_image(driver):
    try:
        wait = WebDriverWait(driver, 20)
        print("Waiting for image element...")
        image_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='encounters-story-profile-image']//img")))
        print("Image element found.")
        
        image_url = image_element.get_attribute('src')
        print(f"Image URL: {image_url}")

        image_response = requests.get(image_url)
        image_path = "/Users/frederic/tinder-bot/profile_image_bumble.jpg"

        image = Image.open(io.BytesIO(image_response.content))
        image = image.convert("RGB")
        image.save(image_path, "JPEG")

        print(f"Image téléchargée et convertie en JPEG : {image_path}")
        return image_path

    except Exception as e:
        print(f"Erreur : {e}")
        return None

if __name__ == "__main__":
    print("Loading session...")
    with open('/Users/frederic/tinder-bot/session_bumble.pkl', 'rb') as file:
        session_id = pickle.load(file)
        executor_url = pickle.load(file)

    print(f"Restoring session: {session_id}, {executor_url}")
    driver = attach_to_session(executor_url, session_id)
    image_path = extract_image(driver)
    if image_path:
        print(f"L'image est enregistrée à l'emplacement : {image_path}")
    else:
        print("Échec de l'extraction de l'image.")
    # Remove the driver.quit() line
    # driver.quit()
