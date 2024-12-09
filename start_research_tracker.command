#!/bin/bash

# 切换到项目目录
cd "$(dirname "$0")"

# 初始化环境
source ~/.zshrc

# 激活conda环境
conda activate research_tracker

# 启动 Python 后端服务
python app.py &

# 等待服务启动
sleep 2

# 打开默认浏览器访问应用
open http://localhost:5001 