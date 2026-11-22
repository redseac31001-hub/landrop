#!/bin/bash
# 生成双击客户端 Landrop.app 到桌面（覆盖旧版）
# 行为：双击 → 服务活着直接开窗口；没跑先拉起再开窗口（Chrome 应用模式，无地址栏）
DIR="$(cd "$(dirname "$0")/.." && pwd)"
ESC="${DIR//\"/\\\"}"
if osacompile -o "$HOME/Desktop/Landrop.app" <<APPLESCRIPT
-- Landrop.app — 双击启动：确保后台服务在跑，然后弹出独立客户端窗口
set serverUp to false
try
	do shell script "curl -s -m 2 http://127.0.0.1:8989/api/info >/dev/null"
	set serverUp to true
end try

if not serverUp then
	do shell script "nohup python3 '$ESC/server.py' >> /tmp/landrop.log 2>&1 &"
	delay 1.2
end if

try
	do shell script "test -d '/Applications/Google Chrome.app' && open -na 'Google Chrome' --args --app=http://127.0.0.1:8989"
on error
	open location "http://127.0.0.1:8989"
end try
APPLESCRIPT
then
  echo "✅ 已生成桌面客户端：$HOME/Desktop/Landrop.app"
  echo "   以后双击它即可；想改行为可重新运行本脚本覆盖生成"
else
  echo "[!] 生成失败，请把本文件拖进终端回车，把报错发出来排查"
  exit 1
fi
