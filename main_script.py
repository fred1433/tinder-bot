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

# Step 3: Wait a few more seconds to ensure the browser is fully ready
time.sleep(10)

# Step 4: Run extract_image.py
print("Running extract_image.py...")
subprocess.run(["python3", "/Users/frederic/tinder-bot/extract_image.py"])

# Step 5: Wait for user to close the browser manually
input("Press Enter to close the browser manually...")
open_tinder_process.terminate()

# Clean up the session ready file
os.remove(session_ready_path)
