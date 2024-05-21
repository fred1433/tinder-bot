# main_script_bumble.py

import subprocess
import time
import os
import random
import pygame
from datetime import datetime
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='tinder_bot.log', filemode='w')
logger = logging.getLogger()

def run_script(script_path, args=[]):
    try:
        logger.info(f"Running script: {script_path} with args: {args}")
        result = subprocess.run(["python3", script_path] + args, capture_output=True, text=True, check=True)
        logger.info(result.stdout)
        logger.error(result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run script {script_path} with args {args}: {e.stderr}")
        return None

def play_sound(sound_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to play sound {sound_path}: {e}")

def close_chrome():
    try:
        logger.info("Fermeture de Google Chrome...")
        subprocess.run(["pkill", "-f", "Google Chrome"])
        time.sleep(5)
        logger.info("Google Chrome est fermé.")
    except Exception as e:
        logger.error(f"Failed to close Google Chrome: {e}")

def main():
    logger.info("Le processus commencera dans 3 secondes.")
    play_sound("/Users/frederic/tinder-bot/alert_sound.mp3")
    time.sleep(3)
    close_chrome()

    logger.info("Running open_bumble.py...")
    try:
        open_bumble_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_bumble.py"])
    except Exception as e:
        logger.error(f"Failed to start open_bumble.py: {e}")
        return

    logger.info("Waiting for session to be ready...")
    session_ready_path = '/Users/frederic/tinder-bot/session_ready_bumble.txt'
    while not os.path.exists(session_ready_path):
        time.sleep(2)

    logger.info("Session is ready. Starting extraction and evaluation process...")
    time.sleep(10)

    start_time = time.time()
    run_duration = random.uniform(20 * 60, 25 * 60)  # Random duration between 20 and 25 minutes

    while time.time() - start_time < run_duration:
        logger.info("Running extract_image_bumble.py...")
        run_script("/Users/frederic/tinder-bot/extract_image_bumble.py")

        logger.info("Running evaluation_bumble.py...")
        evaluation_result = run_script("/Users/frederic/tinder-bot/evaluation_bumble.py")
        if evaluation_result is None:
            continue

        is_beautiful = "Image: Belle" in evaluation_result.stdout if evaluation_result.stdout else False
        logger.info(f"Evaluation result: is_beautiful={is_beautiful}")

        logger.info(f"Running navigate_bumble.py with is_beautiful={is_beautiful}...")
        run_script("/Users/frederic/tinder-bot/navigate_bumble.py", [str(is_beautiful).lower()])

        time.sleep(random.uniform(0.2, 0.3))

    logger.info("Terminating the browser...")
    open_bumble_process.terminate()
    logger.info("Browser terminated.")
    try:
        os.remove(session_ready_path)
        logger.info("session_ready_bumble.txt removed.")
    except Exception as e:
        logger.error(f"Failed to remove session_ready_bumble.txt: {e}")

if __name__ == "__main__":
    main()
