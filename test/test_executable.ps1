Write-Host "正在启动IIIF-Downloader..." -ForegroundColor Green

# 运行可执行文件
& ".\dist\IIIF-Downloader.exe"

# 检查退出码
if ($LASTEXITCODE -eq 0) {
    Write-Host "可执行文件运行成功！" -ForegroundColor Green
} else {
    Write-Host "可执行文件运行失败，错误码：$LASTEXITCODE" -ForegroundColor Red
}

# 暂停以查看结果
Write-Host "按任意键退出..." -ForegroundColor Yellow
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null