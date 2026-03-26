@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🦞 璇玑的Obsidian对话保存工具
echo ========================================
echo.

REM 设置颜色
color 0A

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo ✅ Python环境正常

REM 检查Obsidian库
if not exist "D:\LDD\璇玑台" (
    echo ⚠️ 警告: 未找到Obsidian库
    echo 默认路径: D:\LDD\璇玑台
    echo.
    set /p custom_path="请输入Obsidian库路径 (直接回车使用默认): "
    if not "%custom_path%"=="" (
        if not exist "%custom_path%" (
            echo ❌ 错误: 路径不存在
            pause
            exit /b 1
        )
        set VAULT_PATH=%custom_path%
    ) else (
        echo ❌ 错误: 必须提供有效的Obsidian库路径
        pause
        exit /b 1
    )
) else (
    set VAULT_PATH=D:\LDD\璇玑台
    echo ✅ Obsidian库: %VAULT_PATH%
)

echo.
echo 📋 可用功能:
echo   1. 保存今日对话到Obsidian
echo   2. 查看已保存的对话
echo   3. 打开Obsidian库
echo   4. 退出
echo.

:menu
set /p choice="请选择功能 (1-4): "

if "%choice%"=="1" goto save_today
if "%choice%"=="2" goto view_saved
if "%choice%"=="3" goto open_vault
if "%choice%"=="4" goto exit_program

echo ❌ 无效选择，请重新输入
goto menu

:save_today
echo.
echo 🚀 正在保存今日对话...
python obsidian_quick_save.py
echo.
echo 📝 保存完成！
echo.
pause
goto menu

:view_saved
echo.
echo 📁 已保存的对话:
echo.
if exist "%VAULT_PATH%\对话记录" (
    dir "%VAULT_PATH%\对话记录\*.md" /b /od
) else (
    echo 暂无对话记录
)
echo.
pause
goto menu

:open_vault
echo.
echo 📂 正在打开Obsidian库...
if exist "%VAULT_PATH%" (
    explorer "%VAULT_PATH%"
    echo ✅ 已打开库文件夹
) else (
    echo ❌ 无法打开库文件夹
)
echo.
pause
goto menu

:exit_program
echo.
echo 👋 感谢使用璇玑的Obsidian保存工具
echo 🦞 再见！
timeout /t 2 >nul
exit /b 0