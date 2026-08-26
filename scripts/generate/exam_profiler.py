"""
Phase 3 – Exam Profile Generator
Analyses all available exam texts (Probeklausuren + historical Klausuren)
and writes exam_profile.json with task types, point distributions,
question patterns and professor fingerprint.

Usage:
    python scripts/generate/exam_profiler.py [--out exam_profile.json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FULL_TEXT_DIR = Path("scripts/output/full_text")


def load_text(stem: str) -> str:
    p = FULL_TEXT_DIR / f"{stem}.json"
    if not p.exists():
        return ""
    data = json.loads(p.read_text(encoding="utf-8"))
    return "\n\n".join(pg["text"] for pg in data["pages"])


# ---------------------------------------------------------------------------
# Task block extraction
# ---------------------------------------------------------------------------

_TASK_BLOCK_RE = re.compile(
    r"(\d+)\.\s+([\w\s/\-\u00c0-\u024f]+?)\s+\((\d+)\s+Punkte?\)",
    re.IGNORECASE,
)

_SUBTASK_RE = re.compile(r"\(([a-z])\)\s+(.{10,200})", re.IGNORECASE)

_POINTS_RE = re.compile(r"\((\d+)\s+Punkte?\)")

_TRUE_FALSE_RE = re.compile(r"wahr\s+oder\s+falsch", re.IGNORECASE)

_CALCULATION_KEYWORDS = [
    "berechnen", "berechne", "wie hoch ist", "wie hoch sind",
    "bestimmen sie", "ermitteln sie", "errechnen", "berechnung",
]
_TRANSFER_KEYWORDS = [
    "nehmen sie an", "betrachten sie", "angenommen", "welche strategie",
    "präferieren", "im interesse", "wieso", "warum",
]
_FORMULA_KEYWORDS = ["formel", "laut mmt", "laut modigliani", "wacc", "rendite ="]
_LISTING_KEYWORDS = ["nennen sie", "nennen", "welche", "aufzählen"]
_EXPLANATION_KEYWORDS = ["erläutern", "erklären", "erklären sie", "begründen"]


def classify_subtask(text: str) -> str:
    tl = text.lower()
    if any(k in tl for k in _CALCULATION_KEYWORDS):
        return "calculation"
    if any(k in tl for k in _FORMULA_KEYWORDS):
        return "formula"
    if any(k in tl for k in _EXPLANATION_KEYWORDS):
        return "explanation"
    if any(k in tl for k in _LISTING_KEYWORDS):
        return "listing"
    if any(k in tl for k in _TRANSFER_KEYWORDS):
        return "transfer"
    return "other"


def parse_tasks(text: str, source_label: str) -> list[dict]:
    tasks = []
    for m in _TASK_BLOCK_RE.finditer(text):
        num = int(m.group(1))
        title = m.group(2).strip()
        points = int(m.group(3))

        # Extract the block of text for this task
        start = m.start()
        # Find next task or end of text
        next_m = _TASK_BLOCK_RE.search(text, m.end())
        end = next_m.start() if next_m else start + 3000
        block = text[start:end]

        is_true_false = bool(_TRUE_FALSE_RE.search(block))

        subtasks = []
        for sm in _SUBTASK_RE.finditer(block):
            subtasks.append({
                "label": sm.group(1),
                "text": sm.group(2).strip(),
                "type": classify_subtask(sm.group(2)),
                "points": None,  # enriched below
            })

        # Assign points to subtasks from inline "(N Punkte)" markers
        point_markers = _POINTS_RE.findall(block)
        # First match is the task total; remaining are subtask points
        sub_points = point_markers[1:] if len(point_markers) > 1 else []
        for i, st in enumerate(subtasks):
            if i < len(sub_points):
                try:
                    st["points"] = int(sub_points[i])
                except ValueError:
                    pass

        task = {
            "number": num,
            "title": title,
            "totalPoints": points,
            "isTrueFalse": is_true_false,
            "subtaskCount": len(subtasks),
            "subtasks": subtasks,
            "dominantType": _dominant_type(subtasks, is_true_false),
            "source": source_label,
        }
        tasks.append(task)
    return tasks


def _dominant_type(subtasks: list[dict], is_true_false: bool) -> str:
    if is_true_false:
        return "trueFalse"
    if not subtasks:
        return "other"
    from collections import Counter
    c = Counter(st["type"] for st in subtasks)
    return c.most_common(1)[0][0]


# ---------------------------------------------------------------------------
# Professor fingerprint
# ---------------------------------------------------------------------------

def build_professor_fingerprint(all_tasks: list[dict]) -> dict:
    from collections import Counter, defaultdict

    type_counts: Counter = Counter()
    topic_mentions: Counter = Counter()
    total_points = 0
    total_tasks = len(all_tasks)

    for t in all_tasks:
        type_counts[t["dominantType"]] += t["totalPoints"]
        total_points += t["totalPoints"]
        title_lower = t["title"].lower()
        for kw in [
            "modigliani", "miller", "kapitalstruktur", "diamond", "dybvig",
            "bankrun", "bank run", "eigenkapital", "fremdkapital", "wacc",
            "steuer", "konkurs", "insolvenz", "too big", "regulierung",
            "wahr oder falsch", "agentur", "agency",
        ]:
            if kw in title_lower:
                topic_mentions[kw] += 1

    tp = max(total_points, 1)
    type_shares = {k: round(v / tp, 2) for k, v in type_counts.items()}

    return {
        "pointsByType": type_shares,
        "repeatedTopics": [k for k, v in topic_mentions.most_common(10) if v > 0],
        "avgTasksPerExam": round(total_tasks / max(1, 2), 1),  # 2 exams
        "avgPointsPerExam": round(total_points / max(1, 2), 0),
        "examStructureNotes": [
            "4 Pflichtaufgaben je Klausur.",
            "60 Punkte / 60 Minuten.",
            "Aufgabe 1 immer Kapitalstruktur / MM-Theorem (multi-part Berechnung).",
            "Aufgabe 2 immer formal-modell-basiert (Diamond/Dybvig oder ähnliches).",
            "Aufgabe 3 Anwendungsfall mit Agency-Theorie / finanzieller Notlage.",
            "Aufgabe 4 immer 3× Wahr/Falsch + je max. 2-Satz-Begründung.",
            "Hilfsmittel: Wörterbuch + nicht-programmierbarer Taschenrechner.",
            "Rechenweg ist Pflicht bei Rechenaufgaben.",
            "Stichwortartige Antworten erlaubt, solange logische Zusammenhänge erkennbar.",
        ],
    }


# ---------------------------------------------------------------------------
# Repeated concepts (cross-year)
# ---------------------------------------------------------------------------

CONCEPT_PROBE = [
    ("Modigliani-Miller-Theorem", ["modigliani", "miller", "mmt"]),
    ("WACC", ["wacc", "gewichtete durchschnittliche kapitalkosten"]),
    ("Eigenkapitalrendite / Leverage-Effekt", ["eigenkapitalrendite", "hebel", "leverage"]),
    ("Diamond/Dybvig Bank-Run-Modell", ["diamond", "dybvig", "bank run", "liquidity"]),
    ("Agency-Kosten / Asset Substitution", ["asset substit", "agency", "schuldnerfreundlich"]),
    ("Eigenkapitalregulierung / Basel", ["eigenkapitalregulierung", "basel"]),
    ("Too-big-to-fail", ["too big to fail", "tbtf"]),
    ("Konkurskosten", ["konkurskosten", "insolvenzkosten"]),
    ("Steuervorteil Fremdkapital", ["steuervorteil", "tax shield"]),
    ("Wahr oder falsch", ["wahr oder falsch"]),
]


def cross_year_concepts(exam_texts: dict[str, str]) -> list[dict]:
    results = []
    for concept, aliases in CONCEPT_PROBE:
        appearances = {}
        for label, text in exam_texts.items():
            tl = text.lower()
            if any(a in tl for a in aliases):
                appearances[label] = True
        results.append({
            "concept": concept,
            "appearsIn": list(appearances.keys()),
            "frequency": len(appearances),
            "examRelevance": min(1.0, round(0.5 + 0.25 * len(appearances), 2)),
        })
    return sorted(results, key=lambda x: x["frequency"], reverse=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="exam_profile.json")
    args = parser.parse_args()

    exam_sources = {
        "2026_Probeklausur (aktuell)": load_text("2026_Probeklausur FMI"),
        "2026_Probeklausur Lsg (aktuell)": load_text("2026_Probeklausur FMI_Lsg"),
        "2020_Klausur (historisch)": load_text("2020 Klausur FMI"),
    }

    all_tasks = []
    tasks_by_exam = {}
    for label, text in exam_sources.items():
        tasks = parse_tasks(text, label)
        tasks_by_exam[label] = tasks
        all_tasks.extend(tasks)
        print(f"  {label}: {len(tasks)} tasks parsed")

    fingerprint = build_professor_fingerprint(all_tasks)
    cross_year = cross_year_concepts(exam_sources)

    profile = {
        "meta": {
            "generatedAt": "2026-08-27",
            "generatedBy": "scripts/generate/exam_profiler.py",
            "examSources": list(exam_sources.keys()),
        },
        "examStructure": {
            "totalPoints": 60,
            "durationMinutes": 60,
            "numberOfTasks": 4,
            "allTasksCompulsory": True,
            "allowedAids": ["Wörterbuch", "nicht-programmierbarer Taschenrechner"],
            "answerStyle": "knapp und präzise; Stichwortantworten mit erkennbaren Zusammenhängen",
            "calculationRequirement": "Lösungsweg bei Rechenaufgaben Pflicht",
        },
        "professorFingerprint": fingerprint,
        "crossYearConcepts": cross_year,
        "tasksByExam": tasks_by_exam,
        "typicalExamLayout": [
            {
                "taskNumber": 1,
                "typicalTitle": "Die Kapitalstruktur in einem vollkommenen Markt / MM-Theorem",
                "typicalPoints": 15,
                "format": "Multi-part Berechnung (a)–(k), mit abschließender Konzeptfrage",
                "coreTopics": [
                    "Erwartungswert berechnen",
                    "Unternehmenswert (vollk. Markt)",
                    "EK-Rendite bei Eigenfinanzierung",
                    "Leverage-Effekt: EK-Rendite bei Fremdfinanzierung",
                    "WACC Berechnung",
                    "MMT II: r_E = r_U + D/E * (r_U - r_D)",
                    "Gründe für Verletzung der MM-Annahmen (Stichpunkte)",
                ],
                "flashcardTypes": ["calculation", "formula", "listing"],
            },
            {
                "taskNumber": 2,
                "typicalTitle": "Diamond/Dybvig (Banken, Liquiditätsschocks)",
                "typicalPoints": 18,
                "format": "Formales Modell: Optimierungsproblem + Gleichgewichtsanalyse",
                "coreTopics": [
                    "Autarkie-Gleichgewicht (FOC, Ecklösung)",
                    "Finanzmarkt-Gleichgewicht (Gleichgewichtspreis p)",
                    "First-best-Lösung (Gleichungssystem lösen)",
                    "Anreizverträglichkeitsbedingungen",
                    "Bank-Run-Gleichgewicht",
                    "Narrow Banking / Einlagenversicherung",
                ],
                "flashcardTypes": ["calculation", "formula", "understanding"],
            },
            {
                "taskNumber": 3,
                "typicalTitle": "Fremd- und Eigenkapital / Agency-Theorie / finanzielle Notlage",
                "typicalPoints": 17,
                "format": "Szenario + Berechnungen + Begründung",
                "coreTopics": [
                    "Auszahlungsfunktionen FK und EK zeichnen",
                    "Asset Substitution in finanzieller Notlage",
                    "Debt Overhang (unterinvestierte Projekte)",
                    "Indifferenzpunkt Berechnung",
                    "Anteilseigner vs. Gläubiger-Interessen",
                ],
                "flashcardTypes": ["transfer", "calculation", "understanding"],
            },
            {
                "taskNumber": 4,
                "typicalTitle": "Wahr oder falsch?",
                "typicalPoints": 9,
                "format": "3 Aussagen × 3 Punkte, je max. 2 Sätze Begründung",
                "coreTopics": [
                    "Eigenkapitalregulierung Banken",
                    "Too-big-to-fail und Wettbewerb",
                    "Eigenkapitalanforderungen und Pufferfunktion",
                ],
                "flashcardTypes": ["trueFalse"],
            },
        ],
    }

    Path(args.out).write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nExam profile written to: {args.out}")
    print(f"Cross-year concepts (top 5):")
    for c in cross_year[:5]:
        print(f"  {c['concept']}: appears in {c['frequency']} sources, examRel={c['examRelevance']}")


if __name__ == "__main__":
    main()
