# auto-sync.ps1
# Automatically pull latest changes from GitHub

$repoPath = "C:\Claude"
$logFile  = "$repoPath\scripts\sync.log"
$branch   = "master"

function Write-Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp $msg" | Tee-Object -FilePath $logFile -Append
}

Set-Location $repoPath

git fetch origin $branch 2>&1 | Out-Null

$local  = git rev-parse HEAD
$remote = git rev-parse "origin/$branch"

if ($local -eq $remote) {
    Write-Log "Already up to date."
    exit 0
}

$result = git pull origin $branch 2>&1
Write-Log "Pulled: $result"
Write-Log "Sync complete."
