@echo off
chcp 65001 >nul 2>&1
echo ==========================================
echo   打包中国股市分析工具 (Windows版)
echo ==========================================
echo.

:: 安装打包工具
pip install pyinstaller

:: 执行打包
echo [打包] 正在打包为Windows可执行文件...
pyinstaller build_windows.spec --clean

echo.
if exist "dist\中国股市分析工具" (
    echo [成功] 打包完成！
    echo 输出目录: dist\中国股市分析工具\
    echo 运行: dist\中国股市分析工具\中国股市分析工具.exe
) else (
    echo [失败] 打包失败，请检查错误信息
)

pause
