
#main_script.py

import subprocess
import time
import os
import random

def run_script(script_path):
    return subprocess.run(["python3", script_path])

# Step 1: Run open_tinder.py
print("Running open_tinder.py...")
open_tinder_process = subprocess.Popen(["python3", "/Users/frederic/tinder-bot/open_tinder.py"])

# Step 2: Wait for the session to be ready
print("Waiting for session to be ready...")
session_ready_path = '/Users/frederic/tinder-bot/session_ready.txt'
while not os.path.exists(session_ready_path):
    time.sleep(1)

# Step 3: Wait a few more seconds to ensure the browser is fully ready
time.sleep(20)

# Step 4: Start the loop for 20 to 30 minutes
start_time = time.time()
run_duration = random.uniform(20 * 60, 30 * 60)  # Random duration between 20 and 30 minutes

while time.time() - start_time < run_duration:
    # Step 5: Run extract_image.py
    print("Running extract_image.py...")
    run_script("/Users/frederic/tinder-bot/extract_image.py")

    # Step 6: Run evaluation.py and capture the result
    print("Running evaluation.py...")
    evaluation_result = subprocess.run(["python3", "/Users/frederic/tinder-bot/evaluation.py"], capture_output=True, text=True)
    print(evaluation_result.stdout)

    # Parse the evaluation result to determine if the person is beautiful
    is_beautiful = "Image: Belle" in evaluation_result.stdout

    # Step 7: Run navigate_tinder.py with the evaluation result
    print(f"Running navigate_tinder.py with is_beautiful={is_beautiful}...")
    subprocess.run(["python3", "/Users/frederic/tinder-bot/navigate_tinder.py", str(is_beautiful)])

    # Step 8: Wait for 1 to 3 seconds before the next iteration
    time.sleep(random.uniform(1, 3))

# Step 9: Wait for user to close the browser manually
input("Please close the browser manually when you are done...")
open_tinder_process.terminate()

# Clean up the session ready file
os.remove(session_ready_path)
