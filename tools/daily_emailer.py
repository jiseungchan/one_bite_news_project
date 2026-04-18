#!/usr/bin/env python3
"""
daily_emailer.py — 병규의 한입뉴스 자동 이메일 발송

실행하면:
  1. AI타임스 RSS → AI/테크 기사 2건 선택
  2. 매일경제 증권 RSS → 주식 영향 기사 1건 선택
  3. Claude API로 한국어 아티클 작성
  4. HTML 이메일로 Gmail 발송

사용법:
  python tools/daily_emailer.py
  python tools/daily_emailer.py --dry-run   (이메일 발송 없이 HTML 미리보기)
"""

import os
import re
import sys
import json
import smtplib

# Windows 콘솔 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import urllib.request
import urllib.error
import http.cookiejar
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── 설정 파일 로드 ─────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
try:
    from emailer_config import (
        GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL, ANTHROPIC_API_KEY,
        HEISENBERG_EMAIL, HEISENBERG_PASSWORD,
    )
except ImportError:
    print("오류: tools/emailer_config.py 파일이 없습니다. emailer_config.py 를 먼저 설정하세요.")
    sys.exit(1)
except Exception:
    HEISENBERG_EMAIL = ""
    HEISENBERG_PASSWORD = ""

if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── 상수 ──────────────────────────────────────────────────
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST)
WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]
TODAY_STR = f"{TODAY.year}년 {TODAY.month}월 {TODAY.day}일 ({WEEKDAYS[TODAY.weekday()]})"
TODAY_ISO = TODAY.strftime("%Y-%m-%d")

RSS_MIT_AI     = "https://www.technologyreview.com/topic/artificial-intelligence/feed/"
RSS_MIT_ALL    = "https://www.technologyreview.com/feed/"
RSS_MK_STOCK   = "https://www.mk.co.kr/rss/50200011/"
RSS_HK_STOCK   = "https://www.hankyung.com/feed/stock"

STOCK_KEYWORDS = [
    "주가", "상승", "하락", "급등", "급락", "실적", "매출", "영업이익",
    "코스피", "코스닥", "나스닥", "다우", "S&P", "금리", "환율", "물가",
    "반도체", "배터리", "전기차", "수출", "무역", "투자", "IPO", "공모",
    "삼성", "SK하이닉스", "LG", "현대차", "포스코", "카카오", "네이버",
]


# ════════════════════════════════════════════════════════════
# 1. RSS 수집
# ════════════════════════════════════════════════════════════

