@echo off
chcp 65001 >nul
rem 停止 Landrop 服务
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(python|py|python3|pythonw)\.exe$' -and $_.CommandLine -match 'server\.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Landrop 已停止
pause
