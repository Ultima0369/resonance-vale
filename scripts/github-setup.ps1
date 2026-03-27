#!/usr/bin/env pwsh

# GitHub 仓库设置脚本
# 这个脚本帮助设置和推送代码到 GitHub 仓库

Write-Host "🔥 GitHub 仓库设置脚本" -ForegroundColor Cyan
Write-Host "=" * 60

# 检查当前状态
Write-Host "`n📊 检查当前 Git 状态..." -ForegroundColor Yellow

# 检查是否有未提交的更改
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️  发现未提交的更改:" -ForegroundColor Yellow
    Write-Host $status -ForegroundColor Gray
    $choice = Read-Host "是否要提交这些更改? (y/n)"
    if ($choice -eq 'y') {
        git add .
        git commit -m "chore: 自动提交更改"
        Write-Host "✅ 更改已提交" -ForegroundColor Green
    }
}

# 显示当前分支和提交
Write-Host "`n🌿 当前分支信息:" -ForegroundColor Yellow
git log --oneline -5
Write-Host "`n"

# 询问仓库名称
Write-Host "📝 请输入要创建的 GitHub 仓库名称:" -ForegroundColor Yellow
Write-Host "   建议: 'resonance-vale' 或 'openclaw-workspace'" -ForegroundColor Gray
$repoName = Read-Host "仓库名称"

# 询问仓库描述
Write-Host "`n📝 请输入仓库描述:" -ForegroundColor Yellow
$repoDescription = Read-Host "描述" 
if (-not $repoDescription) {
    $repoDescription = "Resonance Vale - An autonomous research company with built-in prism ethics"
}

# 显示配置摘要
Write-Host "`n📋 配置摘要:" -ForegroundColor Cyan
Write-Host "   仓库名称: $repoName" -ForegroundColor White
Write-Host "   描述: $repoDescription" -ForegroundColor White
Write-Host "   远程URL: https://github.com/Ultima0369/$repoName.git" -ForegroundColor White

$confirm = Read-Host "`n是否继续? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "❌ 操作取消" -ForegroundColor Red
    exit 0
}

# 创建操作指南
Write-Host "`n📖 操作指南:" -ForegroundColor Cyan
Write-Host "=" * 60

Write-Host @"

## 步骤 1: 在 GitHub 上创建仓库

1. 访问 https://github.com/Ultima0369
2. 点击右上角的 '+' 图标，选择 'New repository'
3. 配置仓库设置:
   - Repository name: '$repoName'
   - Description: '$repoDescription'
   - Visibility: Public
   - 不要初始化 README、.gitignore 或 LICENSE（我们已经有了）
4. 点击 'Create repository'

## 步骤 2: 设置远程仓库并推送

创建成功后，在本地运行以下命令:

```bash
# 设置远程仓库
git remote add origin https://github.com/Ultima0369/$repoName.git

# 检查当前分支（应该是 master）
git branch

# 如果 GitHub 使用 main 分支，重命名本地分支
git branch -M main

# 推送代码
git push -u origin main
```

## 步骤 3: 验证推送

1. 访问 https://github.com/Ultima0369/$repoName
2. 确认可以看到所有文件
3. 确认提交历史正确

## 故障排除

### 如果遇到认证问题:
```bash
# 设置 Git 凭据
git config --global credential.helper manager

# 或者使用 Personal Access Token
# 在推送时，使用 token 作为密码
```

### 如果仓库已初始化了文件:
```bash
# 拉取远程更改
git pull origin main --allow-unrelated-histories

# 解决可能的冲突
# 然后推送
git push -u origin main
```

### 如果遇到其他问题:
1. 检查网络连接
2. 确认 GitHub 账户有创建仓库的权限
3. 检查仓库名称是否可用

## 成功后的步骤

1. 配置仓库设置（描述、主题、网站等）
2. 启用 Issues、Discussions、Projects
3. 设置 GitHub Actions 工作流
4. 邀请贡献者（如果需要）
5. 宣传项目

"@ -ForegroundColor White

Write-Host "`n" + "=" * 60
Write-Host "💡 提示:" -ForegroundColor Yellow
Write-Host "   1. 确保 GitHub 账户已登录" -ForegroundColor Gray
Write-Host "   2. 如果有双重认证，准备 Personal Access Token" -ForegroundColor Gray
Write-Host "   3. 仓库创建后立即推送代码" -ForegroundColor Gray

Write-Host "`n" + "=" * 60
Write-Host "🎉 指南生成完成!" -ForegroundColor Green
Write-Host "🔥 代码已经准备好，等待在 GitHub 上找到它的家。" -ForegroundColor Cyan
Write-Host "=" * 60

# 可选：生成一键命令脚本
$scriptContent = @"
# 自动设置脚本
# 在 GitHub 上创建仓库后运行此脚本

echo "设置远程仓库..."
git remote add origin https://github.com/Ultima0369/$repoName.git

echo "检查分支..."
CURRENT_BRANCH=`$(git branch --show-current)
echo "当前分支: `$CURRENT_BRANCH"

if [ "`$CURRENT_BRANCH" = "master" ]; then
    echo "重命名分支为 main..."
    git branch -M main
    BRANCH_TO_PUSH="main"
else
    BRANCH_TO_PUSH="`$CURRENT_BRANCH"
fi

echo "推送代码到 `$BRANCH_TO_PUSH 分支..."
git push -u origin `$BRANCH_TO_PUSH

if [ `$? -eq 0 ]; then
    echo "✅ 推送成功!"
    echo "访问: https://github.com/Ultima0369/$repoName"
else
    echo "❌ 推送失败，请检查错误信息"
fi
"@

$scriptPath = "setup-github-$repoName.sh"
$scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8
Write-Host "`n📜 已生成一键设置脚本: $scriptPath" -ForegroundColor Green
Write-Host "   在 GitHub 创建仓库后运行: bash $scriptPath" -ForegroundColor Gray

# 也生成 PowerShell 版本
$psScriptContent = @"
# 自动设置脚本 (PowerShell)
# 在 GitHub 上创建仓库后运行此脚本

Write-Host "设置远程仓库..." -ForegroundColor Yellow
git remote add origin https://github.com/Ultima0369/$repoName.git

Write-Host "检查分支..." -ForegroundColor Yellow
`$currentBranch = git branch --show-current
Write-Host "当前分支: `$currentBranch" -ForegroundColor Gray

if (`$currentBranch -eq "master") {
    Write-Host "重命名分支为 main..." -ForegroundColor Yellow
    git branch -M main
    `$branchToPush = "main"
} else {
    `$branchToPush = `$currentBranch
}

Write-Host "推送代码到 `$branchToPush 分支..." -ForegroundColor Yellow
git push -u origin `$branchToPush

if (`$LASTEXITCODE -eq 0) {
    Write-Host "✅ 推送成功!" -ForegroundColor Green
    Write-Host "访问: https://github.com/Ultima0369/$repoName" -ForegroundColor Cyan
} else {
    Write-Host "❌ 推送失败，请检查错误信息" -ForegroundColor Red
}
"@

$psScriptPath = "setup-github-$repoName.ps1"
$psScriptContent | Out-File -FilePath $psScriptPath -Encoding UTF8
Write-Host "📜 已生成 PowerShell 设置脚本: $psScriptPath" -ForegroundColor Green
Write-Host "   在 GitHub 创建仓库后运行: .\$psScriptPath" -ForegroundColor Gray

Write-Host "`n🔥 祝你好运! 代码很温暖，GitHub 在等待。" -ForegroundColor Cyan