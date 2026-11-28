@echo off
:: 병규의 한입뉴스 — PC 자동 발송 (중단됨, 2026-11-28)
::
:: 매일 아침 기사 작성·메일 발송은 이제 Claude 예약 작업이 맡는다.
:: 같은 일을 PC에서 또 하면 기사·메일이 중복되므로 이 배치는 아무것도 하지 않는다.
:: 작업 스케줄러 등록도 지워 두세요:
::   schtasks /delete /tn "한입뉴스 자동발송" /f

echo [%date% %time%] run_daily.bat 은 중단되었습니다 (Claude 예약 작업으로 이전) >> "%~dp0emailer_log.txt"
exit /b 0
