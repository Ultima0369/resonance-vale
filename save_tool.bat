@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Save Tool for Cognitive Slice Theory
echo ========================================
echo.

REM Check Python
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo Python environment OK

REM Check document
if not exist "cognitive_slice_integrated.md" (
    echo ERROR: Document not found
    echo Looking for: cognitive_slice_integrated.md
    pause
    exit /b 1
)

echo Document found

REM Check Obsidian vault
set VAULT_PATH=D:\LDD\xuanjital
if not exist "%VAULT_PATH%" (
    echo WARNING: Obsidian vault not found
    echo Default path: %VAULT_PATH%
    echo.
    set /p CUSTOM_PATH=Enter Obsidian vault path: 
    if not "!CUSTOM_PATH!"=="" (
        if not exist "!CUSTOM_PATH!" (
            echo ERROR: Path does not exist
            pause
            exit /b 1
        )
        set VAULT_PATH=!CUSTOM_PATH!
    ) else (
        echo ERROR: Valid Obsidian vault path required
        pause
        exit /b 1
    )
)

echo Obsidian vault: %VAULT_PATH%

echo.
echo Options:
echo   1. Run full save script
echo   2. Exit
echo.

:menu
set /p CHOICE=Choose (1-2): 

if "%CHOICE%"=="1" goto run_script
if "%CHOICE%"=="2" goto exit_program

echo Invalid choice
goto menu

:run_script
echo.
echo Running save script...
python save_cognitive_slice_to_obsidian.py
echo.
echo Script completed!
pause
goto menu

:exit_program
echo.
echo Goodbye!
timeout /t 2 >nul
exit /b 0