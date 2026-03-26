@echo off
echo 🦞 启动认知切片论深度共创环境
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
echo 📦 检查依赖包...
pip list | findstr requests >nul
if errorlevel 1 (
    echo ⚠️ 缺少requests包，正在安装...
    pip install requests
) else (
    echo ✅ requests已安装
)

echo.
echo 🎯 配置说明：
echo 1. 你需要一个DeepSeek API Key
echo 2. 可以从 https://platform.deepseek.com/api_keys 获取
echo 3. 首次运行会提示输入API Key
echo.
echo 📝 对话模式：
echo   /phase1 - 灵感碰撞（快速产生想法）
echo   /phase2 - 深度探索（深入探讨概念）- 默认
echo   /phase3 - 整理输出（系统化论述）
echo   /save   - 保存对话记录
echo   /stats  - 查看统计信息
echo   /exit   - 退出
echo.
echo 🧠 特别功能：
echo   - 自动检测对话阶段
echo   - 切片自觉提醒
echo   - 具象比喻提取
echo   - 对话统计
echo.

set /p choice="是否现在启动? (y/n): "
if /i "%choice%" neq "y" (
    echo 取消启动
    pause
    exit /b 0
)

echo.
echo 🚀 启动认知切片论深度共创...
python cognitive_slice_config.py

echo.
echo 💾 对话记录已保存到当前目录
echo 🦞 感谢使用认知切片论深度共创工具！
pause