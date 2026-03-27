#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
确保UTF-8编码的脚本头
"""

import sys
import io

# 强制UTF-8编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
快速Docker测试 - 验证基本功能
"""

import sys
import os

# 设置UTF-8编码
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

print("🚀 快速Docker环境测试")
print("=" * 40)

# 测试1: 基本Python功能
print("1. Python基本信息:")
print(f"   版本: {sys.version}")
print(f"   平台: {sys.platform}")
print(f"   编码: {sys.getdefaultencoding()}")

# 测试2: 文件系统
print("\n2. 文件系统测试:")
workspace = os.getcwd()
print(f"   工作目录: {workspace}")
print(f"   目录存在: {os.path.exists(workspace)}")

# 列出关键文件
key_files = ["Dockerfile", "docker-compose.yml", "lingshu", "autoresearch"]
for file in key_files:
    exists = os.path.exists(os.path.join(workspace, file))
    print(f"   {file}: {'✅ 存在' if exists else '❌ 缺失'}")

# 测试3: 编码测试
print("\n3. 编码测试:")
test_texts = [
    "中文测试",
    "🎉 Docker环境",
    "🦞 灵枢系统",
    "🔥 火堆旁开发"
]

for text in test_texts:
    try:
        print(f"   ✅ {text}")
    except UnicodeEncodeError:
        print(f"   ❌ 编码错误: {text}")

# 测试4: 路径测试
print("\n4. 路径测试:")
test_path = os.path.join(workspace, "lingshu", "config", "identity.yaml")
print(f"   灵枢身份文件: {test_path}")
print(f"   文件存在: {os.path.exists(test_path)}")

print("\n" + "=" * 40)
print("📋 测试完成")
print("💡 如果看到所有✅，环境基本正常")
print("🐳 等待Docker镜像构建完成...")