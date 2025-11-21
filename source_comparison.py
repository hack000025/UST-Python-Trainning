#!/usr/bin/env python3
"""Recreated document comparison tool from screenshots supplied by the user."""

from __future__ import annotations

import difflib
import os
import re
from collections import Counter
from typing import Any, Dict, List, Sequence, Tuple

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyMuPDF (fitz) is required. Install it with `pip install pymupdf`."
    ) from exc

PDFWord = Dict[str, Any]


def normalize_word(text: str) -> str:
    """Normalize text so diffs ignore case and punctuation."""
    cleaned = re.sub(r"\s+", " ", text).strip().lower()
    return re.sub(r"[^a-z0-9]+", "", cleaned)


def chunk_text(words: Sequence[PDFWord]) -> str:
    """Concatenate the original text of a sequence of word dictionaries."""
    return " ".join(word["text"] for word in words).strip()


def extract_words_from_pdf(pdf_path: str) -> Tuple[List[List[PDFWord]], bytes]:
    """Return word metadata for every page plus the raw PDF bytes."""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with open(pdf_path, "rb") as fh:
        pdf_bytes = fh.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    words_pages: List[List[PDFWord]] = []

    for page in doc:
        page_words: List[PDFWord] = []
        for entry in page.get_text("words"):
            x0, y0, x1, y1, text, block, line, word_no = entry
            text = text.strip()
            normalized = normalize_word(text)
            if not text or not normalized:
                continue
            page_words.append(
                {
                    "text": text,
                    "normalized": normalized,
                    "rect": (x0, y0, x1, y1),
                    "block": int(block),
                    "line": int(line),
                    "word": int(word_no),
                    "page": page.number,
                }
            )
        words_pages.append(page_words)

    doc.close()
    return words_pages, pdf_bytes


def _consume_budget(words: Sequence[PDFWord], budget: Counter) -> List[PDFWord]:
    """Return the subset of words that still have budget (i.e., truly added/removed)."""
    selected: List[PDFWord] = []
    for word in words:
        key = word.get("normalized")
        if not key:
            continue
        remaining = budget.get(key, 0)
        if remaining <= 0:
            continue
        selected.append(word)
        if remaining == 1:
            del budget[key]
        else:
            budget[key] = remaining - 1
    return selected


def compute_word_diffs(
    words_pages1: List[List[PDFWord]], words_pages2: List[List[PDFWord]]
) -> List[Dict[str, Any]]:
    """Generate word-level diff metadata using difflib."""
    words1_full = [word for page in words_pages1 for word in page]
    words2_full = [word for page in words_pages2 for word in page]

    words1 = [word["normalized"] for word in words1_full]
    words2 = [word["normalized"] for word in words2_full]

    deleted_budget = Counter(words1) - Counter(words2)
    inserted_budget = Counter(words2) - Counter(words1)

    matcher = difflib.SequenceMatcher(a=words1, b=words2, autojunk=False)
    diffs: List[Dict[str, Any]] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "delete":
            chunk = _consume_budget(words1_full[i1:i2], deleted_budget)
            if chunk:
                diffs.append(
                    {"type": "deleted", "words": chunk, "text": chunk_text(chunk)}
                )
        elif tag == "insert":
            chunk = _consume_budget(words2_full[j1:j2], inserted_budget)
            if chunk:
                diffs.append(
                    {"type": "inserted", "words": chunk, "text": chunk_text(chunk)}
                )
        elif tag == "replace":
            old_chunk = _consume_budget(words1_full[i1:i2], deleted_budget)
            new_chunk = _consume_budget(words2_full[j1:j2], inserted_budget)
            if old_chunk and new_chunk:
                diffs.append(
                    {
                        "type": "replaced",
                        "old": old_chunk,
                        "new": new_chunk,
                        "old_text": chunk_text(old_chunk),
                        "new_text": chunk_text(new_chunk),
                    }
                )
            elif old_chunk:
                diffs.append(
                    {"type": "deleted", "words": old_chunk, "text": chunk_text(old_chunk)}
                )
            elif new_chunk:
                diffs.append(
                    {"type": "inserted", "words": new_chunk, "text": chunk_text(new_chunk)}
                )

    return diffs


def _annotate_words(
    doc: fitz.Document, words: Sequence[PDFWord], *, color: Tuple[float, float, float], label: str, title: str
) -> None:
    """Apply rectangle annotations for all provided words."""
    for word in words:
        rect = fitz.Rect(*word["rect"])
        annot = doc[word["page"]].add_rect_annot(rect)
        annot.set_colors(stroke=color, fill=color)
        annot.set_border(width=0.6)
        annot.set_opacity(0.25)
        annot.set_info({"title": title, "content": label})
        annot.update()