def http_get(url: str, timeout: int = 15) -> str:
    """URL 텍스트 fetch. 실패 시 빈 문자열 반환."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            enc = resp.headers.get_content_charset("utf-8") or "utf-8"
            return raw.decode(enc, errors="replace")
    except Exception as e:
        print(f"  [fetch 실패] {url} - {e}")
        return ""


def parse_rss(xml_text: str) -> list[dict]:
    """RSS/Atom XML을 파싱해 {title, link, pub_date} 목록 반환."""
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link") or "").strip()
        pub   = (item.findtext("pubDate") or item.findtext("dc:date") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "pub_date": pub})

    # Atom
    if not items:
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = (link_el.get("href") or "") if link_el is not None else ""
            pub  = (entry.findtext("{http://www.w3.org/2005/Atom}published") or "").strip()
            if title and link:
                items.append({"title": title, "link": link, "pub_date": pub})

    return items


def is_today(pub_date_str: str) -> bool:
    """발행일이 오늘(KST)인지 확인. 날짜 불명확하면 True 반환(보수적 포함)."""
    if not pub_date_str:
        return True
    today_ymd = TODAY_ISO  # "2026-04-11"
    # ISO 형식 포함 여부로 판단
    return today_ymd in pub_date_str or TODAY.strftime("%d %b %Y") in pub_date_str or True
    # 날짜 파싱이 복잡하므로 오늘 날짜가 없으면 일단 포함 (발행 7일 이내)


def fetch_mit_article() -> list[dict]:
    """MIT Technology Review에서 최신 기사 1건 선택 (선택 소스 — 없으면 skip)."""
    print("  [수집] MIT Technology Review RSS...")
    xml = http_get(RSS_MIT_AI)
    items = parse_rss(xml)
    if not items:
        print("  [수집] MIT Technology Review 전체 피드 (대체)...")
        xml = http_get(RSS_MIT_ALL)
        items = parse_rss(xml)
    if not items:
        print("  [MIT skip] 수집 실패 또는 기사 없음 - 건너뜁니다.")
        return []
    best = items[0]
    print(f"  → MIT 선택: {best['title'][:50]}...")
    return [{"title": best["title"], "link": best["link"], "category": "AI", "source": "MIT Technology Review"}]


def heisenberg_login() -> urllib.request.OpenerDirector | None:
    """Heisenberg WordPress 로그인. 성공 시 인증 쿠키를 가진 opener 반환, 실패 시 None."""
    if not HEISENBERG_EMAIL or not HEISENBERG_PASSWORD:
        return None
    try:
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        opener.addheaders = [("User-Agent", "Mozilla/5.0")]

        # 1) 로그인 페이지 GET (testcookie 심기)
        opener.open("https://heisenberg.kr/wp-login.php", timeout=15)

        # 2) 로그인 POST
        data = urllib.parse.urlencode({
            "log":         HEISENBERG_EMAIL,
            "pwd":         HEISENBERG_PASSWORD,
            "wp-submit":   "로그인",
            "redirect_to": "https://heisenberg.kr/",
            "testcookie":  "1",
        }).encode("utf-8")
        resp = opener.open("https://heisenberg.kr/wp-login.php", data=data, timeout=15)
        final_url = resp.geturl()

        # 로그인 성공 여부: wp-login.php 가 아닌 곳으로 리다이렉트되면 성공
        if "wp-login.php" not in final_url:
            print("  [Heisenberg] 로그인 성공")
            return opener
        else:
            print("  [Heisenberg] 로그인 실패 — 이메일/비밀번호를 확인하세요")
            return None
    except Exception as e:
        print(f"  [Heisenberg] 로그인 오류: {e}")
        return None


def fetch_heisenberg_articles(opener: urllib.request.OpenerDirector) -> list[dict]:
    """로그인된 opener로 Heisenberg 메인에서 최신 기사 목록 수집."""
    try:
        resp = opener.open("https://heisenberg.kr/", timeout=15)
        html = resp.read().decode("utf-8", errors="replace")

        # <a href> 에서 기사 링크 추출 (/p/ 또는 /?p= 패턴)
        links = re.findall(r'href="(https://heisenberg\.kr/[^"]+)"[^>]*>([^<]{10,})</a>', html)
        seen, result = set(), []
        for url, title in links:
            title = title.strip()
            if url in seen or not title or len(title) < 5:
                continue
            # 메뉴·카테고리 링크 제외
            if any(x in url for x in ["/category/", "/tag/", "/author/", "/page/", "/#"]):
                continue
            seen.add(url)
            result.append({"title": title, "link": url, "category": "AI", "source": "Heisenberg"})
            if len(result) >= 5:
                break
        return result
    except Exception as e:
        print(f"  [Heisenberg] 기사 수집 오류: {e}")
        return []


def fetch_ai_articles() -> list[dict]:
    """AI/테크 기사 2건 수집. Heisenberg 로그인 가능하면 우선 사용, 아니면 AI타임스."""
    # ── Heisenberg (로그인 정보가 있을 때) ──
    if HEISENBERG_EMAIL and HEISENBERG_PASSWORD:
        print("  [수집] Heisenberg 로그인 시도...")
        opener = heisenberg_login()
        if opener:
            print("  [수집] Heisenberg 기사 수집...")
            items = fetch_heisenberg_articles(opener)
            if items:
                result = items[:2]
                print(f"  → AI/테크 {len(result)}건 선택 (Heisenberg)")
                return result

    # ── AI타임스 (폴백) ──
    print("  [수집] AI타임스 RSS...")
    items = parse_rss(http_get("https://www.aitimes.com/rss/allArticle.xml"))
    if len(items) < 2:
        print("  [수집] 인공지능신문 RSS (보완)...")
        items += parse_rss(http_get("https://www.aitimes.kr/rss/allArticle.xml"))
    result = [{"title": i["title"], "link": i["link"], "category": "AI", "source": "AI타임스"} for i in items[:2]]
    print(f"  → AI/테크 {len(result)}건 선택")
    return result


def fetch_stock_article() -> list[dict]:
    """매일경제/한국경제 RSS에서 주식 관련성 높은 기사 1건 선택."""
    print("  [수집] 매일경제 증권 RSS...")
    items = parse_rss(http_get(RSS_MK_STOCK))
    if len(items) < 3:
        print("  [수집] 한국경제 증권 RSS (보완)...")
        items += parse_rss(http_get(RSS_HK_STOCK))

    def score(item):
        t = item["title"]
        return sum(1 for kw in STOCK_KEYWORDS if kw in t)

    items.sort(key=score, reverse=True)
    if not items:
        return []
    best = items[0]
    print(f"  → 주식 선택: {best['title'][:40]}...")
    return [{"title": best["title"], "link": best["link"], "category": "경제·주식"}]


# ════════════════════════════════════════════════════════════
# 2. 기사 본문 fetch + HTML 정제
# ════════════════════════════════════════════════════════════

def fetch_article_body(url: str, max_chars: int = 3000) -> str:
    """기사 URL 방문해 본문 텍스트 추출 (max_chars 제한)."""
    html = http_get(url)
    if not html:
        return ""
    # 스크립트·스타일 제거
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    # 태그 제거
    text = re.sub(r"<[^>]+>", " ", html)
    # 공백 정리
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


# ════════════════════════════════════════════════════════════
# 3. Claude API 호출
# ════════════════════════════════════════════════════════════

def call_claude(prompt: str, max_tokens: int = 1000) -> str:
    """Claude Haiku API 호출. 실패 시 빈 문자열."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text.strip()
    except Exception as e:
        print(f"  [Claude API 오류] {e}")
        return ""


