@echo off
chcp 65001 >nul 2>&1
title 打包中国股市分析工具

echo.
echo  正在打包「中国股市分析工具」...
echo.

set ZIP_NAME=中国股市分析工具_v1.0.0.zip
set SCRIPT_DIR=%~dp0

:: 检查 PowerShell
powershell -Command "exit 0" >nul 2>&1
if errorlevel 1 (
    echo  [错误] 需要 PowerShell，请在 Windows 10/11 上运行
    pause
    exit /b 1
)

:: 删除旧的压缩包
if exist "%SCRIPT_DIR%%ZIP_NAME%" del "%SCRIPT_DIR%%ZIP_NAME%"

:: 用 PowerShell 打包
powershell -NoProfile -Command ^
  "$src = '%SCRIPT_DIR%'; $zip = '%SCRIPT_DIR%%ZIP_NAME%'; " ^
  "$exclude = @('__pycache__', '*.pyc', 'build', 'dist', '*.spec', '打包工具.bat', $zip); " ^
  "$files = Get-ChildItem -Path $src -Recurse | Where-Object { " ^
  "  $rel = $_.FullName.Substring($src.Length); " ^
  "  $skip = $false; " ^
  "  foreach ($ex in $exclude) { if ($rel -like \"*$ex*\") { $skip = $true; break } }; " ^
  "  -not $skip -and -not $_.PSIsContainer " ^
  "}; " ^
  "Compress-Archive -Path $files.FullName -DestinationPath $zip -Force; " ^
  "Write-Host \"  打包完成：$zip\""

if exist "%SCRIPT_DIR%%ZIP_NAME%" (
    echo.
    echo  ╔══════════════════════════════════════════════════╗
    echo  ║  [成功] 打包完成！                               ║
    echo  ║                                                  ║
    echo  ║  文件：%ZIP_NAME%  ║
    echo  ║                                                  ║
    echo  ║  发给朋友的步骤：                                ║
    echo  ║  1. 发送此 ZIP 文件                              ║
    echo  ║  2. 解压到任意文件夹                             ║
    echo  ║  3. 双击「一键启动.bat」即可使用                 ║
    echo  ╚══════════════════════════════════════════════════╝
) else (
    echo  [错误] 打包失败
)

echo.
pause
