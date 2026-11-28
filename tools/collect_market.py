"""
collect_market.py — 시장 지표 자동 수집 (LLM 토큰 0, 표준 라이브러리만)

금·달러·유가·채권·금리·주요 국가 지수와 반도체 대표 종목의 종가를 모아
  web/market/latest.json            최신값 + 최근 30거래일 종가
  web/market/history/YYYY-MM-DD.json 그날 스냅샷
에 저장한다. 예약 작업(한입뉴스·데일리 마켓 브리핑)은 이 파일의 수치를 그대로 인용한다.

출처: Yahoo Finance chart API (지수·환율·원자재·종목·미 국채 수익률),
      FRED (미 2년물·연방기금금리 — 접속 실패 시 Yahoo 대체값 사용)

사용법:  python tools/collect_market.py            (프로젝트 루트에서)
         python tools/collect_market.py --stdout   (파일 저장 없이 표 출력)
"""
from __future__ import annotations

import csv
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "web" / "market"
UA = {"User-Agent": "Mozilla/5.0 (one-bite-news market collector)"}

# (key, 이름, 그룹, 단위, Yahoo 심볼)
SERIES = [
    # 주요 국가 지수
    ("kospi",   "코스피",            "index",   "pt",   "^KS11"),
    ("kosdaq",  "코스닥",            "index",   "pt",   "^KQ11"),
    ("spx",     "S&P 500",           "index",   "pt",   "^GSPC"),
    ("ndx",     "나스닥 종합",        "index",   "pt",   "^IXIC"),
    ("dji",     "다우존스",           "index",   "pt",   "^DJI"),
    ("sox",     "필라델피아 반도체",  "index",   "pt",   "^SOX"),
    ("nikkei",  "닛케이 225",         "index",   "pt",   "^N225"),
    ("shcomp",  "상하이 종합",        "index",   "pt",   "000001.SS"),
    ("hsi",     "항셍",              "index",   "pt",   "^HSI"),
    ("twii",    "대만 가권",          "index",   "pt",   "^TWII"),
    ("stoxx50", "유로스톡스 50",      "index",   "pt",   "^STOXX50E"),
    # 환율·달러
    ("usdkrw",  "원/달러 환율",       "fx",      "원",   "KRW=X"),
    ("dxy",     "달러인덱스",         "fx",      "pt",   "DX-Y.NYB"),
    ("usdjpy",  "엔/달러 환율",       "fx",      "엔",   "JPY=X"),
    ("usdcny",  "위안/달러 환율",     "fx",      "위안", "CNY=X"),
    # 원자재
    ("gold",    "금 (COMEX 선물)",    "commodity", "$/oz",  "GC=F"),
    ("silver",  "은 (COMEX 선물)",    "commodity", "$/oz",  "SI=F"),
    ("wti",     "WTI 원유",           "commodity", "$/bbl", "CL=F"),
    ("brent",   "브렌트유",           "commodity", "$/bbl", "BZ=F"),
    ("copper",  "구리 (COMEX 선물)",  "commodity", "$/lb",  "HG=F"),
    # 금리·채권 (수익률, %)
    ("us3m",    "미 국채 3개월",      "rate",    "%",    "^IRX"),
    ("us5y",    "미 국채 5년",        "rate",    "%",    "^FVX"),
    ("us10y",   "미 국채 10년",       "rate",    "%",    "^TNX"),
    ("us30y",   "미 국채 30년",       "rate",    "%",    "^TYX"),
    # 위험 심리
    ("vix",     "VIX 변동성지수",     "risk",    "pt",   "^VIX"),
    ("btc",     "비트코인",           "risk",    "$",    "BTC-USD"),
    # 반도체 대표 종목
    ("samsung", "삼성전자",           "semis",   "원",   "005930.KS"),
    ("hynix",   "SK하이닉스",         "semis",   "원",   "000660.KS"),
    ("nvda",    "엔비디아",           "semis",   "$",    "NVDA"),
    ("tsm",     "TSMC (ADR)",         "semis",   "$",    "TSM"),
    ("mu",      "마이크론",           "semis",   "$",    "MU"),
    ("asml",    "ASML",               "semis",   "$",    "ASML"),
]

# FRED (키 불필요) — 실패해도 전체 수집은 계속
FRED_SERIES = [
    ("us2y", "미 국채 2년", "rate", "%", "DGS2"),
    ("fedfunds", "미 연방기금 실효금리", "rate", "%", "DFF"),
]

GROUPS = {
    "index": "주요 지수", "fx": "환율·달러", "commodity": "원자재",
    "rate": "금리·채권", "risk": "위험 심리", "semis": "반도체 대표 종목",
}


def http_get(url: str, timeout: int = 20) -> bytes:
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # 429·일시 오류 대비 재시도
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def yahoo_closes(symbol: str) -> list[tuple[str, float]]:
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(symbol) + "?range=3mo&interval=1d")
    data = json.loads(http_get(url))
    res = data["chart"]["result"][0]
    tz = timezone(timedelta(seconds=res["meta"].get("gmtoffset", 0)))
    ts = res.get("timestamp") or []
    closes = res["indicators"]["quote"][0].get("close") or []
    out = []
    for t, c in zip(ts, closes):
        if c is None:
            continue
        out.append((datetime.fromtimestamp(t, tz).strftime("%Y-%m-%d"), float(c)))
    # 같은 날짜가 두 번 오면(장중 값) 마지막 값만 남긴다
    dedup = {}
    for d, c in out:
        dedup[d] = c
    return sorted(dedup.items())


