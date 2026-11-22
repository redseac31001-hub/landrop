@echo off
chcp 65001 >nul
title Landrop 启动器
cd /d "%~dp0.."

rem ---- Find Python ----
set "PY="
where python >nul 2>nul && python -c "print(1)" >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && py -c "print(1)" >nul 2>nul && set "PY=py"
if not defined PY (
  echo [!] 没有找到可用的 Python。
  echo     一键安装（PowerShell 执行）：winget install -e --id Python.Python.3.12
  echo     或去 https://www.python.org/downloads/ 下载安装包，
  echo     安装时务必勾选 "Add Python to PATH"，装完重新双击本文件。
  pause
  exit /b 1
)

rem ---- Already running? ----
powershell -NoProfile -Command "try{(Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 'http://127.0.0.1:8989/api/info').StatusCode|Out-Null;exit 0}catch{exit 1}" >nul 2>nul
if %errorlevel%==0 (
  echo Landrop 服务已在运行，直接打开页面。
) else (
  start "Landrop Server" /min cmd /c "%PY% server.py"
  timeout /t 2 /nobreak >nul
  echo 服务已启动（最小化窗口 "Landrop Server"，关掉那个窗口 = 停止服务）。
)

start http://127.0.0.1:8989
echo 本机访问: http://127.0.0.1:8989
echo 其他设备访问: 页面顶部列出的局域网地址
echo 首次运行如弹出防火墙提示，请点"允许访问"。
pause
