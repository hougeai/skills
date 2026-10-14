#!/usr/bin/env python3
"""Top Conference Digest — 抓取指定会议指定 task 下的论文，关键词过滤

用法:
  python3 top-conf-digest.py --conference cvpr-2026 --task object-detection

输出:
  digest-{conference}-{task}.json
"""

import urllib.request
import json
import sys
import os
import argparse

# === 关键词配置（与 arXiv digest 同步） ===
INCLUDE_KEYWORDS = [
    "object detection",
    "object detector",
    "yolo",
    "detr",
    "open-vocabulary detection",
    "open vocabulary detection",
    "small object",
    "anchor-free",
]

EXCLUDE_KEYWORDS = [
    "bev", "bird eye", "bird-eye", "lidar", "point cloud",
    "3d object", "3d detection", "action recognition",
    "sign language", "3d point",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))
API_BASE = "https://paperswithcode.co/api/v1/conferences"


def fetch_all_papers(conference: str, task: str) -> list[dict]:
    """分页拉取指定会议+task 下的全部论文"""
    all_papers = []
    page = 1

    while True:
        url = f"{API_BASE}/{conference}/papers?task={task}&page={page}&items_per_page=100"
        print(f"Fetching page {page}...", file=sys.stderr)

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode("utf-8"))

        results = data.get("results", [])
        if not results:
            break

        for p in results:
            all_papers.append({
                "id": p["id"],
                "arxiv_id": p.get("arxiv_id", ""),
                "title": p.get("title", ""),
                "abstract": p.get("abstract", ""),
                "authors": p.get("authors", []),
                "url_abs": p.get("url_abs", ""),
                "url_pdf": p.get("url_pdf", ""),
                "proceeding": p.get("proceeding", ""),
                "tasks": [t["slug"] for t in (p.get("tasks") or [])],
            })

        print(f"  Got {len(results)} papers (total: {len(all_papers)})", file=sys.stderr)

        if not data.get("next_page"):
            break
        page += 1

    return all_papers


def filter_papers(papers: list[dict]) -> list[dict]:
    """按关键词过滤（标题+全文摘要）"""
    result = []
    for p in papers:
        text = (p["title"] + " " + p.get("abstract", "")).lower()

        inc = [kw for kw in INCLUDE_KEYWORDS if kw in text]
        if not inc:
            continue

        if any(kw in text for kw in EXCLUDE_KEYWORDS):
            continue

        p["matched_keywords"] = inc
        result.append(p)

    return result


def main():
    parser = argparse.ArgumentParser(description="Top Conference Digest")
    parser.add_argument("--conference", required=True, help="Conference slug, e.g. cvpr-2026")
    parser.add_argument("--task", required=True, help="Task slug, e.g. object-detection")
    args = parser.parse_args()

    print(f"Fetching {args.conference} / {args.task}...", file=sys.stderr)

    all_papers = fetch_all_papers(args.conference, args.task)
    print(f"Total papers in task: {len(all_papers)}", file=sys.stderr)

    if not all_papers:
        print("No papers found", file=sys.stderr)
        sys.exit(0)

    filtered = filter_papers(all_papers)
    print(f"After keyword filter: {len(filtered)} papers", file=sys.stderr)

    output = {
        "conference": args.conference,
        "task": args.task,
        "total_in_task": len(all_papers),
        "matched_count": len(filtered),
        "papers": filtered,
    }

    output_path = os.path.join(DATA_DIR, f"digest-{args.conference}-{args.task}.json")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved: {output_path}", file=sys.stderr)
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
