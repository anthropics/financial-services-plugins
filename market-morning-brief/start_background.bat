@echo off
chcp 65001 > nul
setlocal

:: ── 检查配置文件 ────────────────────────────────────────────────────
if not exist .env (
    echo [错误] 未找到 .env 配置文件，请先运行 install.bat
    pause
    exit /b 1
)

:: ── 检查是否已在运行 ─────────────────────────────────────────────────
if exist cache\service.pid (
    set /p OLD_PID=<cache\service.pid
    tasklist /FI "PID eq !OLD_PID!" 2>nul | find /i "python" >nul
    if not errorlevel 1 (
        echo  [提示] 服务已在后台运行（PID: !OLD_PID!）
        echo  如需重启，请先运行 stop.bat
        pause
        exit /b 0
    )
)

if not exist cache mkdir cache

:: ── 后台启动（无控制台窗口）─────────────────────────────────────────
echo 正在后台启动市场晨报服务...

powershell -Command "& { $p = Start-Process pythonw -ArgumentList 'src\main.py' -WorkingDirectory '%~dp0' -PassThru; $p.Id | Out-File -FilePath '%~dp0cache\service.pid' -Encoding ascii }"

timeout /t 2 /nobreak > nul

:: ── 验证启动 ─────────────────────────────────────────────────────────
if exist cache\service.pid (
    set /p SVC_PID=<cache\service.pid
    echo  ✓ 服务已在后台启动（PID: %SVC_PID%）
    echo.
    echo  调度时间（北京时间 CST）：
    echo    09:00  A股+港股 开盘前分析
    echo    15:30  A股+港股 收盘复盘
    echo    21:00  美股 开盘前分析
    echo.
    echo  日志：cache\market_brief.log
    echo  停止：运行 stop.bat
    echo  状态：运行 check_status.bat
) else (
    echo  [错误] 启动失败，请检查：
    echo    1. pythonw.exe 是否在 PATH 中（重新安装 Python 并勾选 Add to PATH）
    echo    2. 依赖是否安装：pip install -r requirements.txt
    echo    3. 尝试用 start.bat 前台模式查看报错
)
echo.
pause
