@echo off
chcp 65001 >nul 2>&1
title 中国股市分析工具

echo ╔══════════════════════════════════════════════════╗
echo ║         中国股市分析工具 v1.0.0                  ║
echo ║     A股 + 港股 | 免费数据源                      ║
echo ╚══════════════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

:: Check if dependencies installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [提示] 首次运行，正在安装依赖包...
    echo 这可能需要几分钟，请耐心等待...
    echo.
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo.
    echo [成功] 依赖安装完成！
    echo.
)

echo [启动] 正在启动服务器...
echo [提示] 浏览器将自动打开，如未打开请手动访问 http://localhost:8888
echo [提示] 按 Ctrl+C 停止服务器
echo.
python app.py --host 0.0.0.0 --port 8888

pause
