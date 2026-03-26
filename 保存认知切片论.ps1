# 认知切片论保存工具 - PowerShell版本

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "认知切片论保存工具" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 检查Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python环境正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未找到Python" -ForegroundColor Red
    Write-Host "请先安装Python 3.8或更高版本" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit
}

# 检查整合版文档
if (-not (Test-Path "认知切片论-整合版.md")) {
    Write-Host "❌ 错误: 未找到整合版文档" -ForegroundColor Red
    Write-Host "请先创建'认知切片论-整合版.md'" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit
}

Write-Host "✅ 找到整合版文档" -ForegroundColor Green

# 检查Obsidian库
$vaultPath = "D:\LDD\璇玑台"
if (-not (Test-Path $vaultPath)) {
    Write-Host "⚠️ 警告: 未找到Obsidian库" -ForegroundColor Yellow
    Write-Host "默认路径: $vaultPath" -ForegroundColor Yellow
    $customPath = Read-Host "请输入Obsidian库路径"
    if ($customPath -and (Test-Path $customPath)) {
        $vaultPath = $customPath
    } else {
        Write-Host "❌ 错误: 必须提供有效的Obsidian库路径" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit
    }
}

Write-Host "✅ Obsidian库: $vaultPath" -ForegroundColor Green

# 显示菜单
function Show-Menu {
    Write-Host "`n📋 保存选项:" -ForegroundColor Cyan
    Write-Host "   1. 完整保存（推荐）" -ForegroundColor White
    Write-Host "   2. 仅保存主文档" -ForegroundColor White
    Write-Host "   3. 仅更新概念文件" -ForegroundColor White
    Write-Host "   4. 查看生成的文件" -ForegroundColor White
    Write-Host "   5. 退出" -ForegroundColor White
    Write-Host ""
}

do {
    Show-Menu
    $choice = Read-Host "请选择 (1-5)"
    
    switch ($choice) {
        "1" {
            Write-Host "`n🚀 开始完整保存..." -ForegroundColor Green
            python save_cognitive_slice_to_obsidian.py
            Write-Host "`n✅ 保存完成！" -ForegroundColor Green
            Read-Host "按回车键继续"
        }
        "2" {
            Write-Host "`n📄 仅保存主文档..." -ForegroundColor Green
            python -c "
import os
from pathlib import Path
vault = Path(r'$vaultPath')
project_folder = vault / '项目' / '认知切片论'
project_folder.mkdir(parents=True, exist_ok=True)
with open('认知切片论-整合版.md', 'r', encoding='utf-8') as f:
    content = f.read()
with open(project_folder / '认知切片论-整合版.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('✅ 主文档已保存到:', str(project_folder / '认知切片论-整合版.md'))
"
            Read-Host "按回车键继续"
        }
        "3" {
            Write-Host "`n🔗 更新概念文件..." -ForegroundColor Green
            python -c "
import re
from pathlib import Path
vault = Path(r'$vaultPath')
concept_folder = vault / '概念'
concept_folder.mkdir(exist_ok=True)
with open('认知切片论-整合版.md', 'r', encoding='utf-8') as f:
    content = f.read()
concepts = re.findall(r'\[\[(.*?)\]\]', content)
unique_concepts = list(set(concepts))
updated = []
for concept in unique_concepts:
    if concept.strip():
        concept_file = concept_folder / f'{concept}.md'
        if concept_file.exists():
            with open(concept_file, 'r', encoding='utf-8') as f:
                existing = f.read()
            if '[[认知切片论-整合版]]' not in existing:
                with open(concept_file, 'a', encoding='utf-8') as f:
                    f.write('\n- [[认知切片论-整合版]]\n')
                updated.append(concept)
print(f'✅ 更新了 {len(updated)} 个概念文件')
"
            Read-Host "按回车键继续"
        }
        "4" {
            Write-Host "`n📁 生成的文件结构:" -ForegroundColor Green
            $projectPath = Join-Path $vaultPath "项目\认知切片论"
            if (Test-Path $projectPath) {
                Write-Host "项目文件夹: $projectPath" -ForegroundColor White
                Write-Host ""
                Get-ChildItem $projectPath | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }
                
                $chaptersPath = Join-Path $projectPath "章节"
                if (Test-Path $chaptersPath) {
                    Write-Host "`n章节文件夹:" -ForegroundColor White
                    Get-ChildItem $chaptersPath | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }
                }
            } else {
                Write-Host "项目文件夹尚未创建" -ForegroundColor Yellow
            }
            Write-Host ""
            Read-Host "按回车键继续"
        }
        "5" {
            Write-Host "`n👋 感谢使用认知切片论保存工具" -ForegroundColor Cyan
            Write-Host "🦞 再见！" -ForegroundColor Cyan
            Start-Sleep -Seconds 2
            exit
        }
        default {
            Write-Host "❌ 无效选择，请重新输入" -ForegroundColor Red
        }
    }
} while ($true)