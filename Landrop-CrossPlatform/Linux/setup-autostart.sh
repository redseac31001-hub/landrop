#!/bin/bash
# Linux 开机自启（systemd 用户级）：登录后自动拉起服务一次
# 卸载：终端执行本脚本并加参数 remove
DIR="$(cd "$(dirname "$0")/.." && pwd)"
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "[!] 没找到 python3，请先安装 Python 3"
  exit 1
fi
if [ "$1" = "remove" ]; then
  systemctl --user disable --quiet landrop.service 2>/dev/null
  rm -f "$HOME/.config/systemd/user/landrop.service"
  systemctl --user daemon-reload
  echo "已移除 Linux 开机自启"
  exit 0
fi
mkdir -p "$HOME/.config/systemd/user"
pkill -f "$DIR/server.py" 2>/dev/null
sleep 0.3
cat > "$HOME/.config/systemd/user/landrop.service" <<EOF
[Unit]
Description=Landrop LAN file transfer
After=network.target

[Service]
ExecStart="$PY" "$DIR/server.py"

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now landrop.service
sleep 1
if systemctl --user is-active --quiet landrop.service; then
  echo "✅ 已设置开机自启，服务正在运行：systemctl --user status landrop"
else
  echo "✅ 已写入自启配置，启动状态可用 systemctl --user status landrop 查看"
fi
echo "无桌面/SSH 长期挂机需执行一次: loginctl enable-linger \$USER"
echo "卸载: 在终端执行 '$0' remove"
