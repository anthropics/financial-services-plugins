@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ========================================================
echo    三地股市智能晨报/晚报系统  Windows 安装向导
echo ========================================================
echo.

:: ── 1. 检查 Python ───────────────────────────────────────────────────
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [错误] 未检测到 Python！
    echo.
    echo  请先安装 Python 3.12+：
    echo    https://www.python.org/downloads/
    echo.
    echo  安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  ✓ Python %PYVER% 已安装

:: ── 2. 安装依赖 ──────────────────────────────────────────────────────
echo.
echo [2/4] 安装 Python 依赖（可能需要 3-5 分钟）...
echo  使用清华镜像源加速下载...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if errorlevel 1 (
    echo  镜像源失败，切换到阿里云镜像...
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --quiet
    if errorlevel 1 (
        echo  [警告] 镜像源均失败，使用官方源（速度较慢）...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo  [错误] 依赖安装失败！请检查网络连接后重试。
            pause
            exit /b 1
        )
    )
)
echo  ✓ 依赖安装完成

:: ── 3. 创建配置文件 ───────────────────────────────────────────────────
echo.
echo [3/4] 配置环境变量...
if not exist .env (
    copy .env.example .env > nul
    echo  ✓ 已创建 .env 配置文件
    echo.
    echo  -------------------------------------------------
    echo    接下来请在记事本中填写以下配置：
    echo.
    echo    ANTHROPIC_API_KEY  -- Claude 分析（强烈推荐）
    echo    FEISHU_WEBHOOK_URLS -- 飞书 Webhook（必填）
    echo  -------------------------------------------------
    echo.
    echo  即将打开 .env 配置文件，填写后保存关闭记事本...
    timeout /t 3 /nobreak > nul
    notepad .env
) else (
    echo  ✓ .env 文件已存在，跳过创建
)

:: ── 4. 创建缓存目录 ───────────────────────────────────────────────────
echo.
echo [4/4] 创建缓存目录...
if not exist cache mkdir cache
echo  ✓ cache 目录已就绪

:: ── 完成 ──────────────────────────────────────────────────────────────
echo.
echo ========================================================
echo  安装完成！下一步：
echo.
echo  1. 确认 .env 中已填写 FEISHU_WEBHOOK_URLS
echo  2. 双击 start.bat 启动服务（保持窗口不关闭）
echo  3. 或双击 start_background.bat 在后台静默运行
echo.
echo  测试推送：python src\main.py --test
echo  立即触发：python src\main.py --now premarket_asia
echo ========================================================
echo.
pause
