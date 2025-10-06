@echo off
powershell -Command "Set-Location C:\Users\Administrator\Desktop\splunk_int_v3; Write-Host 'Pulling latest changes from repository...' -ForegroundColor Green; git pull; Write-Host 'Pull complete!' -ForegroundColor Green"
pause
