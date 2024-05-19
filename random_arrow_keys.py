import pyautogui
import random
import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg19 import preprocess_input
from PIL import Image
import matplotlib.pyplot as plt

# Charger le modèle pré-entraîné
model = load_model('/mnt/data/model_V3.h5')

def capture_screenshot(region=None):
    # Capturer une capture d'écran
    screenshot = pyautogui.screenshot(region=region)
    screenshot = screenshot.convert('RGB')  # Convertir en RGB
    return screenshot

def classify_image(image):
    # Convertir l'image PIL en array NumPy
    image = np.array(image)
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    
    # Faire la prédiction
    preds = model.predict(image)
    return 'right' if preds[0][1] > preds[0][0] else 'left'

def press_random_arrow_key():
    end_time = time.time() + random.uniform(20 * 60, 30 * 60)  # Durée aléatoire entre 20 et 30 minutes
    while time.time() < end_time:
        # Définir la région de capture (centre de l'écran, à ajuster selon la taille de l'écran)
        screen_width, screen_height = pyautogui.size()
        region = (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)  # Capture du centre de l'écran
        
        # Capturer l'image de la page web
        screenshot = capture_screenshot(region)
        
        # Afficher l'image capturée pour vérification
        plt.imshow(screenshot)
        plt.show()
        
        # Classifier l'image
        key = classify_image(screenshot)
        
        if key:
            # Appuyer sur la touche choisie
            pyautogui.press(key)
            # Afficher la touche appuyée pour le suivi
            print(f'Pressed {key} arrow key')
        
        # Attendre un intervalle de temps aléatoire entre 1 et 3 secondes
        time_interval = random.uniform(1, 3)
        time.sleep(time_interval)

def run_bot_hourly():
    while True:
        press_random_arrow_key()
        # Attendre jusqu'à la prochaine heure pour redémarrer le bot
        current_time = time.localtime()
        next_hour = (current_time.tm_hour + 1) % 24
        next_run_time = time.mktime((current_time.tm_year, current_time.tm_mon, current_time.tm_mday, next_hour, 0, 0, 0, 0, -1))
        sleep_time = next_run_time - time.time()
        print(f'Sleeping for {sleep_time / 60:.2f} minutes until the next run.')
        time.sleep(sleep_time)

# Démarrer le bot avec exécution horaire
run_bot_hourly()
