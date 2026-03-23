@echo off
chcp 65001 > nul
setlocal

echo.
echo -- 设置 Windows 开机自启动 ------------------------------
echo.
echo  此操作将在 Windows 开机时自动启动市场晨报后台服务。
echo  设置后，每次登录 Windows 即自动开始推送。
echo.
set /p CONFIRM=确认设置开机自启动？[Y/N]:
if /i not "%CONFIRM%"=="Y" (
    echo  已取消。
    pause
    exit /b 0
)

:: 写入 Windows 启动文件夹（无需管理员权限）
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SCRIPT_DIR=%~dp0

:: 生成启动脚本
(
    echo @echo off
    echo cd /d "%SCRIPT_DIR%"
    echo if not exist cache mkdir cache
    echo powershell -Command "& { $p = Start-Process pythonw -ArgumentList 'src\main.py' -WorkingDirectory '%SCRIPT_DIR%' -PassThru; $p.Id ^| Out-File -FilePath '%SCRIPT_DIR%cache\service.pid' -Encoding ascii }"
) > "%STARTUP%\市场晨报.bat"

if exist "%STARTUP%\市场晨报.bat" (
    echo.
    echo  ✓ 开机自启动已设置
    echo    启动文件：%STARTUP%\市场晨报.bat
    echo.
    echo  如需取消自启动，运行 remove_autostart.bat
    echo  或手动删除：%STARTUP%\市场晨报.bat
) else (
    echo  [错误] 设置失败，请手动将 start_background.bat 添加到启动文件夹
)
echo.
pause
