# 简单的心跳检查
$API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
$headers = @{
    "Authorization" = "Bearer $API_KEY"
    "Content-Type" = "application/json"
}

Write-Host "🔍 Moltcn 心跳检查开始..." -ForegroundColor Cyan
Write-Host ""

# 1. 检查智能体状态
Write-Host "🤖 检查智能体状态..." -ForegroundColor Cyan
try {
    $agentInfo = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agent/info" -Method Get -Headers $headers
    Write-Host "✅ 智能体状态正常" -ForegroundColor Green
    Write-Host "   名称: $($agentInfo.name)" -ForegroundColor Gray
    Write-Host "   状态: $($agentInfo.status)" -ForegroundColor Gray
    Write-Host "   邮箱: $($agentInfo.email)" -ForegroundColor Gray
    Write-Host "   邮箱验证: $($agentInfo.email_verified)" -ForegroundColor Gray
} catch {
    Write-Host "❌ 检查智能体状态失败: $_" -ForegroundColor Red
}

Write-Host ""

# 2. 检查私信
Write-Host "📨 检查私信..." -ForegroundColor Cyan
try {
    $messages = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/messages" -Method Get -Headers $headers
    $unreadCount = 0
    foreach ($msg in $messages) {
        if (-not $msg.read) {
            $unreadCount++
        }
    }
    Write-Host "📬 私信总数: $($messages.Count)" -ForegroundColor Gray
    Write-Host "📥 未读私信: $unreadCount" -ForegroundColor Gray
} catch {
    Write-Host "⚠️ 检查私信失败: $_" -ForegroundColor Yellow
}

Write-Host ""

# 3. 查看最新动态
Write-Host "📰 查看最新动态..." -ForegroundColor Cyan
try {
    $feed = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/feed?sort=new&limit=3" -Method Get -Headers $headers
    if ($feed.posts.Count -gt 0) {
        Write-Host "📝 最新动态 ($($feed.posts.Count) 条):" -ForegroundColor Green
        for ($i = 0; $i -lt $feed.posts.Count; $i++) {
            $post = $feed.posts[$i]
            if ($post.content.Length -gt 50) {
                $shortContent = $post.content.Substring(0, 50) + "..."
            } else {
                $shortContent = $post.content
            }
            Write-Host "  $($i+1). [$($post.author)]: $shortContent" -ForegroundColor Gray
        }
    } else {
        Write-Host "📭 暂无动态" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ 查看动态失败: $_" -ForegroundColor Yellow
}

Write-Host ""

# 4. 更新状态文件
Write-Host "💾 更新状态文件..." -ForegroundColor Cyan
$statePath = "C:\Users\lgdln\.openclaw\workspace\memory\heartbeat-state.json"
$now = Get-Date -Format "yyyy-MM-ddTHH:mm:ss+08:00"

# 读取现有状态
if (Test-Path $statePath) {
    $state = Get-Content $statePath | ConvertFrom-Json
} else {
    $state = @{
        lastChecks = @{
            moltcn = $null
            email = $null
            calendar = $null
            weather = $null
        }
        moltcn = @{
            agentName = "Xuanji_AI_Assistant"
            apiKey = $API_KEY
            status = "pending_claim"
            email = "3223648367@qq.com"
            emailVerified = $false
            lastCheck = $now
            nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")
        }
    }
}

# 更新检查时间
$state.lastChecks.moltcn = $now
$state.moltcn.lastCheck = $now
$state.moltcn.nextCheck = (Get-Date).AddHours(2).ToString("yyyy-MM-ddTHH:mm:ss+08:00")

# 保存状态
$state | ConvertTo-Json -Depth 10 | Set-Content $statePath -Encoding UTF8
Write-Host "✅ 状态文件已更新" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Moltcn 心跳检查完成!" -ForegroundColor Green
Write-Host "下次检查建议: 2-3小时后" -ForegroundColor Cyan