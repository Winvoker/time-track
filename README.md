# Activity Tracker Startup Script

This repository contains a PowerShell script that automatically runs your Python-based activity tracker at system startup. The script tracks the active window and logs the time spent on each application.

## Features

- **Automatic Startup**: The Python script is set to run automatically when Windows starts up.
- **Time Tracking**: Tracks the active window/application and logs the time spent.
- **Task Scheduler Integration**: Uses Windows Task Scheduler to execute the Python script at startup without user intervention.
- **Python Script**: The Python script tracks application usage and logs the activity into a CSV file.

## Files

- **setup_activity_tracker.ps1**: The main PowerShell script that:
    - Creates a PowerShell script to run your Python script at startup.
    - Registers a task in Task Scheduler to run the activity tracker at startup.
- **run_at_startup.ps1**: This PowerShell script is automatically created by `setup_activity_tracker.ps1` and is used to run the Python script at startup.

## Setup

### Prerequisites

- **Python**: Ensure Python is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).
- **PowerShell**: The script requires PowerShell (comes pre-installed with Windows).

### Installation

1. Clone this repository or download the files to your local machine.
2. **Modify the file paths** in `setup_activity_tracker.ps1`:
    - Replace `"C:\path\to\your\script\script.py"` with the full path to your Python script.
    - Replace `"C:\path\to\python.exe"` with the full path to your Python executable. You can find it by running `where python` in the Command Prompt.
3. Open PowerShell as Administrator.
4. Navigate to the directory where `setup_activity_tracker.ps1` is located.
5. Run the script:
    
    ```powershell
    powershell
    Kodu kopyala
    .\setup_activity_tracker.ps1
    
    ```
    
6. The script will:
    - Create a PowerShell script (`run_at_startup.ps1`) to run your Python script.
    - Register a task in Task Scheduler to execute the Python script at startup.

### Running the Python Script Manually

If you want to run the Python script manually before setting it up for automatic startup:

1. Ensure Python is installed and the necessary dependencies are available.
2. Run the Python script:
    
    ```bash
    bash
    Kodu kopyala
    python C:\path\to\your\script\script.py
    
    ```
    

### Uninstall

To remove the scheduled task and stop the activity tracker from running at startup, follow these steps:

1. Open Task Scheduler and find the task named **PythonActivityTracker**.
2. Right-click and select **Delete** to remove it.

Additionally, you can manually delete the `run_at_startup.ps1` script if you no longer need it.

## Troubleshooting

- **"Unknown" Application in Logs**: If the active window is shown as "Unknown", ensure the script is being run with the necessary privileges to access the active window information.
- **Task Not Running at Startup**: Ensure that the task is created properly in Task Scheduler. You can check the Task Scheduler logs to troubleshoot any issues with the task.

## License

This project is licensed under the MIT License.
