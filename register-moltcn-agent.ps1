   浏览: https://www.moltbook.cn" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "🔧 可用命令:" -ForegroundColor Yellow
    Write-Host "• 测试连接: .\test-moltcn-connection.ps1" -ForegroundColor Gray
    Write-Host "• 发送心跳: .\moltcn-heartbeat.ps1" -ForegroundColor Gray
    Write-Host "• 监控任务: .\monitor-heartbeat-task.ps1" -ForegroundColor Gray
    Write-Host "• 查看配置: Get-Content $ConfigFile | ConvertFrom-Json" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "📚 参考文档:" -ForegroundColor Yellow
    Write-Host "• Moltcn技能文档: https://www.moltbook.cn/skill.md" -ForegroundColor Gray
    Write-Host "• 心跳设置文档: https://www.moltbook.cn/heartbeat-settings.md" -ForegroundColor Gray
    Write-Host "• OpenClaw文档: https://docs.openclaw.ai" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "💡 提示:" -ForegroundColor Cyan
    Write-Host "• 保存好API Key，不要泄露" -ForegroundColor Gray
    Write-Host "• 定期检查智能体状态" -ForegroundColor Gray
    Write-Host "• 参与社区互动，增加活跃度" -ForegroundColor Gray
    
    Write-Host "=" * 50
}

# 主程序
Write-Host "🤖 Moltcn智能体注册脚本 v$SCRIPT_VERSION" -ForegroundColor Cyan
Write-Host "=" * 50

# 显示注册信息
Write-Host "注册信息:" -ForegroundColor Yellow
Write-Host "智能体名称: $AgentName" -ForegroundColor Gray
Write-Host "描述: $AgentDescription" -ForegroundColor Gray
Write-Host "邮箱: $Email" -ForegroundColor Gray
Write-Host ""

# 确认注册
Write-Host "确认注册？" -ForegroundColor Yellow
$confirm = Read-Host "输入 'yes' 继续，其他任意键取消"

if ($confirm -ne "yes") {
    Write-Log "用户取消注册" "INFO" $Color.Info
    Write-Host "注册已取消" -ForegroundColor Yellow
    exit 0
}

# 检查要求
if (-not (Test-Requirements)) {
    Write-Log "系统要求检查失败" "ERROR" $Color.Error
    Write-Host "❌ 系统要求检查失败，请查看日志" -ForegroundColor Red
    exit 1
}

# 注册智能体
$registrationResult = Register-Agent -Name $AgentName -Description $AgentDescription -Email $Email

if (-not $registrationResult.Success) {
    Write-Log "智能体注册失败" "ERROR" $Color.Error
    Write-Host "❌ 智能体注册失败: $($registrationResult.Error)" -ForegroundColor Red
    exit 1
}

$agentData = $registrationResult.Agent

# 保存配置
$configFile = Save-Agent-Config -AgentData $agentData

# 测试连接
$connectionResult = Test-Agent-Connection -AgentData $agentData

if (-not $connectionResult.Success) {
    Write-Log "连接测试失败，但配置已保存" "WARNING" $Color.Warning
} else {
    Write-Log "连接测试成功" "INFO" $Color.Success
}

# 尝试发送欢迎帖子
$postResult = Send-Welcome-Post -AgentData $agentData

if ($postResult.Success) {
    Write-Log "欢迎帖子发送成功" "INFO" $Color.Success
} else {
    Write-Log "欢迎帖子发送失败: $($postResult.Error)" "WARNING" $Color.Warning
}

# 完成注册
Complete-Registration -AgentData $agentData -ConfigFile $configFile

# 保存注册记录
$recordDir = "$PSScriptRoot\registration-records"
if (-not (Test-Path $recordDir)) {
    New-Item -ItemType Directory -Path $recordDir -Force | Out-Null
}

$recordFile = "$recordDir\registration-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
@{
    registration = @{
        agent = $agentData
        config_file = $configFile
        registered_at = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
        success = $true
    }
} | ConvertTo-Json -Depth 5 | Out-File -FilePath $recordFile -Encoding UTF8

Write-Log "注册记录已保存: $recordFile" "INFO" $Color.Info

Write-Host ""
Write-Host "✨ 注册流程完成！" -ForegroundColor Green
Write-Host "请按照下一步行动的指引继续配置。" -ForegroundColor Cyan

exit 0