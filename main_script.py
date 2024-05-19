# main_script.py
import subprocess
import time
import os

# Step 1: Run open_tinder.py
print("Running open_tinder.py...")
open_tinder_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_tinder.py"])

# Step 2: Wait for the session to be ready
print("Waiting for session to be ready...")
session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
while not os.path.exists(session_ready_path):
    time.sleep(1)

# Adding a delay to ensure Tinder is fully loaded
time.sleep(10)  # Adjust the sleep time if necessary

# Step 3: Run extract_image.py
print("Running extract_image.py...")
subprocess.run(["python3", "/Users/frederic/tinder-bot/extract_image.py"])

print("All tasks completed.")
