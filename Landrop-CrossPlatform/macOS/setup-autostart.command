#!/bin/bash
# macOS 开机自启（launchd）：登录后自动拉起服务一次
# 卸载：终端执行本脚本并加参数 remove
DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="$(command -v python3 || command -v python)"
PLIST="$HOME/Library/LaunchAgents/com.landrop.server.plist"
if [ -z "$PY" ]; then
  echo "[!] 没找到 python3，请先安装 Python 3"
  exit 1
fi
if [ "$1" = "remove" ]; then
  launchctl unload "$PLIST" 2>/dev/null
  rm -f "$PLIST"
  echo "已移除 macOS 开机自启"
  exit 0
fi
mkdir -p "$HOME/Library/LaunchAgents"
launchctl unload "$PLIST" 2>/dev/null
pkill -f "$DIR/server.py" 2>/dev/null
sleep 0.3
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.landrop.server</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PY</string>
    <string>$DIR/server.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>/tmp/landrop.log</string>
  <key>StandardErrorPath</key><string>/tmp/landrop.log</string>
</dict>
</plist>
EOF
launchctl load "$PLIST"
sleep 1.2
if curl -s -m 3 http://127.0.0.1:8989/api/info >/dev/null 2>&1; then
  echo "✅ 已设置开机自启，服务现在就在跑；注销/重启后登录也会自动拉起"
else
  echo "✅ 已写入自启配置（下次登录生效）。日志: /tmp/landrop.log"
fi
echo "卸载: 在终端执行 '$0' remove"
