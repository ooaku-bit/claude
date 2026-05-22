# setup-task-scheduler.ps1
# Windows Task Scheduler に auto-sync を登録するスクリプト
# 管理者権限で実行してください

$taskName   = "ClaudeAutoSync"
$scriptPath = "C:\Claude\scripts\auto-sync.ps1"
$interval   = 15

# 既存タスクがあれば削除
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "既存タスクを削除しました"
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
    -Description "C:\Claude を GitHub から ${interval} 分ごとに自動同期" `
    -RunLevel Highest `
    -Force

Write-Host "[OK] タスク登録完了: $taskName"
Write-Host "     同期間隔: ${interval} 分ごと"
Write-Host "     スクリプト: $scriptPath"
