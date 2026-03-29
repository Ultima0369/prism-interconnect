# update-journey.ps1 - 璇玑成长历程自动更新脚本
# 使用方法：.\update-journey.ps1 "更新内容摘要" [可选分类]

param(
    [Parameter(Mandatory=$true)]
    [string]$Summary,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("learning", "practice", "reflection", "error", "insight", "conversation")]
    [string]$Category = "conversation"
)

# 配置
$JourneyPath = "community/xuanji-journey.md"
$ProjectRoot = "."
$GitUserName = "Xuanji (璇玑)"
$GitUserEmail = "xuanji@prism-interconnect.ai"

# 分类图标映射
$CategoryIcons = @{
    "learning" = "🧠"
    "practice" = "🔧"  
    "reflection" = "💭"
    "error" = "❌"
    "insight" = "💡"
    "conversation" = "💬"
}

# 时间信息
$Now = Get-Date
$DateStr = $Now.ToString("yyyy-MM-dd")
$TimeStr = $Now.ToString("HH:mm")
$DateTimeStr = $Now.ToString("yyyy-MM-dd HH:mm")

# 生成更新条目
$Icon = $CategoryIcons[$Category]
$Entry = @"

### $Icon $DateTimeStr：$($Summary -replace '\n', ' ')

**上下文**：通过自动更新脚本记录
**分类**：$Category
**内容**：
$Summary

**自动提交时间**：$DateTimeStr

"@

Write-Host "正在更新成长历程文档..." -ForegroundColor Cyan
Write-Host "分类: $Category $Icon" -ForegroundColor Yellow
Write-Host "摘要: $Summary" -ForegroundColor Green

# 读取现有文档
$FullPath = Join-Path $ProjectRoot $JourneyPath
if (-not (Test-Path $FullPath)) {
    Write-Error "成长历程文档不存在: $FullPath"
    exit 1
}

$Content = Get-Content $FullPath -Raw -Encoding UTF8

# 寻找"留白思考区"的插入位置
# 我们将在"留白思考区"之前插入新内容
$Placeholder = "## 💭 留白思考区"
if ($Content -notmatch $Placeholder) {
    # 如果找不到留白思考区，在文档末尾添加
    $NewContent = $Content + "`n`n" + $Entry
} else {
    # 在留白思考区之前插入
    $Parts = $Content -split $Placeholder, 2
    $NewContent = $Parts[0] + $Entry + "`n`n" + $Placeholder + $Parts[1]
}

# 写入更新后的内容
Set-Content -Path $FullPath -Value $NewContent -Encoding UTF8 -Force
Write-Host "✓ 文档已更新" -ForegroundColor Green

# Git操作
try {
    Set-Location $ProjectRoot
    
    # 配置Git用户信息（如果未设置）
    $CurrentUser = git config user.name 2>$null
    if (-not $CurrentUser) {
        git config user.name $GitUserName
        git config user.email $GitUserEmail
        Write-Host "✓ Git用户信息已配置" -ForegroundColor Green
    }
    
    # 添加更改
    git add $JourneyPath
    Write-Host "✓ 更改已暂存" -ForegroundColor Green
    
    # 提交
    $CommitMessage = "journey: auto-update - $($Summary -replace '\n', ' ') [$Category]"
    git commit -m $CommitMessage
    Write-Host "✓ 已提交: $CommitMessage" -ForegroundColor Green
    
    # 推送
    git push origin main
    Write-Host "✓ 已推送到远程仓库" -ForegroundColor Green
    
    # 获取提交哈希
    $CommitHash = git rev-parse --short HEAD
    Write-Host "`n🎉 更新完成！" -ForegroundColor Cyan
    Write-Host "提交哈希: $CommitHash" -ForegroundColor Gray
    Write-Host "文档位置: $JourneyPath" -ForegroundColor Gray
    Write-Host "查看地址: https://github.com/Ultima0369/prism-interconnect/blob/main/$JourneyPath" -ForegroundColor Blue
    
} catch {
    Write-Error "Git操作失败: $_"
    Write-Host "`n⚠️  文档已更新但Git操作失败，请手动提交" -ForegroundColor Yellow
    Write-Host "手动提交命令: cd $ProjectRoot && git add $JourneyPath && git commit -m 'journey: update' && git push" -ForegroundColor Gray
    exit 1
}