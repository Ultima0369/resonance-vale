@echo off
echo 🦞 对话关键词保存到Obsidian
echo ========================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境正常

REM 检查依赖
echo.
echo 📦 检查脚本依赖...
if not exist "save_to_obsidian.py" (
    echo ❌ 找不到保存脚本: save_to_obsidian.py
    pause
    exit /b 1
)

echo ✅ 脚本文件正常

REM 检查Obsidian库
if not exist "D:\LDD\璇玑台" (
    echo ⚠️ Obsidian库不存在: D:\LDD\璇玑台
    echo 请检查Obsidian库路径是否正确
    set /p vault_path="请输入Obsidian库路径: "
    if "%vault_path%"=="" (
        echo ❌ 未提供库路径
        pause
        exit /b 1
    )
) else (
    set vault_path=D:\LDD\璇玑台
)

echo ✅ Obsidian库: %vault_path%

echo.
echo 📝 功能说明:
echo   1. 读取今天的对话记录
echo   2. 提取关键词和核心概念
echo   3. 创建Obsidian笔记
echo   4. 生成关键词索引
echo   5. 更新概念文件
echo.

set /p choice="是否现在运行? (y/n): "
if /i "%choice%" neq "y" (
    echo 取消运行
    pause
    exit /b 0
)

echo.
echo 🚀 开始保存对话到Obsidian...
python save_to_obsidian.py

echo.
echo 📋 生成的文件:
echo   对话记录文件夹: %vault_path%\对话记录
echo   关键词索引文件夹: %vault_path%\关键词索引
echo   概念文件夹: %vault_path%\概念
echo.
echo 💡 提示:
echo   1. 打开Obsidian查看生成的笔记
echo   2. 使用关键词索引快速查找概念
echo   3. 双击 .bat 文件可再次运行
echo.

pause