def highlight_pdf_diff(
    pdf_bytes: bytes,
    words_pages: List[List[PDFWord]],
    diff_info: List[Dict[str, Any]],
    original: bool = True,
) -> bytes:
    """Return new PDF bytes with highlights showing differences."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    title = "ORIGINAL" if original else "UPDATED"

    for diff in diff_info:
        diff_type = diff["type"]
        if diff_type == "deleted":
            if not original:
                continue
            label = f"Deleted: {diff['text']}"
            _annotate_words(doc, diff["words"], color=(0.87, 0.27, 0.27), label=label, title=title)
        elif diff_type == "inserted":
            if original:
                continue
            label = f"Inserted: {diff['text']}"
            _annotate_words(doc, diff["words"], color=(0.24, 0.62, 0.36), label=label, title=title)
        elif diff_type == "replaced":
            target = diff["old"] if original else diff["new"]
            if not target:
                continue
            which = "old" if original else "new"
            label = f"Replaced ({which}): {diff[f'{which}_text']}"
            _annotate_words(doc, target, color=(0.97, 0.78, 0.29), label=label, title=title)

    pdf_data = doc.tobytes()
    doc.close()
    return pdf_data


def generate_html_report(
    old_pdf_path: str,
    new_pdf_path: str,
    highlighted_old_pdf_path: str,
    highlighted_new_pdf_path: str,
    output_html: str,
) -> None:
    """Create a simple HTML dashboard to view highlighted PDFs side-by-side."""
    old_name = os.path.basename(old_pdf_path)
    new_name = os.path.basename(new_pdf_path)
    old_embed = os.path.basename(highlighted_old_pdf_path)
    new_embed = os.path.basename(highlighted_new_pdf_path)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Document Comparison Tool</title>
    <style>
        :root {{
            --red: #dc4c4c;
            --green: #3ca873;
            --amber: #f5b942;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            padding: 2rem;
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #f7f9fc, #eef2f7);
            color: #1f2933;
        }}
        .shell {{
            max-width: 1200px;
            margin: 0 auto;
            background: #fff;
            padding: 2.5rem;
            border-radius: 18px;
            box-shadow: 0 25px 55px rgba(15, 23, 42, 0.15);
        }}
        header {{
            text-align: center;
            margin-bottom: 2.5rem;
        }}
        header h1 {{
            margin: 0;
            font-size: 2rem;
            letter-spacing: 0.02em;
        }}
        header p {{
            margin: 0.35rem 0 0;
            color: #5f6c7b;
        }}
        .pdf-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }}
        .panel {{
            border: 1px solid #e4e9f2;
            border-radius: 14px;
            padding: 1.25rem;
            background: #fbfcfe;
            box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.05);
        }}
        .panel h2 {{
            margin: 0 0 0.75rem;
            font-size: 1.1rem;
            color: #374151;
        }}
        iframe {{
            width: 100%;
            min-height: 640px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
            background: #fff;
        }}
        footer {{
            margin-top: 2rem;
            text-align: center;
            color: #6b7280;
            font-size: 0.95rem;
        }}
        footer span {{
            font-weight: 600;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            iframe {{
                min-height: 520px;
            }}
        }}
    </style>
</head>
<body>
    <div class="shell">
        <header>
            <h1>Document Comparison Tool (Optimized)</h1>
            <p><strong>Old document:</strong> {old_name}</p>
            <p><strong>New document:</strong> {new_name}</p>
        </header>
        <section class="pdf-grid">
            <article class="panel">
                <h2>Highlighted – Old PDF</h2>
                <iframe src="{old_embed}" title="Old PDF with highlights"></iframe>
            </article>
            <article class="panel">
                <h2>Highlighted – New PDF</h2>
                <iframe src="{new_embed}" title="New PDF with highlights"></iframe>
            </article>
        </section>
        <footer>
            <span>Legend:</span> Red = deleted text, Green = inserted text, Amber = modified text.
        </footer>
    </div>
</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as fh:
        fh.write(html)


def main() -> None:
    """CLI entry point."""
    print("=== Document Comparison Tool ===")
    try:
        old_pdf_path = input("Enter path to the OLD / ORIGINAL PDF: ").strip()
        new_pdf_path = input("Enter path to the NEW / UPDATED PDF: ").strip()
        output_dir = input(
            "Enter output directory (leave empty to reuse the original folder): "
        ).strip()
    except EOFError:
        print("Input aborted.")
        return

    if not old_pdf_path or not new_pdf_path:
        print("Both PDF paths are required.")
        return

    if not output_dir:
        output_dir = os.path.dirname(os.path.abspath(old_pdf_path)) or os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    print("Extracting words and loading PDFs...")
    words_pages1, pdf_bytes1 = extract_words_from_pdf(old_pdf_path)
    words_pages2, pdf_bytes2 = extract_words_from_pdf(new_pdf_path)

    print("Computing differences...")
    diff_info = compute_word_diffs(words_pages1, words_pages2)

    print("Creating highlighted PDFs...")
    highlighted_old = highlight_pdf_diff(pdf_bytes1, words_pages1, diff_info, original=True)
    highlighted_new = highlight_pdf_diff(pdf_bytes2, words_pages2, diff_info, original=False)

    highlighted_old_path = os.path.join(output_dir, "highlighted_old.pdf")
    highlighted_new_path = os.path.join(output_dir, "highlighted_new.pdf")
    with open(highlighted_old_path, "wb") as fh:
        fh.write(highlighted_old)
    with open(highlighted_new_path, "wb") as fh:
        fh.write(highlighted_new)

    report_path = os.path.join(output_dir, "comparison_report.html")
    generate_html_report(
        old_pdf_path,
        new_pdf_path,
        highlighted_old_path,
        highlighted_new_path,
        report_path,
    )

    print("\nAll done!")
    print(f" - Highlighted OLD PDF: {highlighted_old_path}")
    print(f" - Highlighted NEW PDF: {highlighted_new_path}")
    print(f" - HTML report       : {report_path}")


if __name__ == "__main__":
    main()

