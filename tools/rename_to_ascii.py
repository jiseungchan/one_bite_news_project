"""
rename_to_ascii.py — Korean filenames → ASCII slugs
Renames web/posts/*.md files and updates web/posts.json
"""
import os
import json
import shutil

BASE = r"c:\Claude 공부\Claude code\01. 카드뉴스 만들기"
POSTS_DIR = os.path.join(BASE, "web", "posts")
POSTS_JSON = os.path.join(BASE, "web", "posts.json")

# Manual mapping: old filename → new ASCII filename
RENAME_MAP = {
    "2026-04-12-chatgpt-vs-claude-ai자산.md":         "2026-04-12-chatgpt-vs-claude.md",
    "2026-04-12-ai-모델-프리미어리그-베팅.md":         "2026-04-12-ai-models-premier-league.md",
    "2026-04-12-한국은행-기준금리-7연속동결.md":        "2026-04-12-bok-rate-freeze-7th.md",
    "2026-04-12-마이크로소프트-maia200-AI가속기.md":   "2026-04-12-microsoft-maia200.md",
    "2026-04-12-openclaw-ai-에이전트.md":              "2026-04-12-openclaw-ai-agent.md",
    "2026-04-12-엔비디아-바이오-arc-institute.md":     "2026-04-12-nvidia-bio-arc-institute.md",
    "2026-04-11-무스타파-술레이만-AI-성장한계-MIT.md": "2026-04-11-mustafa-suleyman-ai-growth-mit.md",
    "2026-04-11-딥엑스-온디바이스AI칩.md":             "2026-04-11-deepx-on-device-ai-chip.md",
    "2026-04-11-삼성-소캠2-저온납땜.md":               "2026-04-11-samsung-socamm2-soldering.md",
    "2026-04-11-앤트로픽-어드바이저-전략.md":          "2026-04-11-anthropic-advisor-strategy.md",
}

# Rename files
renamed = 0
for old, new in RENAME_MAP.items():
    old_path = os.path.join(POSTS_DIR, old)
    new_path = os.path.join(POSTS_DIR, new)
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"[OK] {old} -> {new}")
        renamed += 1
    elif os.path.exists(new_path):
        print(f"[SKIP] already renamed: {new}")
    else:
        print(f"[MISS] not found: {old}")

print(f"\nRenamed {renamed} files.")

# Update posts.json
with open(POSTS_JSON, encoding="utf-8") as f:
    data = json.load(f)

updated = 0
for post in data["posts"]:
    fn = post.get("filename", "")
    if fn in RENAME_MAP:
        post["filename"] = RENAME_MAP[fn]
        updated += 1

with open(POSTS_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated} entries in posts.json.")
print("Done.")
