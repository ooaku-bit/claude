# setup-task-scheduler.ps1
# Run as Administrator

$taskName   = "ClaudeAutoSync"
$scriptPath = "C:\Claude\scripts\auto-sync.ps1"
$interval   = 15

if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Removed existing task."
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

$trigger = New-ScheduledTaskTrigger `
    -RepetitionInterval (New-TimeSpan -Minutes $interval) `
    -Once `
    -At (Get-Date)

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 2) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Auto sync C:\Claude from GitHub every $interval min" `
    -RunLevel Highest `
    -Force

Write-Host "[OK] Task registered: $taskName"
Write-Host "     Interval: $interval min"
Write-Host "     Script: $scriptPath"