def write_ai_article(title: str, url: str, body: str) -> str:
    """AI/테크 기사 한국어 아티클 작성."""
    prompt = f"""다음 기사를 읽고 한국어 큐레이터 아티클을 작성해줘.

[원문 제목] {title}
[원문 URL] {url}
[원문 내용]
{body}

[독자 수준]
- 지적 호기심이 강하지만 이 분야 전문가가 아닌 일반 독자
- 전문 용어가 처음 등장할 때 괄호 안에 한 줄 설명 필수
  예) HBM(고대역폭 메모리 — AI GPU용 초고속 반도체)
- 비유·아날로지를 한 곳 이상 사용할 것

[작성 규칙]
- 1인칭 큐레이터 톤 (설명이 아닌 공유하는 태도)
- "~를 알아보겠습니다" 강의 말투 절대 금지
- "놀랍게도!", "충격적인" 과장 표현 금지
- 원문에 없는 수치나 사실 추가 금지
- 번역투 문장 금지 — 한국어로 다시 쓴다는 감각으로

[섹션별 작성 기준]

## 한 줄 요약
→ "~했다"가 아니라 "~로, ~가 가능해졌다"처럼 의미·함의까지 담은 한 문장

## 리드 — 왜 지금 이게 중요한가?
→ 첫 문장은 반드시 구체적 수치나 팩트로 시작
→ 2~3문장. 이 사건이 지금 왜 주목받는지까지 설명

## 배경 — 기존에는 어땠나?
→ 이 기술·사건 이전의 업계 '상식'이나 '관행'을 먼저 서술
→ 그 상식이 왜 문제였는지 — 비용, 속도, 정확도, 한계 구체적으로
→ 2~3문단. 비전문가도 "아, 그래서 이게 필요했구나" 느낄 수 있도록

## 핵심 — 무엇이 다른가?
→ 동작 원리를 단계별로 설명
→ 기존 방식과의 차이를 표로 정리 (항목 3~4개):
   | 항목 | 기존 방식 | 새로운 방식 |
→ 전문 용어 첫 등장 시 즉시 괄호 설명 추가

## 시장 영향 — 어디에 쓰이나?
→ 벤치마크 수치를 불릿으로 정리
→ 실제 도입 기업명 명시 (있으면)
→ 어떤 산업·직군에 영향을 주는지

## 병규의 한 줄
→ "흥미롭다", "주목된다" 수준 금지
→ 이 기술이 담고 있는 설계 철학 또는 업계 패러다임 변화를 한 문장으로
→ 예) "이번에 흥미로운 건 수치보다 철학이다. '~라는 가정'을 이번에 깼다."

[분량 목표] 전체 1,000~1,500자 (한국어 기준)
"""
    return call_claude(prompt, max_tokens=1200)


