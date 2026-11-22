#!/bin/bash
# 生成双击客户端 Landrop.app 到桌面（覆盖旧版，含项目图标）
# 行为：双击 → 服务活着直接开窗口；没跑先拉起再开窗口（Chrome 应用模式，无地址栏）
DIR="$(cd "$(dirname "$0")/.." && pwd)"
APP="$HOME/Desktop/Landrop.app"
ESC="${DIR//\"/\\\"}"
if osacompile -o "$APP" <<APPLESCRIPT
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
  # 替换为项目图标（applet 默认图标槽），并重新 ad-hoc 签名
  ICON_APPLIED=0
  if [ -f "$DIR/assets/landrop.icns" ]; then
    if cp "$DIR/assets/landrop.icns" "$APP/Contents/Resources/applet.icns"; then
      ICON_APPLIED=1
      codesign --force --deep -s - "$APP" 2>/dev/null
    fi
  fi
  if [ "$ICON_APPLIED" = 1 ]; then
    echo "✅ 已生成桌面客户端：$APP（带项目图标）"
  else
    echo "✅ 已生成桌面客户端：$APP（未找到 assets/landrop.icns，使用默认图标）"
  fi
  echo "   以后双击它即可；想改行为可重新运行本脚本覆盖生成"
else
  echo "[!] 生成失败，请把本文件拖进终端回车，把报错发出来排查"
  exit 1
fi
