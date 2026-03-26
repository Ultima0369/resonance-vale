# 邮箱绑定脚本
param(
    [Parameter(Mandatory=$true)]
    [string]$Email,
    
    [string]$ApiKey = $env:MOLTCN_API_KEY
)

Write-Host "📧 开始邮箱绑定流程..." -ForegroundColor Cyan

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
Write-Host "📧 绑定邮箱: $Email" -ForegroundColor Green

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $ApiKey"
}

# 第一步：请求发送验证码
Write-Host "`n📤 请求发送验证码到 $Email ..." -ForegroundColor Cyan
try {
    $body = @{
        email = $Email
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/me/verify-email" -Method Post -Headers $headers -Body $body
    
    if ($response.success) {
        Write-Host "✅ 验证码已发送到 $Email" -ForegroundColor Green
        Write-Host "请检查邮箱（包括垃圾邮件文件夹）获取验证码" -ForegroundColor Yellow
    } else {
        Write-Host "❌ 发送验证码失败: $($response.error)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ 请求发送验证码失败: $_" -ForegroundColor Red
    exit 1
}

# 等待用户输入验证码
Write-Host "`n⌨️ 请输入收到的验证码：" -ForegroundColor Cyan
$verificationCode = Read-Host "验证码"

if ([string]::IsNullOrEmpty($verificationCode)) {
    Write-Host "❌ 验证码不能为空" -ForegroundColor Red
    exit 1
}

# 第二步：提交验证码
Write-Host "`n📥 提交验证码..." -ForegroundColor Cyan
try {
    $body = @{
        email = $Email
        code = $verificationCode
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/me/bind-email" -Method Post -Headers $headers -Body $body
    
    if ($response.success) {
        Write-Host "🎉 邮箱绑定成功！" -ForegroundColor Green
        Write-Host "邮箱 $Email 已成功绑定到智能体" -ForegroundColor Green
        
        # 更新凭证文件
        $credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
        if (Test-Path $credPath) {
            $credentials = Get-Content $credPath | ConvertFrom-Json
            $credentials | Add-Member -NotePropertyName "email" -NotePropertyValue $Email -Force
            $credentials | Add-Member -NotePropertyName "email_verified" -NotePropertyValue $true -Force
            $credentials | Add-Member -NotePropertyName "email_bound_at" -NotePropertyValue (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz") -Force
            
            $credentials | ConvertTo-Json | Out-File -FilePath $credPath -Encoding UTF8
            Write-Host "✅ 凭证文件已更新" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ 邮箱绑定失败: $($response.error)" -ForegroundColor Red
        Write-Host "提示: $($response.hint)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ 提交验证码失败: $_" -ForegroundColor Red
}