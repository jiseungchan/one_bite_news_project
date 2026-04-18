@echo off
chcp 65001 > nul
echo.
echo ===================================
echo   한입뉴스 웹사이트 배포
echo ===================================

cd /d "c:\Claude 공부\Claude code\01. 카드뉴스 만들기\web"

:: 변경된 파일 확인
git status --short > temp_status.txt
set /p STATUS=<temp_status.txt
del temp_status.txt

if "%STATUS%"=="" (
    echo 변경된 파일 없음 — 배포 불필요
    goto end
)

:: 커밋 메시지에 날짜 포함
for /f "tokens=1-3 delims=/ " %%a in ("%DATE%") do (
    set TODAY=%%a-%%b-%%c
)

git add .
git commit -m "기사 업데이트: %TODAY%"
git push origin main

echo.
echo 배포 완료!
echo 사이트: https://jiseungchan.github.io/one_bite_news
echo.

:end
pause
