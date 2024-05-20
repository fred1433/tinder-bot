
#main_script.py

import subprocess
import time
import os
import random
import pygame
from datetime import datetime, timedelta
import pytz

def run_script(script_path):
    return subprocess.run(["python3", script_path])

def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def close_chrome():
    print("Fermeture de Google Chrome...")
    subprocess.run(["pkill", "-f", "Google Chrome"])
    time.sleep(5)
    print("Google Chrome est fermé.")

def main():
    print("Le processus commencera dans 8 secondes.")
    play_sound("/Users/frederic/tinder-bot/alert_sound.mp3")
    time.sleep(8)
    close_chrome()

    print("Running open_tinder.py...")
    open_tinder_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_tinder.py"])

    print("Waiting for session to be ready...")
    session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
    while not os.path.exists(session_ready_path):
        time.sleep(1)

    time.sleep(10)

    start_time = time.time()
    run_duration = random.uniform(20 * 60, 25 * 60)

    while time.time() - start_time < run_duration:
        print("Running extract_image.py...")
        run_script("/Users/frederic/tinder-bot/extract_image.py")

        print("Running evaluation.py...")
        evaluation_result = subprocess.run(["python3", "/Users/frederic/tinder-bot/evaluation.py"], capture_output=True, text=True)
        print(evaluation_result.stdout)

        is_beautiful = "Image: Belle" in evaluation_result.stdout

        print(f"Running navigate_tinder.py with is_beautiful={is_beautiful}...")
        subprocess.run(["python3", "/Users/frederic/tinder-bot/navigate_tinder.py", str(is_beautiful)])

        time.sleep(random.uniform(0.2, 0.3))

    print("Terminating the browser...")
    open_tinder_process.terminate()
    print("Browser terminated.")
    os.remove(session_ready_path)
    print("Browser terminated and script finished.")

if __name__ == "__main__":
    timezone = pytz.timezone("America/Sao_Paulo")
    while True:
        current_time = datetime.now(timezone)
        if current_time.hour >= 8 and current_time.hour < 23:
            main()
            wait_time = random.uniform(2 * 60 * 60, 2.5 * 60 * 60)
            print(f"Waiting for {wait_time / 3600:.2f} hours before the next run.")
            time.sleep(wait_time)
        else:
            next_run_time = datetime(current_time.year, current_time.month, current_time.day, 8, 2, tzinfo=timezone)
            if current_time.hour >= 23:
                next_run_time += timedelta(days=1)
            sleep_time = (next_run_time - current_time).total_seconds()
            print(f"Current time is outside the allowed range. Sleeping for {sleep_time / 3600:.2f} hours until next allowed run time.")
            time.sleep(sleep_time)
