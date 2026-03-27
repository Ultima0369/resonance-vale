# PowerShell脚本启动Git Bash
Write-Host "🚀 启动Git Bash进行开发..." -ForegroundColor Green
Write-Host ""

# Git Bash路径
$gitBashPath = "C:\Program Files\Git\bin\bash.exe"

if (Test-Path $gitBashPath) {
    Write-Host "✅ 找到Git Bash: $gitBashPath" -ForegroundColor Green
    
    # 启动Git Bash
    Start-Process $gitBashPath -ArgumentList "--login" -NoNewWindow
    
    Write-Host ""
    Write-Host "💡 在Git Bash中，你可以:" -ForegroundColor Cyan
    Write-Host "   • 使用 ls, grep, find 等Unix命令"
    Write-Host "   • 运行 python test_lingshu_ascii.py"
    Write-Host "   • 正常显示中文和表情符号"
    Write-Host "   • 使用 /c/Users/lgdln/.openclaw/workspace 访问工作空间"
    
} else {
    Write-Host "❌ 未找到Git Bash，请安装Git for Windows" -ForegroundColor Red
    Write-Host "下载地址: https://gitforwindows.org/" -ForegroundColor Yellow
}