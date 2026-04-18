"""
merge-one-bite-legacy.py

https://github.com/jiseungchan/one_bite_news 의 posts.json + posts/*.md 를
one_bite_news_project 의 web/ 쪽에 병합한다.

- posts.json: filename 기준으로 레거시 항목과 매칭되면
  - 레거시에 image 가 있으면 그 URL로 덮어쓴다(배포 카드 썸네일).
  - 레거시에 tags 가 있고 프로젝트에 없으면 복사한다.
  - 프로젝트에만 있는 기사는 그대로 둔다(합집합).
- 레거시에만 있는 기사는 posts 배열에 추가하고 MD 파일을 복사한다.
- --copy-md: 매칭되는 filename 의 본문을 레포지토리 원문으로 덮어쓴다(선택).

사용 예:
  python tools/merge-one-bite-legacy.py
  python tools/merge-one-bite-legacy.py --legacy-dir "C:\\path\\to\\one_bite_news"
  python tools/merge-one-bite-legacy.py --copy-md
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_POSTS = ROOT / "web" / "posts"
POSTS_JSON = ROOT / "web" / "posts.json"
DEFAULT_REPO = "https://github.com/jiseungchan/one_bite_news.git"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def clone_legacy(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", DEFAULT_REPO, str(dest)],
        check=True,
    )


def sort_posts(posts: list) -> list:
    def key(p):
        return (p.get("date") or "", p.get("filename") or "")

    return sorted(posts, key=key, reverse=True)


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Merge one_bite_news into web/posts + posts.json")
    ap.add_argument(
        "--legacy-dir",
        type=Path,
        help="one_bite_news 저장소 루트 (posts/, posts.json 포함). 없으면 임시 클론.",
    )
    ap.add_argument(
        "--copy-md",
        action="store_true",
        help="동일 filename 의 마크다운을 레거시 원문으로 덮어쓴다.",
    )
    args = ap.parse_args()

    tmp: Path | None = None
    if args.legacy_dir:
        legacy_root = args.legacy_dir.resolve()
    else:
        tmp = Path(tempfile.mkdtemp(prefix="one_bite_news_merge_"))
        legacy_root = tmp / "repo"
        print(f"Cloning {DEFAULT_REPO} …")
        clone_legacy(legacy_root)

    leg_posts_path = legacy_root / "posts.json"
    leg_posts_dir = legacy_root / "posts"
    if not leg_posts_path.is_file():
        print(f"Missing {leg_posts_path}", file=sys.stderr)
        return 1
    if not leg_posts_dir.is_dir():
        print(f"Missing {leg_posts_dir}", file=sys.stderr)
        return 1

    legacy = load_json(leg_posts_path)
    project = load_json(POSTS_JSON)

    leg_by_fn = {p["filename"]: p for p in legacy.get("posts", []) if p.get("filename")}
    proj_posts = project.get("posts", [])
    proj_by_fn = {p["filename"]: p for p in proj_posts if p.get("filename")}

    updated_meta = 0
    copied_md = 0
    added_new = 0

    for fn, leg in leg_by_fn.items():
        md_src = leg_posts_dir / fn
        if fn in proj_by_fn:
            p = proj_by_fn[fn]
            img = leg.get("image")
            if img and str(img).strip():
                if p.get("image") != img:
                    p["image"] = img
                    updated_meta += 1
            if leg.get("tags") and not p.get("tags"):
                p["tags"] = leg["tags"]
                updated_meta += 1
            if args.copy_md and md_src.is_file():
                WEB_POSTS.mkdir(parents=True, exist_ok=True)
                shutil.copy2(md_src, WEB_POSTS / fn)
                copied_md += 1
        else:
            proj_posts.append(dict(leg))
            proj_by_fn[fn] = proj_posts[-1]
            added_new += 1
            if md_src.is_file():
                WEB_POSTS.mkdir(parents=True, exist_ok=True)
                shutil.copy2(md_src, WEB_POSTS / fn)
                copied_md += 1

    project["posts"] = sort_posts(proj_posts)
    save_json(POSTS_JSON, project)

    print(f"posts.json 갱신 완료: 총 {len(project['posts'])}건")
    print(f"  메타(image/tags) 갱신·추가 처리: {updated_meta}건 (추정)")
    print(f"  신규 기사 추가: {added_new}건")
    if args.copy_md:
        print(f"  MD 복사(덮어쓰기): {copied_md}건")

    if tmp and tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
