# main_script_combined.py

import subprocess
import logging
import time
import random
from datetime import datetime, timedelta
import pytz

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='tinder_bot_combined.log', filemode='w')
logger = logging.getLogger()

def run_script(script_path):
    try:
        logger.info(f"Running script: {script_path}")
        result = subprocess.run(["python3", script_path], capture_output=True, text=True, check=True)
        logger.info(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run script {script_path}: {e.stderr}")
        return False

def update_profile_count(script_path, count):
    logger.info(f"{script_path} swiped {count} profiles.")

def execute_scripts():
    bumble_success = run_script("/Users/frederic/tinder-bot/main_script_bumble.py")
    if bumble_success:
        update_profile_count("/Users/frederic/tinder-bot/main_script_bumble.py", 100)  # Placeholder count
        logger.info("Bumble script completed successfully.")
        with open("last_success_bumble.txt", "w") as f:
            f.write(f"Last successful Bumble run: {datetime.now()}")
    else:
        logger.error("Bumble script encountered an error.")
        with open("last_error_bumble.txt", "w") as f:
            f.write(f"Last Bumble error: {datetime.now()}")
    
    time.sleep(10)  # Wait 10 seconds between scripts

    tinder_success = run_script("/Users/frederic/tinder-bot/main_script_tinder.py")
    if tinder_success:
        update_profile_count("/Users/frederic/tinder-bot/main_script_tinder.py", 150)  # Placeholder count
        logger.info("Tinder script completed successfully.")
        with open("last_success_tinder.txt", "w") as f:
            f.write(f"Last successful Tinder run: {datetime.now()}")
    else:
        logger.error("Tinder script encountered an error.")
        with open("last_error_tinder.txt", "w") as f:
            f.write(f"Last Tinder error: {datetime.now()}")

def main():
    timezone = pytz.timezone("America/Sao_Paulo")
    while True:
        current_time = datetime.now(timezone)
        if 8 <= current_time.hour < 23 or (current_time.hour == 23 and current_time.minute <= 30):
            execute_scripts()
            wait_time = random.uniform(1.25 * 60 * 60, 1.5 * 60 * 60)
            logger.info(f"Waiting for {wait_time / 3600:.2f} hours before the next run.")
            time.sleep(wait_time)
        else:
            next_run_time = datetime(current_time.year, current_time.month, current_time.day, 8, 0, tzinfo=timezone)
            if current_time.hour >= 23 and current_time.minute > 30:
                next_run_time += timedelta(days=1)
            sleep_time = (next_run_time - current_time).total_seconds()
            logger.info(f"Current time is outside the allowed range. Sleeping for {sleep_time / 3600:.2f} hours until next allowed run time.")
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()