def fred_closes(series_id: str) -> list[tuple[str, float]]:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    text = http_get(url).decode("utf-8")
    rows = list(csv.reader(io.StringIO(text)))[1:]
    out = []
    for row in rows[-120:]:
        if len(row) >= 2 and row[1] not in ("", "."):
            out.append((row[0], float(row[1])))
    return out


def build_item(key, name, group, unit, closes, source, symbol):
    if len(closes) < 2:
        raise ValueError("종가가 2개 미만")
    (d0, last), (_, prev) = closes[-1], closes[-2]
    chg = last - prev
    item = {
        "key": key, "name": name, "group": group, "unit": unit,
        "date": d0, "last": round(last, 4), "prev": round(prev, 4),
        "chg": round(chg, 4),
        "chg_pct": round(chg / prev * 100, 2) if prev else None,
        "source": source, "symbol": symbol,
        "history": [[d, round(c, 4)] for d, c in closes[-30:]],
    }
    # 1주·1개월 전 대비 (거래일 기준 5·21일)
    for label, n in (("1w", 5), ("1m", 21)):
        if len(closes) > n and closes[-1 - n][1]:
            item[f"chg_{label}_pct"] = round((last / closes[-1 - n][1] - 1) * 100, 2)
            if group == "rate":
                item[f"chg_{label}_bp"] = round((last - closes[-1 - n][1]) * 100, 1)
    if group == "rate":  # 금리는 %p 변화가 더 의미 있다
        item["chg_bp"] = round(chg * 100, 1)
    return item


def collect() -> dict:
    items, errors = [], []
    for key, name, group, unit, sym in SERIES:
        try:
            items.append(build_item(key, name, group, unit, yahoo_closes(sym),
                                    "Yahoo Finance", sym))
        except Exception as e:
            errors.append({"key": key, "symbol": sym, "error": str(e)[:200]})
    for key, name, group, unit, sid in FRED_SERIES:
        try:
            items.append(build_item(key, name, group, unit, fred_closes(sid), "FRED", sid))
        except Exception as e:
            if key == "us2y":  # 대체: 2년물 국채 수익률 선물
                try:
                    items.append(build_item(key, name + " (선물 대체)", group, unit,
                                            yahoo_closes("2YY=F"), "Yahoo Finance", "2YY=F"))
                    continue
                except Exception as e2:
                    e = e2
            errors.append({"key": key, "symbol": sid, "error": str(e)[:200]})

    by = {i["key"]: i for i in items}
    derived = {}
    if "us10y" in by and "us2y" in by:
        derived["us10y_2y_spread_bp"] = round((by["us10y"]["last"] - by["us2y"]["last"]) * 100, 1)
    if "gold" in by and "usdkrw" in by:  # 원화 환산 금값 (1돈 = 3.75g)
        krw_per_g = by["gold"]["last"] * by["usdkrw"]["last"] / 31.1035
        derived["gold_krw_per_don"] = round(krw_per_g * 3.75)

    order = {k: n for n, (k, *_rest) in enumerate(SERIES + FRED_SERIES)}
    items.sort(key=lambda i: (list(GROUPS).index(i["group"]), order.get(i["key"], 99)))
    return {
        "asof_kst": datetime.now(KST).strftime("%Y-%m-%d %H:%M"),
        "note": "각 값은 해당 시장의 직전 거래일 종가(또는 수집 시점 최신값)이며, 등락은 그 전 거래일 대비입니다. 금리는 bp(0.01%p) 단위.",
        "groups": GROUPS,
        "items": items,
        "derived": derived,
        "errors": errors,
    }


def fmt(v):
    return f"{v:,.2f}" if abs(v) < 1000 else f"{v:,.0f}"


def print_table(data):
    print(f"기준: {data['asof_kst']} KST")
    for i in data["items"]:
        sign = "+" if i["chg"] >= 0 else ""
        print(f"  [{i['group']:<9}] {i['name']:<14} {fmt(i['last']):>12} {i['unit']:<5} "
              f"{sign}{i['chg_pct']}%  ({i['date']}, {i['source']})")
    print("  파생:", data["derived"])
    if data["errors"]:
        print("  실패:", ", ".join(e["key"] for e in data["errors"]))


def main():
    data = collect()
    if "--stdout" in sys.argv:
        print_table(data)
        return
    if len(data["items"]) < len(SERIES) // 2:
        print_table(data)
        print("수집 성공 항목이 절반 미만 — 기존 파일을 덮어쓰지 않습니다.")
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "history").mkdir(exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    (OUT_DIR / "latest.json").write_text(payload, encoding="utf-8")
    snap = {k: v for k, v in data.items() if k != "items"}
    snap["items"] = [{k: v for k, v in i.items() if k != "history"} for i in data["items"]]
    day = data["asof_kst"][:10]
    (OUT_DIR / "history" / f"{day}.json").write_text(
        json.dumps(snap, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print_table(data)


if __name__ == "__main__":
    main()
