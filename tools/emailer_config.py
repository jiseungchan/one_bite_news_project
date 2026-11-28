# ──────────────────────────────────────────────────────────
# emailer_config.py  — 한입뉴스 이메일 발송 설정 (환경변수 전용)
#
# 비밀값은 이 파일에 절대 적지 않는다. 저장소가 공개(public)라서
# 파일에 적은 값은 누구나 볼 수 있다. 아래 환경변수로만 넘긴다.
#
#   GMAIL_SENDER        발신 Gmail 주소
#   GMAIL_APP_PASSWORD  Google 앱 비밀번호 (myaccount.google.com/apppasswords)
#   GMAIL_RECIPIENT     수신 주소
#   HEISENBERG_EMAIL / HEISENBERG_PASSWORD  (비우면 Heisenberg 수집 건너뜀)
#   ANTHROPIC_API_KEY
#
# 참고: 매일 아침 발송은 이제 Claude 예약 작업(Gmail 커넥터)이 맡는다.
#       이 스크립트는 수동 실행용으로만 남겨 둔다.
# ──────────────────────────────────────────────────────────
import os

GMAIL_USER = os.environ.get("GMAIL_SENDER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENT_EMAIL = os.environ.get("GMAIL_RECIPIENT", "byungkyu.lee@sk.com")

HEISENBERG_EMAIL = os.environ.get("HEISENBERG_EMAIL", "")
HEISENBERG_PASSWORD = os.environ.get("HEISENBERG_PASSWORD", "")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
