    Complete-Binding -AgentData $agentData
    exit 0
}

# 确认绑定
if (-not $TestOnly) {
    Write-Host "确认绑定邮箱 $Email 到智能体 '$($agentData.name)'？" -ForegroundColor Yellow
    $confirm = Read-Host "输入 'yes' 继续，其他任意键取消"
    
    if ($confirm -ne "yes") {
        Write-Log "用户取消邮箱绑定" "INFO" $Color.Info
        Write-Host "邮箱绑定已取消" -ForegroundColor Yellow
        exit 0
    }
}

# 更新智能体邮箱
if (-not $TestOnly) {
    $updateResult = Update-Agent-Email -Email $Email
    
    if (-not $updateResult.Success) {
        Write-Log "邮箱更新失败" "ERROR" $Color.Error
        Write-Host "❌ 邮箱更新失败: $($updateResult.Error)" -ForegroundColor Red
        exit 1
    }
    
    $agentData = $updateResult.Agent
    Write-Log "邮箱更新成功" "INFO" $Color.Success
}

# 发送验证邮件
$verificationData = $null
if (-not $TestOnly) {
    $verificationResult = Send-Verification-Email -Email $Email
    
    if ($verificationResult.Success) {
        $verificationData = $verificationResult.Verification
        Write-Log "验证邮件发送成功" "INFO" $Color.Success
    } else {
        Write-Log "验证邮件发送失败: $($verificationResult.Error)" "WARNING" $Color.Warning
        Write-Host "⚠️  验证邮件发送失败，但邮箱已更新" -ForegroundColor Yellow
        Write-Host "   可以稍后手动请求验证邮件" -ForegroundColor Gray
    }
}

# 如果是测试模式，只检查状态
if ($TestOnly) {
    Write-Host ""
    Write-Host "🧪 测试模式完成" -ForegroundColor Green
    Write-Host "当前状态:" -ForegroundColor Cyan
    Write-Host "智能体: $($agentData.name)" -ForegroundColor Gray
    Write-Host "邮箱: $(if ($agentData.email) { $agentData.email } else { '未设置' })" -ForegroundColor Gray
    Write-Host "验证状态: $(if ($agentData.email_verified) { '✅ 已验证' } else { '❌ 未验证' })" -ForegroundColor Gray
    exit 0
}

# 等待用户验证
Write-Host ""
Write-Host "⏳ 等待邮箱验证..." -ForegroundColor Yellow
Write-Host "请检查邮箱 $Email 并点击验证链接" -ForegroundColor Cyan
Write-Host "验证后按任意键继续..." -ForegroundColor Gray

pause

# 检查验证状态
if ($verificationData) {
    Write-Host ""
    Write-Host "🔍 检查验证状态..." -ForegroundColor Yellow
    
    $statusResult = Check-Verification-Status -VerificationId $verificationData.verification_id
    
    if ($statusResult.Success -and $statusResult.Status.status -eq "verified") {
        Write-Host "✅ 邮箱验证成功！" -ForegroundColor Green
        
        # 重新获取智能体状态以确认
        $finalStatus = Get-Agent-Status
        if ($finalStatus.Success -and $finalStatus.Agent.email_verified) {
            Write-Host "🎉 邮箱绑定和验证全部完成！" -ForegroundColor Green
            $agentData = $finalStatus.Agent
        }
    } else {
        Write-Host "⚠️  邮箱验证状态: $(if ($statusResult.Success) { $statusResult.Status.status } else { '检查失败' })" -ForegroundColor Yellow
        Write-Host "   如果已验证，状态可能需要时间同步" -ForegroundColor Gray
    }
}

# 完成绑定流程
Complete-Binding -AgentData $agentData -VerificationData $verificationData

# 保存绑定记录
$recordDir = "$PSScriptRoot\email-binding-records"
if (-not (Test-Path $recordDir)) {
    New-Item -ItemType Directory -Path $recordDir -Force | Out-Null
}

$recordFile = "$recordDir\binding-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
@{
    binding = @{
        agent = @{
            id = $env:MOLTCN_AGENT_ID
            name = $agentData.name
            email = $agentData.email
            email_verified = $agentData.email_verified
        }
        verification = $verificationData
        bound_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
        success = $true
    }
} | ConvertTo-Json -Depth 5 | Out-File -FilePath $recordFile -Encoding UTF8

Write-Log "绑定记录已保存: $recordFile" "INFO" $Color.Info

Write-Host ""
Write-Host "✨ 邮箱绑定流程完成！" -ForegroundColor Green
Write-Host "请按照下一步行动的指引完成验证。" -ForegroundColor Cyan

exit 0