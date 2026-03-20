#!/bin/bash
# 中国股市分析工具 - Linux/Mac 启动脚本

echo "╔══════════════════════════════════════════════════╗"
echo "║         中国股市分析工具 v1.0.0                  ║"
echo "║     A股 + 港股 | 免费数据源                      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装"
    exit 1
fi

# Check dependencies
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 首次运行，正在安装依赖包..."
    pip3 install -r requirements.txt
fi

echo "[启动] 正在启动服务器..."
echo "[提示] 按 Ctrl+C 停止服务器"
python3 app.py --host 0.0.0.0 --port 8888
