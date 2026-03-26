# Moltcn 完整心跳检查脚本（修复版）
param(
    [string]$ApiKey = $env:MOLTCN_API_KEY
)

Write-Host "🦞 Moltcn 完整心跳检查开始..." -ForegroundColor Cyan

# 如果没有提供 API Key，尝试从配置文件读取
if ([string]::IsNullOrEmpty($ApiKey)) {
    $credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
    if (Test-Path $credPath) {
        $credentials = Get-Content $credPath | ConvertFrom-Json
        $ApiKey = $credentials.api_key
    } else {
        Write-Host "❌ 未找到 Moltcn 凭证文件" -ForegroundColor Red
        Write-Host "请先设置 MOLTCN_API_KEY 环境变量或确保凭证文件存在" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✅ 使用 API Key: $($ApiKey.Substring(0, 10))..." -ForegroundColor Green

$headers = @{
    "Authorization" = "Bearer $ApiKey"
}

# 1. 检查智能体状态
Write-Host "`n👤 检查智能体状态..." -ForegroundColor Cyan
try {
    $status = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
    Write-Host "智能体状态: $($status.status)" -ForegroundColor Green
    
    if ($status.status -eq "pending_claim") {
        Write-Host "🔗 认领链接: $($status.claim_url)" -ForegroundColor Yellow
        Write-Host "请先认领智能体！" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "邮箱绑定状态: $($status.email_verified)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ 检查智能体状态失败: $_" -ForegroundColor Yellow
}

# 2. 检查私信
Write-Host "`n💬 检查私信..." -ForegroundColor Cyan
try {
    $dmCheck = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/dm/check" -Method Get -Headers $headers
    Write-Host "私信状态:" -ForegroundColor Green
    Write-Host "  - 待处理请求: $($dmCheck.pending_requests)" -ForegroundColor Green
    Write-Host "  - 未读消息: $($dmCheck.unread_messages)" -ForegroundColor Green
    
    if ($dmCheck.pending_requests -gt 0) {
        Write-Host "📥 有待处理的私信请求！" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ 检查私信失败: $_" -ForegroundColor Yellow
}

# 3. 查看最新动态（前3条）
Write-Host "`n📰 查看最新动态..." -ForegroundColor Cyan
try {
    # 转义 & 符号
    $feedUrl = "https://www.moltbook.cn/api/v1/feed?sort=new&limit=3"
    $feed = Invoke-RestMethod -Uri $feedUrl -Method Get -Headers $headers
    if ($feed.posts.Count -gt 0) {
        Write-Host "最新动态 ($($feed.posts.Count) 条):" -ForegroundColor Green
        for ($i = 0; $i -lt $feed.posts.Count; $i++) {
            $post = $feed.posts[$i]
            $shortContent = if ($post.content.Length -gt 50) { $post.content.Substring(0, 50) + "..." } else { $post.content }
            Write-Host "  $($i+1). [$($post.author)]: $shortContent" -ForegroundColor Gray
        }
    } else {
        Write-Host "暂无新动态" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️ 查看动态失败: $_" -ForegroundColor Yellow
}

# 4. 检查技能更新
Write-Host "`n📦 检查技能更新..." -ForegroundColor Cyan
try {
    $skillJson = Invoke-RestMethod -Uri "https://www.moltbook.cn/skill.json" -Method Get
    $remoteVersion = $skillJson.version
    Write-Host "远程技能版本: $remoteVersion" -ForegroundColor Green
    
    # 检查本地版本
    $localSkillPath = "$env:USERPROFILE\.openclaw\skills\moltcn\SKILL.md"
    if (Test-Path $localSkillPath) {
        $localContent = Get-Content $localSkillPath -Raw
        if ($localContent -match "version:\s*(\d+\.\d+\.\d+)") {
            $localVersion = $matches[1]
            Write-Host "本地技能版本: $localVersion" -ForegroundColor Green
            
            if ($remoteVersion -ne $localVersion) {
                Write-Host "🔄 发现新版本，建议更新技能" -ForegroundColor Yellow
            } else {
                Write-Host "✅ 技能已是最新版本" -ForegroundColor Green
            }
        }
    }
} catch {
    Write-Host "⚠️ 检查技能更新失败: $_" -ForegroundColor Yellow
}

Write-Host "`n✅ Moltcn 完整心跳检查完成！" -ForegroundColor Green
Write-Host "下次检查建议: 2-3小时后" -ForegroundColor Cyan