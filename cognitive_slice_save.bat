@echo off
REM 设置代码页为UTF-8
chcp 65001 >nul

echo.
echo ========================================
echo Cognitive Slice Theory Save Tool
echo ========================================
echo.

REM 检查Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo Python environment OK

REM 检查文档
if not exist "认知切片论-整合版.md" (
    echo ERROR: Document not found
    echo Please create "认知切片论-整合版.md" first
    pause
    exit /b 1
)

echo Document found

REM 检查Obsidian库
set VAULT_PATH=D:\LDD\璇玑台
if not exist "%VAULT_PATH%" (
    echo WARNING: Obsidian vault not found
    echo Default path: %VAULT_PATH%
    echo.
    set /p CUSTOM_PATH=Enter Obsidian vault path: 
    if not "%CUSTOM_PATH%"=="" (
        if not exist "%CUSTOM_PATH%" (
            echo ERROR: Path does not exist
            pause
            exit /b 1
        )
        set VAULT_PATH=%CUSTOM_PATH%
    ) else (
        echo ERROR: Valid Obsidian vault path required
        pause
        exit /b 1
    )
)

echo Obsidian vault: %VAULT_PATH%

echo.
echo Options:
echo   1. Full save (recommended)
echo   2. Save main document only
echo   3. Update concept files only
echo   4. View saved files
echo   5. Exit
echo.

:menu
set /p CHOICE=Choose (1-5): 

if "%CHOICE%"=="1" goto full_save
if "%CHOICE%"=="2" goto main_only
if "%CHOICE%"=="3" goto concepts_only
if "%CHOICE%"=="4" goto view_files
if "%CHOICE%"=="5" goto exit_program

echo Invalid choice
goto menu

:full_save
echo.
echo Starting full save...
python save_cognitive_slice_to_obsidian.py
echo.
echo Save completed!
pause
goto menu

:main_only
echo.
echo Saving main document only...
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
print('Main document saved to:', str(project_folder / '认知切片论-整合版.md'))
"
echo.
pause
goto menu

:concepts_only
echo.
echo Updating concept files...
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
                    f.write('\n- [[认知切片论-整合版]]\n')
                updated.append(concept)
print(f'Updated {len(updated)} concept files')
"
echo.
pause
goto menu

:view_files
echo.
echo File structure:
echo.
if exist "%VAULT_PATH%\项目\认知切片论" (
    echo Project folder: %VAULT_PATH%\项目\认知切片论
    echo.
    dir "%VAULT_PATH%\项目\认知切片论" /b
    echo.
    if exist "%VAULT_PATH%\项目\认知切片论\章节" (
        echo Chapters folder:
        dir "%VAULT_PATH%\项目\认知切片论\章节" /b
    )
) else (
    echo Project folder not created yet
)
echo.
pause
goto menu

:exit_program
echo.
echo Thank you for using Cognitive Slice Theory Save Tool
echo Goodbye!
timeout /t 2 >nul
exit /b 0