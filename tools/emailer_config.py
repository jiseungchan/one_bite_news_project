# ──────────────────────────────────────────────────────────
# emailer_config.py  — 한입뉴스 이메일 발송 설정
#
# 이 파일을 채운 뒤 daily_emailer.py 를 실행하세요.
# 보안 주의: 이 파일은 .gitignore 에 포함되어 있습니다.
# ──────────────────────────────────────────────────────────

# ── Gmail 설정 ─────────────────────────────────────────────
# 발신 Gmail 주소 (수신도 같은 주소면 동일하게 입력)
GMAIL_USER = "forcisco02@gmail.com"

# Google 앱 비밀번호 (16자리, 공백 포함 가능)
# 발급 방법: myaccount.google.com/apppasswords
# (2단계 인증이 먼저 활성화되어야 합니다)
GMAIL_APP_PASSWORD = "wxsq zsfn qfda gxim"

# 수신 이메일 주소
RECIPIENT_EMAIL = "forcisco02@gmail.com"

# ── Heisenberg 로그인 ────────────────────────────────────
# 이메일+비밀번호 로그인. 비워두면 Heisenberg 수집 건너뜁니다.
HEISENBERG_EMAIL    = "forcisco02"
HEISENBERG_PASSWORD = "Destiny96!"

# ── Claude API ────────────────────────────────────────────
# 비워두면 환경변수 ANTHROPIC_API_KEY 를 자동으로 사용합니다
ANTHROPIC_API_KEY = ""
