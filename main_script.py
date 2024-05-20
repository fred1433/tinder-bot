
#main_script.py

import subprocess
import time
import os
import random
import pygame

def run_script(script_path):
    return subprocess.run(["python3", script_path])

def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Step 1: Play an alert sound and wait for 8 seconds
print("Veuillez fermer Google Chrome. Le processus commencera dans 8 secondes.")
play_sound("/Users/frederic/tinder-bot/alert_sound.mp3")  # Chemin vers le fichier sonore MP3
time.sleep(8)

# Step 2: Run open_tinder.py
print("Running open_tinder.py...")
open_tinder_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_tinder.py"])

# Step 3: Wait for the session to be ready
print("Waiting for session to be ready...")
session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
while not os.path.exists(session_ready_path):
    time.sleep(1)

# Step 4: Wait a few more seconds to ensure the browser is fully ready
time.sleep(10)  # Reduced from 20 seconds to 10 seconds

# Step 5: Start the loop for 20 to 30 minutes
start_time = time.time()
run_duration = random.uniform(0.5 * 60, 1 * 60) 

while time.time() - start_time < run_duration:
    # Step 6: Run extract_image.py
    print("Running extract_image.py...")
    run_script("/Users/frederic/tinder-bot/extract_image.py")

    # Step 7: Run evaluation.py and capture the result
    print("Running evaluation.py...")
    evaluation_result = subprocess.run(["python3", "/Users/frederic/tinder-bot/evaluation.py"], capture_output=True, text=True)
    print(evaluation_result.stdout)

    # Parse the evaluation result to determine if the person is beautiful
    is_beautiful = "Image: Belle" in evaluation_result.stdout

    # Step 8: Run navigate_tinder.py with the evaluation result
    print(f"Running navigate_tinder.py with is_beautiful={is_beautiful}...")
    subprocess.run(["python3", "/Users/frederic/tinder-bot/navigate_tinder.py", str(is_beautiful)])

    # Step 9: Wait for 0.5 to 1.5 seconds before the next iteration
    time.sleep(random.uniform(0.1, 0.3))

# Step 10: Terminate the browser automatically
print("Terminating the browser...")
open_tinder_process.terminate()
print("Browser terminated.")

# Clean up the session ready file
os.remove(session_ready_path)
