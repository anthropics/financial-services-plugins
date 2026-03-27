@echo off
chcp 65001 > nul
setlocal

echo.
echo ================================================
echo   三地股市智能晨报/晚报系统  启动中...
echo ================================================
echo.

:: ── 检查配置文件 ────────────────────────────────────────────────────
if not exist .env (
    echo  [错误] 未找到 .env 配置文件！
    echo  请先运行 install.bat 完成安装。
    echo.
    pause
    exit /b 1
)

:: ── 检查 Python ──────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [错误] 未检测到 Python，请先运行 install.bat
    pause
    exit /b 1
)

:: ── 创建 cache 目录 ──────────────────────────────────────────────────
if not exist cache mkdir cache

:: ── 显示调度计划 ─────────────────────────────────────────────────────
powershell -NoProfile -Command "Write-Host '  Schedule (Beijing CST):'; Write-Host '   09:00  A股+港股 开盘前分析 -> 推送飞书'; Write-Host '   16:30  A股+港股 收盘复盘   -> 推送飞书'; Write-Host '   21:00  美股 开盘前分析     -> 推送飞书'"
echo.
echo  注意：关闭此窗口将停止推送！
echo  如需后台运行，请使用 start_background.bat
echo.
echo  日志文件：cache\market_brief.log
echo  按 Ctrl+C 可停止服务
echo ------------------------------------------------
echo.

:: ── 启动服务 ─────────────────────────────────────────────────────────
python src\main.py

echo.
echo  服务已停止。
pause
