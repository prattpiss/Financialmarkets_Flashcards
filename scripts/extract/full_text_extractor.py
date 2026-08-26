"""
Phase 2a – Full Text Extractor
Extracts complete text from all PDFs (all pages), fixes German umlaut encoding,
and saves structured text files for downstream knowledge extraction.

Usage:
    python scripts/extract/full_text_extractor.py [--source-dir <path>] [--out-dir <path>]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("Run: pip install pdfplumber")


# ---------------------------------------------------------------------------
# Encoding fixes (LaTeX beamer PDF artifacts)
# ---------------------------------------------------------------------------

# Combining diaeresis character is emitted as ¨ followed by the base letter
_UMLAUT_MAP = {
    "¨a": "ä", "¨u": "ü", "¨o": "ö",
    "¨A": "Ä", "¨U": "Ü", "¨O": "Ö",
    "a¨": "ä", "u¨": "ü", "o¨": "ö",  # reversed order variant
    # Acute / other accents seen in some exports
    "´a": "á", "´e": "é", "´i": "í", "´o": "ó", "´u": "ú",
}

# (cid:N) → unicode replacements for common symbols in beamer PDFs
_CID_MAP = {
    136: "•",   # bullet
    150: "–",   # en dash
    151: "—",   # em dash
    164: "€",   # euro
    174: "®",
    176: "°",
    180: "´",
    183: "·",
    8226: "•",
}

_CID_RE = re.compile(r"\(cid:(\d+)\)")


def fix_encoding(text: str) -> str:
    """Fix encoding artifacts from pdfplumber on LaTeX-generated PDFs."""
    # CID symbols
    def replace_cid(m: re.Match) -> str:
        n = int(m.group(1))
        return _CID_MAP.get(n, f"[cid:{n}]")

    text = _CID_RE.sub(replace_cid, text)

    # Umlaut combinations – apply longest match first
    for wrong, right in _UMLAUT_MAP.items():
        text = text.replace(wrong, right)

    return text


# ---------------------------------------------------------------------------
# Slide / page metadata extraction
# ---------------------------------------------------------------------------

_SLIDE_NUM_RE = re.compile(r"^(\d+)/(\d+)\s*$", re.MULTILINE)


def extract_full_text(pdf_path: Path) -> list[dict]:
    """
    Returns a list of page dicts:
        {"page": int, "text": str, "slide_num": int | None, "total_slides": int | None}
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        total_slides: int | None = None
        for page_idx, page in enumerate(pdf.pages):
            raw = page.extract_text() or ""
            text = fix_encoding(raw)

            # Detect slide counter (e.g. "42/612")
            slide_num: int | None = None
            m = _SLIDE_NUM_RE.search(text)
            if m:
                slide_num = int(m.group(1))
                total_slides = int(m.group(2))
                # Remove the counter line from content
                text = _SLIDE_NUM_RE.sub("", text).strip()

            pages.append({
                "page": page_idx + 1,
                "slideNum": slide_num,
                "totalSlides": total_slides,
                "text": text,
            })
    return pages


# ---------------------------------------------------------------------------
# Chapter / section detector
# ---------------------------------------------------------------------------

# Roman numeral section headers: "I.", "II.", "III.", "IV.", ...
_ROMAN_RE = re.compile(r"^(I{1,3}|IV|V|VI{1,3}|IX|X)\.[ \t]+(.+)$", re.MULTILINE)
# Arabic section headers: "1.", "2.1", "2.1.1" etc.
_ARABIC_RE = re.compile(r"^(\d+(?:\.\d+)*)\.[ \t]+(.+)$", re.MULTILINE)
# Common German keyword markers on their own line
_HEADER_KEYWORDS = re.compile(
    r"^(Einführung|Zusammenfassung|Fazit|Literatur|Gliederung|Lernziele?|Definition|Überblick|Motivation)$",
    re.MULTILINE | re.IGNORECASE,
)


def detect_chapters(pages: list[dict]) -> list[dict]:
    """Annotate each page with chapter/section if a header is detected."""
    current_part = ""
    current_chapter = ""
    current_section = ""

    for page in pages:
        text = page["text"]

        roman = _ROMAN_RE.search(text)
        if roman:
            current_part = roman.group(2).strip()
            current_chapter = ""
            current_section = ""

        arabic = _ARABIC_RE.search(text)
        if arabic:
            num = arabic.group(1)
            title = arabic.group(2).strip()
            depth = num.count(".") + 1
            if depth == 1:
                current_chapter = f"{num}. {title}"
                current_section = ""
            else:
                current_section = f"{num} {title}"

        page["part"] = current_part
        page["chapter"] = current_chapter
        page["section"] = current_section

    return pages


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_pdf(pdf_path: Path, out_dir: Path) -> dict:
    """Extract, fix, annotate and save one PDF. Returns metadata."""
    print(f"  Extracting: {pdf_path.name} ...", end=" ", flush=True)
    pages = extract_full_text(pdf_path)
    pages = detect_chapters(pages)

    # Save structured JSON
    out_json = out_dir / f"{pdf_path.stem}.json"
    out_json.write_text(
        json.dumps({"file": pdf_path.name, "pages": pages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Save plain text (joined, for easy reading)
    out_txt = out_dir / f"{pdf_path.stem}_full.txt"
    joined = "\n\n---PAGE---\n\n".join(p["text"] for p in pages if p["text"].strip())
    out_txt.write_text(joined, encoding="utf-8")

    print(f"{len(pages)} pages → {out_json.name}")
    return {
        "file": pdf_path.name,
        "pageCount": len(pages),
        "outputJson": str(out_json),
        "outputTxt": str(out_txt),
    }


def main():
    parser = argparse.ArgumentParser(description="Phase 2a – Full Text Extractor")
    parser.add_argument("--source-dir", default=".", help="Directory with PDFs")
    parser.add_argument("--out-dir", default="scripts/output/full_text", help="Output directory")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(source_dir.glob("*.pdf"))
    print(f"Extracting {len(pdf_files)} PDFs from {source_dir}\n")

    results = []
    for pdf_path in pdf_files:
        meta = process_pdf(pdf_path, out_dir)
        results.append(meta)

    # Write manifest
    manifest = out_dir / "manifest.json"
    manifest.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. Manifest: {manifest}")


if __name__ == "__main__":
    main()
