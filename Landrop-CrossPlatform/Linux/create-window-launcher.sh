#!/bin/bash
# 生成应用菜单入口 Landrop（Chrome 应用模式独立窗口；GNOME/KDE 按下 Win 键搜 Landrop）
DIR="$(cd "$(dirname "$0")/.." && pwd)"
BROWSER="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || command -v microsoft-edge || command -v brave-browser || true)"
if [ -z "$BROWSER" ]; then
  echo "[!] 没找到 Chrome / Chromium / Edge / Brave，先装一个再运行本脚本"
  exit 1
fi
mkdir -p "$HOME/.local/share/applications" "$HOME/bin"
cat > "$HOME/bin/landrop-open.sh" <<EOF
#!/bin/bash
"$DIR/start.sh" >/dev/null 2>&1 &
sleep 1.2
"$BROWSER" --app="http://127.0.0.1:8989" >/dev/null 2>&1 &
EOF
chmod +x "$HOME/bin/landrop-open.sh"
cat > "$HOME/.local/share/applications/landrop.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Landrop
Comment=局域网快传
Exec=$HOME/bin/landrop-open.sh
Icon=folder-download
Categories=Network;FileTransfer;
Terminal=false
EOF
echo "✅ 已创建应用菜单入口 Landrop（按 Win 键搜索 Landrop 即可打开独立窗口）"
