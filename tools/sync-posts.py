"""
sync-posts.py — 토큰 0 소비 동기화 도구

_posts/*.md 에 있는 모든 아티클을 읽어
  1. web/posts/ 에 복사 (없는 파일만)
  2. web/posts.json 에 메타데이터 추가 (없는 항목만)

사용법:
  python tools/sync-posts.py

실행 위치: 프로젝트 루트 (01. 카드뉴스 만들기/)
외부 라이브러리 불필요. Python 3.6+ 표준 라이브러리만 사용.
"""

import json
import re
import shutil
import sys
from pathlib import Path

# Windows 터미널 한글 출력 보장
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── 경로 설정 ──────────────────────────────────────────────
ROOT = Path(__file__).parent.parent          # 프로젝트 루트
POSTS_DIR = ROOT / "_posts"                  # 마스터 마크다운
WEB_POSTS_DIR = ROOT / "web" / "posts"      # 웹 서버용 사본
POSTS_JSON = ROOT / "web" / "posts.json"    # 메타데이터 인덱스


def parse_frontmatter(text: str) -> dict:
    """--- ... --- 블록에서 key: value 쌍을 파싱."""
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def load_posts_json() -> dict:
    if POSTS_JSON.exists():
        with open(POSTS_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def save_posts_json(data: dict):
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sync():
    WEB_POSTS_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    if not md_files:
        print("_posts/ 에 마크다운 파일이 없습니다.")
        return

    data = load_posts_json()
    existing_filenames = {p["filename"] for p in data["posts"]}

    copied = 0
    added = 0

    for md_file in md_files:
        filename = md_file.name

        # 1. web/posts/ 에 없으면 복사
        dest = WEB_POSTS_DIR / filename
        if not dest.exists():
            shutil.copy2(md_file, dest)
            copied += 1
            print(f"  복사: {filename}")

        # 2. posts.json 에 없으면 추가
        if filename not in existing_filenames:
            text = md_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)

            entry = {
                "filename": filename,
                "title":    fm.get("title", filename),
                "category": fm.get("category", ""),
                "date":     fm.get("date", ""),
                "source":   fm.get("source", ""),
                "sourceUrl":fm.get("sourceUrl", ""),
                "description": fm.get("description", ""),
            }
            data["posts"].append(entry)
            existing_filenames.add(filename)
            added += 1
            print(f"  등록: {filename}")

    # 날짜 내림차순 정렬 (최신이 앞에)
    data["posts"].sort(key=lambda p: p.get("date", ""), reverse=True)

    save_posts_json(data)

    print(f"\n완료: 복사 {copied}건, posts.json 추가 {added}건, 전체 {len(data['posts'])}건")


if __name__ == "__main__":
    sync()
