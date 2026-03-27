#!/usr/bin/env python3
"""
Windows编码修复工具
解决GBK编码导致的UnicodeEncodeError问题
"""

import sys
import io
import os

def setup_utf8_environment():
    """设置UTF-8编码环境"""
    print("🔧 设置UTF-8编码环境...")
    
    # 方法1: 重新配置标准输出
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        print("✅ 使用reconfigure方法")
    else:
        # 方法2: 包装标准输出
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        print("✅ 使用TextIOWrapper方法")
    
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    return True

def test_encoding():
    """测试编码是否正常"""
    print("\n🧪 编码测试...")
    
    test_cases = [
        "中文测试",
        "🎉 表情符号",
        "🦞 灵枢系统", 
        "🔥 火堆旁开发",
        "🩺 中医伦理诊断",
        "璇玑 → 灵枢 → autoresearch"
    ]
    
    success = True
    for text in test_cases:
        try:
            print(f"  ✅ {text}")
        except UnicodeEncodeError as e:
            print(f"  ❌ 错误: {text} - {e}")
            success = False
    
    return success

def create_utf8_wrapper():
    """创建UTF-8包装脚本"""
    print("\n📝 创建UTF-8包装脚本...")
    
    wrapper_content = '''#!/usr/bin/env python3
"""
UTF-8包装脚本 - 确保所有Python脚本使用UTF-8编码
"""

import sys
import io
import os
import subprocess

def main():
    # 设置UTF-8环境
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 获取要运行的脚本
    if len(sys.argv) < 2:
        print("用法: python utf8_wrapper.py <script.py> [args...]")
        return 1
    
    script = sys.argv[1]
    args = sys.argv[2:]
    
    # 运行原始脚本
    cmd = [sys.executable, script] + args
    result = subprocess.run(cmd, capture_output=False)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open('utf8_wrapper.py', 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    print("✅ 创建了 utf8_wrapper.py")
    print("   用法: python utf8_wrapper.py your_script.py")
    
    return True

def update_existing_scripts():
    """更新现有脚本的编码设置"""
    print("\n📝 更新现有脚本...")
    
    scripts_to_update = [
        'test_lingshu_ascii.py',
        'quick_docker_test.py',
        'test_docker_ready.py'
    ]
    
    encoding_header = '''#!/usr/bin/env python3
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
'''
    
    updated_count = 0
    for script in scripts_to_update:
        if os.path.exists(script):
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否已经有编码声明
                if '# -*- coding: utf-8 -*-' not in content:
                    # 在shebang后插入编码声明
                    lines = content.split('\n')
                    new_lines = []
                    for i, line in enumerate(lines):
                        new_lines.append(line)
                        if line.startswith('#!/usr/bin/env python3') and i == 0:
                            new_lines.append('# -*- coding: utf-8 -*-')
                            new_lines.append('')
                            new_lines.append(encoding_header)
                    
                    new_content = '\n'.join(new_lines)
                    
                    with open(script, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"  ✅ 更新了 {script}")
                    updated_count += 1
                else:
                    print(f"  ⏭️  {script} 已有编码声明")
                    
            except Exception as e:
                print(f"  ❌ 更新 {script} 失败: {e}")
    
    return updated_count

def main():
    """主函数"""
    print("🚀 Windows编码修复工具")
    print("=" * 50)
    
    # 1. 设置当前环境
    setup_utf8_environment()
    
    # 2. 测试当前环境
    encoding_ok = test_encoding()
    
    if not encoding_ok:
        print("\n⚠️  编码测试失败，需要进一步修复")
    
    # 3. 创建包装脚本
    create_utf8_wrapper()
    
    # 4. 更新现有脚本
    updated = update_existing_scripts()
    
    print("\n" + "=" * 50)
    print("📋 修复完成总结")
    print("=" * 50)
    
    if encoding_ok:
        print("✅ 当前环境编码正常")
    else:
        print("⚠️  当前环境仍有编码问题")
    
    print(f"✅ 创建了UTF-8包装脚本")
    print(f"✅ 更新了 {updated} 个现有脚本")
    
    print("\n💡 使用建议:")
    print("1. 运行脚本时使用: python utf8_wrapper.py your_script.py")
    print("2. 或直接在脚本开头添加编码设置")
    print("3. 长期方案: 迁移到Docker/Linux环境")
    
    print("\n🔥 火堆旁编码修复完成")
    print("🦞 现在可以正常显示中文和表情符号了")

if __name__ == "__main__":
    # 先设置当前脚本的编码
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    main()