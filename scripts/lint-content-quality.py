#!/usr/bin/env python3
"""
Content Quality Linter (CI Quality Gate)
========================================
Validates handbook lesson markdown files for frontmatter completeness
and required metadata fields.
"""

import sys
import re
from pathlib import Path

REQUIRED_FRONTMATTER_KEYS = ["title", "description"]

def check_file(filepath: Path) -> list[str]:
    errors = []
    content = filepath.read_text(encoding="utf-8")
    
    # Check frontmatter for lesson markdown files
    if "lessons/" in str(filepath):
        if not content.startswith("---"):
            errors.append("Missing YAML frontmatter opening '---'")
        else:
            frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not frontmatter_match:
                errors.append("Invalid or unclosed YAML frontmatter")
            else:
                fm_text = frontmatter_match.group(1)
                for key in REQUIRED_FRONTMATTER_KEYS:
                    if not re.search(rf"^{key}:", fm_text, re.MULTILINE):
                        errors.append(f"Missing required frontmatter key: '{key}'")

    return errors

def main():
    docs_dir = Path("docs")
    md_files = list(docs_dir.glob("**/*.md"))
    
    total_errors = 0
    print(f"Scanning {len(md_files)} documentation files for quality standards...\n")
    
    for filepath in md_files:
        errs = check_file(filepath)
        if errs:
            total_errors += len(errs)
            print(f"❌ {filepath}:")
            for e in errs:
                print(f"   - {e}")
                
    if total_errors > 0:
        print(f"\n❌ Quality check failed with {total_errors} issue(s).")
        sys.exit(1)
    else:
        print("✅ Content quality linting passed! All lessons meet required standards.")

if __name__ == "__main__":
    main()
