@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 正在停止市场晨报后台服务...

if exist cache\service.pid (
    set /p SVC_PID=<cache\service.pid
    echo  PID: !SVC_PID!
    powershell -Command "Stop-Process -Id !SVC_PID! -Force -ErrorAction SilentlyContinue"
    del cache\service.pid > nul 2>&1
    echo  ✓ 服务已停止
) else (
    echo  [提示] 未找到 PID 文件，尝试按进程名停止...
    taskkill /F /IM pythonw.exe /T >nul 2>&1
    if not errorlevel 1 (
        echo  ✓ 已停止所有 pythonw 进程
    ) else (
        echo  [提示] 未找到正在运行的后台服务
    )
)
echo.
pause
