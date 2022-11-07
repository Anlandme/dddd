#!/bin/bash
PROJ_DIR=$(dirname $(pwd))

# 创建 log 目录
LOG_DIR=${PROJ_DIR}/log
if [ ! -d $LOG_DIR ];then
    mkdir $LOG_DIR
fi

# 启动服务
export PYTHONPATH=${PROJ_DIR}
nohup python3 ${PROJ_DIR}/src/main.py 1 >> ${PROJ_DIR}/log/main.log 2>&1 &

# 检查启动情况
sleep 1
PROJ_DIR=$(dirname $(pwd))
pid=$(pgrep -f "${PROJ_DIR}/src/main.py")
echo ${pid}
