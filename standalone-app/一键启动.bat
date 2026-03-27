@echo off
chcp 65001 >nul 2>&1
title 中国股市分析工具 v1.0.0

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║            中国股市分析工具 v1.0.0                   ║
echo  ║        A股 + 港股  免费数据  无需注册                 ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

:: ── 第一步：检测 Python ────────────────────────────────────────
set PYTHON_CMD=
for %%p in (python python3) do (
    %%p --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=%%p
        goto :found_python
    )
)

:: 尝试常见安装路径
for %%d in (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "%ProgramFiles%\Python311\python.exe"
) do (
    if exist %%d (
        set PYTHON_CMD=%%d
        goto :found_python
    )
)

:: 未找到 Python，自动下载安装
echo  [提示] 未检测到 Python，即将自动下载安装...
echo  [提示] 文件约 25MB，请确保网络畅通，大约需要 1-3 分钟
echo.
set PY_INSTALLER=%TEMP%\python_installer.exe
set PY_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

echo  正在下载 Python 3.11...
powershell -NoProfile -Command "try { (New-Object Net.WebClient).DownloadFile('%PY_URL%', '%PY_INSTALLER%'); Write-Host '  下载完成' } catch { Write-Host '  下载失败，请手动安装 Python: https://www.python.org/downloads/'; exit 1 }"
if errorlevel 1 goto :error_python

echo  正在安装 Python（静默安装，请稍候）...
"%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=1
if errorlevel 1 (
    echo  [错误] 自动安装失败
    echo  请手动下载安装：https://www.python.org/downloads/
    echo  安装时请勾选 "Add Python to PATH"
    goto :error_python
)

:: 刷新环境变量
call :refresh_path
set PYTHON_CMD=python
python --version >nul 2>&1
if errorlevel 1 (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
)
echo  [成功] Python 安装完成！
echo.

:found_python
echo  [√] 检测到 Python:
%PYTHON_CMD% --version
echo.

:: ── 第二步：安装依赖 ────────────────────────────────────────────
%PYTHON_CMD% -c "import flask, akshare, yfinance" >nul 2>&1
if not errorlevel 1 goto :start_app

echo  [提示] 首次运行，正在安装必要组件...
echo  [提示] 约需 2-5 分钟，安装一次即可，以后秒开
echo.

:: 优先使用国内镜像加速
%PYTHON_CMD% -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple -q
%PYTHON_CMD% -m pip install flask akshare yfinance baostock pandas requests waitress -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo  [提示] 国内镜像失败，切换官方源重试...
    %PYTHON_CMD% -m pip install flask akshare yfinance baostock pandas requests waitress
    if errorlevel 1 (
        echo.
        echo  [错误] 组件安装失败，请检查网络连接后重试
        pause
        exit /b 1
    )
)

echo.
echo  [成功] 所有组件安装完成！
echo.

:: ── 第三步：启动程序 ────────────────────────────────────────────
:start_app
echo  ╔══════════════════════════════════════════════════════╗
echo  ║  [启动中] 正在启动中国股市分析工具...               ║
echo  ║                                                      ║
echo  ║  浏览器会自动打开，如未打开请访问：                  ║
echo  ║  http://localhost:8888                               ║
echo  ║                                                      ║
echo  ║  手机访问（同一WiFi下）：                            ║
echo  ║  http://[电脑IP地址]:8888                            ║
echo  ║                                                      ║
echo  ║  关闭程序：直接关闭此窗口或按 Ctrl+C                ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

%PYTHON_CMD% app.py --host 0.0.0.0 --port 8888
goto :end

:error_python
echo.
echo  ══════════════════════════════════════════════════
echo  请手动安装 Python：
echo  1. 打开浏览器，访问 https://www.python.org/downloads/
echo  2. 点击 "Download Python 3.11.x"
echo  3. 运行安装包，勾选 "Add Python to PATH"
echo  4. 安装完成后，重新双击本程序
echo  ══════════════════════════════════════════════════
echo.
pause
exit /b 1

:refresh_path
:: 尝试刷新 PATH 以包含新安装的 Python
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USER_PATH=%%b"
set "PATH=%PATH%;%USER_PATH%"
exit /b 0

:end
pause
