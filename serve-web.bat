@echo off
chcp 65001 >nul
cd /d "%~dp0web"
echo.
echo  [한입뉴스] 로컬 미리보기 서버
echo  브라우저에서 다음 주소를 여세요:  http://localhost:8765/
echo  종료: 이 창에서 Ctrl+C
echo.
python -m http.server 8765 2>nul
if errorlevel 1 py -3 -m http.server 8765 2>nul
if errorlevel 1 (
  echo.
  echo Python을 찾을 수 없습니다. https://www.python.org/downloads/ 에서 설치한 뒤 다시 실행하세요.
  pause
  exit /b 1
)
pause
