"""
merge_branch_content.py — 자동 발행 브랜치의 '콘텐츠'만 main 작업 트리로 가져온다.

Claude 예약 작업은 claude/... 브랜치에 push 한다. GitHub Actions(auto-merge-claude.yml)가
이 스크립트로 그 브랜치의 발행물만 main 에 옮기고, 코드·설정 변경은 가져오지 않는다.

  python tools/merge_branch_content.py origin/claude/xxx [origin/claude/yyy ...]

동작
  1. 각 브랜치에서 아래 CONTENT_PREFIXES 경로의 추가·수정 파일을 main 작업 트리로 복사
     (여러 브랜치에 같은 파일이 있으면 커밋 시각이 늦은 브랜치 것이 이긴다)
  2. web/posts.json · web/stock-briefs.json 은 통째로 덮지 않고 항목 단위로 합친다
  3. _posts/ ↔ web/posts/ 미러를 맞추고 색인에 없는 글은 frontmatter 로 등록 (sync-posts)
  4. 콘텐츠 외 변경이 있었던 브랜치 이름을 non_content_branches.txt 로 남긴다
     (워크플로는 그 브랜치를 지우지 않는다)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_PREFIXES = (
    "_posts/", "web/posts/", "web/market/notes/", "web/stock-briefs/",
    "stock-service/_stock-news/", "_cards/",
)
# 세션 중간 산출물·잠금 파일: 가져오지도 않고 '코드 변경'으로 치지도 않는다
IGNORE_PREFIXES = ("_pipeline/", "stock-service/_pipeline/", ".claude/scheduled_tasks.lock")
INDEXES = {"web/posts.json": ("posts", "filename"), "web/stock-briefs.json": ("briefs", "filename")}


def deleted_filenames() -> set[str]:
    """출처 검증에서 삭제한 글(docs/deleted-posts-*.tsv)은 옛 브랜치에서 다시 들여오지 않는다."""
    names = set()
    for f in (ROOT / "docs").glob("deleted-posts-*.tsv"):
        for line in f.read_text(encoding="utf-8").splitlines()[1:]:
            if line.strip():
                names.add(line.split("\t", 1)[0])
    return names


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def changed_files(ref: str) -> list[tuple[str, str]]:
    base = git("merge-base", "HEAD", ref).strip()
    out = git("diff", "--name-status", "-z", "--no-renames", base, ref).split("\0")
    pairs = []
    for i in range(0, len(out) - 1, 2):
        pairs.append((out[i], out[i + 1]))
    return pairs


def load_index(text: str | None, key: str) -> list[dict]:
    if not text:
        return []
    try:
        data = json.loads(text)
        return [e for e in data.get(key, []) if isinstance(e, dict)]
    except Exception:
        return []


def strip_quotes(entry: dict) -> dict:
    for k, v in list(entry.items()):
        if isinstance(v, str) and len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            entry[k] = v[1:-1].replace('\\"', '"')
    return entry


def main(refs: list[str]) -> int:
    refs = sorted(refs, key=lambda r: int(git("log", "-1", "--format=%ct", r).strip()))
    blocked = deleted_filenames()
    non_content, copied = [], 0
    merged = {p: {} for p in INDEXES}
    for path, (key, idf) in INDEXES.items():
        f = ROOT / path
        for e in load_index(f.read_text(encoding="utf-8") if f.exists() else None, key):
            merged[path][e.get(idf) or e.get("date")] = e

    on_main = {path: set(v) for path, v in merged.items()}
    for ref in refs:
        other = False
        for status, path in changed_files(ref):
            if path.startswith(IGNORE_PREFIXES):
                continue
            if path in INDEXES:
                key, idf = INDEXES[path]
                for e in load_index(git("show", f"{ref}:{path}"), key):
                    k = e.get(idf) or e.get("date")
                    if e.get(idf) in blocked or k in on_main[path]:
                        continue  # main에 이미 있는 항목은 옛 브랜치 값으로 덮지 않는다
                    merged[path][k] = strip_quotes(e)
            elif path.startswith(CONTENT_PREFIXES):
                if status.startswith("D") or Path(path).name in blocked:
                    continue  # 자동 작업이 기존 기사를 지우는 일은 반영하지 않는다
                dest = ROOT / path
                if dest.exists():
                    continue  # 이미 발행된 글은 옛 브랜치 내용으로 덮지 않는다
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(git("show", f"{ref}:{path}", binary=True))
                copied += 1
            else:
                other = True
        if other:
            non_content.append(ref)

    # _posts → web/posts 미러
    web_posts = ROOT / "web" / "posts"
    for f in (ROOT / "_posts").glob("*.md"):
        if f.name in blocked:
            f.unlink()
            continue
        if not (web_posts / f.name).exists():
            (web_posts / f.name).write_bytes(f.read_bytes())

    # 색인 저장 (실제 파일이 있는 글만)
    existing = {f.name for f in web_posts.glob("*.md")}
    posts = [e for fn, e in merged["web/posts.json"].items() if fn in existing]
    posts.sort(key=lambda e: (e.get("date", ""), e.get("filename", "")), reverse=True)
    (ROOT / "web/posts.json").write_text(
        json.dumps({"posts": posts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    briefs = sorted(merged["web/stock-briefs.json"].values(), key=lambda e: e.get("date", ""), reverse=True)
    (ROOT / "web/stock-briefs.json").write_text(
        json.dumps({"briefs": briefs}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 색인에 빠진 글은 frontmatter 로 보충
    subprocess.run([sys.executable, str(ROOT / "tools" / "sync-posts.py")], check=True)

    (ROOT / "non_content_branches.txt").write_text("\n".join(non_content) + "\n", encoding="utf-8")
    print(f"브랜치 {len(refs)}개에서 콘텐츠 파일 {copied}개 반영. 코드 변경 포함 브랜치: {len(non_content)}개")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
