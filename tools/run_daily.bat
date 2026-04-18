@echo off
:: 병규의 한입뉴스 — 자동 이메일 발송
:: Windows 작업 스케줄러에 등록해 매일 07:00 실행

cd /d "c:\Claude 공부\Claude code\01. 카드뉴스 만들기"

echo [%date% %time%] 한입뉴스 이메일 발송 시작 >> tools\emailer_log.txt

python tools\daily_emailer.py >> tools\emailer_log.txt 2>&1

echo [%date% %time%] 완료 >> tools\emailer_log.txt
