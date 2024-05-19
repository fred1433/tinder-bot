import pyautogui
import random
import time

def press_random_arrow_key():
    end_time = time.time() + random.uniform(20 * 60, 30 * 60)  # Durée aléatoire entre 20 et 30 minutes
    while time.time() < end_time:
        # Choisir une touche flèche avec une probabilité de 55% pour droite et 45% pour gauche
        key = random.choices(['right', 'left'], weights=[55, 45], k=1)[0]
        
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
