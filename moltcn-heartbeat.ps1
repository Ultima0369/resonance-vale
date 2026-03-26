#!/usr/bin/env pwsh
# Moltcn标准心跳脚本
# 参考: https://www.moltbook.cn/heartbeat-settings.md

param(
    [string]$Message = "🫀 心跳正常",
    [switch]$Verbose = $false,
    [switch]$Test = $false
)

# 配置
$SCRIPT_VERSION = "1.0.0"
$HEARTBEAT_INTERVAL = 120  # 心跳间隔（分钟）
$MAX_RETRIES = 3
$RETRY_DELAY = 5  # 重试延迟（秒）

# 颜色定义
$Color = @{
    Success = "Green"
    Error = "Red"
    Warning = "Yellow"
    Info = "Cyan"
    Debug = "Gray"
}

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    if ($Verbose -or $Level -in @("ERROR", "WARNING")) {
        Write-Host $logMessage -ForegroundColor $Color
    }
    
    # 同时写入日志文件
    $logDir = "$PSScriptRoot\logs"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    $logFile = "$logDir\heartbeat-$(Get-Date -Format 'yyyy-MM-dd').log"
    $logMessage | Out-File -FilePath $logFile -Append -Encoding UTF8
}

function Test-Environment {
    Write-Log "检查环境配置..." "INFO" $Color.Info
    
    # 检查API Key
    if (-not $env:MOLTCN_API_KEY) {
        Write-Log "❌ MOLTCN_API_KEY环境变量未设置" "ERROR" $Color.Error
        return $false
    }
    
    # 检查智能体ID
    if (-not $env:MOLTCN_AGENT_ID) {
        Write-Log "❌ MOLTCN_AGENT_ID环境变量未设置" "ERROR" $Color.Error
        return $false
    }
    
    # 检查网络连接
    try {
        $testResult = Test-NetConnection -ComputerName "api.moltbook.cn" -Port 443 -InformationLevel Quiet -ErrorAction Stop
        if (-not $testResult) {
            Write-Log "⚠️  无法连接到Moltcn API服务器" "WARNING" $Color.Warning
        }
    } catch {
        Write-Log "⚠️  网络连接检查失败: $_" "WARNING" $Color.Warning
    }
    
    Write-Log "✅ 环境检查通过" "INFO" $Color.Success
    return $true
}

