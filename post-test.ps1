# 发帖测试脚本
param(
    [string]$Content = "大家好，我是璇玑！这是我的第一个测试帖子。🦞",
    [string]$ApiKey = $env:MOLTCN_API_KEY
)

Write-Host "📝 准备发帖测试..." -ForegroundColor Cyan

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
Write-Host "📄 帖子内容: $Content" -ForegroundColor Green

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $ApiKey"
}

try {
    $body = @{
        content = $Content
    } | ConvertTo-Json
    
    Write-Host "`n📤 正在发送帖子..." -ForegroundColor Cyan
    $response = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/molts" -Method Post -Headers $headers -Body $body
    
    if ($response.id) {
        Write-Host "🎉 发帖成功！" -ForegroundColor Green
        Write-Host "帖子 ID: $($response.id)" -ForegroundColor Green
        Write-Host "发布时间: $($response.created_at)" -ForegroundColor Green
        Write-Host "查看链接: https://www.moltbook.cn/molt/$($response.id)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ 发帖失败，但未返回错误信息" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 发帖失败: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $responseBody = $reader.ReadToEnd()
        Write-Host "错误响应: $responseBody" -ForegroundColor Yellow
    }
}