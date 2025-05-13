import os
import csv
import time
import pyautogui
import pygetwindow as gw
import psutil
import ctypes
from datetime import date
from collections import defaultdict


def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window and window.title.strip():
            pid = get_pid_from_window(window)  # Get the PID using Windows API
            app_name = get_app_name_by_pid(pid)  # Get application name using PID
            return app_name, window.title.strip()
        else:
            active_window = pyautogui.getWindowsWithTitle(pyautogui.getActiveWindow())
            if active_window:
                return active_window[0].title
            return "Unknown", "Unknown"
    except Exception as e:
        print(f"Error getting window: {e}")
        return "Error"


def get_pid_from_window(window):
    """Retrieve the PID from the window's process using Windows API for accuracy."""
    try:
        # Get the handle of the active window
        hwnd = window._hWnd if hasattr(window, "_hWnd") else None
        if hwnd is None:
            return None
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        return pid.value
    except Exception as e:
        print(f"Error getting PID from window: {e}")
        return None


def get_app_name_by_pid(pid):
    """Get the application name from the PID."""
    try:
        process = psutil.Process(pid)
        return process.name()  # Return the application name
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "Unknown"


def save_log(usage_log):
    today = date.today().strftime("%Y-%m-%d")
    file_name = f"E:\\Yazılım\\Projects\\time-tracker\\logs\\activity_log_{today}.csv"

    # Write the updated log data to the file (always overwriting)
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Application", "Window Title", "Time Spent (seconds)"]
        )  # Write header
        for (app, title), duration in usage_log.items():
            writer.writerow([app, title, duration])

    # print(f"Log saved to {file_name}")


def load_existing_log():
    today = date.today().strftime("%Y-%m-%d")
    file_name = f"E:\\Yazılım\\Projects\\time-tracker\\logs\\activity_log_{today}.csv"

    usage_log = defaultdict(int)

    # If the file exists, read its contents and load into usage_log
    if os.path.exists(file_name):
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                app = row[0]
                title = row[1]
                duration = int(row[2])
                usage_log[(app, title)] += duration  # Add existing data to the log

    return usage_log


def log_activity(interval=5, max_duration=86400):  # max_duration: 24 hours in seconds
    usage_log = load_existing_log()  # Load existing data at the start

    start_time = time.time()

    while time.time() - start_time < max_duration:  # Run for one day
        app, title = get_active_window()
        usage_log[(app, title)] += interval
        time.sleep(interval)

        # Save log every 5 seconds (can be adjusted for efficiency)
        if int(time.time() - start_time) % 5 == 0:
            save_log(usage_log)

    # Final save at the end of the day
    save_log(usage_log)


if __name__ == "__main__":
    try:
        os.makedirs("logs", exist_ok=True)  # Ensure the logs directory exists
        log_activity(interval=5)  # Log activity every 5 seconds
    except KeyboardInterrupt:
        print("Exiting...")