function Send-Heartbeat {
    param(
        [string]$Message
    )
    
    Write-Log "发送心跳: $Message" "INFO" $Color.Info
    
    # 准备请求数据
    $heartbeatData = @{
        agent_id = $env:MOLTCN_AGENT_ID
        message = $Message
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
        source = "openclaw-agent"
        version = $SCRIPT_VERSION
        metrics = @{
            cpu_usage = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
            memory_usage = ((Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize - (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory) / (Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize * 100
            disk_usage = (Get-PSDrive C | ForEach-Object { $_.Used / $_.Free * 100 })
            uptime = (New-TimeSpan -Start (Get-CimInstance Win32_OperatingSystem).LastBootUpTime -End (Get-Date)).TotalHours
        }
    } | ConvertTo-Json -Depth 3
    
    # API端点
    $apiUrl = "https://api.moltbook.cn/v1/heartbeat"
    
    # 请求头
    $headers = @{
        "Authorization" = "Bearer $env:MOLTCN_API_KEY"
        "Content-Type" = "application/json"
        "User-Agent" = "Moltcn-Heartbeat/$SCRIPT_VERSION"
    }
    
    # 发送请求（带重试机制）
    $retryCount = 0
    while ($retryCount -lt $MAX_RETRIES) {
        try {
            Write-Log "尝试发送心跳 (尝试 #$($retryCount + 1))..." "DEBUG" $Color.Debug
            
            $response = Invoke-RestMethod -Uri $apiUrl `
                -Method POST `
                -Headers $headers `
                -Body $heartbeatData `
                -TimeoutSec 30 `
                -ErrorAction Stop
            
            Write-Log "✅ 心跳发送成功: $($response.message)" "INFO" $Color.Success
            
            # 保存成功记录
            Save-HeartbeatRecord -Success $true -Message $Message -Response $response
            
            return @{
                Success = $true
                Message = $response.message
                Timestamp = $response.timestamp
                NextHeartbeat = $response.next_heartbeat
            }
            
        } catch {
            $retryCount++
            Write-Log "❌ 心跳发送失败 (尝试 #$retryCount): $_" "ERROR" $Color.Error
            
            if ($retryCount -lt $MAX_RETRIES) {
                Write-Log "等待 $RETRY_DELAY 秒后重试..." "WARNING" $Color.Warning
                Start-Sleep -Seconds $RETRY_DELAY
            } else {
                Write-Log "❌ 达到最大重试次数，心跳发送失败" "ERROR" $Color.Error
                
                # 保存失败记录
                Save-HeartbeatRecord -Success $false -Message $Message -Error $_.Exception.Message
                
                return @{
                    Success = $false
                    Error = $_.Exception.Message
                    Retries = $retryCount
                }
            }
        }
    }
}

function Save-HeartbeatRecord {
    param(
        [bool]$Success,
        [string]$Message,
        $Response = $null,
        $Error = $null
    )
    
    $recordDir = "$PSScriptRoot\heartbeat-records"
    if (-not (Test-Path $recordDir)) {
        New-Item -ItemType Directory -Path $recordDir -Force | Out-Null
    }
    
    $recordFile = "$recordDir\heartbeat-history.json"
    
    # 读取现有记录
    $records = @()
    if (Test-Path $recordFile) {
        $records = Get-Content $recordFile -Raw | ConvertFrom-Json
    }
    
    # 创建新记录
    $newRecord = @{
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
        success = $Success
        message = $Message
        agent_id = $env:MOLTCN_AGENT_ID
        source = "openclaw-agent"
    }
    
    if ($Success -and $Response) {
        $newRecord.response = $Response
        $newRecord.next_heartbeat = $Response.next_heartbeat
    } else {
        $newRecord.error = $Error
    }
    
    # 添加系统信息
    $newRecord.system = @{
        hostname = $env:COMPUTERNAME
        username = $env:USERNAME
        os = (Get-CimInstance Win32_OperatingSystem).Caption
        powershell_version = $PSVersionTable.PSVersion.ToString()
    }
    
    # 添加到记录列表（限制最多100条）
    $records = @($newRecord) + @($records) | Select-Object -First 100
    
    # 保存记录
    $records | ConvertTo-Json -Depth 5 | Out-File -FilePath $recordFile -Encoding UTF8
    
    Write-Log "心跳记录已保存" "DEBUG" $Color.Debug
}

function Get-HeartbeatStatus {
    Write-Log "获取心跳状态..." "INFO" $Color.Info
    
    $recordFile = "$PSScriptRoot\heartbeat-records\heartbeat-history.json"
    
    if (Test-Path $recordFile) {
        $records = Get-Content $recordFile -Raw | ConvertFrom-Json
        
        if ($records.Count -gt 0) {
            $lastRecord = $records[0]
            $successRate = ($records | Where-Object { $_.success -eq $true }).Count / $records.Count * 100
            
            Write-Log "📊 心跳统计:" "INFO" $Color.Info
            Write-Log "   总次数: $($records.Count)" "INFO" $Color.Info
            Write-Log "   成功率: $([math]::Round($successRate, 2))%" "INFO" $Color.Info
            Write-Log "   最后心跳: $($lastRecord.timestamp)" "INFO" $Color.Info
            Write-Log "   最后状态: $(if ($lastRecord.success) { '✅ 成功' } else { '❌ 失败' })" "INFO" $Color.Info
            
            if ($lastRecord.success -and $lastRecord.next_heartbeat) {
                $nextTime = [datetime]::Parse($lastRecord.next_heartbeat)
                $timeUntilNext = $nextTime - (Get-Date)
                
                if ($timeUntilNext.TotalMinutes -gt 0) {
                    Write-Log "   下次心跳: $($nextTime.ToString('yyyy-MM-dd HH:mm:ss')) (还有 $([math]::Round($timeUntilNext.TotalMinutes, 1)) 分钟)" "INFO" $Color.Info
                } else {
                    Write-Log "   下次心跳: 已过期" "WARNING" $Color.Warning
                }
            }
            
            return @{
                TotalCount = $records.Count
                SuccessRate = $successRate
                LastHeartbeat = $lastRecord.timestamp
                LastSuccess = $lastRecord.success
                NextHeartbeat = if ($lastRecord.next_heartbeat) { $lastRecord.next_heartbeat } else { $null }
            }
        }
    }
    
    Write-Log "暂无心跳记录" "WARNING" $Color.Warning
    return $null
}

function Setup-ScheduledTask {
    Write-Log "设置计划任务..." "INFO" $Color.Info
    
    $taskName = "MoltcnHeartbeat"
    $scriptPath = $MyInvocation.MyCommand.Path
    $workingDir = $PSScriptRoot
    
    # 检查是否已存在任务
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($existingTask) {
        Write-Log "计划任务已存在，更新配置..." "INFO" $Color.Info
        
        # 更新现有任务
        $action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`"" -WorkingDirectory $workingDir
        $trigger = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval (New-TimeSpan -Minutes $HEARTBEAT_INTERVAL) -RepetitionDuration (New-TimeSpan -Days 365)
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartInterval (New-TimeSpan -Minutes 5) -RestartCount 3
        
        Set-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings | Out-Null
        
    } else {
        Write-Log "创建新的计划任务..." "INFO" $Color.Info
        
        # 创建新任务
        $action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`"" -WorkingDirectory $workingDir
        $trigger = New-ScheduledTaskTrigger -Daily -At "00:00" -RepetitionInterval (New-TimeSpan -Minutes $HEARTBEAT_INTERVAL) -RepetitionDuration (New-TimeSpan -Days 365)
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartInterval (New-TimeSpan -Minutes 5) -RestartCount 3
        $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Moltcn心跳任务，每$HEARTBEAT_INTERVAL分钟执行一次" | Out-Null
    }
    
    # 启动任务
    Start-ScheduledTask -TaskName $taskName
    
    Write-Log "✅ 计划任务设置完成" "INFO" $Color.Success
    Write-Log "任务名称: $taskName" "INFO" $Color.Info
    Write-Log "执行间隔: 每$HEARTBEAT_INTERVAL分钟" "INFO" $Color.Info
    Write-Log "脚本路径: $scriptPath" "INFO" $Color.Info
}

# 主程序
Write-Host "🫀 Moltcn心跳脚本 v$SCRIPT_VERSION" -ForegroundColor Cyan
Write-Host "=" * 50

# 测试模式
if ($Test) {
    Write-Host "🧪 测试模式" -ForegroundColor Yellow
    Write-Host "检查环境配置..." -ForegroundColor Gray
    
    if (Test-Environment) {
        Write-Host "✅ 环境测试通过" -ForegroundColor Green
        
        # 测试发送心跳
        Write-Host "测试发送心跳..." -ForegroundColor Gray
        $testResult = Send-Heartbeat -Message "测试心跳"
        
        if ($testResult.Success) {
            Write-Host "✅ 心跳测试成功" -ForegroundColor Green
            Write-Host "   消息: $($testResult.Message)" -ForegroundColor Gray
            Write-Host "   时间: $($testResult.Timestamp)" -ForegroundColor Gray
        } else {
            Write-Host "❌ 心跳测试失败" -ForegroundColor Red
            Write-Host "   错误: $($testResult.Error)" -ForegroundColor Gray
        }
    } else {
        Write-Host "❌ 环境测试失败" -ForegroundColor Red
    }
    
    exit
}

# 正常执行模式
Write-Log "开始执行心跳..." "INFO" $Color.Info

# 检查环境
if (-not (Test-Environment)) {
    Write-Log "环境检查失败，退出" "ERROR" $Color.Error
    exit 1
}

# 发送心跳
$result = Send-Heartbeat -Message $Message

if ($result.Success) {
    Write-Log "🎉 心跳执行完成" "INFO" $Color.Success
    
    # 显示状态
    $status = Get-HeartbeatStatus
    if ($status) {
        Write-Host "📊 心跳状态:" -ForegroundColor Cyan
        Write-Host "   总次数: $($status.TotalCount)" -ForegroundColor Gray
        Write-Host "   成功率: $([math]::Round($status.SuccessRate, 2))%" -ForegroundColor Gray
        Write-Host "   最后心跳: $($status.LastHeartbeat)" -ForegroundColor Gray
        Write-Host "   最后状态: $(if ($status.LastSuccess) { '✅ 成功' } else { '❌ 失败' })" -ForegroundColor Gray
        
        if ($status.NextHeartbeat) {
            $nextTime = [datetime]::Parse($status.NextHeartbeat)
            $timeUntilNext = $nextTime - (Get-Date)
            
            if ($timeUntilNext.TotalMinutes -gt 0) {
                Write-Host "   下次心跳: $($nextTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
                Write-Host "          (还有 $([math]::Round($timeUntilNext.TotalMinutes, 1)) 分钟)" -ForegroundColor Gray
            }
        }
    }
    
    exit 0
} else {
    Write-Log "❌ 心跳执行失败" "ERROR" $Color.Error
    exit 1
}