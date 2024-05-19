import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def detect_faces(api_key, api_secret, image_path):
    detect_url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    detect_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "return_attributes": "facequality"
    }

    files = {
        "image_file": open(image_path, "rb")
    }

    response = requests.post(detect_url, data=detect_data, files=files)
    return response.json()

def analyze_faces(api_key, api_secret, face_tokens):
    analyze_url = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
    analyze_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "face_tokens": ','.join(face_tokens),
        "return_attributes": "gender,age,beauty"
    }

    time.sleep(2)  # Ajouter une pause de 2 secondes entre les requêtes
    response = requests.post(analyze_url, data=analyze_data)
    return response.json()

def is_beautiful(beauty_score, threshold=7):
    return beauty_score >= threshold

def main():
    api_key = "D-0FxSRjadOI6gja3opbnwjtxaLWlqKy"
    api_secret = "JceEOYbLxQQnhn1MRgRw7UEu12dS18Uf"
    image_folder = "/Users/frederic/tinder-bot/"  # Remplacez par le chemin de votre dossier
    threshold = 70  # Seuil pour décider si une image est "belle" ou "pas belle"

    # Configuration du chemin vers chromedriver
    driver_path = "/opt/homebrew/bin/chromedriver"
    service = Service(driver_path)

    # Chemin vers votre profil Chrome
    user_data_dir = "/Users/frederic/Library/Application Support/Google/Chrome"  # Remplacez par le chemin de votre profil
    profile_directory = "Default"  # Remplacez par le nom de votre profil, généralement "Default"

    # Options pour Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--verbose")

    # Initialisation du driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Ouvrir Tinder
    driver.get("https://tinder.com/app/recs")

    # Attendre le chargement de la page
    time.sleep(10)

    # Localiser l'image centrale
    try:
        image_element = driver.find_element(By.XPATH, "//div[@aria-hidden='false']//img")
        image_url = image_element.get_attribute('src')

        # Télécharger l'image
        image_response = requests.get(image_url)
        image_path = "profile_image.jpg"
        with open(image_path, 'wb') as file:
            file.write(image_response.content)
        
        print(f"Image téléchargée : {image_path}")

        # Envoyer l'image à l'API Face++ pour analyse
        detect_result = detect_faces(api_key, api_secret, image_path)

        if "faces" in detect_result and detect_result["faces"]:
            face_tokens = [face["face_token"] for face in detect_result["faces"]]
            analyze_result = analyze_faces(api_key, api_secret, face_tokens)

            if "faces" in analyze_result:
                for face in analyze_result["faces"]:
                    beauty = face["attributes"]["beauty"]
                    female_beauty_score = beauty['female_score']
                    male_beauty_score = beauty['male_score']
                    is_beautiful_result = is_beautiful(female_beauty_score, threshold)
                    print(f"Image : {'Belle' if is_beautiful_result else 'Pas Belle'} (Female Score: {female_beauty_score}, Male Score: {male_beauty_score})")
            else:
                print(f"No face data in analyze result.")
        else:
            print(f"No face detected in the image.")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
