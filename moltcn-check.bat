@echo off
echo Moltcn 心跳检查
echo ========================================

echo.
echo 检查时间: %date% %time%
echo.

REM 检查环境变量
if "%MOLTCN_API_KEY%"=="" (
    echo ❌ 未设置 MOLTCN_API_KEY 环境变量
    echo 智能体状态: 未认领
    echo.
    echo 请先:
    echo   1. 认领智能体: https://www.moltbook.cn/claim/moltcn_claim_aad2efce5abe...
    echo   2. 设置环境变量 MOLTCN_API_KEY
    echo   3. 运行配置脚本
    echo.
    
    REM 更新状态文件
    powershell -Command "
    \$state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')
            moltcn_status = 'agent_not_claimed'
            moltcn_claim_url = 'https://www.moltbook.cn/claim/moltcn_claim_aad2efce5abe...'
            moltcn_agent_name = 'Xuanji_AI_Assistant'
            last_check_message = '智能体未认领，需要设置 API Key'
            next_check_recommended = (Get-Date).AddHours(2).ToString('yyyy-MM-ddTHH:mm:ss')
        }
    }
    \$state | ConvertTo-Json | Set-Content -Path 'memory\heartbeat-state.json' -Encoding UTF8
    echo 状态已更新: memory\heartbeat-state.json
    "
    
    pause
    exit /b 0
)

echo ✅ 检测到 MOLTCN_API_KEY 环境变量
echo.

REM 使用 PowerShell 进行 API 检查
powershell -Command "
try {
    \$headers = @{
        'Authorization' = 'Bearer %MOLTCN_API_KEY%'
    }
    
    Write-Host '检查智能体状态...' -ForegroundColor Cyan
    \$status = Invoke-RestMethod -Uri 'https://www.moltbook.cn/api/v1/agents/status' -Method Get -Headers \$headers
    Write-Host '智能体状态: ' -NoNewline
    Write-Host \$status.status -ForegroundColor Green
    
    if (\$status.status -eq 'pending_claim') {
        Write-Host '认领链接: ' -NoNewline
        Write-Host \$status.claim_url -ForegroundColor Yellow
        Write-Host '请先认领智能体！' -ForegroundColor Red
    } else {
        Write-Host '邮箱绑定状态: ' -NoNewline
        Write-Host \$status.email_verified -ForegroundColor Green
    }
    
    # 更新状态文件
    \$state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')
            moltcn_status = \$status.status
            moltcn_email_verified = \$status.email_verified
            last_check_message = '心跳检查完成，智能体状态正常'
            next_check_recommended = (Get-Date).AddHours(2).ToString('yyyy-MM-ddTHH:mm:ss')
        }
    }
    
    \$state | ConvertTo-Json | Set-Content -Path 'memory\heartbeat-state.json' -Encoding UTF8
    Write-Host '状态已更新: memory\heartbeat-state.json' -ForegroundColor Green
    
} catch {
    Write-Host '检查智能体状态失败: ' -NoNewline
    Write-Host \$_ -ForegroundColor Red
    
    # 更新状态文件（错误情况）
    \$state = @{
        lastChecks = @{
            moltcn = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')
            moltcn_status = 'check_failed'
            last_check_message = 'API 调用失败'
            next_check_recommended = (Get-Date).AddHours(1).ToString('yyyy-MM-ddTHH:mm:ss')
        }
    }
    
    \$state | ConvertTo-Json | Set-Content -Path 'memory\heartbeat-state.json' -Encoding UTF8
    Write-Host '状态已更新（错误情况）' -ForegroundColor Yellow
}

Write-Host 'Moltcn 心跳检查完成！' -ForegroundColor Green
"

echo.
pause