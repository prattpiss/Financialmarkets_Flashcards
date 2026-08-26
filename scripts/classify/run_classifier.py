"""
Phase 1 – Document Classifier
Reads all PDF files from the source directory, extracts text via pdfplumber,
classifies each document (type, year, current/historical, priority) and writes
the enriched document_inventory.json.

Usage:
    python scripts/classify/run_classifier.py [--source-dir <path>] [--out <path>]

Defaults:
    --source-dir  .  (project root, where the PDFs live)
    --out         document_inventory.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber not installed. Run: pip install pdfplumber")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class DocumentRecord:
    id: str
    file: str
    isCurrent: bool
    ambiguousCurrent: bool
    year: str
    semester: str
    type: str          # script | exercise | solution | mock_exam | other
    subtype: str
    exerciseNumber: Optional[int]
    relatedTo: Optional[str]
    priority: int
    priorityNote: str
    sizeBytes: int
    pageCount: int
    analysisStatus: str  # filename_only | text_extracted | content_classified
    description: str
    role: str
    extractedText: str   # first 2000 chars, used for downstream phases
    detectedKeywords: list[str]
    note: str


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

IS_CURRENT_RE = re.compile(r"jetzt", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(20\d{2})\b")

SCRIPT_RE  = re.compile(r"skript|script", re.IGNORECASE)
EXERCISE_RE = re.compile(r"\bU\d+\b", re.IGNORECASE)
MOCK_EXAM_RE = re.compile(r"probeklausur|probe.klausur", re.IGNORECASE)
EXAM_RE    = re.compile(r"klausur", re.IGNORECASE)
SOLUTION_RE = re.compile(r"lsg|lösung|loesung|solution", re.IGNORECASE)
RECAP_RE   = re.compile(r"recap|zusammenfassung", re.IGNORECASE)
EXERCISE_NUM_RE = re.compile(r"\bU(\d+)\b", re.IGNORECASE)

# Keywords used to detect document type from text when filename is ambiguous
CONTENT_KEYWORDS = {
    "script":    ["kapitel", "abschnitt", "lernziel", "gliederung", "vorlesung"],
    "exercise":  ["aufgabe", "übung", "exercise", "lösung", "berechnen"],
    "mock_exam": ["klausur", "punkte", "bearbeitungszeit", "matrikelnummer"],
    "solution":  ["musterlösung", "muster-lösung", "lösung zur"],
}


def classify_by_filename(stem: str) -> dict:
    is_current = bool(IS_CURRENT_RE.search(stem))
    years = YEAR_RE.findall(stem)
    year = years[0] if years else ("2026" if is_current else "unknown")

    doc_type = "other"
    subtype = ""
    if SOLUTION_RE.search(stem):
        doc_type = "solution"
    elif MOCK_EXAM_RE.search(stem):
        doc_type = "mock_exam"
    elif EXAM_RE.search(stem):
        doc_type = "mock_exam"
    elif SCRIPT_RE.search(stem):
        doc_type = "script"
        if RECAP_RE.search(stem):
            subtype = "recap"
    elif EXERCISE_RE.search(stem):
        doc_type = "exercise"

    exercise_num: Optional[int] = None
    m = EXERCISE_NUM_RE.search(stem)
    if m:
        exercise_num = int(m.group(1))

    ambiguous = not is_current and year == "2026"
    priority = 1 if is_current else 2

    semester = f"SS{year}" if year != "unknown" else "unknown"

    return {
        "isCurrent": is_current,
        "ambiguousCurrent": ambiguous,
        "year": year,
        "semester": semester,
        "type": doc_type,
        "subtype": subtype,
        "exerciseNumber": exercise_num,
        "priority": priority,
    }


def classify_by_content(text: str) -> str:
    """Refine doc type using extracted text when filename was ambiguous."""
    text_lower = text.lower()
    scores: dict[str, int] = {k: 0 for k in CONTENT_KEYWORDS}
    for doc_type, keywords in CONTENT_KEYWORDS.items():
        for kw in keywords:
            scores[doc_type] += text_lower.count(kw)
    return max(scores, key=lambda k: scores[k])


def extract_keywords(text: str) -> list[str]:
    finance_terms = [
        "modigliani-miller", "finanzintermediation", "eigenkapital", "fremdkapital",
        "kapitalstruktur", "leverage", "diskontierung", "rendite", "zinsen",
        "kapitalallokation", "finanzsystem", "bank", "regulierung", "basel",
        "insolvenz", "liquidität", "risiko", "diversifikation", "portfolio",
        "aktien", "anleihen", "etf", "fonds", "derivate", "optionen",
        "finanzmarkteffizienz", "informationsasymmetrie", "moral hazard",
        "adverse selektion", "too big to fail", "systemrisiko", "haircut",
        "repo", "sicherheiten", "hebel", "verschuldungsgrad",
    ]
    found = []
    text_lower = text.lower()
    for term in finance_terms:
        if term in text_lower:
            found.append(term)
    return found


def build_role(doc_type: str, is_current: bool, ambiguous: bool) -> str:
    prefix = "CURRENT" if is_current else ("AMBIGUOUS" if ambiguous else "HISTORICAL")
    return f"{doc_type.upper()}_{prefix}"


# ---------------------------------------------------------------------------
# Main classifier
# ---------------------------------------------------------------------------

def classify_directory(source_dir: Path) -> list[DocumentRecord]:
    pdf_files = sorted(source_dir.glob("*.pdf"))
    records: list[DocumentRecord] = []

    for idx, pdf_path in enumerate(pdf_files, start=1):
        doc_id = f"doc-{idx:03d}"
        size = pdf_path.stat().st_size
        stem = pdf_path.stem

        cls = classify_by_filename(stem)

        # Extract text
        extracted = ""
        page_count = 0
        analysis_status = "filename_only"
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                texts = []
                for page in pdf.pages[:8]:  # first 8 pages for classification
                    t = page.extract_text()
                    if t:
                        texts.append(t)
                extracted = "\n".join(texts)
                analysis_status = "text_extracted"
        except Exception as e:
            extracted = ""
            analysis_status = f"extraction_failed: {e}"

        # Refine type if ambiguous
        if cls["type"] == "other" and extracted:
            cls["type"] = classify_by_content(extracted)
            analysis_status = "content_classified"

        keywords = extract_keywords(extracted)
        preview = extracted[:2000] if extracted else ""

        # Related-to for solutions
        related_to: Optional[str] = None
        if cls["type"] == "solution":
            base = re.sub(r"_?(lsg|lösung|loesung|solution)", "", stem, flags=re.IGNORECASE).strip()
            related_to = f"{base}.pdf"

        note = ""
        if not cls["isCurrent"] and cls["type"] == "exercise":
            ex = cls.get("exerciseNumber")
            if ex:
                current_partner = source_dir / f"U{ex:02d}_jetzt.pdf"
                if not current_partner.exists():
                    note = f"Kein U{ex:02d}_jetzt.pdf vorhanden – Thema möglicherweise nicht mehr aktuell"

        record = DocumentRecord(
            id=doc_id,
            file=pdf_path.name,
            isCurrent=cls["isCurrent"],
            ambiguousCurrent=cls["ambiguousCurrent"],
            year=cls["year"],
            semester=cls["semester"],
            type=cls["type"],
            subtype=cls["subtype"],
            exerciseNumber=cls["exerciseNumber"],
            relatedTo=related_to,
            priority=cls["priority"],
            priorityNote=(
                "Kein 'jetzt'-Label aber Jahreszahl 2026 – potenziell aktuell"
                if cls["ambiguousCurrent"] else ""
            ),
            sizeBytes=size,
            pageCount=page_count,
            analysisStatus=analysis_status,
            description=f"{cls['type'].capitalize()} – {stem}",
            role=build_role(cls["type"], cls["isCurrent"], cls["ambiguousCurrent"]),
            extractedText=preview,
            detectedKeywords=keywords,
            note=note,
        )
        records.append(record)
        print(f"  [{doc_id}] {pdf_path.name} → {cls['type']}, priority={cls['priority']}, pages={page_count}, keywords={len(keywords)}")

    return records


def build_inventory(records: list[DocumentRecord], source_dir: Path) -> dict:
    current = [r for r in records if r.isCurrent]
    historical = [r for r in records if not r.isCurrent and not r.ambiguousCurrent]
    ambiguous = [r for r in records if r.ambiguousCurrent]

    by_type: dict[str, list[str]] = {}
    by_priority: dict[str, list[str]] = {"1_current": [], "2_historical": []}
    for r in records:
        by_type.setdefault(r.type, []).append(r.id)
        key = "1_current" if r.isCurrent else "2_historical"
        by_priority[key].append(r.id)

    # Processing order: current script first, then current exercises, then ambiguous exams, then historical
    def sort_key(r: DocumentRecord):
        if r.isCurrent and r.type == "script": return 0
        if r.isCurrent and r.type == "exercise": return 1
        if r.ambiguousCurrent and r.type == "solution": return 2
        if r.ambiguousCurrent: return 3
        if r.type == "script" and "recap" in r.subtype: return 4
        if r.type == "mock_exam": return 5
        if r.type == "script": return 6
        return 7

    processing_order = [r.file for r in sorted(records, key=sort_key)]

    docs_dicts = []
    for r in records:
        d = asdict(r)
        # Don't bloat the inventory with full text; that goes to a separate cache
        d.pop("extractedText", None)
        docs_dicts.append(d)

    return {
        "meta": {
            "generatedAt": "2026-08-27",
            "generatedBy": "scripts/classify/run_classifier.py",
            "analysisVersion": "1.1.0",
            "sourceDir": str(source_dir),
            "totalFiles": len(records),
            "currentFiles": len(current),
            "historicalFiles": len(historical),
            "ambiguousFiles": len(ambiguous),
        },
        "documents": docs_dicts,
        "summary": {
            "byType": by_type,
            "byPriority": by_priority,
            "processingOrder": processing_order,
        },
    }


def save_text_cache(records: list[DocumentRecord], out_dir: Path) -> None:
    """Save extracted text for downstream phases."""
    cache_dir = out_dir / "text_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for r in records:
        if r.extractedText:
            cache_file = cache_dir / f"{Path(r.file).stem}.txt"
            cache_file.write_text(r.extractedText, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Phase 1 – Document Classifier")
    parser.add_argument("--source-dir", default=".", help="Directory containing PDF files")
    parser.add_argument("--out", default="document_inventory.json", help="Output JSON path")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    out_path = Path(args.out)

    print(f"Scanning: {source_dir}")
    records = classify_directory(source_dir)
    print(f"\nClassified {len(records)} documents.")

    inventory = build_inventory(records, source_dir)

    out_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nInventory written to: {out_path}")

    # Save text extracts for Phase 2
    save_text_cache(records, source_dir / "scripts" / "output")
    print("Text cache written to: scripts/output/text_cache/")


if __name__ == "__main__":
    main()
