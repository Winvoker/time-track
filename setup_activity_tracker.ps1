# Define paths
$pythonScript = ""   # Path to your Python script
$pythonExe = ""                  # Path to your Python executable (replace with your Python path)


# Create PowerShell script to run the Python script at user login
$loginScriptContent = @"
# PowerShell Script to run Python script at user login
Start-Process -FilePath '$pythonExe' -ArgumentList '$pythonScript'
"@


# Check if the task already exists
$taskName = "PythonActivityTracker"
$existingTask = Get-ScheduledTask | Where-Object {$_.TaskName -eq $taskName}

if ($existingTask) {
    # If task exists, delete it
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Existing task '$taskName' has been removed."
}

# Create a scheduled task to run the PowerShell script at user logon
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File $runAtLoginScript"
$Trigger = New-ScheduledTaskTrigger -AtLogon
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -Action $Action -Principal $Principal -Trigger $Trigger -TaskName $taskName -Description "Run the Python activity tracker script at user logon"

Write-Host "Setup complete. The Python activity tracker will now run at user logon."