def write_stock_article(title: str, url: str, body: str) -> str:
    """주식 영향 기사 대본 작성."""
    prompt = f"""다음 경제/주식 기사를 읽고 투자자 관점의 한국어 브리핑을 작성해줘.

[원문 제목] {title}
[원문 URL] {url}
[원문 내용]
{body}

[독자 수준]
- 주식에 관심 있지만 전문 투자자가 아닌 일반 독자
- 경제 용어 첫 등장 시 괄호 안에 간단한 설명 추가
  예) HBM(AI GPU에 사용되는 고성능 메모리), 영업이익률(매출 대비 영업이익 비율)
- 수치가 나오면 그게 왜 중요한지 한 줄 설명 추가

[작성 규칙]
- 팩트와 수치 중심, 뉴스 앵커 톤
- 투자 권유 절대 금지
- 과장 표현 금지
- 원문에 없는 내용 추가 금지

[섹션별 작성 기준]

## 한 줄 요약
→ 이 뉴스가 시장에 미치는 영향을 한 문장으로. 수치 포함 권장

## 배경 — 왜 이 뉴스가 나왔나?
→ 이 기사의 배경 상황 설명 (2~3문장)
→ 왜 지금 이 이슈가 중요한지 — 비전문가도 이해할 수 있도록

## 주식 영향 분석
- **영향 방향**: 긍정 / 부정 / 중립
- **관련 업종·종목**: (해당 종목 코드 포함하면 더 좋음)
- **핵심 근거**: 원문 수치 기반으로 2~3문장

## 오늘의 대본 (30~45초 분량)
[인트로] 핵심 수치나 사건으로 시작. 1~2문장.

[본문] 배경과 구체적 영향. 수치 포함. 3~4문장.

[마무리] 시장 시사점 또는 앞으로 볼 것. 1문장.

*이 내용은 정보 제공 목적이며 투자 권유가 아닙니다.*

[분량 목표] 전체 800~1,200자 (한국어 기준)
"""
    return call_claude(prompt, max_tokens=1100)


# ════════════════════════════════════════════════════════════
# 4. 마크다운 → HTML 변환 (이메일용 인라인 스타일)
# ════════════════════════════════════════════════════════════

