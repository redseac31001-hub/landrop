@echo off
chcp 65001 >nul
rem 开机自启 = 在"启动"文件夹放一个最小化快捷方式，登录后自动后台拉起服务
if not exist "%~dp0autostart.bat" (
  echo [!] 缺少 autostart.bat，请勿单独移动本目录下的文件。
  pause
  exit /b 1
)
powershell -NoProfile -Command "$ws=New-Object -ComObject WScript.Shell;$p=Join-Path ([Environment]::GetFolderPath('Startup')) 'Landrop.lnk';$l=$ws.CreateShortcut($p);$l.TargetPath='%~dp0autostart.bat';$l.WorkingDirectory='%~dp0';$l.WindowStyle=7;$l.Description='Landrop autostart';$l.Save()"
echo 已设置开机自启：登录后自动后台运行（不弹窗口）。
echo 卸载：双击 remove-autostart.bat，或 Win+R 输入 shell:startup 删除 Landrop.lnk
pause
