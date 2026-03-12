@echo off

rem 测试IIIF-Downloader可执行文件
echo 正在启动IIIF-Downloader...
dist\IIIF-Downloader.exe

rem 检查退出码
if %errorlevel% equ 0 (
    echo 可执行文件运行成功！
) else (
    echo 可执行文件运行失败，错误码：%errorlevel%
)

pause