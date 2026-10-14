#!/usr/bin/env python3
"""从 digest-sum.json 生成顶会 VitePress 页面（剔除 ⏭不推荐）"""

import json, sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMO_DIR = os.path.abspath(os.path.join(BASE_DIR, '../data'))

def load_sum(conference: str, task: str) -> dict:
    path = os.path.join(MEMO_DIR, f'digest-{conference}-{task}-sum.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def build_md(data: dict) -> str:
    """从 sum.json 生成 markdown（按 SKILL.md 输出格式）"""
    lines = []
    lines.append(f'## {data["task"]}')
    lines.append('')

    seq = 0
    for p in data['papers']:
        if p['recommendation'] == '⏭不推荐':
            continue

        seq += 1
        authors = "、".join(p["authors"][:4])
        if len(p["authors"]) > 4:
            authors += " 等"

        lines.append(f'### {seq}. [{p["title"]}]({p["url_abs"]})')
        lines.append(f'- **作者**: {authors}')
        lines.append(f'- **推荐度**: {p["recommendation"]}')
        lines.append(f'- **推荐理由**: {p["reason"]}')
        lines.append(f'> {p["summary_cn"]}')
        lines.append('')
        lines.append('---')
        lines.append('')

    return '\n'.join(lines)

def update_index(conference_slug: str, task: str):
    """更新 top-conferences/index.md"""
    index_path = os.path.join(MEMO_DIR, 'index.md')
    
    # Build the entry for this task
    task_label = task.replace('-', ' ').title()
    entry = f'- [{task_label}]({conference_slug}.md)'
    
    # Read existing index
    if os.path.exists(index_path):
        with open(index_path, encoding='utf-8') as f:
            content = f.read()
    else:
        content = '# 顶会整理\n\n---\n\n'
    
    # Check if entry already exists
    if entry in content:
        return  # Already indexed
    
    # Find the right conference section or add it
    if f'## {conference_slug}' in content:
        # Add to existing section (before the next section or end of file)
        section_start = content.index(f'## {conference_slug}')
        section_end = len(content)
        next_section = content.find('\n## ', section_start + 3)
        if next_section > 0:
            section_end = next_section
        content = content[:section_end] + f'\n{entry}' + content[section_end:]
    else:
        # Add new conference section at top (after main header)
        header_end = content.index('\n', content.index('# ') + 2) if '# ' in content else len(content)
        new_section = f'\n## {conference_slug}\n\n{entry}\n'
        content = content[:header_end] + new_section + content[header_end:]
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    if len(sys.argv) < 3:
        print('Usage: python3 digest-check.py --conference cvpr-2026 --task object-detection', file=sys.stderr)
        sys.exit(1)
    
    conf, task = None, None
    for i, arg in enumerate(sys.argv):
        if arg == '--conference' and i + 1 < len(sys.argv):
            conf = sys.argv[i + 1]
        if arg == '--task' and i + 1 < len(sys.argv):
            task = sys.argv[i + 1]
    
    if not conf or not task:
        print('Missing --conference or --task', file=sys.stderr)
        sys.exit(1)
    
    data = load_sum(conf, task)
    md = build_md(data)
    
    # Write/append to conference page
    os.makedirs(MEMO_DIR, exist_ok=True)
    md_path = os.path.join(MEMO_DIR, f'{conf}.md')
    
    # Check if file exists
    if os.path.exists(md_path):
        with open(md_path, encoding='utf-8') as f:
            existing = f.read()
        # Skip if task section already exists
        if f'## {task}' in existing:
            print(f'Skipped: task section already exists in {md_path}')
            return
        # Keep preamble (content before first ## section)
        preamble_end = existing.find('\n## ')
        if preamble_end > 0:
            preamble = existing[:preamble_end]
        else:
            preamble = existing.strip()
        # Append new task section
        full = preamble + '\n\n' + md + '\n'
    else:
        # New file: add title header + task section
        conf_label = conf.replace('-', ' ').upper().replace(' ', '')
        full = f'# {conf_label} 论文整理\n> 关键词：可编辑\n\n---\n\n' + md + '\n'
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(full)
    
    # Update index
    update_index(conf)
    
    print(f'Written: {md_path}')
    print(f'Included: {sum(1 for p in data["papers"] if p["recommendation"] != "⏭不推荐")}/{len(data["papers"])} papers (keeping only recommended)')


if __name__ == '__main__':
    main()
