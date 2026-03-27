#!/bin/bash
# 带超时的 Git 推送脚本

echo "🚀 尝试推送到 GitHub..."
echo "仓库: https://github.com/Ultima0369/resonance-vale"

# 设置超时（30秒）
timeout 30 git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功!"
    echo "访问: https://github.com/Ultima0369/resonance-vale"
elif [ $? -eq 124 ]; then
    echo "⏰ 推送超时（30秒）"
    echo "可能的原因:"
    echo "  1. 网络连接慢"
    echo "  2. 仓库太大"
    echo "  3. GitHub 服务器响应慢"
else
    echo "❌ 推送失败"
    echo "错误代码: $?"
fi