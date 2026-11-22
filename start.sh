#!/bin/bash
# 启动 Landrop 局域网快传（后台常驻，日志在 /tmp/landrop.log）
DIR="$(cd "$(dirname "$0")" && pwd)"
pkill -f "$DIR/server.py" 2>/dev/null
sleep 0.3
nohup python3 "$DIR/server.py" "$@" > /tmp/landrop.log 2>&1 &
for i in 1 2 3 4 5; do
  sleep 0.5
  if curl -s -m 2 http://127.0.0.1:8989/api/info >/dev/null 2>&1; then break; fi
done
echo "--- 状态 ---"
curl -s http://127.0.0.1:8989/api/info && echo
echo "--- 访问地址 ---"
grep '➜' /tmp/landrop.log
echo "日志: /tmp/landrop.log ｜ 停止: $(dirname "$0")/stop.sh"
