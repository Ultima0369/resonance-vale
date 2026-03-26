@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🦞 认知切片论保存工具
echo ========================================
echo.

color 0A

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo ✅ Python环境正常

REM 检查整合版文档
if not exist "认知切片论-整合版.md" (
    echo ❌ 错误: 未找到整合版文档
    echo 请先创建"认知切片论-整合版.md"
    pause
    exit /b 1
)

echo ✅ 找到整合版文档

REM 检查Obsidian库
if not exist "D:\LDD\璇玑台" (
    echo ⚠️ 警告: 未找到Obsidian库
    echo 默认路径: D:\LDD\璇玑台
    echo.
    set /p custom_path="请输入Obsidian库路径: "
    if not "%custom_path%"=="" (
        if not exist "%custom_path%" (
            echo ❌ 错误: 路径不存在
            pause
            exit /b 1
        )
        set VAULT_PATH=%custom_path%
    ) else (
        echo ❌ 错误: 必须提供有效的Obsidian库路径
        pause
        exit /b 1
    )
) else (
    set VAULT_PATH=D:\LDD\璇玑台
    echo ✅ Obsidian库: %VAULT_PATH%
)

echo.
echo 📋 保存选项:
echo   1. 完整保存（推荐）
echo   2. 仅保存主文档
echo   3. 仅更新概念文件
echo   4. 查看生成的文件
echo   5. 退出
echo.

:menu
set /p choice="请选择 (1-5): "

if "%choice%"=="1" goto full_save
if "%choice%"=="2" goto main_only
if "%choice%"=="3" goto concepts_only
if "%choice%"=="4" goto view_files
if "%choice%"=="5" goto exit_program

echo ❌ 无效选择
goto menu

:full_save
echo.
echo 🚀 开始完整保存...
python save_cognitive_slice_to_obsidian.py
echo.
pause
goto menu

:main_only
echo.
echo 📄 仅保存主文档...
python -c "
import os
from pathlib import Path
vault = Path(r'%VAULT_PATH%')
project_folder = vault / '项目' / '认知切片论'
project_folder.mkdir(parents=True, exist_ok=True)
with open('认知切片论-整合版.md', 'r', encoding='utf-8') as f:
    content = f.read()
with open(project_folder / '认知切片论-整合版.md', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'✅ 主文档已保存到: {project_folder / \"认知切片论-整合版.md\"}')
"
echo.
pause
goto menu

:concepts_only
echo.
echo 🔗 更新概念文件...
python -c "
import re
from pathlib import Path
vault = Path(r'%VAULT_PATH%')
concept_folder = vault / '概念'
concept_folder.mkdir(exist_ok=True)
with open('认知切片论-整合版.md', 'r', encoding='utf-8') as f:
    content = f.read()
concepts = re.findall(r'\[\[(.*?)\]\]', content)
unique_concepts = list(set(concepts))
updated = []
for concept in unique_concepts:
    if concept.strip():
        concept_file = concept_folder / f'{concept}.md'
        if concept_file.exists():
            with open(concept_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            if '[[认知切片论-整合版]]' not in existing:
                with open(concept_file, 'a', encoding='utf-8') as f:
                    f.write('\\n- [[认知切片论-整合版]]\\n')
                updated.append(concept)
print(f'✅ 更新了 {len(updated)} 个概念文件')
"
echo.
pause
goto menu

:view_files
echo.
echo 📁 生成的文件结构:
echo.
if exist "%VAULT_PATH%\项目\认知切片论" (
    echo 项目文件夹: %VAULT_PATH%\项目\认知切片论
    echo.
    dir "%VAULT_PATH%\项目\认知切片论" /b
    echo.
    if exist "%VAULT_PATH%\项目\认知切片论\章节" (
        echo 章节文件夹:
        dir "%VAULT_PATH%\项目\认知切片论\章节" /b
    )
) else (
    echo 项目文件夹尚未创建
)
echo.
pause
goto menu

:exit_program
echo.
echo 👋 感谢使用认知切片论保存工具
echo 🦞 再见！
timeout /t 2 >nul
exit /b 0