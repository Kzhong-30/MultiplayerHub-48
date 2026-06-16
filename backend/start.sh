#!/bin/bash

cd "$(dirname "$0")"

echo "检查 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

echo "初始化数据库数据..."
python init_data.py

echo "启动服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
