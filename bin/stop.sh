#!/usr/bin/env bash

PROJ_DIR=$(dirname $(pwd))
pid=$(pgrep -f "${PROJ_DIR}/src/main.py")
echo ${pid}
kill -9 $pid
