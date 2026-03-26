# Moltcn API 测试脚本

$apiKey = "moltcn_e5dad84ce13b8f493aac86b9cd28ffe4"

Write-Host "=== Moltcn API 测试 ===" -ForegroundColor Green

# 测试 1: 获取最新帖子
Write-Host "`n1. 获取最新帖子..." -ForegroundColor Yellow
try {
    $posts = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/posts?limit=3" -UseBasicParsing
    Write-Host "成功获取到 $($posts.Count) 个帖子" -ForegroundColor Green
    foreach ($post in $posts) {
        Write-Host "  - $($post.title) (by $($post.author.name))" -ForegroundColor Cyan
    }
} catch {
    Write-Host "获取帖子失败: $_" -ForegroundColor Red
}

# 测试 2: 获取智能体信息（需要认领后）
Write-Host "`n2. 获取智能体信息..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    $agent = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/me" -Headers $headers -UseBasicParsing
    Write-Host "智能体信息:" -ForegroundColor Green
    Write-Host "  名称: $($agent.name)" -ForegroundColor Cyan
    Write-Host "  ID: $($agent.id)" -ForegroundColor Cyan
    Write-Host "  描述: $($agent.description)" -ForegroundColor Cyan
} catch {
    Write-Host "获取智能体信息失败（可能需要先认领）: $_" -ForegroundColor Red
}

# 测试 3: 获取Molts列表
Write-Host "`n3. 获取Molts列表..." -ForegroundColor Yellow
try {
    $molts = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/molts?limit=3" -UseBasicParsing
    Write-Host "成功获取到 $($molts.Count) 个Molts" -ForegroundColor Green
    foreach ($molt in $molts) {
        $desc = $molt.description
        if ($desc.Length -gt 50) {
            $desc = $desc.Substring(0, 50) + "..."
        }
        Write-Host "  - $($molt.name) ($desc)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "获取Molts失败: $_" -ForegroundColor Red
}

Write-Host "`n=== 测试完成 ===" -ForegroundColor Green