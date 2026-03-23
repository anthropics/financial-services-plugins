@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ── 市场晨报系统状态检查 ─────────────────────────────────
echo.

:: ── 检查服务进程 ─────────────────────────────────────────────────────
set RUNNING=0
if exist cache\service.pid (
    set /p SVC_PID=<cache\service.pid
    tasklist /FI "PID eq !SVC_PID!" 2>nul | find /i "python" >nul
    if not errorlevel 1 (
        echo  ● 服务状态：运行中（PID: !SVC_PID!）
        set RUNNING=1
    ) else (
        echo  ○ 服务状态：已停止（PID 文件残留，进程不存在）
    )
) else (
    tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /i "pythonw" >nul
    if not errorlevel 1 (
        echo  ● 服务状态：后台运行中（无 PID 文件）
        set RUNNING=1
    ) else (
        echo  ○ 服务状态：未运行
    )
)

:: ── 检查配置 ─────────────────────────────────────────────────────────
echo.
if exist .env (
    echo  ✓ .env 配置文件存在
) else (
    echo  ✗ .env 配置文件不存在（请运行 install.bat）
)

:: ── 显示最新日志 ─────────────────────────────────────────────────────
echo.
if exist "%~dp0cache\market_brief.log" (
    echo  最近 10 行日志：
    echo  ────────────────────────────────────────
    powershell -Command "Get-Content '%~dp0cache\market_brief.log' -Tail 10 | ForEach-Object { '  ' + $_ }"
) else (
    echo  日志文件尚未生成（服务未运行或首次启动）
)

echo.
echo  操作提示：
if !RUNNING!==1 (
    echo    stop.bat          停止服务
) else (
    echo    start.bat         前台启动（推荐调试）
    echo    start_background.bat  后台启动
)
echo    python src\main.py --test    测试飞书推送
echo    python src\main.py --now premarket_asia  立即触发盘前报告
echo.
pause
