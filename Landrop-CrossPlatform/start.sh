#!/bin/bash
# 启动 Landrop（后台常驻，日志 /tmp/landrop.log）— macOS / Linux / WSL / Termux 通用
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "[!] 没找到 python3，请先安装 Python 3"
  exit 1
fi
pkill -f "$DIR/server.py" 2>/dev/null
sleep 0.3
nohup "$PY" "$DIR/server.py" "$@" > /tmp/landrop.log 2>&1 &
for i in 1 2 3 4 5; do
  sleep 0.5
  if curl -s -m 2 http://127.0.0.1:8989/api/info >/dev/null 2>&1; then break; fi
done
echo "--- 状态 ---"
curl -s -m 3 http://127.0.0.1:8989/api/info && echo
echo "--- 访问地址 ---"
grep '➜' /tmp/landrop.log
echo "日志: /tmp/landrop.log ｜ 停止: $(dirname "$0")/stop.sh"
