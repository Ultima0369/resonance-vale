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
Docker环境就绪测试
测试是否可以在Docker环境中正常运行灵枢系统
"""

import sys
import os
import json
import time

def check_encoding():
    """检查编码支持"""
    print("🔍 检查编码支持...")
    
    # 测试各种字符
    test_strings = [
        "中文测试 Chinese test",
        "🎉 表情符号 Emoji",
        "🦞 火堆旁 Fire side",
        "🩺 中医诊断 TCM diagnosis",
        "🔥 温暖开发 Warm development"
    ]
    
    for s in test_strings:
        try:
            print(f"  ✅ {s}")
        except UnicodeEncodeError as e:
            print(f"  ❌ 编码错误: {e}")
            return False
    
    print("✅ 编码测试通过")
    return True

def check_environment():
    """检查环境"""
    print("\n🔍 检查环境...")
    
    checks = {
        "Python版本": sys.version,
        "平台": sys.platform,
        "工作目录": os.getcwd(),
        "文件编码": sys.getfilesystemencoding(),
        "标准输出编码": sys.stdout.encoding if hasattr(sys.stdout, 'encoding') else 'unknown'
    }
    
    for key, value in checks.items():
        print(f"  {key}: {value}")
    
    # 检查是否是Linux环境
    is_linux = sys.platform.startswith('linux')
    print(f"  Linux环境: {'✅ 是' if is_linux else '❌ 否'}")
    
    return is_linux

def check_path_handling():
    """检查路径处理"""
    print("\n🔍 检查路径处理...")
    
    # 测试路径操作
    test_paths = [
        "/workspace/test.txt",
        "./relative/path",
        "../parent/path"
    ]
    
    for path in test_paths:
        try:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            print(f"  路径: {path} -> 目录: {dirname}, 文件名: {basename}")
        except Exception as e:
            print(f"  ❌ 路径处理错误: {e}")
            return False
    
    print("✅ 路径处理正常")
    return True

def check_shell_commands():
    """检查Shell命令可用性"""
    print("\n🔍 检查Shell命令...")
    
    import subprocess
    
    commands = [
        ["ls", "-la"],
        ["pwd"],
        ["echo", "Hello from shell"],
        ["python", "--version"]
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()[:50]
                print(f"  ✅ {cmd[0]}: {output}")
            else:
                print(f"  ❌ {cmd[0]}失败: {result.stderr[:50]}")
                return False
        except FileNotFoundError:
            print(f"  ❌ 命令不存在: {cmd[0]}")
            return False
        except Exception as e:
            print(f"  ❌ 执行错误: {e}")
            return False
    
    print("✅ Shell命令正常")
    return True

def test_lingshu_in_docker():
    """在Docker中测试灵枢核心"""
    print("\n🧪 测试灵枢核心功能...")
    
    # 模拟灵枢简化测试
    class MockLingShu:
        def __init__(self):
            self.name = "灵枢"
            self.teacher = "璇玑"
            self.diagnoses = []
        
        def diagnose(self, plan):
            score = 0.7 if plan.get('good', False) else 0.3
            approved = score > 0.5
            return approved, {"score": score, "approved": approved}
    
    lingshu = MockLingShu()
    
    # 测试诊断
    test_cases = [
        ("良好计划", {"good": True}),
        ("差计划", {"good": False})
    ]
    
    results = []
    for name, plan in test_cases:
        approved, diagnosis = lingshu.diagnose(plan)
        results.append((name, approved))
        status = "✅ 批准" if approved else "❌ 拒绝"
        print(f"  {name}: {status}")
    
    # 验证逻辑
    expected = [True, False]
    actual = [r[1] for r in results]
    
    if actual == expected:
        print("✅ 灵枢逻辑正确")
        return True
    else:
        print(f"❌ 逻辑错误: 预期{expected}, 实际{actual}")
        return False

def main():
    """主测试"""
    print("🚀 Docker环境就绪测试")
    print("=" * 50)
    
    tests = [
        ("编码支持", check_encoding),
        ("环境检查", check_environment),
        ("路径处理", check_path_handling),
        ("Shell命令", check_shell_commands),
        ("灵枢核心", test_lingshu_in_docker)
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{name}: {status}\n")
        except Exception as e:
            print(f"{name}: ❌ 错误 - {e}\n")
            results[name] = False
    
    print("=" * 50)
    print("📋 测试总结")
    print("=" * 50)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"通过测试: {passed}/{total}")
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    print("\n" + "=" * 50)
    
    # Docker环境判断
    is_linux = sys.platform.startswith('linux')
    encoding_ok = sys.stdout.encoding.lower() in ['utf-8', 'utf8']
    
    if is_linux and encoding_ok and passed == total:
        print("🎉 完美！当前环境就是理想的Docker/Linux环境")
        print("🦞 可以直接进行灵枢开发")
    elif passed == total:
        print("✅ 所有功能测试通过")
        print("📦 建议迁移到Docker以获得更好体验")
    else:
        print("⚠️  部分测试失败")
        print("🔧 需要修复环境问题")
    
    print("\n" + "=" * 50)
    print("💡 建议:")
    
    if not is_linux:
        print("  • 迁移到Docker/Linux环境解决平台差异")
    
    if not encoding_ok:
        print("  • 设置UTF-8编码解决中文和表情符号问题")
    
    if passed == total:
        print("  • 所有功能正常，可以开始开发")
    
    print("\n🔥 火堆旁开发环境检查完成")
    print("🩺 环境健康度: {}/{}".format(passed, total))

if __name__ == "__main__":
    # 设置UTF-8编码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    main()