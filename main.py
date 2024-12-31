import os
import csv
import time
import pyautogui
import pygetwindow as gw
from datetime import date
from collections import defaultdict


def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window and window.title.strip():
            return window.title.strip()
        # Fallback if pygetwindow doesn't work
        else:
            active_window = pyautogui.getWindowsWithTitle(pyautogui.getActiveWindow())
            if active_window:
                return active_window[0].title
            return "Unknown"
    except Exception as e:
        print(f"Error getting window: {e}")
        return "Error"


def save_log(usage_log):
    today = date.today().strftime("%Y-%m-%d")
    file_name = f"logs/activity_log_{today}.csv"

    # Write the updated log data to the file (always overwriting)
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Application", "Time Spent (seconds)"])  # Write header
        for app, duration in usage_log.items():
            writer.writerow([app, duration])

    print(f"Log saved to {file_name}")


def load_existing_log():
    today = date.today().strftime("%Y-%m-%d")
    file_name = f"logs/activity_log_{today}.csv"

    usage_log = defaultdict(int)

    # If the file exists, read its contents and load into usage_log
    if os.path.exists(file_name):
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                app = row[0]
                duration = int(row[1])
                usage_log[app] += duration  # Add existing data to the log

    return usage_log


def log_activity(interval=5, max_duration=86400):  # max_duration: 24 hours in seconds
    usage_log = load_existing_log()  # Load existing data at the start

    start_time = time.time()

    while time.time() - start_time < max_duration:  # Run for one day
        active_window = get_active_window()
        usage_log[active_window] += interval
        time.sleep(interval)

        # Save log every 1 second (can be adjusted for efficiency)
        if int(time.time() - start_time) % 60 == 0:
            save_log(usage_log)

    # Final save at the end of the day
    save_log(usage_log)


if __name__ == "__main__":
    try:
        os.makedirs("logs", exist_ok=True)  # Ensure the logs directory exists
        log_activity(interval=5)  # Log activity every 5 seconds
    except KeyboardInterrupt:
        print("Exiting...")
