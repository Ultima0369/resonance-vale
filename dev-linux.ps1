# PowerShell脚本：启动Linux开发环境
Write-Host "🚀 启动灵枢Linux开发环境" -ForegroundColor Green
Write-Host "=" * 50

# 检查Docker
Write-Host "🔍 检查Docker状态..." -ForegroundColor Cyan
docker --version
docker ps

Write-Host ""
Write-Host "💡 选择开发方式:" -ForegroundColor Yellow
Write-Host "1. 交互式Shell (推荐)" -ForegroundColor White
Write-Host "2. 运行灵枢测试" -ForegroundColor White
Write-Host "3. 启动Docker Compose环境" -ForegroundColor White
Write-Host "4. 退出" -ForegroundColor White

$choice = Read-Host "请输入选择 (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🐳 启动交互式Shell..." -ForegroundColor Green
        docker run -it --rm `
          -v ${PWD}:/workspace `
          -w /workspace `
          python:3.11-alpine `
          sh
    }
    "2" {
        Write-Host "🧪 运行灵枢测试..." -ForegroundColor Green
        docker run --rm `
          -v ${PWD}:/workspace `
          -w /workspace `
          python:3.11-alpine `
          sh -c "cd autoresearch && python test_lingshu_ascii.py"
    }
    "3" {
        Write-Host "📦 启动Docker Compose..." -ForegroundColor Green
        docker-compose -f docker-simple.yml up
    }
    "4" {
        Write-Host "👋 退出" -ForegroundColor Cyan
    }
    default {
        Write-Host "❌ 无效选择" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔥 火堆旁Linux开发环境就绪" -ForegroundColor Green
Write-Host "🦞 灵枢在纯净的Linux环境中运行" -ForegroundColor Cyan