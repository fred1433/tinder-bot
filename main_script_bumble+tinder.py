import subprocess
import time
import os
import random
import pygame
from datetime import datetime, timedelta
import pytz
import logging

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def run_script(script_path, args=[]):
    try:
        result = subprocess.run(["python3", script_path] + args, capture_output=True, text=True, check=True)
        logger.info(f"Output of {script_path}: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run script {script_path} with args {args}: {e}")
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

def process_bumble():
    logger.info("Running open_bumble.py...")
    try:
        open_bumble_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_bumble.py"])
    except Exception as e:
        logger.error(f"Failed to start open_bumble.py: {e}")
        return

    logger.info("Waiting for session to be ready...")
    session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
    while not os.path.exists(session_ready_path):
        time.sleep(2)

    time.sleep(10)

    start_time = time.time()
    run_duration = 30  # Run for 30 seconds

    while time.time() - start_time < run_duration:
        logger.info("Running extract_image_bumble.py...")
        run_script("/Users/frederic/tinder-bot/extract_image_bumble.py")

        logger.info("Running evaluation_bumble.py...")
        evaluation_result = run_script("/Users/frederic/tinder-bot/evaluation_bumble.py")
        if evaluation_result is None:
            continue

        is_beautiful = "Image: Belle" in evaluation_result.stdout if evaluation_result.stdout else False

        logger.info(f"Running navigate_bumble.py with is_beautiful={is_beautiful}...")
        run_script("/Users/frederic/tinder-bot/navigate_bumble.py", [str(is_beautiful)])

        time.sleep(random.uniform(0.2, 0.3))

    logger.info("Terminating the browser...")
    open_bumble_process.terminate()
    logger.info("Browser terminated.")
    try:
        os.remove(session_ready_path)
        logger.info("session_ready.txt removed.")
    except Exception as e:
        logger.error(f"Failed to remove session_ready.txt: {e}")

def process_tinder():
    logger.info("Running open_tinder.py...")
    try:
        open_tinder_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_tinder.py"])
    except Exception as e:
        logger.error(f"Failed to start open_tinder.py: {e}")
        return

    logger.info("Waiting for session to be ready...")
    session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
    while not os.path.exists(session_ready_path):
        time.sleep(2)

    time.sleep(10)

    start_time = time.time()
    run_duration = 30  # Run for 30 seconds

    while time.time() - start_time < run_duration:
        logger.info("Running extract_image_tinder.py...")
        run_script("/Users/frederic/tinder-bot/extract_image_tinder.py")

        logger.info("Running evaluation_tinder.py...")
        evaluation_result = run_script("/Users/frederic/tinder-bot/evaluation_tinder.py")
        if evaluation_result is None:
            continue

        is_beautiful = "Image: Belle" in evaluation_result.stdout if evaluation_result.stdout else False

        logger.info(f"Running navigate_tinder.py with is_beautiful={is_beautiful}...")
        run_script("/Users/frederic/tinder-bot/navigate_tinder.py", [str(is_beautiful)])

        time.sleep(random.uniform(0.2, 0.3))

    logger.info("Terminating the browser...")
    open_tinder_process.terminate()
    logger.info("Browser terminated.")
    try:
        os.remove(session_ready_path)
        logger.info("session_ready.txt removed.")
    except Exception as e:
        logger.error(f"Failed to remove session_ready.txt: {e}")

def main():
    logger.info("Le processus commencera dans 3 secondes.")
    play_sound("/Users/frederic/tinder-bot/alert_sound.mp3")
    time.sleep(3)
    close_chrome()

    process_bumble()
    close_chrome()  # Ensure Chrome is closed before starting Tinder
    time.sleep(10)  # Short break between processes
    process_tinder()
    close_chrome()  # Ensure Chrome is closed after Tinder process

if __name__ == "__main__":
    timezone = pytz.timezone("America/Sao_Paulo")
    while True:
        current_time = datetime.now(timezone)
        if 8 <= current_time.hour < 23:
            main()
            wait_time = random.uniform(2 * 60 * 60, 2.5 * 60 * 60)
            logger.info(f"Waiting for {wait_time / 3600:.2f} hours before the next run.")
            time.sleep(wait_time)
        else:
            next_run_time = datetime(current_time.year, current_time.month, current_time.day, 8, 2, tzinfo=timezone)
            if current_time.hour >= 23:
                next_run_time += timedelta(days=1)
            sleep_time = (next_run_time - current_time).total_seconds()
            logger.info(f"Current time is outside the allowed range. Sleeping for {sleep_time / 3600:.2f} hours until next allowed run time.")
            time.sleep(sleep_time)
