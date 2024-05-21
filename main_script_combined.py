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
        logger.error(result.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run script {script_path}: {e.stderr}")

def execute_scripts():
    logger.info("Starting Bumble script...")
    run_script("/Users/frederic/tinder-bot/main_script_bumble.py")
    
    logger.info("Bumble script completed. Waiting 10 seconds before starting Tinder script...")
    time.sleep(10)  # Attendre 10 secondes entre les scripts

    logger.info("Starting Tinder script...")
    run_script("/Users/frederic/tinder-bot/main_script_tinder.py")

    logger.info("Tinder script completed.")

def main():
    timezone = pytz.timezone("America/Sao_Paulo")
    while True:
        current_time = datetime.now(timezone)
        if 8 <= current_time.hour < 23 or (current_time.hour == 23 and current_time.minute <= 30):
            execute_scripts()
            wait_time = random.uniform(2 * 60 * 60, 2.5 * 60 * 60)
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
