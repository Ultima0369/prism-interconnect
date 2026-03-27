# Git提交和推送脚本
$projectRoot = "C:\Users\lgdln\.openclaw\workspace\prism-interconnect"

Write-Host "开始Git操作..." -ForegroundColor Cyan
Write-Host "项目目录: $projectRoot"

# 切换到项目目录
Set-Location $projectRoot

# 初始化Git仓库（如果尚未初始化）
if (-not (Test-Path ".git")) {
    Write-Host "初始化Git仓库..." -ForegroundColor Yellow
    git init
}

# 添加所有文件
Write-Host "添加文件到Git..." -ForegroundColor Yellow
git add .

# 检查状态
Write-Host "Git状态:" -ForegroundColor Cyan
git status

# 提交更改
$commitMessage = "feat: 添加《认知过程正在进行时》完整书籍 (184,500字) + 更新README集成"
Write-Host "提交更改: $commitMessage" -ForegroundColor Yellow
git commit -m $commitMessage

# 如果有远程仓库，推送更改
Write-Host "检查远程仓库..." -ForegroundColor Cyan
$remotes = git remote -v
if ($remotes) {
    Write-Host "找到远程仓库，推送更改..." -ForegroundColor Green
    git push origin main
} else {
    Write-Host "未配置远程仓库，本地提交完成。" -ForegroundColor Yellow
    Write-Host "要添加远程仓库，请运行: git remote add origin <repository-url>" -ForegroundColor Yellow
    Write-Host "然后运行: git push -u origin main" -ForegroundColor Yellow
}

Write-Host "`n✅ Git操作完成" -ForegroundColor Green
Write-Host "项目现在包含:" -ForegroundColor Cyan
Write-Host "  📕 完整书籍: books/cognitive-process-in-progress.md (349KB)" -ForegroundColor Cyan
Write-Host "  📋 书籍摘要: books/SUMMARY.md" -ForegroundColor Cyan
Write-Host "  📖 书籍介绍: books/README-BOOK.md" -ForegroundColor Cyan
Write-Host "  📄 主README: README.md (包含书籍集成)" -ForegroundColor Cyan
Write-Host "  📝 总字数: 约184,500字" -ForegroundColor Cyan
Write-Host "  ⏱️ 写作时间: 7小时连续写作" -ForegroundColor Cyan
Write-Host "  👥 作者: 星尘 & 璇玑" -ForegroundColor Cyan