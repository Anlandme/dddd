#!/bin/bash

# 检查启动情况
PROJ_DIR=$(dirname $(pwd))
pid=$(pgrep -f "${PROJ_DIR}/src/main.py")
echo ${pid}
