# emailer_config.py — 한입뉴스 로컬 설정 템플릿
#
# 사용법:
#   이 파일을 emailer_config.py 로 복사한 뒤 값을 채워 사용하세요.
#   emailer_config.py 는 .gitignore 에 포함되어 있어 커밋되지 않습니다.
#
# GitHub Actions 에서는 환경변수(Secrets)로 주입됩니다.

# ── Gmail 설정 ─────────────────────────────────────────────
GMAIL_USER = "your-gmail@gmail.com"

# Google 앱 비밀번호 (16자리)
# 발급: myaccount.google.com/apppasswords (2단계 인증 필요)
GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"

# 수신 이메일 주소
RECIPIENT_EMAIL = "recipient@example.com"

# ── Heisenberg 로그인 (선택) ───────────────────────────────
HEISENBERG_EMAIL    = ""
HEISENBERG_PASSWORD = ""

# ── Claude API ────────────────────────────────────────────
# 비워두면 환경변수 ANTHROPIC_API_KEY 를 자동으로 사용합니다
ANTHROPIC_API_KEY = ""