def md_to_html(md: str) -> str:
    """아티클 마크다운을 이메일용 HTML로 변환."""
    lines = md.split("\n")
    html_parts = []
    in_list = False

    for line in lines:
        # 이미지 ![alt](url)
        img_m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', line.strip())
        if img_m:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            alt = esc(img_m.group(1))
            url = img_m.group(2)
            html_parts.append(
                f'<img src="{url}" alt="{alt}" style="max-width:100%;height:auto;'
                f'border-radius:8px;display:block;margin:16px auto;'
                f'box-shadow:0 2px 8px rgba(0,0,0,0.12);">'
            )
            if alt:
                html_parts.append(
                    f'<p style="text-align:center;font-size:12px;color:#9CA3AF;'
                    f'margin:-8px 0 16px;">{alt}</p>'
                )
            continue

        # H2 섹션
        if line.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            heading = line[3:].strip()
            html_parts.append(
                f'<h3 style="font-size:13px;font-weight:700;color:#6D28D9;'
                f'text-transform:uppercase;letter-spacing:0.05em;'
                f'margin:20px 0 6px;border-bottom:1px solid #EDE9FE;padding-bottom:6px;">'
                f'{esc(heading)}</h3>'
            )

        # Blockquote (> ...)
        elif line.startswith("> "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            text = inline_md(line[2:].strip())
            html_parts.append(
                f'<blockquote style="margin:8px 0;padding:10px 16px;'
                f'background:#F5F3FF;border-left:4px solid #7C3AED;'
                f'border-radius:0 6px 6px 0;color:#374151;font-size:14px;'
                f'font-style:normal;">{text}</blockquote>'
            )

        # 목록 항목
        elif line.startswith("- ") or line.startswith("* "):
            if not in_list:
                html_parts.append('<ul style="margin:6px 0;padding-left:20px;">')
                in_list = True
            text = inline_md(line[2:].strip())
            html_parts.append(
                f'<li style="margin:3px 0;font-size:14px;color:#374151;">{text}</li>'
            )

        # 빈 줄
        elif not line.strip():
            if in_list:
                html_parts.append("</ul>")
                in_list = False

        # 일반 문단
        elif line.strip():
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            text = inline_md(line.strip())
            html_parts.append(
                f'<p style="margin:6px 0;font-size:14px;line-height:1.7;color:#374151;">'
                f'{text}</p>'
            )

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def inline_md(text: str) -> str:
    """**bold**, *italic* 인라인 처리 + HTML 이스케이프."""
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ════════════════════════════════════════════════════════════
# 5. HTML 이메일 빌드
# ════════════════════════════════════════════════════════════

CAT_COLOR = {
    "AI":       {"bg": "#7C3AED", "light": "#F5F3FF"},
    "경제·주식": {"bg": "#0F766E", "light": "#F0FDF9"},
}

def build_email_html(articles: list[dict]) -> str:
    """완성된 아티클 목록으로 HTML 이메일 생성."""

    def article_block(art: dict, idx: int) -> str:
        cat    = art.get("category", "AI")
        color  = CAT_COLOR.get(cat, CAT_COLOR["AI"])
        title  = esc(art.get("title", ""))
        src    = esc(art.get("source", ""))
        url    = art.get("link", "#")
        body   = md_to_html(art.get("content", "내용을 불러올 수 없습니다."))
        num    = f"0{idx}" if idx < 10 else str(idx)

        return f"""
        <!-- Article {idx} -->
        <tr><td style="padding:0 0 20px 0;">
          <table width="100%" cellpadding="0" cellspacing="0" style="
            background:#FFFFFF;border-radius:12px;
            box-shadow:0 1px 4px rgba(0,0,0,0.08);overflow:hidden;">
            <tr>
              <td style="padding:20px 24px 0 24px;">
                <!-- 번호 + 카테고리 -->
                <table cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="font-size:11px;font-weight:700;color:#D1D5DB;
                      letter-spacing:0.1em;padding-right:10px;">#{num}</td>
                    <td><span style="display:inline-block;padding:3px 10px;
                      background:{color["bg"]};color:#FFFFFF;
                      border-radius:999px;font-size:11px;font-weight:700;
                      letter-spacing:0.05em;">{esc(cat)}</span></td>
                  </tr>
                </table>
                <!-- 제목 -->
                <h2 style="margin:10px 0 4px;font-size:18px;font-weight:800;
                  color:#111827;line-height:1.4;">{title}</h2>
                <!-- 출처 -->
                <p style="margin:0 0 16px;font-size:12px;color:#9CA3AF;">
                  {src} &nbsp;·&nbsp; {TODAY_ISO}</p>
                <!-- 구분선 -->
                <hr style="border:none;border-top:1px solid #F3F4F6;margin:0 0 16px;">
              </td>
            </tr>
            <tr>
              <td style="padding:0 24px 16px 24px;">
                {body}
              </td>
            </tr>
            <tr>
              <td style="padding:0 24px 20px 24px;">
                <a href="{url}" style="display:inline-block;font-size:12px;
                  color:{color["bg"]};text-decoration:none;
                  border:1px solid {color["bg"]};padding:5px 14px;
                  border-radius:6px;">원문 보기 →</a>
              </td>
            </tr>
          </table>
        </td></tr>"""

    articles_html = "\n".join(article_block(a, i+1) for i, a in enumerate(articles))

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>병규의 한입뉴스 — {TODAY_STR}</title>
</head>
<body style="margin:0;padding:0;background:#F3F4F6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo',sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#F3F4F6;">
<tr><td align="center" style="padding:32px 16px;">

  <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

    <!-- 헤더 -->
    <tr><td style="padding:0 0 20px 0;">
      <table width="100%" cellpadding="0" cellspacing="0"
        style="background:#111827;border-radius:12px;overflow:hidden;">
        <tr>
          <td style="padding:28px 32px 24px;">
            <p style="margin:0 0 4px;font-size:11px;font-weight:700;
              color:#7C3AED;letter-spacing:0.15em;text-transform:uppercase;">
              DAILY BRIEFING</p>
            <h1 style="margin:0 0 6px;font-size:26px;font-weight:800;color:#FFFFFF;">
              병규의 한입뉴스</h1>
            <p style="margin:0;font-size:14px;color:#9CA3AF;">{TODAY_STR}</p>
          </td>
          <td align="right" style="padding:28px 32px 24px;">
            <span style="display:inline-block;background:#1F2937;
              border-radius:8px;padding:10px 16px;text-align:center;">
              <span style="display:block;font-size:24px;font-weight:800;
                color:#7C3AED;">4</span>
              <span style="display:block;font-size:10px;color:#6B7280;
                letter-spacing:0.05em;">TODAY'S PICKS</span>
            </span>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding:0 32px 20px;">
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding-right:16px;">
                  <span style="display:inline-block;width:8px;height:8px;
                    background:#7C3AED;border-radius:50%;margin-right:6px;"></span>
                  <span style="font-size:12px;color:#9CA3AF;">MIT·AI·테크 3건</span>
                </td>
                <td>
                  <span style="display:inline-block;width:8px;height:8px;
                    background:#0F766E;border-radius:50%;margin-right:6px;"></span>
                  <span style="font-size:12px;color:#9CA3AF;">경제·주식 1건</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td></tr>

    <!-- 기사 목록 -->
    {articles_html}

    <!-- 푸터 -->
    <tr><td>
      <table width="100%" cellpadding="0" cellspacing="0"
        style="background:#1F2937;border-radius:12px;">
        <tr>
          <td style="padding:20px 24px;text-align:center;">
            <p style="margin:0 0 4px;font-size:13px;font-weight:700;color:#FFFFFF;">
              병규의 한입뉴스</p>
            <p style="margin:0 0 12px;font-size:12px;color:#6B7280;">
              과학기술의 핵심만 한 입에.</p>
            <p style="margin:0;font-size:11px;color:#4B5563;">
              © {TODAY.year} 병규의 한입뉴스. 모든 콘텐츠의 저작권은 원문 출처에 있습니다.<br>
              이 이메일은 정보 제공 목적이며 투자 권유가 아닙니다.
            </p>
          </td>
        </tr>
      </table>
    </td></tr>

  </table>
</td></tr>
</table>

</body>
</html>"""


# ════════════════════════════════════════════════════════════
# 6. 이메일 발송
# ════════════════════════════════════════════════════════════

def load_today_articles() -> list[dict]:
    """오늘 날짜의 기사를 web/posts.json + web/posts/*.md 에서 읽어 반환."""
    posts_json = ROOT / "web" / "posts.json"
    posts_dir  = ROOT / "web" / "posts"
    if not posts_json.exists():
        return []

    with open(posts_json, encoding="utf-8") as f:
        data = json.load(f)

    articles = []
    for meta in data.get("posts", []):
        if meta.get("date") != TODAY_ISO:
            continue
        md_file = posts_dir / meta["filename"]
        if not md_file.exists():
            continue

        text = md_file.read_text(encoding="utf-8")
        # 프론트매터 제거
        body = re.sub(r"^---[\s\S]*?---\s*\n", "", text).strip()

        articles.append({
            "title":    meta.get("title", ""),
            "category": meta.get("category", "AI"),
            "source":   meta.get("source", ""),
            "link":     meta.get("sourceUrl", "#"),
            "content":  body,
        })

    return articles


def send_email(html: str, subject: str) -> bool:
    """Gmail SMTP로 HTML 이메일 발송."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        print(f"  [OK] 이메일 발송 완료 -> {RECIPIENT_EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  [FAIL] Gmail 인증 실패. emailer_config.py 의 앱 비밀번호를 확인하세요.")
        return False
    except Exception as e:
        print(f"  [FAIL] 이메일 발송 실패: {e}")
        return False


# ════════════════════════════════════════════════════════════
# 7. 메인 실행
# ════════════════════════════════════════════════════════════

def main():
    dry_run     = "--dry-run"     in sys.argv
    send_today  = "--send-today"  in sys.argv   # 기존 _posts 기사로 이메일 발송

    # ── --send-today: 새로 수집하지 않고 오늘 작성된 기사만 이메일 발송 ──
    if send_today:
        print(f"\n{'='*50}")
        print(f"병규의 한입뉴스 (오늘 기사 발송) / {TODAY_STR}")
        print(f"{'='*50}\n")
        all_articles = load_today_articles()
        if not all_articles:
            print(f"오류: {TODAY_ISO} 날짜 기사가 없습니다.")
            sys.exit(1)
        print(f"  → 오늘 기사 {len(all_articles)}건 로드")
        subject = f"한입뉴스 브리핑 — {TODAY_STR}"
        html    = build_email_html(all_articles)
        if dry_run:
            preview_path = ROOT / "tools" / f"preview_{TODAY_ISO}.html"
            preview_path.write_text(html, encoding="utf-8")
            print(f"\n[dry-run] 미리보기: {preview_path}")
        else:
            send_email(html, subject)
        print(f"\n완료!")
        return

    # ── 일반 모드: RSS 수집 → Claude 작성 → 발송 ──
    if not ANTHROPIC_API_KEY:
        print("오류: ANTHROPIC_API_KEY 가 설정되지 않았습니다.")
        print("  → tools/emailer_config.py 에 API 키를 입력하세요.")
        sys.exit(1)
    print(f"\n{'='*50}")
    print(f"병규의 한입뉴스 자동 발송 / {TODAY_STR}")
    print(f"{'='*50}\n")

    # ── 기사 선택 (MIT 0~1 + AI/테크 2 + 주식 1 = 3~4건) ──
    print("[1/3] 기사 선택 중...")
    mit_articles   = fetch_mit_article()       # 없으면 skip
    ai_articles    = fetch_ai_articles()       # 2건
    stock_articles = fetch_stock_article()     # 1건
    all_articles   = mit_articles + ai_articles + stock_articles

    if not all_articles:
        print("오류: 수집된 기사가 없습니다.")
        sys.exit(1)
    print(f"  → 총 {len(all_articles)}건 선택 (MIT {len(mit_articles)} + AI {len(ai_articles)} + 주식 {len(stock_articles)})")

    # ── 본문 fetch + Claude 아티클 작성 ──
    print(f"\n[2/3] 아티클 작성 중 ({len(all_articles)}건)...")
    for art in all_articles:
        print(f"  → {art['title'][:50]}...")
        body = fetch_article_body(art["link"])

        if art["category"] == "경제·주식":
            src_name = "매일경제" if "mk.co.kr" in art["link"] else "한국경제"
            art["source"]  = src_name
            art["content"] = write_stock_article(art["title"], art["link"], body)
        else:
            if art.get("source"):          # MIT 등 이미 소스명이 지정된 경우
                src_name = art["source"]
            elif "technologyreview" in art["link"]:
                src_name = "MIT Technology Review"
            else:
                src_name = "AI타임스"
            art["source"]  = src_name
            art["content"] = write_ai_article(art["title"], art["link"], body)

    # ── HTML 이메일 생성 ──
    print("\n[3/3] HTML 이메일 생성 중...")
    html    = build_email_html(all_articles)
    subject = f"한입뉴스 브리핑 — {TODAY_STR}"

    if dry_run:
        # 미리보기 파일 저장
        preview_path = ROOT / "tools" / f"preview_{TODAY_ISO}.html"
        preview_path.write_text(html, encoding="utf-8")
        print(f"\n[dry-run] HTML 미리보기 저장: {preview_path}")
        print("브라우저에서 위 파일을 열어 이메일 디자인을 확인하세요.")
    else:
        # 이메일 발송
        send_email(html, subject)

    print(f"\n완료!")


if __name__ == "__main__":
    main()
