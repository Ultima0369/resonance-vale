#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Direct save script - no batch file needed

import os
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("Cognitive Slice Theory - Direct Save Tool")
    print("=" * 60)
    
    # 1. Check document
    doc_name = "认知切片论-整合版.md"
    if not os.path.exists(doc_name):
        print(f"❌ Error: Document '{doc_name}' not found")
        input("Press Enter to exit...")
        return
    
    with open(doc_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✅ Document loaded: {len(content)} characters")
    
    # 2. Check Obsidian vault
    vault_path = "D:\\LDD\\璇玑台"
    vault = Path(vault_path)
    
    if not vault.exists():
        print(f"❌ Error: Obsidian vault not found: {vault_path}")
        custom_path = input("Enter Obsidian vault path: ").strip()
        if custom_path:
            vault = Path(custom_path)
            if not vault.exists():
                print("❌ Path does not exist")
                input("Press Enter to exit...")
                return
        else:
            print("❌ Valid path required")
            input("Press Enter to exit...")
            return
    
    print(f"✅ Obsidian vault: {vault}")
    
    # 3. Create project folder
    project_folder = vault / "项目" / "认知切片论"
    project_folder.mkdir(parents=True, exist_ok=True)
    
    # 4. Save main document
    main_file = project_folder / "认知切片论-整合版.md"
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Main document saved: {main_file}")
    
    # 5. Create simple index
    index_content = f"""# Cognitive Slice Theory - Project

**Saved**: 2026-03-23
**Status**: Active

## Quick Start

1. Read [[认知切片论-整合版]]
2. Explore related concepts
3. Practice the tools

## Files

- [[认知切片论-整合版]] - Main document

---

*Saved by direct_save.py*"""
    
    index_file = project_folder / "Index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Index created: {index_file}")
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("🎉 Save completed successfully!")
    print(f"\n📁 Location: {project_folder}")
    print("\n💡 Next:")
    print("   1. Open Obsidian to view files")
    print("   2. Read the main document")
    print("   3. Start exploring!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()