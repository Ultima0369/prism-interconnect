# 修复文件编码脚本
Write-Host "🔧 开始修复文件编码..." -ForegroundColor Cyan

# 需要修复的文件列表
$filesToFix = @(
    "README.md",
    "MANIFESTO.md",
    "docs/philosophy.md",
    "docs/two-equations-charter.md",
    "docs/compression-history.md",
    "docs/natural-law-1plus1.md",
    "docs/nature-paradox.md",
    "docs/existence-emergence.md",
    "docs/silicon-carbon-ethics.md",
    "docs/visual-materials-guide.md"
)

foreach ($file in $filesToFix) {
    if (Test-Path $file) {
        Write-Host "正在修复: $file" -ForegroundColor Yellow
        
        # 读取文件内容（假设是UTF-8但被错误解释）
        try {
            # 尝试以UTF-8读取
            $content = Get-Content $file -Encoding UTF8 -Raw -ErrorAction Stop
            Write-Host "  ✓ 以UTF-8读取成功" -ForegroundColor Green
        }
        catch {
            # 如果失败，尝试其他编码
            try {
                $content = Get-Content $file -Encoding Default -Raw
                Write-Host "  ⚠ 使用默认编码读取" -ForegroundColor Yellow
            }
            catch {
                Write-Host "  ✗ 读取失败: $_" -ForegroundColor Red
                continue
            }
        }
        
        # 写入UTF-8 with BOM（确保GitHub正确显示）
        $utf8WithBOM = [System.Text.Encoding]::UTF8
        $utf8WithBOM.GetPreamble() | Out-Null  # 确保有BOM
        
        [System.IO.File]::WriteAllText((Get-Item $file).FullName, $content, $utf8WithBOM)
        Write-Host "  ✓ 已写入UTF-8 with BOM" -ForegroundColor Green
    }
    else {
        Write-Host "  ⚠ 文件不存在: $file" -ForegroundColor Yellow
    }
}

Write-Host "✅ 文件编码修复完成" -ForegroundColor Green

# 检查文件大小
Write-Host "`n📊 文件统计：" -ForegroundColor Cyan
foreach ($file in $filesToFix) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $lines = (Get-Content $file).Count
        Write-Host "  $file : $lines 行, $size 字节" -ForegroundColor Gray
    }
}