@echo off
chcp 65001 >nul
rem 移除开机自启（删除启动文件夹里的 Landrop.lnk）
powershell -NoProfile -Command "$p=Join-Path ([Environment]::GetFolderPath('Startup')) 'Landrop.lnk';if(Test-Path $p){Remove-Item $p -Force;Write-Host '已移除开机自启'}else{Write-Host '本来就没设置开机自启'}"
pause
