#!/usr/bin/env python3
"""RSS 수집 스크립트 — stock-service 파이프라인 Phase 1

GitHub Actions에서 실행되어 15개 RSS 피드에서 오늘 기사를 수집하고
stock-service/_pipeline/stock-01-rss-pool.md 에 저장한다.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

KST = timezone(timedelta(hours=9))
TODAY_KST = datetime.now(KST).strftime("%Y-%m-%d")

FEEDS = [
    ("한국경제 주식",        "https://www.hankyung.com/feed/stock",                     "IT/전자"),
    ("한국경제 IT",          "https://www.hankyung.com/feed/it",                         "IT"),
    ("한국경제 경제",        "https://www.hankyung.com/feed/economy",                    "경제"),
    ("한국경제 산업",        "https://www.hankyung.com/feed/industry",                   "산업"),
    ("매일경제 경제",        "https://www.mk.co.kr/rss/30000001/",                       "경제"),
    ("매일경제 IT/과학",     "https://www.mk.co.kr/rss/30100041/",                       "IT/과학"),
    ("매일경제 부동산/금융", "https://www.mk.co.kr/rss/40300001/",                       "부동산/금융"),
    ("매일경제 증권/기업",   "https://www.mk.co.kr/rss/50200011/",                       "증권/기업"),
    ("Reuters Business",     "https://feeds.reuters.com/reuters/businessNews",           "비즈니스"),
    ("Reuters Technology",   "https://feeds.reuters.com/reuters/technologyNews",         "기술"),
    ("Reuters Company",      "https://feeds.reuters.com/reuters/companyNews",            "기업"),
    ("Bloomberg Markets",    "https://feeds.bloomberg.com/markets/news.rss",             "시장"),
    ("Bloomberg Technology", "https://feeds.bloomberg.com/technology/news.rss",         "기술"),
    ("Bloomberg Energy",     "https://feeds.bloomberg.com/energy/news.rss",             "에너지"),
    ("Bloomberg Economics",  "https://feeds.bloomberg.com/economics/news.rss",          "경제"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%a, %d %b %Y %H:%M:%S GMT",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d %H:%M:%S",
]

ATOM_NS = "http://www.w3.org/2005/Atom"


def fetch(url: str) -> bytes | None:
    req = Request(url, headers=HEADERS)
    try:
        with urlopen(req, timeout=15) as resp:
            return resp.read()
    except HTTPError as e:
        print(f"  HTTP {e.code}: {url}", file=sys.stderr)
    except URLError as e:
        print(f"  연결 실패: {url} — {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"  오류: {url} — {e}", file=sys.stderr)
    return None


def parse_date(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(KST).strftime("%Y-%m-%d")
        except ValueError:
            continue
    m = re.search(r"(\d{4}-\d{2}-\d{2})", raw)
    return m.group(1) if m else None


def is_today(date_str: str | None) -> bool:
    """날짜 불명확하면 포함 (보수적)."""
    return date_str is None or date_str == TODAY_KST


def parse_feed(content: bytes, source: str, section: str) -> list[dict]:
    articles = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"  XML 파싱 오류 ({source}): {e}", file=sys.stderr)
        return articles

    # RSS 2.0
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        date  = parse_date(item.findtext("pubDate"))
        if title and link and is_today(date):
            articles.append({"title": title, "link": link,
                             "source": source, "section": section})

    # Atom (fallback)
    if not articles:
        for entry in root.findall(f".//{{{ATOM_NS}}}entry"):
            title = (entry.findtext(f"{{{ATOM_NS}}}title") or "").strip()
            link_el = entry.find(f"{{{ATOM_NS}}}link")
            link  = (link_el.get("href", "") if link_el is not None else "").strip()
            pub   = entry.find(f"{{{ATOM_NS}}}published") or entry.find(f"{{{ATOM_NS}}}updated")
            date  = parse_date(pub.text if pub is not None else None)
            if title and link and is_today(date):
                articles.append({"title": title, "link": link,
                                 "source": source, "section": section})
    return articles


def build_markdown(articles: list[dict], feed_status: list[str], success: int) -> str:
    lines = [
        "# RSS 수집 결과",
        f"수집일: {TODAY_KST}",
        f"수집 피드: {success}개 / {len(FEEDS)}개 성공",
        f"총 기사: {len(articles)}건",
        "",
        "## 피드별 수집 상태",
        "",
        "| 소스 | URL | 상태 |",
        "|------|-----|------|",
        *feed_status,
        "",
        "## 기사 목록",
        "",
        "| # | 제목 | 출처 | 섹션 | 링크 |",
        "|---|------|------|------|------|",
    ]
    if articles:
        for i, a in enumerate(articles, 1):
            title = a["title"].replace("|", "｜")[:100]
            lines.append(f"| {i} | {title} | {a['source']} | {a['section']} | {a['link']} |")
    else:
        lines.append("| - | (수집된 기사 없음) | - | - | - |")
    return "\n".join(lines) + "\n"


def main() -> int:
    project_root = os.environ.get(
        "PROJECT_ROOT",
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    output = os.path.join(project_root, "stock-service", "_pipeline", "stock-01-rss-pool.md")
    os.makedirs(os.path.dirname(output), exist_ok=True)

    all_articles: list[dict] = []
    feed_status: list[str] = []
    success = 0

    for source, url, section in FEEDS:
        print(f"수집 중: {source}", file=sys.stderr)
        content = fetch(url)
        if content is None:
            feed_status.append(f"| {source} | {url} | ❌ 접근 불가 |")
            continue
        articles = parse_feed(content, source, section)
        feed_status.append(f"| {source} | {url} | ✅ {len(articles)}건 |")
        all_articles.extend(articles)
        success += 1

    md = build_markdown(all_articles, feed_status, success)
    with open(output, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n완료: {success}/{len(FEEDS)} 피드 성공, 오늘 기사 {len(all_articles)}건")
    print(f"저장: {output}")
    return 0 if success > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
