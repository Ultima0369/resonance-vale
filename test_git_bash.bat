@echo off
REM 测试Git Bash环境的批处理文件
echo 测试Git Bash环境...
echo.

REM 启动Git Bash并运行测试
"C:\Program Files\Git\bin\bash.exe" -c "
echo '🚀 Git Bash环境测试'
echo '==================='
echo ''
echo '1. 基本命令测试:'
echo '   当前目录:'
pwd
echo ''
echo '   目录列表:'
ls -la
echo ''
echo '2. 编码测试:'
echo '   ✅ 中文测试'
echo '   🎉 表情符号'
echo '   🦞 灵枢系统'
echo ''
echo '3. Python测试:'
python --version
echo ''
echo '4. 运行灵枢测试:'
cd /c/Users/lgdln/.openclaw/workspace
python test_lingshu_ascii.py
echo ''
echo '🔥 测试完成'
"