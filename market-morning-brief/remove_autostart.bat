@echo off
chcp 65001 > nul
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

if exist "%STARTUP%\市场晨报.bat" (
    del "%STARTUP%\市场晨报.bat"
    echo  ✓ 已取消开机自启动
) else (
    echo  [提示] 未找到自启动设置，无需操作
)
pause
