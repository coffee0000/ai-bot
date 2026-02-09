#!/usr/bin/env python
import fnmatch
import os
import sys
import zipfile
from datetime import datetime


def load_gitignore_patterns(root: str):
    patterns = []
    gitignore = os.path.join(root, ".gitignore")
    if not os.path.isfile(gitignore):
        return patterns

    with open(gitignore, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("!"):
                # ignore negate patterns for simplicity (same as build.sh)
                continue
            # remove leading slash
            pattern = line.lstrip("/")
            patterns.append(pattern)
    return patterns


def make_excluded_checker(root: str):
    patterns = load_gitignore_patterns(root)

    def is_excluded(rel_path: str) -> bool:
        # normalize to forward slashes
        rel = rel_path.replace(os.sep, "/")
        for pat in patterns:
            p = pat.replace("\\", "/")
            # directory pattern like "foo/"
            if p.endswith("/"):
                if rel == p[:-1] or rel.startswith(p):
                    return True
            if fnmatch.fnmatch(rel, p):
                return True
        return False

    return is_excluded


def main() -> int:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    zip_name = f"teams_ai_bot_project_{timestamp}.zip"
    out_path = os.path.join(parent_dir, zip_name)

    # remove existing file if any
    if os.path.exists(out_path):
        os.remove(out_path)

    print(f"ZIP を作成します: {out_path}")

    is_excluded = make_excluded_checker(script_dir)

    files_to_add = []
    for root, dirs, files in os.walk(script_dir):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, script_dir)
            if is_excluded(rel):
                continue
            files_to_add.append((full, rel))

    # create zip
    with zipfile.ZipFile(out_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for full, rel in files_to_add:
            zf.write(full, rel)

    print(f"完了しました。({len(files_to_add)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
