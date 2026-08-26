"""
Phase 2b – Knowledge Base Builder
Parses the TOC from the current script, maps pages to chapters,
extracts learning objectives / definitions / formulas,
and writes knowledge_base.json.

Usage:
    python scripts/extract/knowledge_builder.py [--out knowledge_base.json]
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Hard-coded TOC parsed from the SS2026 script (pages 2–16)
# This is the authoritative chapter structure.
# ---------------------------------------------------------------------------

CHAPTERS: list[dict] = [
    {
        "part": "I. Einführung",
        "number": "1",
        "title": "Funktionen des Finanzsystems",
        "sections": [],
    },
    {
        "part": "I. Einführung",
        "number": "2",
        "title": "Die globale Finanzkrise und ihre Auswirkungen",
        "sections": [
            "2.1 Stilisierte Fakten über Finanzkrisen",
            "2.2 Die globale Finanzkrise von 2007–2009",
            "2.3 Die Krise im Euroraum",
            "2.4 Die 2020er-Jahre",
        ],
    },
    {
        "part": "II. Die Kapitalstruktur von Unternehmen",
        "number": "3",
        "title": "Die Kapitalstruktur in einem vollkommenen Markt und das Modigliani-Miller-Theorem",
        "sections": [
            "3.1 Finanzierung durch Eigen- oder Fremdkapital",
            "3.2 Das Modigliani-Miller-Theorem",
            "3.3 Kapitalstruktur und Eigenkapitalkosten",
            "3.4 Trugschlüsse bei der Kapitalstruktur",
            "3.5 Fazit",
        ],
    },
    {
        "part": "II. Die Kapitalstruktur von Unternehmen",
        "number": "4",
        "title": "Der Einfluss von Marktunvollkommenheiten auf die Kapitalstruktur",
        "sections": [
            "4.1 Fremdkapital und Steuern",
            "4.1.1 Der fremdfinanzierungsbedingte Steuervorteil",
            "4.1.2 Rekapitalisierung zur Nutzung von Steuervorteilen",
            "4.1.3 Steuern auf Investorenebene",
            "4.1.4 Die optimale Kapitalstruktur mit Steuern",
            "4.1.5 Fazit",
            "4.2 Konkurskosten, Managementanreize und asymmetrische Information",
            "4.2.1 Konkurskosten und der Unternehmenswert",
            "4.2.2 Agency-Theorie der Verschuldung",
            "4.2.3 Asymmetrische Information und Kapitalstruktur",
        ],
    },
    {
        "part": "III. Finanzinstitutionen",
        "number": "5",
        "title": "Funktionen von Banken",
        "sections": [
            "5.1 Versicherung gegen Liquiditätsschocks",
            "5.2 Delegierte Kontrolle",
        ],
    },
    {
        "part": "IV. Finanzstabilität",
        "number": "6",
        "title": "Finanzkrisen und systemische Risiken",
        "sections": [
            "6.1 Das Grundproblem",
            "6.2 Narrow Banking",
            "6.3 Aufhebung der Konvertibilität und Einlagenversicherung",
            "6.4 Effiziente Bank Runs",
            "6.5 Ansteckungseffekte im Finanzsystem",
            "6.6 Der Lender of Last Resort",
            "6.7 Das \"Too-big-to-fail\"-Phänomen",
        ],
    },
    {
        "part": "IV. Finanzstabilität",
        "number": "7",
        "title": "Bankenregulierung",
        "sections": [
            "7.1 Gründe für Bankenregulierung",
            "7.2 Eigenkapitalregulierung",
            "7.3 Funktionen der Eigenkapitalregulierung",
            "7.4 Schwächen der Vorkrisen-Regulierung",
            "7.5 Die Regulierung des systemischen Risikos",
            "7.6 Herausforderungen für die Zukunft",
        ],
    },
]

# ---------------------------------------------------------------------------
# Chapter boundary detection
# ---------------------------------------------------------------------------

def _chapter_header_pattern(num: str, title: str) -> re.Pattern:
    """Build a regex that matches a chapter header line in slide text."""
    # Match the chapter number at start of line, then any text up to the title
    num_escaped = re.escape(num) + r"\."
    # Match first ~30 chars of title (truncated to handle line breaks in slides)
    title_prefix = re.escape(title[:30])
    return re.compile(
        rf"(?:^|\n){num_escaped}\s+{title_prefix}",
        re.IGNORECASE,
    )


def find_chapter_boundaries(pages: list[dict]) -> dict[str, list[int]]:
    """
    Returns {chapter_number: [page_indices_that_belong_to_this_chapter]}.
    Uses slide text to find where each chapter starts.
    """
    # Build patterns for each chapter
    patterns = [
        (_chapter_header_pattern(ch["number"], ch["title"]), ch["number"])
        for ch in CHAPTERS
    ]

    # For each page, check if a chapter header appears in the slide content
    # (not just in the TOC pages 1–17)
    chapter_start_pages: dict[str, int] = {}
    for page in pages:
        pg = page["page"]
        if pg <= 17:   # skip TOC pages
            continue
        text = page["text"]
        for pat, num in patterns:
            if pat.search(text) and num not in chapter_start_pages:
                chapter_start_pages[num] = pg
                break

    # Authoritative anchors from _find_chapters.py (Lernziele/Literatur slide detection)
    MANUAL_ANCHORS = {
        "1": 18,   # slide 16
        "2": 64,   # slide 56
        "3": 102,  # slide 93
        "4": 191,  # slide 174
        "5": 437,  # slide 401
        "6": 530,  # slide 475
        "7": 634,  # slide 560
    }
    # Always override with manual anchors (auto-detection prone to false positives
    # because Gliederung slides repeat all chapter titles)
    chapter_start_pages = dict(MANUAL_ANCHORS)

    # Build page ranges
    sorted_chapters = sorted(chapter_start_pages.items(), key=lambda x: x[1])
    chapter_pages: dict[str, list[int]] = {}
    total_pages = len(pages)
    for i, (num, start) in enumerate(sorted_chapters):
        end = sorted_chapters[i + 1][1] - 1 if i + 1 < len(sorted_chapters) else total_pages
        chapter_pages[num] = list(range(start, end + 1))

    return chapter_pages


# ---------------------------------------------------------------------------
# Text analysis helpers
# ---------------------------------------------------------------------------

# German definition patterns
_DEF_PATTERNS = [
    re.compile(r"(?:^|\n)([A-ZÄÖÜ][^.\n]{3,60})\s+(?:ist|sind|bezeichnet|nennt man|versteht man unter)\s+(.{10,200})", re.MULTILINE),
    re.compile(r"(?:Definition|Def\.)\s*[:\-]\s*(.{10,300})", re.IGNORECASE),
    re.compile(r"([A-ZÄÖÜ][a-zäöüß]+(?:\s+[a-zäöüß]+){0,3})\s*=\s*(.{10,200})"),
]

# Formula patterns (look for mathematical expressions)
_FORMULA_PATTERNS = [
    re.compile(r"([A-Z][A-Z0-9]*)\s*=\s*([^=\n]{5,100})"),   # X = expression
    re.compile(r"r[EFD]\s*=\s*[^=\n]{3,80}"),                 # rE, rD, rF = ...
    re.compile(r"WACC\s*=\s*[^=\n]{5,100}"),
    re.compile(r"V[EFL]\s*=\s*[^=\n]{3,80}"),                  # VE, VF, VL = ...
    re.compile(r"EPS\s*=\s*[^=\n]{5,80}"),
    re.compile(r"NPV\s*=\s*[^=\n]{5,80}"),
    re.compile(r"β[a-z]*\s*=\s*[^=\n]{3,80}"),                # beta formulas
]

# Learning objective markers
_LERNZIEL_RE = re.compile(r"Lernziele?[:\s]*\n((?:▶[^\n]+\n?)+)", re.IGNORECASE)

# Common mistake markers  
_MISTAKE_RE = re.compile(
    r"(?:Trugschluss|häufiger Fehler|falsch|Achtung|Vorsicht|Missverständnis)[:\s]+([^\n]{10,200})",
    re.IGNORECASE,
)


def extract_learning_objectives(pages_text: str) -> list[str]:
    objectives = []
    for m in _LERNZIEL_RE.finditer(pages_text):
        block = m.group(1)
        items = re.findall(r"▶\s*(.+)", block)
        objectives.extend(i.strip() for i in items)
    return objectives


def extract_definitions(pages_text: str) -> list[dict]:
    defs = []
    seen = set()
    for pat in _DEF_PATTERNS:
        for m in pat.finditer(pages_text):
            term = m.group(1).strip()[:80]
            defn = m.group(len(m.groups())).strip()[:300]
            key = term.lower()[:40]
            if key not in seen and len(term) > 3:
                seen.add(key)
                defs.append({"term": term, "definition": defn})
    return defs[:50]  # cap per chapter


def extract_formulas(pages_text: str) -> list[str]:
    formulas = []
    seen = set()
    for pat in _FORMULA_PATTERNS:
        for m in pat.finditer(pages_text):
            f = m.group(0).strip()
            if f not in seen and len(f) > 5:
                seen.add(f)
                formulas.append(f)
    return formulas[:30]


def extract_common_mistakes(pages_text: str) -> list[str]:
    mistakes = []
    for m in _MISTAKE_RE.finditer(pages_text):
        mistakes.append(m.group(1).strip())
    return mistakes[:10]


# ---------------------------------------------------------------------------
# Exercise analysis
# ---------------------------------------------------------------------------

EXERCISE_MAP = {
    "U01_jetzt": "3",   # Kapitalstruktur / MM-Theorem (Teil 1)
    "U02_jetzt": "3",   # MM-Theorem (Teil 2) – assumed
    "U03_jetzt": "4",   # Marktunvollkommenheiten – assumed
    "U04_jetzt": "4",   # assumed
    "U05_jetzt": "5",   # assumed (Banken)
}


def load_exercise_texts(full_text_dir: Path) -> dict[str, str]:
    """Load exercise texts for the current semester."""
    result = {}
    for stem, chapter in EXERCISE_MAP.items():
        json_path = full_text_dir / f"{stem}.json"
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            text = "\n\n".join(p["text"] for p in data["pages"])
            result[stem] = text
    return result


_EXERCISE_RE = re.compile(r"(\d+)\.\s+([^\n]{10,100})\n", re.MULTILINE)


def extract_exercise_topics(text: str) -> list[str]:
    topics = []
    for m in _EXERCISE_RE.finditer(text):
        topics.append(f"{m.group(1)}. {m.group(2).strip()}")
    return topics[:20]


# ---------------------------------------------------------------------------
# Importance scoring
# ---------------------------------------------------------------------------

def score_chapter(
    chapter_num: str,
    has_current_exercise: bool,
    appears_in_exam: bool,
    appears_in_historical: bool,
) -> tuple[float, float]:
    """Return (importance, examRelevance) 0.0 – 1.0."""
    importance = 0.5
    exam_rel = 0.5

    if has_current_exercise:
        importance += 0.3
        exam_rel += 0.3
    if appears_in_exam:
        importance += 0.2
        exam_rel += 0.3
    if appears_in_historical:
        importance += 0.1
        exam_rel += 0.1

    return min(1.0, round(importance, 2)), min(1.0, round(exam_rel, 2))


# ---------------------------------------------------------------------------
# Exam cross-reference
# ---------------------------------------------------------------------------

def load_exam_texts(full_text_dir: Path) -> str:
    """Load all exam texts combined."""
    texts = []
    for name in ["2026_Probeklausur FMI", "2026_Probeklausur FMI_Lsg", "2020 Klausur FMI"]:
        p = full_text_dir / f"{name}.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            texts.append("\n".join(pg["text"] for pg in data["pages"]))
    return "\n\n".join(texts)


def chapter_appears_in_exam(chapter: dict, exam_text: str) -> bool:
    """Check if the chapter title or key terms appear in exam text."""
    title_words = chapter["title"].lower().split()
    significant = [w for w in title_words if len(w) > 5]
    matches = sum(1 for w in significant if w in exam_text.lower())
    return matches >= 2


def chapter_appears_in_historical(chapter: dict, hist_text: str) -> bool:
    title_words = chapter["title"].lower().split()
    significant = [w for w in title_words if len(w) > 5]
    matches = sum(1 for w in significant if w in hist_text.lower())
    return matches >= 2


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_knowledge_base(
    script_json: Path,
    full_text_dir: Path,
    out_path: Path,
) -> None:
    print("Loading script...")
    data = json.loads(script_json.read_text(encoding="utf-8"))
    all_pages = data["pages"]
    all_text = "\n\n".join(p["text"] for p in all_pages)

    print("Finding chapter boundaries...")
    chapter_pages = find_chapter_boundaries(all_pages)

    print("Loading exam texts...")
    exam_text = load_exam_texts(full_text_dir)

    print("Loading historical script...")
    hist_path = full_text_dir / "Skript FMI SS2024.json"
    hist_text = ""
    if hist_path.exists():
        hist_data = json.loads(hist_path.read_text(encoding="utf-8"))
        hist_text = "\n".join(p["text"] for p in hist_data["pages"][:200])  # first 200p for speed

    print("Loading exercises...")
    exercise_texts = load_exercise_texts(full_text_dir)

    knowledge_entries = []

    for chapter in CHAPTERS:
        num = chapter["number"]
        title = chapter["title"]
        print(f"  Processing chapter {num}: {title[:50]}...")

        # Get page text for this chapter
        page_nums = chapter_pages.get(num, [])
        chapter_text = "\n\n".join(
            p["text"] for p in all_pages
            if p["page"] in page_nums
        )

        # Learning objectives from chapter text
        learning_objectives = extract_learning_objectives(chapter_text)

        # Definitions
        definitions = extract_definitions(chapter_text)

        # Formulas
        formulas = extract_formulas(chapter_text)

        # Common mistakes
        common_mistakes = extract_common_mistakes(chapter_text)

        # Exercise association
        current_exercises = [
            stem for stem, ch_num in EXERCISE_MAP.items()
            if ch_num == num
        ]
        exercise_topics: list[str] = []
        for stem in current_exercises:
            if stem in exercise_texts:
                exercise_topics.extend(extract_exercise_topics(exercise_texts[stem]))

        # Scoring
        has_exercise = bool(current_exercises)
        in_exam = chapter_appears_in_exam(chapter, exam_text)
        in_historical = chapter_appears_in_historical(chapter, hist_text)
        importance, exam_rel = score_chapter(num, has_exercise, in_exam, in_historical)

        # Key concept extraction – unique noun phrases (capitalized phrases ≥2 words)
        concept_candidates = re.findall(
            r"\b([A-ZÄÖÜ][a-zäöüß]+(?:[-\s][A-ZÄÖÜ]?[a-zäöüß]+){1,5})\b",
            chapter_text,
        )
        from collections import Counter
        freq = Counter(concept_candidates)
        top_concepts = [c for c, _ in freq.most_common(30) if len(c) > 8]

        entry = {
            "chapterNumber": num,
            "chapterTitle": title,
            "part": chapter["part"],
            "sections": chapter["sections"],
            "pageRange": {
                "start": min(page_nums) if page_nums else None,
                "end": max(page_nums) if page_nums else None,
                "count": len(page_nums),
            },
            "currentSources": [{
                "file": "Skript FMI SS2026_ jetzt.pdf",
                "pages": page_nums[:5],  # first 5 as sample
            }],
            "historicalSources": [{
                "file": "Skript FMI SS2024.pdf",
                "inHistorical": in_historical,
            }],
            "learningObjectives": learning_objectives,
            "topConcepts": top_concepts[:15],
            "definitions": definitions[:10],
            "formulas": formulas[:10],
            "commonMistakes": common_mistakes,
            "exerciseFiles": current_exercises,
            "exerciseTopics": exercise_topics[:10],
            "crossYearAnalysis": {
                "appearsInCurrentScript": True,
                "appearsInHistoricalScript": in_historical,
                "appearsInCurrentExam": in_exam,
                "hasCurrentExercise": has_exercise,
            },
            "importance": importance,
            "examRelevance": exam_rel,
        }
        knowledge_entries.append(entry)

    knowledge_base = {
        "meta": {
            "generatedAt": "2026-08-27",
            "generatedBy": "scripts/extract/knowledge_builder.py",
            "primarySource": "Skript FMI SS2026_ jetzt.pdf",
            "totalChapters": len(knowledge_entries),
        },
        "chapters": knowledge_entries,
        "globalConcepts": _extract_global_concepts(all_text),
        "examProfile": _build_exam_profile(exam_text),
    }

    out_path.write_text(json.dumps(knowledge_base, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKnowledge base written to: {out_path}")


def _extract_global_concepts(text: str) -> list[dict]:
    """Extract the most frequent finance concepts across the entire script."""
    finance_concepts = [
        ("Modigliani-Miller-Theorem", ["MM", "Modigliani", "Miller"]),
        ("Kapitalstruktur", ["Kapitalstruktur", "capital structure"]),
        ("Eigenkapital", ["Eigenkapital", "EK", "equity"]),
        ("Fremdkapital", ["Fremdkapital", "FK", "debt"]),
        ("Verschuldungsgrad", ["Verschuldungsgrad", "leverage"]),
        ("WACC", ["WACC", "gewichtete Kapitalkosten"]),
        ("Steuervorteil", ["Steuervorteil", "tax shield"]),
        ("Konkurskosten", ["Konkurskosten", "Insolvenzkosten"]),
        ("Informationsasymmetrie", ["Informationsasymmetrie", "asymmetrische Information"]),
        ("Moral Hazard", ["Moral Hazard", "moralisches Risiko"]),
        ("Adverse Selektion", ["adverse Selektion", "adverse selection"]),
        ("Finanzintermediation", ["Finanzintermediation", "Intermediär"]),
        ("Losgrößentransformation", ["Losgrößentransformation"]),
        ("Fristentransformation", ["Fristentransformation"]),
        ("Risikotransformation", ["Risikotransformation"]),
        ("Bank Run", ["Bank Run", "Bankensturm"]),
        ("Too Big To Fail", ["too big to fail", "TBTF", "systemisch"]),
        ("Eigenkapitalregulierung", ["Eigenkapitalregulierung", "Basel"]),
        ("Lender of Last Resort", ["Lender of Last Resort", "LoLR", "Letzter Kreditgeber"]),
        ("Systemisches Risiko", ["systemisches Risiko", "Systemrisiko"]),
        ("Direkte Finanzierung", ["direkte Finanzierung"]),
        ("Indirekte Finanzierung", ["indirekte Finanzierung"]),
        ("Kapitalallokation", ["Kapitalallokation"]),
        ("Pecking Order", ["pecking order", "Hackordnung"]),
        ("Trade-Off-Theorie", ["trade-off", "Trade-Off"]),
        ("Agency-Kosten", ["Agency-Kosten", "Agenturkosten"]),
        ("Signaling", ["Signaling", "Signalisierung"]),
        ("Narrow Banking", ["Narrow Banking"]),
        ("Einlagenversicherung", ["Einlagenversicherung", "Depositenversicherung"]),
        ("Haircut", ["Haircut", "Sicherheitsabschlag"]),
    ]

    results = []
    text_lower = text.lower()
    for concept, aliases in finance_concepts:
        count = sum(text_lower.count(a.lower()) for a in aliases)
        if count > 0:
            results.append({
                "concept": concept,
                "frequency": count,
                "importance": min(1.0, round(count / 100, 2)),
            })

    return sorted(results, key=lambda x: x["frequency"], reverse=True)


def _build_exam_profile(exam_text: str) -> dict:
    """Rough exam structure profile from available exam texts."""
    text_lower = exam_text.lower()

    def count(terms: list[str]) -> int:
        return sum(text_lower.count(t) for t in terms)

    # Detect task types
    true_false = count(["wahr", "falsch", "richtig oder falsch", "true or false"])
    calculations = count(["berechnen", "berechnung", "berechne", "wie hoch ist", "wie viel"])
    definitions = count(["definieren", "was versteht man", "was ist", "erklären sie"])
    transfer = count(["nehmen sie an", "betrachten sie", "angenommen", "szenario"])
    multi_part = count(["(a)", "(b)", "(c)", "(d)", "(e)"])

    total = max(true_false + calculations + definitions + transfer + 1, 1)

    return {
        "source": "2026_Probeklausur FMI.pdf + 2020 Klausur FMI.pdf",
        "totalPoints": 60,
        "durationMinutes": 60,
        "numberOfTasks": 4,
        "taskTypes": {
            "calculation": round(calculations / total, 2),
            "trueFalse": round(true_false / total, 2),
            "definition": round(definitions / total, 2),
            "transfer": round(transfer / total, 2),
            "multiPart": round(multi_part / total, 2),
        },
        "allowedAids": ["Wörterbuch", "nicht-programmierbarer Taschenrechner"],
        "notes": [
            "60 Minuten, 60 Punkte – 1 Punkt pro Minute.",
            "Alle 4 Aufgaben sind Pflicht.",
            "Lösungswege bei Rechenaufgaben angeben.",
            "Knappe, präzise Formulierungen erwünscht; Stichwortantworten erlaubt.",
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2b – Knowledge Base Builder")
    parser.add_argument("--full-text-dir", default="scripts/output/full_text")
    parser.add_argument("--out", default="knowledge_base.json")
    args = parser.parse_args()

    full_text_dir = Path(args.full_text_dir)
    script_json = full_text_dir / "Skript FMI SS2026_ jetzt.json"

    if not script_json.exists():
        sys.exit(f"Script JSON not found: {script_json}\nRun full_text_extractor.py first.")

    build_knowledge_base(script_json, full_text_dir, Path(args.out))


if __name__ == "__main__":
    main()
