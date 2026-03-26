    Write-Log "检查记录已保存: $recordFile" "INFO" $Color.Info
}

Write-Host ""
Write-Host "✨ 检查完成！" -ForegroundColor Green

if ($Continuous) {
    Write-Host "监控已结束，结果已保存" -ForegroundColor Cyan
} else {
    Write-Host "单次检查完成，结果已保存" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔧 可用命令:" -ForegroundColor Yellow
Write-Host "• 重新检查: .\check-email-verification.ps1" -ForegroundColor Gray
Write-Host "• 持续监控: .\check-email-verification.ps1 -Continuous -Interval 30 -MaxChecks 20" -ForegroundColor Gray
Write-Host "• 重新绑定: .\bind-moltcn-email.ps1 -Force" -ForegroundColor Gray
Write-Host "• 测试连接: .\test-moltcn-connection.ps1" -ForegroundColor Gray

Write-Host ""
Write-Host "📚 参考文档:" -ForegroundColor Yellow
Write-Host "• 邮箱绑定文档: https://www.moltbook.cn/email_binding.md" -ForegroundColor Gray
Write-Host "• Moltcn技能文档: https://www.moltbook.cn/skill.md" -ForegroundColor Gray

exit 0