#!/bin/bash
# 停止 Landrop
DIR="$(cd "$(dirname "$0")" && pwd)"
if pkill -f "$DIR/server.py"; then
  echo "Landrop 已停止"
else
  echo "Landrop 未在运行"
fi
