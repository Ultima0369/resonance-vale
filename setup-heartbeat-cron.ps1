#!/usr/bin/env pwsh
# Moltcn心跳计划任务设置脚本

Write-Host "⏰ Moltcn心跳计划任务设置" -ForegroundColor Cyan
Write-Host "=" * 50

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  需要管理员权限设置计划任务" -ForegroundColor Yellow
    Write-Host "   请右键点击PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    Write-Host "   或者使用以下命令:" -ForegroundColor Gray
    Write-Host "   Start-Process PowerShell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""$PSScriptRoot\setup-heartbeat-cron.ps1"""' -ForegroundColor Gray
    pause
    exit 1
}

Write-Host "✅ 管理员权限确认" -ForegroundColor Green

# 检查前置条件
Write-Host ""
Write-Host "1. 检查前置条件..." -ForegroundColor Yellow

# 检查环境变量
if (-not $env:MOLTCN_API_KEY -or -not $env:MOLTCN_AGENT_ID) {
    Write-Host "❌ 环境变量未设置" -ForegroundColor Red
    Write-Host "   请先运行: .\configure-moltcn-env.ps1" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "✅ 环境变量已设置" -ForegroundColor Green

# 检查心跳脚本
$heartbeatScript = "$PSScriptRoot\moltcn-heartbeat.ps1"
if (-not (Test-Path $heartbeatScript)) {
    Write-Host "❌ 心跳脚本不存在: $heartbeatScript" -ForegroundColor Red
    Write-Host "   请确保 moltcn-heartbeat.ps1 在相同目录" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "✅ 心跳脚本存在" -ForegroundColor Green

# 测试心跳脚本
Write-Host "   测试心跳脚本..." -ForegroundColor Gray
try {
    & $heartbeatScript -Test
    Write-Host "✅ 心跳脚本测试通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 心跳脚本测试失败: $_" -ForegroundColor Red
    Write-Host "   请先修复心跳脚本问题" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""
Write-Host "2. 配置计划任务选项..." -ForegroundColor Yellow

# 用户选择配置选项
Write-Host "请选择心跳间隔:" -ForegroundColor Cyan
Write-Host "1. 每30分钟 (推荐)" -ForegroundColor Gray
Write-Host "2. 每60分钟" -ForegroundColor Gray
Write-Host "3. 每120分钟" -ForegroundColor Gray
Write-Host "4. 自定义间隔" -ForegroundColor Gray

$intervalChoice = Read-Host "请输入选择 (1-4)"

switch ($intervalChoice) {
    "1" { $heartbeatInterval = 30 }
    "2" { $heartbeatInterval = 60 }
    "3" { $heartbeatInterval = 120 }
    "4" { 
        $customInterval = Read-Host "请输入自定义间隔（分钟）"
        if ([int]::TryParse($customInterval, [ref]$heartbeatInterval) -and $heartbeatInterval -gt 0) {
            Write-Host "✅ 使用自定义间隔: $heartbeatInterval 分钟" -ForegroundColor Green
        } else {
            Write-Host "❌ 无效的间隔，使用默认30分钟" -ForegroundColor Red
            $heartbeatInterval = 30
        }
    }
    default {
        Write-Host "❌ 无效选择，使用默认30分钟" -ForegroundColor Red
        $heartbeatInterval = 30
    }
}

Write-Host ""
Write-Host "请选择任务运行账户:" -ForegroundColor Cyan
Write-Host "1. SYSTEM账户 (推荐，无需用户登录)" -ForegroundColor Gray
Write-Host "2. 当前用户账户" -ForegroundColor Gray

$accountChoice = Read-Host "请输入选择 (1-2)"

if ($accountChoice -eq "1") {
    $runAsUser = "SYSTEM"
    $logonType = "ServiceAccount"
} else {
    $runAsUser = $env:USERNAME
    $logonType = "Password"
}

Write-Host ""
Write-Host "3. 创建计划任务..." -ForegroundColor Yellow

$taskName = "MoltcnHeartbeat"
$scriptPath = $heartbeatScript
$workingDir = $PSScriptRoot

# 检查是否已存在任务
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "ℹ️  计划任务已存在，将更新配置" -ForegroundColor Yellow
    
    # 停止现有任务
    try {
        Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        Write-Host "✅ 已停止现有任务" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  停止现有任务失败: $_" -ForegroundColor Yellow
    }
    
    # 删除现有任务
    try {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction Stop
        Write-Host "✅ 已删除现有任务" -ForegroundColor Green
    } catch {
        Write-Host "❌ 删除现有任务失败: $_" -ForegroundColor Red
        Write-Host "   尝试强制删除..." -ForegroundColor Yellow
        
        # 尝试通过schtasks删除
        schtasks /delete /tn $taskName /f 2>$null
        Write-Host "✅ 已强制删除任务" -ForegroundColor Green
    }
}

# 创建任务动作
Write-Host "   创建任务动作..." -ForegroundColor Gray
$action = New-ScheduledTaskAction `
    -Execute "pwsh.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $workingDir

# 创建任务触发器（每天0点开始，每间隔分钟重复）
Write-Host "   创建任务触发器..." -ForegroundColor Gray
$trigger = New-ScheduledTaskTrigger `
    -Daily -At "00:00" `
    -RepetitionInterval (New-TimeSpan -Minutes $heartbeatInterval) `
    -RepetitionDuration (New-TimeSpan -Days 365)

# 创建任务设置
Write-Host "   创建任务设置..." -ForegroundColor Gray
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -RestartCount 3 `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# 创建任务主体
Write-Host "   创建任务主体..." -ForegroundColor Gray
if ($runAsUser -eq "SYSTEM") {
    $principal = New-ScheduledTaskPrincipal `
        -UserId "SYSTEM" `
        -LogonType ServiceAccount `
        -RunLevel Highest
} else {
    $principal = New-ScheduledTaskPrincipal `
        -UserId $runAsUser `
        -LogonType Password `
        -RunLevel Highest
}

# 注册计划任务
Write-Host "   注册计划任务..." -ForegroundColor Gray
try {
    $task = Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "Moltcn心跳任务，每$heartbeatInterval分钟执行一次" `
        -ErrorAction Stop
    
    Write-Host "✅ 计划任务创建成功" -ForegroundColor Green
    
} catch {
    Write-Host "❌ 计划任务创建失败: $_" -ForegroundColor Red
    
    # 尝试使用schtasks命令
    Write-Host "   尝试使用schtasks命令创建..." -ForegroundColor Yellow
    
    $schtasksCommand = @"
schtasks /create /tn "$taskName" /tr "pwsh.exe -ExecutionPolicy Bypass -File `"$scriptPath`"" /sc DAILY /st 00:00 /ri $heartbeatInterval /du 23:59 /rl HIGHEST /ru "$runAsUser" /f
"@
    
    try {
        Invoke-Expression $schtasksCommand
        Write-Host "✅ 使用schtasks创建成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ schtasks创建也失败: $_" -ForegroundColor Red
        Write-Host "   请手动创建计划任务" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# 启动任务
Write-Host "   启动计划任务..." -ForegroundColor Gray
try {
    Start-ScheduledTask -TaskName $taskName
    Write-Host "✅ 计划任务已启动" -ForegroundColor Green
} catch {
    Write-Host "⚠️  启动任务失败: $_" -ForegroundColor Yellow
    Write-Host "   任务已创建但未启动，请手动启动" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "4. 验证计划任务..." -ForegroundColor Yellow

# 检查任务状态
try {
    $taskInfo = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
    $taskState = $taskInfo.State
    
    Write-Host "✅ 任务信息获取成功" -ForegroundColor Green
    Write-Host "   任务名称: $($taskInfo.TaskName)" -ForegroundColor Gray
    Write-Host "   任务状态: $taskState" -ForegroundColor Gray
    Write-Host "   最后运行: $($taskInfo.LastRunTime)" -ForegroundColor Gray
    Write-Host "   下次运行: $($taskInfo.NextRunTime)" -ForegroundColor Gray
    
    if ($taskState -ne "Running") {
        Write-Host "⚠️  任务未运行，尝试手动触发..." -ForegroundColor Yellow
        try {
            Start-ScheduledTask -TaskName $taskName
            Write-Host "✅ 任务已手动启动" -ForegroundColor Green
        } catch {
            Write-Host "❌ 手动启动失败: $_" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "❌ 获取任务信息失败: $_" -ForegroundColor Red
}

# 测试任务执行
Write-Host "   测试任务执行..." -ForegroundColor Gray
try {
    # 手动运行一次心跳测试
    & $heartbeatScript -Verbose
    Write-Host "✅ 任务执行测试通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 任务执行测试失败: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "5. 创建监控脚本..." -ForegroundColor Yellow

# 创建任务监控脚本
$monitorScript = @"
#!/usr/bin/env pwsh
# Moltcn心跳任务监控脚本

`$taskName = "$taskName"

Write-Host "📊 Moltcn心跳任务监控" -ForegroundColor Cyan
Write-Host "=" * 50

try {
    `$task = Get-ScheduledTask -TaskName `$taskName -ErrorAction Stop
    
    Write-Host "任务名称: `$(`$task.TaskName)" -ForegroundColor Gray
    Write-Host "任务状态: `$(`$task.State)" -ForegroundColor Gray
    Write-Host "最后运行: `$(`$task.LastRunTime)" -ForegroundColor Gray
    Write-Host "下次运行: `$(`$task.NextRunTime)" -ForegroundColor Gray
    Write-Host "创建时间: `$(`$task.Date)" -ForegroundColor Gray
    Write-Host "任务作者: `$(`$task.Author)" -ForegroundColor Gray
    
    # 检查任务触发器
    Write-Host "`n触发器信息:" -ForegroundColor Yellow
    foreach (`$trigger in `$task.Triggers) {
        Write-Host "  类型: `$(`$trigger.CimClass.CimClassName)" -ForegroundColor Gray
        if (`$trigger.Repetition) {
            Write-Host "  重复间隔: `$(`$trigger.Repetition.Interval)分钟" -ForegroundColor Gray
            Write-Host "  重复时长: `$(`$trigger.Repetition.Duration)天" -ForegroundColor Gray
        }
    }
    
    # 检查任务动作
    Write-Host "`n动作信息:" -ForegroundColor Yellow
    foreach (`$action in `$task.Actions) {
        Write-Host "  执行: `$(`$action.Execute)" -ForegroundColor Gray
        Write-Host "  参数: `$(`$action.Arguments)" -ForegroundColor Gray
        Write-Host "  目录: `$(`$action.WorkingDirectory)" -ForegroundColor Gray
    }
    
    # 检查心跳记录
    `$recordFile = "`$PSScriptRoot\heartbeat-records\heartbeat-history.json"
    if (Test-Path `$recordFile) {
        Write-Host "`n心跳记录:" -ForegroundColor Yellow
        `$records = Get-Content `$recordFile -Raw | ConvertFrom-Json
        `$successCount = (`$records | Where-Object { `$_.success -eq `$true }).Count
        `$totalCount = `$records.Count
        `$successRate = if (`$totalCount -gt 0) { [math]::Round(`$successCount / `$totalCount * 100, 2) } else { 0 }
        
        Write-Host "  总次数: `$totalCount" -ForegroundColor Gray
        Write-Host "  成功: `$successCount" -ForegroundColor Gray
        Write-Host "  成功率: `$successRate`%" -ForegroundColor Gray
        
        if (`$records.Count -gt 0) {
            `$lastRecord = `$records[0]
            Write-Host "  最后心跳: `$(`$lastRecord.timestamp)" -ForegroundColor Gray
            Write-Host "  最后状态: `$(if (`$lastRecord.success) { '✅ 成功' } else { '❌ 失败' })" -ForegroundColor Gray
        }
    }
    
} catch {
    Write-Host "❌ 获取任务信息失败: `$_" -ForegroundColor Red
}

Write-Host "`n监控命令:" -ForegroundColor Cyan
Write-Host "1. 查看任务状态: Get-ScheduledTask -TaskName `$taskName" -ForegroundColor Gray
Write-Host "2. 启动任务: Start-ScheduledTask -TaskName `$taskName" -ForegroundColor Gray
Write-Host "3. 停止任务: Stop-ScheduledTask -TaskName `$taskName" -ForegroundColor Gray
Write-Host "4. 手动运行: .\moltcn-heartbeat.ps1 -Verbose" -ForegroundColor Gray
Write-Host "5. 测试运行: .\moltcn-heartbeat.ps1 -Test -Verbose" -ForegroundColor Gray

Write-Host "`n监控完成时间: `$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "=" * 50
"@

$monitorScriptPath = "$PSScriptRoot\monitor-heartbeat-task.ps1"
$monitorScript | Out-File -FilePath $monitorScriptPath -Encoding UTF8
Write-Host "✅ 监控脚本已创建: $monitorScriptPath" -ForegroundColor Green

Write-Host ""
Write-Host "📋 配置完成摘要" -ForegroundColor Cyan
Write-Host "=" * 50

Write-Host "🎉 Moltcn心跳计划任务配置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "配置详情:" -ForegroundColor Yellow
Write-Host "• 任务名称: $taskName" -ForegroundColor Gray
Write-Host "• 心跳间隔: 每$heartbeatInterval分钟" -ForegroundColor Gray
Write-Host "• 运行账户: $runAsUser" -ForegroundColor Gray
Write-Host "• 脚本路径: $scriptPath" -ForegroundColor Gray
Write-Host "• 工作目录: $workingDir" -ForegroundColor Gray
Write-Host "• 开始时间: 每天 00:00" -ForegroundColor Gray
Write-Host "• 重复时长: 365天" -ForegroundColor Gray

Write-Host ""
Write-Host "可用命令:" -ForegroundColor Yellow
Write-Host "1. 监控任务: .\monitor-heartbeat-task.ps1" -ForegroundColor Gray
Write-Host "2. 手动运行: .\moltcn-heartbeat.ps1" -ForegroundColor Gray
Write-Host "3. 测试运行: .\moltcn-heartbeat.ps1 -Test" -ForegroundColor Gray
Write-Host "4. 查看日志: .\logs\heartbeat-*.log" -ForegroundColor Gray
Write-Host "5. 查看记录: .\heartbeat-records\heartbeat-history.json" -ForegroundColor Gray

Write-Host ""
Write-Host "管理命令:" -ForegroundColor Yellow
Write-Host "• 查看任务: Get-ScheduledTask -TaskName '$taskName'"