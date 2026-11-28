"""
verify_sources.py — 기사 원문 주소가 실제로 열리고, 그 원문이 우리 글과 같은 기사인지 확인한다
(LLM 토큰 0, 표준 라이브러리만)

판정
  ok           원문이 열리고(HTTP 200) 제목·본문이 우리 글과 맞는다
  not_found    404·410 등 없는 페이지
  home         사이트 첫 화면 주소이거나, 열었더니 첫 화면으로 돌려보냄 (개별 기사 아님)
  mismatch     열리지만 전혀 다른 기사 (잘못된 주소)
  blocked      401·403 — 매체가 자동 접속을 막음 (주소 자체는 맞을 수 있어 판정 보류)
  retry        429·5xx·시간초과 — 일시 오류, 나중에 다시 확인
  → '잘못된 주소'로 보는 것: not_found, home, mismatch

사용법 (프로젝트 루트에서)
  python tools/verify_sources.py 2026-11-28-x.md ...   # 특정 글 검사 (발행 전 검토용). 잘못된 주소가 있으면 종료코드 1
  python tools/verify_sources.py --all --report out.json  # 전체 검사 결과 저장
  python tools/verify_sources.py --all --delete            # 잘못된 주소 글 삭제 (_posts, web/posts, 카드 이미지, posts.json)
  python tools/verify_sources.py --gate <파일...>          # 워크플로용: 잘못된 주소 글만 삭제하고 계속
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_images import ROOT, POSTS_JSON, CARD_DIR, card_name, fetch, related, tokens  # noqa: E402

BAD = ("not_found", "home", "mismatch")


def post_text(p: dict) -> str:
    md = ROOT / "_posts" / p["filename"]
    body = md.read_text(encoding="utf-8") if md.exists() else ""
    return " ".join([p.get("title", ""), p.get("description", ""), body])


def page_title_of(text: str) -> str:
    for pat in (r'<meta[^>]+property=["\']og:title["\'][^>]*content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:title',
                r"<title[^>]*>([^<]+)</title>"):
        m = re.search(pat, text, re.I)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def body_overlap(our_title: str, page_text: str) -> float:
    """우리 제목의 핵심 단어가 원문 페이지 본문에 얼마나 나오는지 (0~1)."""
    toks = {t for t in tokens(our_title) if len(t) >= 2}
    if not toks:
        return 0.0
    low = re.sub(r"<[^>]+>", " ", page_text).lower()
    return sum(1 for t in toks if t in low) / len(toks)


def check(p: dict) -> dict:
    url = p.get("sourceUrl", "")
    res = {"filename": p["filename"], "date": p.get("date", ""), "title": p.get("title", ""),
           "sourceUrl": url, "source": p.get("source", "")}
    pu = urllib.parse.urlparse(url)
    if pu.scheme not in ("http", "https"):
        return {**res, "status": "home", "why": "주소 없음"}
    if len(pu.path.strip("/")) <= 3 and not pu.query:
        return {**res, "status": "home", "why": "사이트 첫 화면 주소"}
    for attempt in range(2):
        try:
            status, ctype, body, final = fetch(url, timeout=15, max_bytes=1_500_000)
            break
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return {**res, "status": "not_found", "why": f"HTTP {e.code}"}
            if e.code in (401, 403, 451):
                return {**res, "status": "blocked", "why": f"HTTP {e.code}"}
            if attempt == 0:
                time.sleep(3)
                continue
            return {**res, "status": "retry", "why": f"HTTP {e.code}"}
        except Exception as e:
            if attempt == 0:
                time.sleep(3)
                continue
            return {**res, "status": "retry", "why": type(e).__name__}
    if "html" not in ctype:  # PDF 등 문서 직접 링크는 열리면 통과
        return {**res, "status": "ok", "why": ctype}
    fp = urllib.parse.urlparse(final)
    if fp.path.strip("/") in ("", "index.html", "index.php") and not fp.query:
        return {**res, "status": "home", "why": "첫 화면으로 이동됨"}
    text = body.decode("utf-8", errors="ignore")
    if re.search(r"alert\(['\"][^'\"]*(존재하지 않는|검토중인 기사|삭제된|없는 기사)", text[:3000]):
        return {**res, "status": "not_found", "why": "매체가 '없는 기사' 안내"}
    ptitle = page_title_of(text)
    if re.search(r"(404|not found|페이지를 찾을 수 없|존재하지 않는|삭제된 기사|없는 기사)", ptitle, re.I):
        return {**res, "status": "not_found", "why": f"오류 페이지: {ptitle[:60]}", "pageTitle": ptitle}
    if related(ptitle, post_text(p)):
        return {**res, "status": "ok", "pageTitle": ptitle}
    if ptitle and len(re.findall(r"[가-힣]", ptitle)) < 3:
        # 영문 원문을 한국어로 다시 쓴 글은 단어 대조가 안 된다. 열리는 기사면 통과시키고,
        # 내용 일치는 발행 전 Claude 검토(원문 대조)에서 확인한다.
        return {**res, "status": "ok", "why": "영문 원문 — 내용 대조는 발행 전 검토", "pageTitle": ptitle}
    ov = body_overlap(p.get("title", ""), text)
    if ov >= 0.5:
        return {**res, "status": "ok", "why": f"본문 일치 {ov:.0%}", "pageTitle": ptitle}
    return {**res, "status": "mismatch", "why": f"원문 제목 불일치, 본문 일치 {ov:.0%}", "pageTitle": ptitle}


def delete_posts(filenames: set[str]) -> int:
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    before = len(data["posts"])
    data["posts"] = [p for p in data["posts"] if p["filename"] not in filenames]
    POSTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for fn in filenames:
        for path in (ROOT / "_posts" / fn, ROOT / "web" / "posts" / fn, CARD_DIR / card_name(fn)):
            if path.exists():
                path.unlink()
    return before - len(data["posts"])


def main(argv: list[str]) -> int:
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    targets = [a for a in argv if a.endswith(".md")]
    posts = data["posts"] if "--all" in argv else [p for p in data["posts"] if p["filename"] in targets]
    missing = set(targets) - {p["filename"] for p in posts}
    for fn in missing:
        print(f"[색인 없음] {fn} — web/posts.json 에 먼저 등록하세요")
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(check, posts))
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        if r["status"] != "ok" and not ("--all" in argv and "--verbose" not in argv):
            print(f"[{r['status']}] {r['filename']} — {r.get('why', '')} — {r['sourceUrl']}")
    print("결과:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if "--report" in argv:
        out = Path(argv[argv.index("--report") + 1])
        out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
        print("보고서:", out)
    bad = {r["filename"] for r in results if r["status"] in BAD}
    if "--delete" in argv or "--gate" in argv:
        n = delete_posts(bad)
        print(f"잘못된 주소 글 {n}건 삭제")
        return 0
    return 1 if bad or missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
