@echo off
chcp 65001 >nul
rem 静默自启入口（开机登录时被启动文件夹的快捷方式调用）：服务已在跑则直接退出
cd /d "%~dp0.."
set "PY="
where python >nul 2>nul && python -c "print(1)" >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && py -c "print(1)" >nul 2>nul && set "PY=py"
if not defined PY exit /b 1
powershell -NoProfile -Command "try{(Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:8989/api/info').StatusCode|Out-Null;exit 0}catch{exit 1}" >nul 2>nul
if %errorlevel%==0 exit /b 0
start "Landrop Server" /min cmd /c "%PY% server.py"
exit /b 0
