#!/usr/bin/env python3
"""
update_readme.py

Scans the repo for problem folders (e.g. array-string/001-two-sum/notes.md),
reads difficulty + title from each notes.md, and rewrites the stats tables
in README.md between marker comments.

Expected notes.md format (see leetcode-repo-template.md):

    # [1] Two Sum

    **Difficulty:** Easy
    **Tags:** Array, Hash Table
    **Link:** https://leetcode.com/problems/two-sum/

Usage:
    python update_readme.py
    python update_readme.py --root . --readme README.md
"""

import argparse
import re
from pathlib import Path
from collections import defaultdict

# Folders to ignore when scanning for categories
IGNORE_DIRS = {".git", ".github", "__pycache__", "node_modules"}

TITLE_RE = re.compile(r"^#\s*\[(\d+)\]\s*(.+)$", re.MULTILINE)
DIFF_RE = re.compile(r"\*\*Difficulty:\*\*\s*(\w+)", re.MULTILINE)

CATEGORY_START = "<!-- STATS:START -->"
CATEGORY_END = "<!-- STATS:END -->"


def humanize(folder_name: str) -> str:
    """dynamic-programming -> Dynamic Programming"""
    return " ".join(w.capitalize() for w in folder_name.split("-"))


def scan_repo(root: Path):
    """Returns dict: category -> list of (number, title, difficulty, relpath)"""
    categories = defaultdict(list)

    for category_dir in sorted(root.iterdir()):
        if not category_dir.is_dir() or category_dir.name in IGNORE_DIRS:
            continue
        if category_dir.name.startswith("."):
            continue

        found_any = False
        for problem_dir in sorted(category_dir.iterdir()):
            notes_path = problem_dir / "notes.md"
            if not notes_path.exists():
                continue

            text = notes_path.read_text(encoding="utf-8")
            title_match = TITLE_RE.search(text)
            diff_match = DIFF_RE.search(text)

            if not title_match:
                print(f"  [skip] {notes_path} — no '# [N] Title' header found")
                continue

            number = title_match.group(1)
            title = title_match.group(2).strip()
            difficulty = diff_match.group(1) if diff_match else "Unknown"
            relpath = problem_dir.relative_to(root).as_posix() + "/"

            categories[category_dir.name].append((number, title, difficulty, relpath))
            found_any = True

        if not found_any:
            continue

    return categories


def build_stats_block(categories: dict) -> str:
    lines = [CATEGORY_START]

    total = 0
    diff_counts = defaultdict(int)
    cat_counts = {}

    for cat, problems in categories.items():
        cat_counts[cat] = len(problems)
        total += len(problems)
        for _, _, diff, _ in problems:
            diff_counts[diff] += 1

    # Category summary table
    lines.append("\n## 진행 현황\n")
    lines.append("| Category | Solved |")
    lines.append("|---|---|")
    for cat in sorted(cat_counts):
        lines.append(f"| {humanize(cat)} | {cat_counts[cat]} |")
    lines.append(f"| **Total** | **{total}** |")

    # Difficulty summary
    lines.append("\n## 난이도별 통계\n")
    for diff in ["Easy", "Medium", "Hard", "Unknown"]:
        if diff_counts.get(diff):
            lines.append(f"- {diff}: {diff_counts[diff]}")

    # Per-category problem tables
    lines.append("\n## 문제 목록\n")
    for cat in sorted(categories):
        problems = sorted(categories[cat], key=lambda p: int(p[0]))
        lines.append(f"### {humanize(cat)}\n")
        lines.append("| # | Title | Difficulty | Solution |")
        lines.append("|---|---|---|---|")
        for number, title, difficulty, relpath in problems:
            lines.append(f"| {number} | {title} | {difficulty} | [Link]({relpath}) |")
        lines.append("")

    lines.append(CATEGORY_END)
    return "\n".join(lines)


def update_readme(readme_path: Path, stats_block: str):
    if not readme_path.exists():
        print(f"  [warn] {readme_path} not found — creating a minimal one")
        readme_path.write_text(
            f"# LeetCode Solutions\n\n{stats_block}\n", encoding="utf-8"
        )
        return

    content = readme_path.read_text(encoding="utf-8")

    if CATEGORY_START in content and CATEGORY_END in content:
        pattern = re.compile(
            re.escape(CATEGORY_START) + r".*?" + re.escape(CATEGORY_END),
            re.DOTALL,
        )
        new_content = pattern.sub(stats_block, content)
    else:
        # Markers not found — append at the end
        new_content = content.rstrip() + "\n\n" + stats_block + "\n"

    readme_path.write_text(new_content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Update README stats from problem folders")
    parser.add_argument("--root", default=".", help="Repo root (default: current dir)")
    parser.add_argument("--readme", default="README.md", help="README file path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    readme_path = root / args.readme

    print(f"Scanning {root} ...")
    categories = scan_repo(root)

    total = sum(len(v) for v in categories.values())
    print(f"Found {total} problems across {len(categories)} categories.")

    stats_block = build_stats_block(categories)
    update_readme(readme_path, stats_block)
    print(f"Updated {readme_path}")


if __name__ == "__main__":
    main()