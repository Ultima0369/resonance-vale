#!/bin/bash
# 灵枢开发环境设置脚本
# 在Docker容器内运行

set -e  # 出错时退出

echo "🚀 设置灵枢开发环境"
echo "===================="

# 检查Python版本
echo "📦 检查Python环境..."
python --version
pip --version

# 安装项目依赖
echo "📦 安装Python依赖..."
pip install --user --no-cache-dir \
    pyyaml \
    pytest \
    black \
    flake8 \
    mypy

# 创建必要的目录
echo "📁 创建项目目录..."
mkdir -p lingshu/{config,diagnosis,prescriptions,fire_side}

# 设置Git（如果可用）
if command -v git &> /dev/null; then
    echo "🔧 配置Git..."
    git config --global user.name "灵枢开发者"
    git config --global user.email "lingshu@example.com"
    git config --global core.autocrlf input
    git config --global core.eol lf
fi

# 设置编码环境
echo "🔧 设置编码环境..."
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export PYTHONUTF8=1

# 创建测试脚本
echo "📝 创建测试脚本..."
cat > test_encoding.py << 'EOF'
#!/usr/bin/env python3
# 编码测试脚本

import sys
import io

# 强制UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("✅ UTF-8编码测试")
print("🎉 中文显示正常")
print("🔥 表情符号: 🦞 🎨 🧠")
print("🩺 灵枢系统编码正常")
EOF

# 运行测试
echo "🧪 运行编码测试..."
python test_encoding.py

# 创建开发别名
echo "🔧 设置开发别名..."
cat >> ~/.bashrc << 'EOF'

# 灵枢开发别名
alias ll='ls -la'
alias py='python'
alias pytest='python -m pytest'
alias black='python -m black'
alias flake8='python -m flake8'

# 项目特定命令
alias test-lingshu='python test_lingshu_ascii.py'
alias run-dev='cd /workspace && python -c "print(\"🚀 开发环境就绪\")"'

# 显示欢迎信息
echo "🦞 欢迎来到灵枢开发环境"
echo "📁 工作目录: /workspace"
echo "🐍 Python: $(python --version)"
echo "🔥 输入 'test-lingshu' 测试灵枢系统"
EOF

echo ""
echo "🎉 开发环境设置完成！"
echo "===================="
echo "📋 可用命令:"
echo "  test-lingshu    - 测试灵枢系统"
echo "  pytest          - 运行测试"
echo "  black .         - 格式化代码"
echo "  flake8 .        - 代码检查"
echo ""
echo "🔥 重新加载配置: source ~/.bashrc"
echo "🦞 开始开发吧！"