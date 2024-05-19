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

# Step 5: Run evaluation.py
print("Running evaluation.py...")
subprocess.run(["python3", "/Users/frederic/tinder-bot/evaluation.py"])

# Step 6: Notify the user to close the browser manually
print("Please close the browser manually when you are done.")

# Clean up the session ready file
os.remove(session_ready_path)
print("All steps completed successfully.")
