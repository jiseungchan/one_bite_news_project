"""
fix_images.py — 기사 카드 사진을 '기사와 관련된 사진'으로 맞춘다 (LLM 토큰 0, 표준 라이브러리만)

규칙
  1. 원문(sourceUrl) 페이지가 실제로 열리면(HTTP 200) 그 기사에 첨부된 대표 사진
     (og:image → twitter:image → 본문 첫 사진)을 쓴다. 로고·기본 이미지는 제외.
  2. 원문 사진이 없거나 열리지 않으면 글 내용(제목·요약·분야)으로 카드 이미지를 만든다.
     → web/images/cards/<이름>.svg  (주제 그림 + 핵심 키워드 + 한 줄 제목)
  3. 모든 글에 만든 카드(imageFallback)를 함께 기록해, 원문 사진이 나중에 깨져도 카드로 대체된다.
  Unsplash·picsum 같은 관련 없는 무료 사진은 쓰지 않는다.

사용법 (프로젝트 루트에서)
  python tools/fix_images.py                 # 사진이 아직 정리되지 않은 글만
  python tools/fix_images.py --all           # 전체 다시 판정
  python tools/fix_images.py 2026-11-28-x.md # 특정 글만
  python tools/fix_images.py --offline       # 원문 조회 없이 카드만 생성
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_JSON = ROOT / "web" / "posts.json"
CARD_DIR = ROOT / "web" / "images" / "cards"
SITE = "https://jiseungchan.github.io/one_bite_news_project/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
STOCK_HOSTS = ("images.unsplash.com", "picsum.photos", "source.unsplash.com")
BAD_IMAGE_WORDS = ("logo", "default", "placeholder", "noimage", "no_image", "blank", "favicon", "sns_share")

CAT_COLORS = {  # CLAUDE.md 카테고리 색상
    "AI": "#7C3AED", "바이오": "#059669", "나노·소재": "#D97706", "물리·우주": "#0284C7",
    "에너지": "#16A34A", "경제·주식": "#0F766E", "이번 주 픽": "#DC2626",
}


# ───────────────────────── 원문 사진 찾기 ─────────────────────────
def fetch(url: str, timeout: int = 12, referer: str | None = None, max_bytes: int = 600_000):
    headers = {"User-Agent": UA, "Accept-Language": "ko,en;q=0.8"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read(max_bytes), r.geturl()


def is_article_url(url: str) -> bool:
    p = urllib.parse.urlparse(url)
    return p.scheme in ("http", "https") and len(p.path.strip("/")) > 3 or bool(p.query)


def find_source_image(url: str, post_text: str | None = None) -> str | None:
    if not is_article_url(url):
        return None  # 사이트 첫 화면 주소면 그 기사 사진이 아니다
    try:
        status, ctype, body, final = fetch(url)
    except Exception:
        return None
    if status != 200 or "html" not in ctype:
        return None
    if urllib.parse.urlparse(final).path.strip("/") in ("", "index.html"):
        return None  # 없는 기사라 첫 화면으로 돌려보낸 경우
    text = body.decode("utf-8", errors="ignore")
    page_title = ""
    for pat in (r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:title',
                r"<title[^>]*>([^<]+)</title>"):
        mt = re.search(pat, text, re.I)
        if mt:
            page_title = html.unescape(mt.group(1)).strip()
            break
    if post_text is not None and not related(page_title, post_text):
        return None  # 주소는 열리지만 다른 기사(잘못된 출처 주소)다
    cands = []
    for prop in ("og:image", "og:image:url", "twitter:image", "twitter:image:src"):
        for m in re.finditer(r"<meta[^>]+>", text, re.I):
            tag = m.group(0)
            if re.search(r'(?:property|name)\s*=\s*["\']' + re.escape(prop) + r'["\']', tag, re.I):
                c = re.search(r'content\s*=\s*["\']([^"\']+)', tag, re.I)
                if c:
                    cands.append(c.group(1))
    art = re.search(r"<article[\s\S]*?</article>", text, re.I)
    if art:
        cands += re.findall(r'<img[^>]+src\s*=\s*["\']([^"\']+)', art.group(0), re.I)[:3]
    for c in cands:
        img = urllib.parse.urljoin(final, html.unescape(c.strip()))
        low = img.lower()
        if not low.startswith("http") or any(w in low for w in BAD_IMAGE_WORDS):
            continue
        if low.endswith((".svg", ".gif", ".ico")):
            continue
        if image_ok(img):
            return img
    return None


STOP = set("the a an of to in on for and with from is are as at by its it this that how why what new will "
           "has have more than into over after about says said 기자 뉴스 단독 속보 오늘 공개 발표".split())


def tokens(s: str) -> set[str]:
    s = s.lower()
    toks = set(re.findall(r"[a-z][a-z0-9\-]{2,}|\d[\d.,]*\d|\d", s)) | set(re.findall(r"[가-힣]{2,}", s))
    return {t for t in toks if t not in STOP}


def related(page_title: str, post_text: str) -> bool:
    """원문 페이지 제목의 핵심 단어가 우리 글(제목·요약·본문)에 충분히 나오는지."""
    pt = tokens(re.split(r"\s[|\-–—]\s(?=[^|\-–—]*$)", page_title)[0])  # '… | 매체명' 꼬리 제거
    if len(pt) < 2:
        return False
    body = post_text.lower()
    hit = 0
    for t in pt:
        if t in body or (re.fullmatch(r"[가-힣]+", t) and len(t) >= 3 and t[:2] in body):
            hit += 1
    return hit >= 2 and hit / len(pt) >= 0.3


def image_ok(url: str) -> bool:
    """사이트에서 직접 불러와도 보이는지(핫링크 차단 여부 포함) 확인."""
    try:
        status, ctype, body, _ = fetch(url, referer=SITE, max_bytes=4096)
        return status == 200 and ctype.startswith("image/") and len(body) > 1000
    except Exception:
        return False


# ───────────────────────── 카드 이미지 만들기 ─────────────────────────
MOTIFS = [  # (그림, 키워드) — 위에서부터 먼저 맞는 것
    ("chip", "반도체 HBM 메모리 D램 DRAM 낸드 NAND 파운드리 웨이퍼 GPU 칩 TSMC 하이닉스 마이크론 엔비디아 2나노 3나노 EUV ASML 패키징"),
    ("globe", "수출통제 수출 라이선스 우회 관세 미중 무역 제재 국제 외교 정상회담 백악관 EU 중국 대만 일본 전쟁 지정학 동맹"),
    ("gavel", "규제 법안 기본법 법원 판결 소송 저작권 정책 정부 국회 의회 행정명령 위원회"),
    ("chart", "코스피 코스닥 증시 주가 지수 실적 영업이익 매출 시총 나스닥 금리 환율 투자 상장 IPO 펀드 ETF 목표주가 연준"),
    ("robot", "로봇 휴머노이드 자율주행 드론 피지컬"),
    ("bolt", "에너지 전력 배터리 원전 데이터센터 전기 태양광 수소 냉각 그리드"),
    ("dna", "바이오 단백질 의료 신약 유전 헬스케어 병원 진단 세포"),
    ("rocket", "우주 위성 로켓 양자 물리 핵융합 천문"),
    ("shield", "보안 해킹 안전 프라이버시 사이버 딥페이크 허위"),
    ("phone", "스마트폰 갤럭시 아이폰 온디바이스 기기 PC 노트북"),
    ("code", "코딩 개발자 소프트웨어 오픈소스 깃허브 코드"),
    ("paper", "논문 연구진 연구원 과학 벤치마크 학계 실험 저널 해석가능성 발견"),
    ("chat", "챗봇 비서 어시스턴트 가입자 이용자 대화 검색 음성 메신저"),
    ("people", "직원 인재 채용 일자리 고용 교육 인력 노동 유권자 경영진 CEO"),
    ("brain", "AI 인공지능 모델 LLM GPT 에이전트 클로드 제미나이 챗GPT 추론 학습 오픈AI 앤트로픽"),
]
ENTITIES = ("삼성전자 SK하이닉스 하이닉스 엔비디아 TSMC 인텔 AMD 마이크론 ASML 애플 구글 메타 아마존 "
            "마이크로소프트 오픈AI OpenAI 앤트로픽 Anthropic 네이버 카카오 LG SKT KT 현대차 테슬라 화웨이 "
            "딥시크 알리바바 바이두 퀄컴 브로드컴 코스피 나스닥 연준 백악관 트럼프 중국 미국 일본 대만 EU").split()
GENERIC = {"AI", "THE", "AND", "CEO", "IT", "US", "UN"}


def pick_motif(title: str, desc: str, category: str) -> str:
    """제목에 나온 주제어는 3점, 요약에 나온 주제어는 1점. 가장 높은 그림을 고른다."""
    t, d = title.lower(), desc.lower()
    best, best_score = None, 0
    for motif, words in MOTIFS:
        score = sum(3 * (w.lower() in t) + (w.lower() in d) for w in words.split())
        if motif == "brain":
            score = min(score, 1)  # 'AI'는 거의 모든 글에 나오므로 다른 주제가 없을 때만
        if score > best_score:
            best, best_score = motif, score
    if best:
        return best
    return {"바이오": "dna", "물리·우주": "rocket", "에너지": "bolt", "경제·주식": "chart",
            "나노·소재": "chip"}.get(category, "brain")


def keywords(title: str, desc: str) -> list[str]:
    found = []
    text = f"{title} {desc}"
    for e in ENTITIES:
        if e in text and e not in found and not any(e in f for f in found):
            found.append(e)
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9\-\.]*\d[A-Za-z0-9\-]*|[A-Z]{2,}[0-9A-Z\-]*", title):
        tok = tok.strip(".-")
        if tok.upper() not in GENERIC and tok not in found and len(tok) <= 12:
            found.append(tok)
    found.sort(key=lambda k: text.find(k))
    return found[:3]


def headline(title: str) -> list[str]:
    main = re.split(r"\s[—–\-]\s|\s?[—–]\s?", title)[0].strip().strip("'\"‘’“”")
    lines, cur = [], ""
    for w in main.split():
        if len(cur) + len(w) + 1 > 15 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    if len(lines) > 2:
        lines = lines[:2]
        lines[1] = lines[1][:13].rstrip() + "…"
    return [l if len(l) <= 17 else l[:16] + "…" for l in lines]


def shade(hex_color: str, f: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f < 0:
        r, g, b = (int(c * (1 + f)) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def motif_svg(m: str, seed: int) -> str:
    """오른쪽 영역(가로 470~800)에 주제 그림. 흰색 선·면, 투명도로 깊이감."""
    W = 'stroke="#fff" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    rnd = lambda i, a, b: a + (seed >> (i % 24) & 0xFF) / 255 * (b - a)  # noqa: E731
    if m == "chip":
        pins = "".join(
            f'<line x1="{575 + i * 30}" y1="95" x2="{575 + i * 30}" y2="125" {W} stroke-width="6" opacity=".8"/>'
            f'<line x1="{575 + i * 30}" y1="325" x2="{575 + i * 30}" y2="355" {W} stroke-width="6" opacity=".8"/>'
            f'<line x1="505" y1="{160 + i * 30}" x2="535" y2="{160 + i * 30}" {W} stroke-width="6" opacity=".8"/>'
            f'<line x1="745" y1="{160 + i * 30}" x2="775" y2="{160 + i * 30}" {W} stroke-width="6" opacity=".8"/>'
            for i in range(5))
        return (f'{pins}<rect x="535" y="125" width="210" height="200" rx="18" fill="#fff" fill-opacity=".14" {W} stroke-width="6"/>'
                f'<rect x="585" y="175" width="110" height="100" rx="10" fill="#fff" fill-opacity=".28" {W} stroke-width="4"/>'
                f'<path d="M600 225h80M640 190v70" {W} stroke-width="3" opacity=".7"/>')
    if m == "globe":
        return (f'<circle cx="640" cy="225" r="135" fill="#fff" fill-opacity=".1" {W} stroke-width="6"/>'
                f'<ellipse cx="640" cy="225" rx="60" ry="135" {W} stroke-width="4" opacity=".8"/>'
                f'<path d="M505 225h270M525 160h230M525 290h230" {W} stroke-width="4" opacity=".7"/>'
                f'<path d="M560 110 Q640 {int(rnd(1, 40, 90))} 735 150" {W} stroke-width="5" stroke-dasharray="4 12"/>'
                f'<circle cx="560" cy="110" r="10" fill="#fff"/><circle cx="735" cy="150" r="10" fill="#fff"/>')
    if m == "gavel":
        return (f'<rect x="560" y="110" width="170" height="70" rx="14" transform="rotate(-30 645 145)" fill="#fff" fill-opacity=".25" {W} stroke-width="6"/>'
                f'<line x1="620" y1="190" x2="700" y2="330" {W} stroke-width="14"/>'
                f'<rect x="520" y="330" width="230" height="30" rx="8" fill="#fff" fill-opacity=".3" {W} stroke-width="5"/>')
    if m == "chart":
        ys = [int(rnd(i * 3, 120, 330)) for i in range(7)]
        ys[-1] = min(ys) - 10 if seed % 3 else max(ys) + 10
        ys[-1] = max(90, min(345, ys[-1]))
        pts = " ".join(f"{510 + i * 45},{y}" for i, y in enumerate(ys))
        bars = "".join(f'<rect x="{500 + i * 45}" y="{360 - h}" width="26" height="{h}" rx="4" fill="#fff" fill-opacity=".14"/>'
                       for i, h in enumerate(int(rnd(i * 5 + 2, 40, 150)) for i in range(7)))
        return (f'{bars}<polyline points="{pts}" {W} stroke-width="7"/>'
                f'<circle cx="{510 + 6 * 45}" cy="{ys[-1]}" r="12" fill="#fff"/>'
                f'<path d="M490 365h300" {W} stroke-width="4" opacity=".6"/>')
    if m == "robot":
        return (f'<rect x="555" y="120" width="170" height="140" rx="30" fill="#fff" fill-opacity=".16" {W} stroke-width="6"/>'
                f'<circle cx="605" cy="185" r="16" fill="#fff"/><circle cx="675" cy="185" r="16" fill="#fff"/>'
                f'<path d="M610 230h60" {W} stroke-width="6"/><path d="M640 120V85" {W} stroke-width="6"/><circle cx="640" cy="78" r="10" fill="#fff"/>'
                f'<rect x="580" y="270" width="120" height="85" rx="16" fill="#fff" fill-opacity=".1" {W} stroke-width="6"/>'
                f'<path d="M580 295l-50 40M700 295l50 40" {W} stroke-width="8"/>')
    if m == "bolt":
        return (f'<circle cx="640" cy="225" r="140" fill="#fff" fill-opacity=".08"/>'
                f'<path d="M665 85 570 245h70l-25 125 105-175h-72z" fill="#fff" fill-opacity=".85"/>'
                f'<path d="M500 225a140 140 0 0 1 60-115M780 225a140 140 0 0 1-60 115" {W} stroke-width="6" opacity=".6"/>')
    if m == "dna":
        rungs = "".join(f'<line x1="{560 + 14 * abs(3 - i % 7)}" y1="{95 + i * 26}" x2="{720 - 14 * abs(3 - i % 7)}" y2="{95 + i * 26}" {W} stroke-width="4" opacity=".55"/>'
                        for i in range(11))
        return (f'{rungs}<path d="M560 90 C720 160 560 230 720 300 S560 370 600 380" {W} stroke-width="8"/>'
                f'<path d="M720 90 C560 160 720 230 560 300 S720 370 680 380" {W} stroke-width="8" opacity=".75"/>')
    if m == "rocket":
        stars = "".join(f'<circle cx="{int(rnd(i * 2, 500, 790))}" cy="{int(rnd(i * 2 + 1, 70, 380))}" r="{2 + i % 3}" fill="#fff" opacity=".7"/>'
                        for i in range(10))
        return (f'{stars}<path d="M640 80c60 50 70 150 40 230h-80c-30-80-20-180 40-230z" fill="#fff" fill-opacity=".2" {W} stroke-width="6"/>'
                f'<circle cx="640" cy="190" r="24" {W} stroke-width="6"/>'
                f'<path d="M600 300l-40 50 50-10M680 300l40 50-50-10M620 320l20 50 20-50" {W} stroke-width="6"/>')
    if m == "shield":
        return (f'<path d="M640 85l120 45v90c0 80-55 135-120 160-65-25-120-80-120-160v-90z" fill="#fff" fill-opacity=".16" {W} stroke-width="7"/>'
                f'<path d="M590 230l35 35 70-80" {W} stroke-width="10"/>')
    if m == "phone":
        return (f'<rect x="575" y="80" width="140" height="285" rx="26" fill="#fff" fill-opacity=".14" {W} stroke-width="6"/>'
                f'<rect x="595" y="115" width="100" height="190" rx="8" fill="#fff" fill-opacity=".22"/>'
                f'<circle cx="645" cy="335" r="10" fill="#fff"/>'
                f'<path d="M735 150a60 60 0 0 1 0 90M760 125a95 95 0 0 1 0 140" {W} stroke-width="5" opacity=".7"/>')
    if m == "code":
        return (f'<rect x="505" y="95" width="275" height="260" rx="18" fill="#fff" fill-opacity=".12" {W} stroke-width="6"/>'
                f'<path d="M505 135h275" {W} stroke-width="4" opacity=".6"/>'
                f'<path d="M590 190l-40 40 40 40M695 190l40 40-40 40M660 175l-35 110" {W} stroke-width="9"/>')
    if m == "paper":
        lines = "".join(f'<path d="M585 {175 + i * 28}h{110 - (i % 3) * 25}" {W} stroke-width="5" opacity=".7"/>' for i, _ in enumerate(range(5)))
        return (f'<rect x="600" y="95" width="150" height="200" rx="10" fill="#fff" fill-opacity=".1" {W} stroke-width="5" opacity=".6"/>'
                f'<rect x="560" y="120" width="160" height="220" rx="12" fill="#fff" fill-opacity=".18" {W} stroke-width="6"/>'
                f'<path d="M585 150h80" {W} stroke-width="8"/>{lines}'
                f'<circle cx="720" cy="320" r="38" fill="#fff" fill-opacity=".25" {W} stroke-width="6"/><path d="M747 347l30 30" {W} stroke-width="10"/>')
    if m == "chat":
        return (f'<path d="M520 110h200a24 24 0 0 1 24 24v90a24 24 0 0 1-24 24H600l-45 35v-35h-35a24 24 0 0 1-24-24v-90a24 24 0 0 1 24-24z" fill="#fff" fill-opacity=".18" {W} stroke-width="6"/>'
                f'<circle cx="570" cy="180" r="10" fill="#fff"/><circle cx="620" cy="180" r="10" fill="#fff"/><circle cx="670" cy="180" r="10" fill="#fff"/>'
                f'<path d="M640 270h120a20 20 0 0 1 20 20v50a20 20 0 0 1-20 20h-30v28l-35-28h-55a20 20 0 0 1-20-20v-50a20 20 0 0 1 20-20z" fill="#fff" fill-opacity=".3" {W} stroke-width="5"/>')
    if m == "people":
        ppl = ""
        for i, (x, y, r) in enumerate([(560, 200, 30), (720, 200, 30), (640, 170, 40)]):
            ppl += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" fill-opacity="{.3 if i < 2 else .5}" {W} stroke-width="5"/>'
                    f'<path d="M{x - r * 1.7} {y + r * 3.6}a{r * 1.7} {r * 1.7} 0 0 1 {r * 3.4} 0" fill="#fff" fill-opacity="{.15 if i < 2 else .3}" {W} stroke-width="5"/>')
        return ppl
    # brain / AI network
    nodes = [(530, 140), (530, 225), (530, 310), (640, 110), (640, 190), (640, 260), (640, 340), (750, 180), (750, 270)]
    edges = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" {W} stroke-width="3" opacity="{.25 + ((seed >> (i % 20)) & 3) * .15:.2f}"/>'
                    for i, (a, b) in enumerate((a, b) for a in nodes for b in nodes if b[0] - a[0] == 110))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{13 if x == 640 else 11}" fill="#fff" fill-opacity="{.95 if (seed >> i) & 1 else .55}"/>'
                   for i, (x, y) in enumerate(nodes))
    return edges + dots


def clean_fill(svg: str) -> str:
    """선 기본값 fill="none"과 면 색 fill 이 한 태그에 겹치면 면 색만 남긴다."""
    return re.sub(r"<[^>]+>", lambda m: m.group(0).replace(' fill="none"', "")
                  if m.group(0).count(" fill=") > 1 else m.group(0), svg)


def make_card(post: dict) -> str:
    title, desc = post.get("title", ""), post.get("description", "")
    cat = post.get("category", "AI")
    base = CAT_COLORS.get(cat, "#7C3AED")
    seed = int(hashlib.md5(post["filename"].encode()).hexdigest()[:8], 16)
    motif = pick_motif(title, desc, cat)
    kws = keywords(title, desc)
    lines = headline(title)
    esc = lambda s: html.escape(s, quote=True)  # noqa: E731
    font = "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic','맑은 고딕',sans-serif"
    chips, x = [], 48
    for k in kws:
        w = 20 + int(sum(15 if ord(c) > 0x2E80 else 9.5 for c in k))
        chips.append(f'<rect x="{x}" y="300" width="{w}" height="38" rx="19" fill="#fff" fill-opacity=".18"/>'
                     f'<text x="{x + w / 2}" y="325" text-anchor="middle" font-size="17" font-weight="700" fill="#fff">{esc(k)}</text>')
        x += w + 10
    head = "".join(f'<text x="48" y="{170 + i * 50}" font-size="38" font-weight="800" fill="#fff">{esc(l)}</text>'
                   for i, l in enumerate(lines))
    date = esc(post.get("date", ""))
    src = esc((post.get("source") or "")[:24])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450" font-family="{font}">
<defs><linearGradient id="g" x1="0" y1="{(seed % 5) / 10}" x2="1" y2="{1 - (seed % 3) / 10}"><stop offset="0" stop-color="{shade(base, -0.45)}"/><stop offset="1" stop-color="{shade(base, 0.05)}"/></linearGradient></defs>
<rect width="800" height="450" fill="url(#g)"/>
<circle cx="{640 + seed % 60}" cy="{60 + seed % 50}" r="190" fill="#fff" fill-opacity=".05"/>
<g>{clean_fill(motif_svg(motif, seed))}</g>
<rect x="48" y="72" width="{24 + len(cat) * 17}" height="32" rx="6" fill="#fff" fill-opacity=".22"/>
<text x="60" y="94" font-size="17" font-weight="700" fill="#fff">{esc(cat)}</text>
{head}
{"".join(chips)}
<text x="48" y="400" font-size="15" fill="#fff" fill-opacity=".75">{date}{" · " + src if src else ""} · 한입뉴스</text>
</svg>
'''


def card_name(filename: str) -> str:
    stem = Path(filename).stem
    if re.fullmatch(r"[A-Za-z0-9._\-]+", stem):
        return stem + ".svg"
    return stem[:10] + "-" + hashlib.md5(stem.encode()).hexdigest()[:10] + ".svg"


# ───────────────────────── 글 갱신 ─────────────────────────
def set_frontmatter_image(path: Path, image: str):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return
    fm = m.group(1)
    line = f'image: "{image}"'
    fm2 = re.sub(r"(?m)^image:.*$", line, fm) if re.search(r"(?m)^image:", fm) else fm + "\n" + line
    if fm2 != fm:
        path.write_text(text[:m.start(1)] + fm2 + text[m.end(1):], encoding="utf-8")


def needs_work(p: dict) -> bool:
    img = p.get("image", "")
    host = urllib.parse.urlparse(img).netloc
    return (not img) or host in STOCK_HOSTS or not p.get("imageFallback")


def process(p: dict, offline: bool) -> tuple[dict, str]:
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    name = card_name(p["filename"])
    (CARD_DIR / name).write_text(make_card(p), encoding="utf-8")
    card = f"images/cards/{name}"
    current = p.get("image", "")
    # 사람이 직접 넣은 사진만 유지 후보 (이 도구가 넣은 사진은 매번 다시 판정)
    keep_current = current and p.get("imageType") in (None, "kept") \
        and urllib.parse.urlparse(current).netloc not in STOCK_HOSTS \
        and not current.startswith("images/cards/")
    md = ROOT / "_posts" / p["filename"]
    post_text = " ".join([p.get("title", ""), p.get("description", ""),
                          md.read_text(encoding="utf-8") if md.exists() else ""])
    src_img = None if offline else find_source_image(p.get("sourceUrl", ""), post_text)
    if src_img:
        image, kind = src_img, "source"
    elif keep_current and (offline or image_ok(current)):
        image, kind = current, "kept"
    else:
        image, kind = card, "card"
    p["image"], p["imageFallback"], p["imageType"] = image, card, kind
    for d in ("_posts", "web/posts"):
        set_frontmatter_image(ROOT / d / p["filename"], image)
    return p, kind


def main(argv: list[str]) -> int:
    offline = "--offline" in argv
    targets = [a for a in argv if a.endswith(".md")]
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    posts = data["posts"]
    if targets:
        todo = [p for p in posts if p["filename"] in targets]
    elif "--all" in argv:
        todo = posts
    else:
        todo = [p for p in posts if needs_work(p)]
    stats = {"source": 0, "kept": 0, "card": 0}
    with ThreadPoolExecutor(max_workers=12) as ex:
        for _, kind in ex.map(lambda p: process(p, offline), todo):
            stats[kind] += 1
    # 여러 글이 같은 원문 사진을 쓰면 매체 기본 이미지로 보고 카드로 바꾼다
    count: dict[str, int] = {}
    for p in posts:
        if p.get("imageType") == "source":
            count[p["image"]] = count.get(p["image"], 0) + 1
    for p in posts:
        if p.get("imageType") == "source" and count[p["image"]] >= 3:
            p["image"], p["imageType"] = p["imageFallback"], "card"
            stats["source"] -= 1
            stats["card"] += 1
            for d in ("_posts", "web/posts"):
                set_frontmatter_image(ROOT / d / p["filename"], p["image"])
    POSTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"처리 {len(todo)}건 — 원문 사진 {stats['source']} · 기존 유지 {stats['kept']} · 내용 기반 카드 {stats['card']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
