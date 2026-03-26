#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 简化版保存脚本

import os
from pathlib import Path

print("Starting Cognitive Slice Theory Save Tool...")
print("=" * 50)

# 1. Check Obsidian vault
vault_path = "D:\\LDD\\璇玑台"
vault = Path(vault_path)

if not vault.exists():
    print(f"Error: Obsidian vault not found: {vault}")
    input("Press Enter to exit...")
    exit(1)

print(f"✅ Obsidian vault: {vault}")

# 2. Check document
doc_path = "C:\\Users\\lgdln\\.openclaw\\workspace\\认知切片论-整合版.md"

if not os.path.exists(doc_path):
    print(f"Error: Document not found: {doc_path}")
    input("Press Enter to exit...")
    exit(1)

with open(doc_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ Document loaded ({len(content)} characters)")

# 3. Save to Obsidian
project_folder = vault / "项目" / "认知切片论"
project_folder.mkdir(parents=True, exist_ok=True)

main_file = project_folder / "认知切片论-整合版.md"
with open(main_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Main document saved: {main_file}")

# 4. Create project index
index_content = f"""# Cognitive Slice Theory - Project Index

**Status**: Active  
**Created**: 2026-03-23  
**Last Updated**: 2026-03-23  
**Collaborators**: 星尘 & 璇玑

## Project Overview

Cognitive Slice Theory is a deep theoretical framework about human cognition.

## Quick Links

- [[认知切片论-整合版]] - Main document
- [[章节索引]] - Chapter index

## Next Steps

1. Read the main document
2. Explore related concepts
3. Practice with the tools

---

*Project maintained by 璇玑*"""

index_file = project_folder / "Project Index.md"
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"✅ Project index created: {index_file}")

print("\n" + "=" * 50)
print("🎉 Save completed successfully!")
print(f"\n📁 Files saved to: {project_folder}")
print("\n💡 Next steps:")
print("   1. Open Obsidian to view the files")
print("   2. Read the main document")
print("   3. Explore the project structure")

input("\nPress Enter to exit...")