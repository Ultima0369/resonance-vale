#!/usr/bin/env python3
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
