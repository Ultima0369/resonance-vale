#!/bin/bash
# Docker测试脚本

echo "🚀 Docker灵枢测试"
echo "===================="

# 运行测试
docker run --rm \
  -v "$(pwd):/workspace" \
  -w /workspace \
  python:3.11-alpine \
  sh -c "
    echo '📦 环境信息:' &&
    python --version &&
    echo '' &&
    echo '📁 工作目录内容:' &&
    ls -la &&
    echo '' &&
    echo '🧪 运行灵枢测试:' &&
    python test_lingshu_ascii.py
  "