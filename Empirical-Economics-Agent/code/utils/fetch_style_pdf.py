"""
code/utils/fetch_style_pdf.py — 核心范文 PDF 下载工具

基于 Semantic Scholar API 下载论文 PDF，按 DOI、标题+作者或期刊+关键词搜索。
闭源论文自动降级为 working paper 版本。生成的 .meta.json 显式分离阅读版本与引用版本。

用法：
    # 按 DOI 下载（主用）
    python code/utils/fetch_style_pdf.py --doi 10.1093/rfs/hhac001

    # 按标题+作者下载（交互式确认候选）
    python code/utils/fetch_style_pdf.py --title "Nonbank Lending and Credit Cyclicality" --author "Fleckenstein"

    # 按期刊+关键词搜索（限定 journal-list.md 期刊范围）
    python code/utils/fetch_style_pdf.py --journal "RFS" --keywords "credit" --years 2024-2026

    # 指定输出目录（默认: paper-lib/style-references/pdfs/）
    python code/utils/fetch_style_pdf.py --doi <DOI> --output-dir paper-lib/style-references/pdfs/

依赖：
    - requests >= 2.28.0
    - Semantic Scholar API（免费，无需 API key）
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper-lib" / "style-references" / "pdfs"

SS_API_BASE = "https://api.semanticscholar.org/graph/v1"
SS_PAPER_SEARCH = f"{SS_API_BASE}/paper/search"
SS_PAPER_DETAIL = f"{SS_API_BASE}/paper"  # + /{paper_id} or /DOI:{doi}
SS_USER_AGENT = "ZBWQ-Empirical-Workflow/1.0 (mailto:research@example.com)"

# ── 期刊列表加载（用于验证搜索范围） ──────────────────
def _load_journal_list() -> set[str]:
    """从 paper-lib/journal-list.md 解析期刊全名集合。"""
    journal_list_path = REPO_ROOT / "paper-lib" / "journal-list.md"
    if not journal_list_path.exists():
        return set()
    content = journal_list_path.read_text(encoding="utf-8")
    journals = set()
    for line in content.splitlines():
        m = re.match(r"^\|\s*[A-Za-z]+\s*\|\s*(.+?)\s*\|", line)
        if m:
            name = m.group(1).strip()
            if name and len(name) > 3:
                journals.add(name)
    return journals


# ── Semantic Scholar API 交互 ──────────────────────────
def _ss_get(endpoint: str, params: dict | None = None, timeout: int = 30) -> dict | None:
    """GET 请求 Semantic Scholar API，含速率限制退避。"""
    url = f"{SS_API_BASE}/{endpoint.lstrip('/')}"
    headers = {"User-Agent": SS_USER_AGENT}
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            if resp.status_code == 429:
                wait = 2 ** attempt
                print(f"速率限制，等待 {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            if attempt == 2:
                print(f"API 请求失败: {e}")
                return None
            time.sleep(2 ** attempt)
    return None


def search_by_title(title: str, author: str | None = None, limit: int = 5) -> list[dict]:
    """按标题搜索，返回候选论文列表。"""
    query = title
    if author:
        query = f"{title} {author}"
    params = {"query": query, "limit": limit, "fields": "title,authors,year,journal,externalIds,isOpenAccess,openAccessPdf"}
    result = _ss_get("paper/search", params)
    if not result or "data" not in result:
        return []
    return result["data"]


def get_paper_by_doi(doi: str) -> dict | None:
    """按 DOI 获取单篇论文元信息。"""
    fields = "title,authors,year,journal,externalIds,isOpenAccess,openAccessPdf,publicationTypes,citationStyles"
    params = {"fields": fields}
    return _ss_get(f"paper/DOI:{quote(doi, safe='')}", params)


def search_by_journal_keywords(
    journal: str, keywords: str, years: str | None = None, limit: int = 10
) -> list[dict]:
    """按期刊+关键词搜索，限定 journal-list.md 期刊范围。"""
    known_journals = _load_journal_list()
    journal_full = journal
    for j in known_journals:
        if journal.lower() in j.lower():
            journal_full = j
            break
    query = f"{keywords}"
    params = {
        "query": query,
        "limit": limit * 2,
        "fields": "title,authors,year,journal,externalIds,isOpenAccess,openAccessPdf",
    }
    if years:
        params["year"] = years
    result = _ss_get("paper/search", params)
    if not result or "data" not in result:
        return []
    candidates = []
    for paper in result["data"]:
        jn = (paper.get("journal") or {}).get("name", "")
        if journal_full.lower() in jn.lower() or journal.lower() in jn.lower():
            candidates.append(paper)
    return candidates[:limit]


# ── PDF 下载 ────────────────────────────────────────────
def download_pdf(url: str, output_path: Path) -> bool:
    """下载 PDF 文件，校验文件头。"""
    headers = {"User-Agent": SS_USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=120, stream=True)
        resp.raise_for_status()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        # 校验 PDF 头
        with open(output_path, "rb") as f:
            header = f.read(4)
            if header != b"%PDF":
                print(f"警告：下载的文件不是有效 PDF（文件头: {header!r}）")
                output_path.unlink(missing_ok=True)
                return False
        print(f"PDF 已保存: {output_path}")
        return True
    except requests.RequestException as e:
        print(f"下载失败: {e}")
        return False


# ── 元信息生成 ──────────────────────────────────────────
def _pick_author_name(authors: list[dict]) -> str:
    """从作者列表取第一作者姓。"""
    if authors and authors[0].get("name"):
        return authors[0]["name"].split()[-1].lower()
    return "unknown"


def _build_filename(paper: dict) -> str:
    """构造文件名: author-year-shorttitle.pdf"""
    authors = paper.get("authors") or []
    first_author = _pick_author_name(authors)
    year = paper.get("year", "0000")
    title = (paper.get("title") or "untitled").lower()
    title_slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")[:60]
    return f"{first_author}-{year}-{title_slug}.pdf"


def _build_meta(paper: dict, reading_type: str, reading_url: str) -> dict:
    """生成 .meta.json 内容。"""
    journal_info = paper.get("journal") or {}
    external_ids = paper.get("externalIds") or {}
    doi = external_ids.get("DOI", "")
    citation = paper.get("citationStyles", {}).get("bibtex", "")

    return {
        "doi": doi,
        "title": paper.get("title", ""),
        "authors": [a.get("name", "") for a in (paper.get("authors") or [])],
        "year": paper.get("year"),
        "journal": journal_info.get("name", ""),
        "reading_copy": {
            "type": reading_type,
            "url": reading_url,
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
        },
        "citation_info": {
            "type": "article",
            "journal_full": journal_info.get("name", ""),
            "volume": journal_info.get("volume", ""),
            "pages": journal_info.get("pages", ""),
            "doi": doi,
        },
        "bibtex": citation,
    }


# ── 主流程 ──────────────────────────────────────────────
def resolve_and_download(
    doi: str | None = None,
    title: str | None = None,
    author: str | None = None,
    journal: str | None = None,
    keywords: str | None = None,
    years: str | None = None,
    output_dir: Path | None = None,
    interactive: bool = True,
) -> int:
    """主入口：解析论文 → 下载 PDF → 写 .meta.json。"""
    output_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. 查找论文 ─────────────────────────────────────
    paper = None

    if doi:
        print(f"按 DOI 查询: {doi}")
        paper = get_paper_by_doi(doi)
        if not paper:
            print(f"未找到 DOI: {doi}")
            return 1
    elif journal and keywords:
        print(f"按期刊+关键词搜索: {journal} / {keywords}")
        candidates = search_by_journal_keywords(journal, keywords, years)
        if not candidates:
            print("未找到匹配论文")
            return 1
        if interactive:
            print(f"\n找到 {len(candidates)} 篇候选：\n")
            for i, c in enumerate(candidates):
                auths = ", ".join(a["name"] for a in (c.get("authors") or [])[:3])
                jn = (c.get("journal") or {}).get("name", "?")
                oa = "OA" if c.get("isOpenAccess") else "闭源"
                print(f"  [{i+1}] {c.get('title','?')} ({jn}, {c.get('year','?')}) [{oa}] — {auths}")
            choice = input(f"\n选择论文编号 (1-{len(candidates)}) 或按 Enter 跳过: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(candidates):
                paper = candidates[int(choice) - 1]
            else:
                print("已跳过")
                return 0
        else:
            paper = candidates[0]
    elif title:
        print(f"按标题搜索: {title}")
        candidates = search_by_title(title, author)
        if not candidates:
            print("未找到匹配论文")
            return 1
        if interactive and len(candidates) > 1:
            print(f"\n找到 {len(candidates)} 篇候选：\n")
            for i, c in enumerate(candidates):
                auths = ", ".join(a["name"] for a in (c.get("authors") or [])[:3])
                jn = (c.get("journal") or {}).get("name", "?")
                oa = "OA" if c.get("isOpenAccess") else "闭源"
                print(f"  [{i+1}] {c.get('title','?')} ({jn}, {c.get('year','?')}) [{oa}] — {auths}")
            choice = input(f"\n选择论文编号 (1-{len(candidates)}) 或按 Enter 选第1篇: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(candidates):
                paper = candidates[int(choice) - 1]
            else:
                paper = candidates[0]
        else:
            paper = candidates[0]
    else:
        print("请指定 --doi、--title 或 --journal + --keywords")
        return 1

    title_str = paper.get("title", "未知标题")
    print(f"\n选中: {title_str}")

    # ── 2. 尝试下载 ─────────────────────────────────────
    reading_type = "published"
    reading_url = ""

    if paper.get("isOpenAccess"):
        oa_info = paper.get("openAccessPdf") or {}
        reading_url = oa_info.get("url", "")
    if not reading_url and doi:
        # 补查完整 detail 以获取 openAccessPdf
        detail = get_paper_by_doi(doi)
        if detail:
            oa_info = detail.get("openAccessPdf") or {}
            reading_url = oa_info.get("url", "")

    if reading_url:
        print(f"开放获取 PDF: {reading_url}")
    else:
        print("非开放获取。尝试搜索 working paper 版本...")
        # 用标题搜索，看是否有 arXiv / SSRN / 作者主页版本
        candidates = search_by_title(title_str, limit=10)
        for c in candidates:
            if c.get("isOpenAccess"):
                oa = c.get("openAccessPdf") or {}
                alt_url = oa.get("url", "")
                if alt_url and ("arxiv" in alt_url.lower() or "ssrn" in alt_url.lower()):
                    reading_url = alt_url
                    reading_type = "working_paper"
                    print(f"找到 working paper: {reading_url}")
                    break
        if not reading_url:
            print("未能找到可下载版本。请手动下载 PDF 放入 pdfs/ 目录。")
            # 仍生成 meta，但标记为未下载
            meta = _build_meta(paper, "unavailable", "")
            meta_path = output_dir / _build_filename(paper).replace(".pdf", ".meta.json")
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"元信息已保存: {meta_path}")
            return 1

    # ── 3. 下载并保存 ────────────────────────────────────
    filename = _build_filename(paper)
    pdf_path = output_dir / filename
    if not download_pdf(reading_url, pdf_path):
        return 1

    meta = _build_meta(paper, reading_type, reading_url)
    meta_path = output_dir / pdf_path.stem + ".meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"元信息已保存: {meta_path}")

    # ── 4. 汇总输出 ──────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"标题: {title_str}")
    print(f"阅读版本: {reading_type}")
    print(f"正式引用: {meta['citation_info']['journal_full']}, {meta['citation_info']['volume']}, {meta['citation_info']['pages']}")
    print(f"DOI: {meta['doi']}")
    print(f"PDF: {pdf_path}")
    print(f"Meta: {meta_path}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="核心范文 PDF 下载工具（Semantic Scholar API）"
    )
    parser.add_argument("--doi", type=str, help="按 DOI 下载")
    parser.add_argument("--title", type=str, help="按标题搜索")
    parser.add_argument("--author", type=str, help="按标题搜索时的作者筛选")
    parser.add_argument("--journal", type=str, help="按期刊搜索（限定 journal-list.md 范围）")
    parser.add_argument("--keywords", type=str, help="按期刊搜索时的关键词")
    parser.add_argument("--years", type=str, help="年份范围（如 2024-2026）")
    parser.add_argument("--output-dir", type=Path, default=None, help="输出目录")
    parser.add_argument("--no-interactive", action="store_true", help="非交互模式，直接选第一篇")
    args = parser.parse_args()

    if not any([args.doi, args.title, args.journal]):
        parser.print_help()
        return 1

    return resolve_and_download(
        doi=args.doi,
        title=args.title,
        author=args.author,
        journal=args.journal,
        keywords=args.keywords,
        years=args.years,
        output_dir=args.output_dir,
        interactive=not args.no_interactive,
    )


if __name__ == "__main__":
    raise SystemExit(main())
