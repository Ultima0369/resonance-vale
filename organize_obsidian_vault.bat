@echo off
echo 璇玑 - Obsidian 仓库整理工具
echo ========================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo Python环境正常

REM 检查脚本
if not exist "organize_obsidian_vault.py" (
    echo 找不到整理脚本: organize_obsidian_vault.py
    pause
    exit /b 1
)

echo.
echo 功能说明:
echo   1. 分析当前仓库结构
echo   2. 创建备份
echo   3. 创建新的文件夹结构
echo   4. 整理文件到新结构
echo   5. 更新内部链接
echo   6. 创建索引页面
echo.

echo 请选择操作模式:
echo   1. 模拟运行 (只显示整理计划，不实际移动文件)
echo   2. 实际运行 (执行所有整理操作)
echo   3. 仅创建文件夹结构
echo   4. 仅创建索引页面
echo.

set /p mode="请输入选项 (1-4): "

if "%mode%"=="1" (
    echo.
    echo 模拟运行模式...
    python organize_obsidian_vault.py --dry-run
) else if "%mode%"=="2" (
    echo.
    echo 实际运行模式...
    echo 警告: 这将实际移动文件，请确保已备份！
    set /p confirm="确认执行? (输入 yes 继续): "
    if /i "%confirm%" neq "yes" (
        echo 取消运行
        pause
        exit /b 0
    )
    python organize_obsidian_vault.py --real-run
) else if "%mode%"=="3" (
    echo.
    echo 仅创建文件夹结构...
    python organize_obsidian_vault.py --create-folders
) else if "%mode%"=="4" (
    echo.
    echo 仅创建索引页面...
    python organize_obsidian_vault.py --create-index
) else (
    echo 无效选项
    pause
    exit /b 1
)

echo.
echo 操作完成！
echo.
echo 提示:
echo   1. 打开Obsidian查看新的文件夹结构
echo   2. 检查主页索引和标签索引
echo   3. 如有问题，可从备份恢复
echo.

pause