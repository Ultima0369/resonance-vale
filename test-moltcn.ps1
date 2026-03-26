# Simple test script for Moltcn
Write-Host "Testing Moltcn API..." -ForegroundColor Cyan

# Read credentials file
$credPath = "$env:USERPROFILE\.config\moltcn\credentials.json"
if (Test-Path $credPath) {
    Write-Host "Found credentials file" -ForegroundColor Green
    $content = Get-Content $credPath -Raw
    Write-Host "File content length: $($content.Length)" -ForegroundColor Gray
    
    # Try to parse JSON
    try {
        $credentials = $content | ConvertFrom-Json
        Write-Host "Successfully parsed JSON" -ForegroundColor Green
        Write-Host "API Key: $($credentials.api_key)" -ForegroundColor Gray
        Write-Host "Agent Name: $($credentials.agent_name)" -ForegroundColor Gray
        
        # Test API call
        $headers = @{
            "Authorization" = "Bearer $($credentials.api_key)"
        }
        
        Write-Host "`nTesting API call..." -ForegroundColor Cyan
        $response = Invoke-RestMethod -Uri "https://www.moltbook.cn/api/v1/agents/status" -Method Get -Headers $headers
        Write-Host "API Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Green
        
    } catch {
        Write-Host "Error parsing JSON: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Credentials file not found" -ForegroundColor Red
}