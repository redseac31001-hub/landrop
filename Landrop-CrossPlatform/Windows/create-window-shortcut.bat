@echo off
chcp 65001 >nul
rem 在桌面创建 Landrop 独立窗口快捷方式（Chrome / Edge 应用模式，无地址栏、无标签页）
set "CHROME="
for %%p in (
  "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
  "%LocalAppData%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
  "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) do if exist "%%~p" set "CHROME=%%~p"
if not defined CHROME (
  echo [!] 没找到 Chrome / Edge，先装一个再运行本脚本。
  pause
  exit /b 1
)
powershell -NoProfile -Command "$ws=New-Object -ComObject WScript.Shell;$p=[Environment]::GetFolderPath('Desktop')+'\Landrop.lnk';$l=$ws.CreateShortcut($p);$l.TargetPath='%CHROME%';$l.Arguments='--app=http://127.0.0.1:8989';$l.IconLocation='%CHROME%,0';$l.Description='Landrop LAN transfer';$l.Save()"
echo 已在桌面创建 Landrop.lnk（双击即弹出独立窗口）。
echo 使用顺序：先双击 Windows\start.bat 起服务，再双击桌面 Landrop 图标开窗口。
pause
