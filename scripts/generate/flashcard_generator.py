"""
Phase 4 – Flashcard Generator
Generates high-quality, exam-oriented flashcards for
"Finanzmärkte und -institutionen" (SS2026, Prof. Farzad Saidi).

Strategy:
- Hardcoded expert cards for the highest-priority exam topics
- Template-generated cards from knowledge_base.json learning objectives
- Exercise-derived cards from U01–U05_jetzt
- Validation and deduplication built-in

Output: flashcards.json (project root) + public/data/flashcards.json (web app)

Usage:
    python scripts/generate/flashcard_generator.py [--out flashcards.json]
"""
from __future__ import annotations

import json
import hashlib
import re
from datetime import date
from pathlib import Path
from typing import Optional

TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Data model helpers
# ---------------------------------------------------------------------------

_counter = 0

def _next_id(chapter: str) -> str:
    global _counter
    _counter += 1
    return f"fmfi-{chapter.replace('.', '')}-{_counter:03d}"


def card(
    *,
    chapter: str,
    section: str,
    question: str,
    answer: str,
    card_type: str,        # definition | understanding | contrast | calculation | trueFalse | transfer | listing | formula | empirical
    difficulty: int,       # 1–8 per spec
    importance: float,
    exam_relevance: float,
    tags: list[str],
    source_current: Optional[str] = "Skript FMI SS2026_ jetzt.pdf",
    source_historical: Optional[list[str]] = None,
    solution_steps: Optional[list[str]] = None,
    formula: Optional[str] = None,
    variables: Optional[dict] = None,
    numeric_answer: Optional[float] = None,
    tolerance: Optional[float] = None,
    note: Optional[str] = None,
) -> dict:
    cid = _next_id(chapter.split(".")[0])
    return {
        "id": cid,
        "question": question.strip(),
        "answer": answer.strip(),
        "type": card_type,
        "difficulty": difficulty,
        "importance": round(importance, 2),
        "examRelevance": round(exam_relevance, 2),
        "chapter": chapter,
        "section": section,
        "tags": tags,
        "source": {
            "current": [{"file": source_current}] if source_current else [],
            "historical": source_historical or [],
        },
        **({"solutionSteps": solution_steps} if solution_steps else {}),
        **({"formula": formula} if formula else {}),
        **({"variables": variables} if variables else {}),
        **({"numericAnswer": numeric_answer, "tolerance": tolerance} if numeric_answer is not None else {}),
        **({"note": note} if note else {}),
        "validation": {"status": "ok", "issues": []},
        "learning": {
            "repetitions": 0,
            "ease": 2.5,
            "interval": 0,
            "due": TODAY,
            "lastReviewed": None,
        },
    }


# ---------------------------------------------------------------------------
# KAPITEL 1 – Funktionen des Finanzsystems
# ---------------------------------------------------------------------------

def cards_chapter1() -> list[dict]:
    ch = "1. Funktionen des Finanzsystems"
    tags1 = ["Finanzsystem", "Grundlagen"]

    return [
        card(
            chapter=ch, section="Überblick",
            question="Welche drei Kerngruppen von Akteuren sind im Finanzsystem aktiv?",
            answer=(
                "1. Finanzmärkte und Finanzintermediäre (Banken, Versicherungen, Investmentfonds)\n"
                "2. Akteure, die auf den Märkten handeln oder mit Intermediären Verträge schließen: "
                "Haushalte, Unternehmen, Regierungen (in- und ausländisch)\n"
                "3. Finanzinfrastruktur (Börsen, Zahlungssysteme, Ratingagenturen)"
            ),
            card_type="listing", difficulty=1, importance=0.85, exam_relevance=0.8,
            tags=tags1 + ["Akteure"],
        ),
        card(
            chapter=ch, section="Direkte vs. indirekte Finanzierung",
            question="Was ist direkte Finanzierung? Gib ein Beispiel.",
            answer=(
                "Bei direkter Finanzierung tritt der Kapitalnehmer (z.B. Unternehmen) direkt mit "
                "dem Kapitalanleger (z.B. Haushalt) in Kontakt – ohne einen Intermediär. "
                "Beispiel: Haushalt kauft eine Unternehmensanleihe direkt am Kapitalmarkt."
            ),
            card_type="definition", difficulty=1, importance=0.9, exam_relevance=0.85,
            tags=tags1 + ["Finanzierung", "direkte Finanzierung"],
        ),
        card(
            chapter=ch, section="Direkte vs. indirekte Finanzierung",
            question="Was ist indirekte Finanzierung? Wie unterscheidet sie sich von direkter Finanzierung?",
            answer=(
                "Bei indirekter Finanzierung fließen die Mittel über einen Finanzintermediär "
                "(z.B. Bank). Der Intermediär nimmt Einlagen entgegen und vergibt Kredite. "
                "Unterschied: Bei direkter Finanzierung kein Intermediär; "
                "bei indirekter Finanzierung transformiert der Intermediär Losgröße, Frist und Risiko."
            ),
            card_type="contrast", difficulty=2, importance=0.9, exam_relevance=0.85,
            tags=tags1 + ["Finanzintermediation", "indirekte Finanzierung"],
        ),
        card(
            chapter=ch, section="Direkte vs. indirekte Finanzierung",
            question=(
                "Transfer: Ein Haushalt kauft eine Unternehmensanleihe direkt vom Unternehmen. "
                "Welche Finanzierungsform liegt vor? Begründe."
            ),
            answer=(
                "Direkte Finanzierung: Der Haushalt tritt als Kapitalanleger direkt mit dem "
                "Kapitalnehmer (Unternehmen) in Kontakt, ohne dass ein Intermediär zwischengeschaltet ist."
            ),
            card_type="transfer", difficulty=3, importance=0.85, exam_relevance=0.8,
            tags=tags1 + ["Finanzierung", "Transfer"],
        ),
        card(
            chapter=ch, section="Hauptfunktionen",
            question="Welche Hauptfunktionen hat das Finanzsystem für die Volkswirtschaft?",
            answer=(
                "1. Mobilisierung und Sammlung von Ersparnissen\n"
                "2. Kapitalallokation (Mittel → produktivste Verwendung)\n"
                "3. Risikoverteilung und -diversifikation\n"
                "4. Überwachung von Managern / Unternehmenskontrolle\n"
                "5. Erleichterung des Zahlungsverkehrs\n"
                "6. Reduktion von Transaktionskosten und Informationsasymmetrien"
            ),
            card_type="listing", difficulty=2, importance=0.9, exam_relevance=0.85,
            tags=tags1 + ["Funktionen", "Kapitalallokation"],
        ),
        card(
            chapter=ch, section="Wachstum",
            question="Warum könnte ein entwickeltes Finanzsystem das Wirtschaftswachstum fördern?",
            answer=(
                "Ein effizientes Finanzsystem leitet finanzielle Mittel zu den produktivsten "
                "Verwendungen (höchste Rendite) und fördert so Kapitalallokation. "
                "Dadurch steigt die Produktivität einer Volkswirtschaft, was langfristig "
                "Wirtschaftswachstum erzeugt. Aber: Korrelation ≠ Kausalität."
            ),
            card_type="understanding", difficulty=2, importance=0.85, exam_relevance=0.8,
            tags=tags1 + ["Wachstum", "Kapitalallokation", "Evidenz"],
        ),
        card(
            chapter=ch, section="Wachstum",
            question=(
                "Wahr oder falsch? Ein größeres Finanzsystem fördert immer das Wirtschaftswachstum. "
                "Begründe in max. 2 Sätzen."
            ),
            answer=(
                "Falsch. Ab einer gewissen Größe kann ein Finanzsystem 'zu groß' werden: "
                "Ressourcen werden weg von der Realwirtschaft gezogen, systemische Risiken steigen. "
                "Die Beziehung ist empirisch nicht monoton positiv."
            ),
            card_type="trueFalse", difficulty=4, importance=0.85, exam_relevance=0.9,
            tags=tags1 + ["Wachstum", "Wahr/Falsch"],
        ),
        card(
            chapter=ch, section="Banken vs. Märkte",
            question="Vergleiche bank- vs. marktbasierte Finanzsysteme: Vor- und Nachteile.",
            answer=(
                "Bankbasiert (z.B. Deutschland):\n"
                "  + Enge Beziehung / Monitoring; Kreditvergabe auch bei Informationsasymmetrie\n"
                "  – Weniger Innovationsanreize; geringere Liquidität\n\n"
                "Marktbasiert (z.B. USA):\n"
                "  + Liquidität, Preisfindung, breite Risikostreuung\n"
                "  – Größere Volatilität; kurzfristiger Zeithorizont"
            ),
            card_type="contrast", difficulty=3, importance=0.75, exam_relevance=0.7,
            tags=tags1 + ["Bankensystem", "Finanzmärkte"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 2 – Die globale Finanzkrise und ihre Auswirkungen
# ---------------------------------------------------------------------------

def cards_chapter2() -> list[dict]:
    ch = "2. Die globale Finanzkrise und ihre Auswirkungen"
    tags2 = ["Finanzkrise", "Makroökonomie"]

    return [
        card(
            chapter=ch, section="2.1 Stilisierte Fakten",
            question="Nennen Sie drei stilisierte Fakten über Finanzkrisen.",
            answer=(
                "1. Finanzkrisen gehen häufig einem starken Kredit- und Vermögenspreisanstieg voraus.\n"
                "2. Sie sind teuer: tiefe Rezessionen, hohe Staatsschulden, dauerhafter BIP-Verlust.\n"
                "3. Sie verlaufen oft in Phasen: Bankenkrise → Staatsschuldenkrise → ggf. Währungskrise."
            ),
            card_type="listing", difficulty=2, importance=0.75, exam_relevance=0.7,
            tags=tags2 + ["Stilisierte Fakten"],
        ),
        card(
            chapter=ch, section="2.1 Stilisierte Fakten",
            question="Welche drei Typen von Finanzkrisen unterscheidet der Kurs?",
            answer=(
                "1. Bankenkrise: Bankensystem unter Stress; Bank Runs, Insolvenzen.\n"
                "2. Staatsschuldenkrise: Staat kann Schulden nicht bedienen; Vertrauensverlust.\n"
                "3. Währungskrise: Starke Abwertung der Währung; spekulativer Angriff auf Wechselkurs."
            ),
            card_type="listing", difficulty=2, importance=0.8, exam_relevance=0.75,
            tags=tags2 + ["Krisentypen"],
        ),
        card(
            chapter=ch, section="2.2 Globale Finanzkrise 2007–2009",
            question=(
                "Was war der zentrale Auslöser der globalen Finanzkrise 2007–2009 "
                "und wie pflanzte sie sich fort?"
            ),
            answer=(
                "Auslöser: Platzen der US-Immobilienblase; steigende Zahlungsausfälle bei Subprime-Hypotheken.\n"
                "Übertragung: Via verbriefte Produkte (CDOs, MBS) weltweit verteilt; "
                "Intransparenz führte zu Vertrauensverlust; Interbankenmarkt fror ein; "
                "Banken benötigten staatliche Rettung (Lehman Brothers Insolvenz Sept. 2008)."
            ),
            card_type="understanding", difficulty=3, importance=0.8, exam_relevance=0.75,
            tags=tags2 + ["2007-2009", "Subprime"],
        ),
        card(
            chapter=ch, section="2.3 Krise im Euroraum",
            question="Wie entstand die Staatsschuldenkrise im Euroraum nach 2010?",
            answer=(
                "Bankkrisen führten zu Staatsschuldenerhöhung (Rettungsmaßnahmen, Konjunkturprogramme). "
                "Märkte bezweifelten Zahlungsfähigkeit einzelner Eurostaaten (PIIGS). "
                "Teufelskreis: Schwache Banken → schwacher Staat → schwache Banken "
                "(durch Staatsanleihen im Bankportfolio). Vertrauensverlust → steigende Spreads."
            ),
            card_type="understanding", difficulty=3, importance=0.75, exam_relevance=0.7,
            tags=tags2 + ["Eurozone", "Staatsschuldenkrise"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 3 – MM-Theorem (vollkommener Markt)
# ---------------------------------------------------------------------------

def cards_chapter3() -> list[dict]:
    ch = "3. Kapitalstruktur: vollkommener Markt & MM-Theorem"
    tags3 = ["MM-Theorem", "Kapitalstruktur", "Eigenkapital", "Fremdkapital"]

    return [
        # --- Definitions ---
        card(
            chapter=ch, section="3.1 Finanzierung",
            question="Was sind die Kernunterschiede zwischen Eigenkapital und Fremdkapital?",
            answer=(
                "Eigenkapital (EK):\n"
                "  – Residualanspruch (Rest nach FK-Bedienung)\n"
                "  – Unbegrenzte Laufzeit\n"
                "  – Verlustbeteiligung\n"
                "  – Dividende nicht steuerlich abzugsfähig (DE)\n\n"
                "Fremdkapital (FK):\n"
                "  – Vorrangiger Anspruch (fixer Betrag)\n"
                "  – Feste Laufzeit, feste Zinsen\n"
                "  – Keine Verlustbeteiligung über den Kreditbetrag hinaus\n"
                "  – Zinsen steuerlich abzugsfähig → Steuervorteil"
            ),
            card_type="contrast", difficulty=2, importance=0.95, exam_relevance=0.95,
            tags=tags3,
        ),
        card(
            chapter=ch, section="3.2 MM-Theorem I",
            question="Was besagt das Modigliani-Miller-Theorem I (MMT I)?",
            answer=(
                "In einem vollkommenen Kapitalmarkt ist der Gesamtwert eines Unternehmens "
                "unabhängig von seiner Kapitalstruktur. "
                "V_L = V_U (verschuldetes = unverschuldetes Unternehmen).\n"
                "Intuition: Investoren können die Kapitalstruktur durch private Verschuldung "
                "selbst replizieren (Homemade Leverage)."
            ),
            card_type="definition", difficulty=2, importance=1.0, exam_relevance=1.0,
            formula="V_L = V_U",
            tags=tags3 + ["MMT I"],
        ),
        card(
            chapter=ch, section="3.2 MM-Theorem II",
            question="Was besagt das Modigliani-Miller-Theorem II (MMT II) und wie lautet die Formel?",
            answer=(
                "Die erwartete Rendite des Eigenkapitals steigt linear mit dem Verschuldungsgrad D/E.\n\n"
                "Formel: r_E = r_U + (D/E) × (r_U − r_D)\n\n"
                "r_U = EK-Rendite bei vollständiger Eigenfinanzierung\n"
                "r_D = Fremdkapitalkosten\n"
                "D/E = Verschuldungsgrad (Marktwerte)\n\n"
                "Interpretation: Mehr Fremdkapital erhöht EK-Rendite, "
                "aber auch EK-Risiko im gleichen Maß → kein Wert geschaffen."
            ),
            card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0,
            formula="r_E = r_U + (D/E) × (r_U − r_D)",
            variables={"r_E": "EK-Rendite (erwartet)", "r_U": "EK-Rendite bei 100% EK", "r_D": "FK-Zinssatz", "D/E": "Verschuldungsgrad (Marktwerte)"},
            tags=tags3 + ["MMT II", "Formel"],
        ),
        card(
            chapter=ch, section="3.3 WACC",
            question="Wie lautet die WACC-Formel und was folgt aus dem MM-Theorem für den WACC?",
            answer=(
                "WACC = (E/(E+D)) × r_E + (D/(E+D)) × r_D\n\n"
                "Im vollkommenen Markt gilt: WACC = r_U = konstant, unabhängig von der Kapitalstruktur.\n"
                "Mehr FK erhöht zwar r_E (MMT II), aber die Gewichte verschieben sich hin zum günstigeren FK "
                "→ WACC bleibt konstant."
            ),
            card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0,
            formula="WACC = (E/(E+D)) × r_E + (D/(E+D)) × r_D = r_U",
            variables={"E": "Marktwert EK", "D": "Marktwert FK", "r_E": "EK-Rendite", "r_D": "FK-Zinssatz", "r_U": "Kapitalkosten unverschuldet"},
            tags=tags3 + ["WACC", "Formel"],
        ),
        card(
            chapter=ch, section="3.2 MM-Theorem I",
            question=(
                "Klausur: Ein Unternehmen ist vollständig eigenkapitalfinanziert mit r_U = 12%. "
                "Der risikolose Zins beträgt 5%. Wie hoch ist der WACC bei einem Verschuldungsgrad D/E = 1? "
                "(vollkommener Markt)"
            ),
            answer=(
                "Im vollkommenen Markt: WACC = r_U = 12% (immer, unabhängig von Kapitalstruktur).\n\n"
                "Kontrolle via MMT II: r_E = 12% + 1 × (12% – 5%) = 19%\n"
                "WACC = 0,5 × 19% + 0,5 × 5% = 9,5% + 2,5% = 12% ✓"
            ),
            card_type="calculation", difficulty=5, importance=1.0, exam_relevance=1.0,
            solution_steps=[
                "WACC = r_U = 12% (MMT I im vollkommenen Markt)",
                "r_E via MMT II: r_E = 12% + (1) × (12% – 5%) = 19%",
                "WACC = 0,5 × 19% + 0,5 × 5% = 12% ✓",
            ],
            numeric_answer=0.12, tolerance=0.001,
            tags=tags3 + ["WACC", "Klausurstil", "Rechnen"],
        ),
        card(
            chapter=ch, section="3.4 Trugschlüsse",
            question="Nennen Sie drei typische Trugschlüsse bei der Kapitalstruktur im vollkommenen Markt.",
            answer=(
                "1. 'FK ist billiger als EK → mehr FK spart Kapitalkosten.' "
                "Falsch: Mehr FK erhöht das EK-Risiko und damit r_E (MMT II) → WACC konstant.\n\n"
                "2. 'Hohe EK-Rendite nach Verschuldung zeigt höhere Rentabilität.' "
                "Falsch: Die höhere Rendite kompensiert genau das höhere Risiko.\n\n"
                "3. 'EK-Emission verwässert EPS → schlecht für Aktionäre.' "
                "Falsch: Im vollkommenen Markt wird durch Emission der Aktienwert genau um den Emissionserlös je Aktie erhöht."
            ),
            card_type="listing", difficulty=3, importance=0.9, exam_relevance=0.95,
            tags=tags3 + ["Trugschlüsse", "Klausurstil"],
        ),
        card(
            chapter=ch, section="3.2 Annahmen",
            question=(
                "Klausur (Listing): Nennen Sie drei Gründe, warum die Annahmen des "
                "Modigliani-Miller-Theorems in der Realität nicht erfüllt sind."
            ),
            answer=(
                "1. Steuern: Zinszahlungen sind steuerlich abzugsfähig → Steuervorteil für FK.\n"
                "2. Konkurskosten: Insolvenz verursacht direkte (Anwalts-/Gerichtskosten) und "
                "indirekte Kosten (Verlust von Kunden, Lieferanten).\n"
                "3. Agency-Kosten / asymmetrische Information: Interessenkonflikte zwischen "
                "Aktionären und Gläubigern (Asset Substitution, Debt Overhang); "
                "Information über Qualität des Unternehmens ungleich verteilt (Signaling)."
            ),
            card_type="listing", difficulty=3, importance=1.0, exam_relevance=1.0,
            tags=tags3 + ["Annahmen", "Klausurstil", "Listing"],
        ),
        card(
            chapter=ch, section="3.1 Bewertung",
            question=(
                "Klausur: Projekt mit EW = 1.120 EUR, Anfangsinvestition = 1.000 EUR (vollk. Markt). "
                "r_U = 12%, r_f = 5%. Wie hoch ist der Unternehmenswert (vollständige EK-Finanzierung)?"
            ),
            answer=(
                "V = EW / (1 + r_U) = 1.120 / 1,12 = 1.000 EUR\n\n"
                "Alternativ: Wenn Investition = 1.000 EUR und Rückzahlung im Erwartungswert = 1.120 EUR, "
                "entspricht das einer Rendite von 12% = r_U. NPV = 1.000 – 1.000 = 0."
            ),
            card_type="calculation", difficulty=4, importance=0.95, exam_relevance=1.0,
            solution_steps=[
                "EW der Zahlungsströme bestimmen",
                "Diskontieren mit r_U: V = EW / (1 + r_U)",
                "V = 1.120 / 1,12 = 1.000 EUR",
            ],
            formula="V_U = EW(CF) / (1 + r_U)",
            tags=tags3 + ["Bewertung", "Rechnen", "Klausurstil"],
        ),
        card(
            chapter=ch, section="3.1 Homemade Leverage",
            question="Was ist 'Homemade Leverage' und warum ist es für das MM-Theorem zentral?",
            answer=(
                "Investoren können die Kapitalstruktur des Unternehmens durch private Verschuldung "
                "(bzw. Anlage in risikofreie Papiere) selbst replizieren. "
                "Daher kann die Unternehmensleitung durch Veränderung der Kapitalstruktur "
                "keinen Mehrwert schaffen – Arbitragefreiheit im vollkommenen Markt verhindert dies. "
                "Dies ist die Grundintuition von MMT I."
            ),
            card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.9,
            tags=tags3 + ["Homemade Leverage", "Arbitrage"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 4 – Marktunvollkommenheiten
# ---------------------------------------------------------------------------

def cards_chapter4() -> list[dict]:
    ch = "4. Der Einfluss von Marktunvollkommenheiten auf die Kapitalstruktur"
    tags4 = ["Kapitalstruktur", "Marktunvollkommenheiten", "Steuern", "Agency-Kosten"]

    return [
        card(
            chapter=ch, section="4.1 Steuervorteil",
            question="Was ist der fremdfinanzierungsbedingte Steuervorteil (Tax Shield)?",
            answer=(
                "Zinszahlungen auf Fremdkapital sind steuerlich abzugsfähig. "
                "Damit zahlen verschuldete Unternehmen weniger Steuern als unverschuldete.\n\n"
                "Steuervorteil pro Periode = τ × r_D × D\n"
                "Barwert des Steuervorteils (bei permanenter Schuld) = τ × D\n\n"
                "MMT mit Steuern: V_L = V_U + τ × D"
            ),
            card_type="definition", difficulty=2, importance=1.0, exam_relevance=1.0,
            formula="V_L = V_U + τ × D",
            variables={"τ": "Unternehmenssteuersatz", "D": "Marktwert Fremdkapital", "V_L": "Wert verschuldetes Unternehmen", "V_U": "Wert unverschuldetes Unternehmen"},
            tags=tags4 + ["Tax Shield", "Steuern", "Formel"],
        ),
        card(
            chapter=ch, section="4.1 Steuervorteil",
            question=(
                "Klausur: Unternehmen hat D = 500 EUR, τ = 40%, r_D = 10%, r_U = 12%. "
                "Wie hoch ist der Unternehmenswert V_L (mit permanenter Schuld)? V_U = 1.000 EUR."
            ),
            answer=(
                "V_L = V_U + τ × D = 1.000 + 0,40 × 500 = 1.000 + 200 = 1.200 EUR\n\n"
                "Der Steuervorteil beträgt 200 EUR."
            ),
            card_type="calculation", difficulty=4, importance=0.95, exam_relevance=1.0,
            solution_steps=[
                "Formel: V_L = V_U + τ × D",
                "V_L = 1.000 + 0,40 × 500",
                "V_L = 1.200 EUR",
            ],
            formula="V_L = V_U + τ × D",
            numeric_answer=1200, tolerance=0.01,
            tags=tags4 + ["Tax Shield", "Rechnen", "Klausurstil"],
        ),
        card(
            chapter=ch, section="4.1.4 Optimale Kapitalstruktur mit Steuern",
            question="Warum ist die optimale Kapitalstruktur mit Steuern allein (ohne Konkurskosten) 100% Fremdkapital?",
            answer=(
                "Mit Steuern steigt V_L = V_U + τ × D monoton mit D. "
                "Mehr FK → mehr Steuervorteil → höherer Unternehmenswert. "
                "Ohne Konkurskosten gibt es keine Gegengewichte. "
                "Diese extreme Vorhersage zeigt, dass Steuern allein das Kapitalstruktur-Puzzle nicht lösen."
            ),
            card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.85,
            tags=tags4 + ["Steuern", "Trade-Off"],
        ),
        card(
            chapter=ch, section="4.2.1 Konkurskosten",
            question="Welche zwei Arten von Konkurskosten gibt es und wie beeinflussen sie die Kapitalstruktur?",
            answer=(
                "1. Direkte Konkurskosten: Rechtliche und administrative Kosten der Insolvenz "
                "(Anwälte, Verwalter, Gerichtsgebühren).\n"
                "2. Indirekte Konkurskosten: Verlust von Kunden, Lieferanten, Mitarbeitern; "
                "Verzerrung von Investitionsentscheidungen in finanzieller Notlage.\n\n"
                "Kapitalstruktur: Höheres FK erhöht Konkursrisiko → erwartetere Konkurskosten steigen "
                "→ Unternehmenswert sinkt. Trade-Off mit Steuervorteil."
            ),
            card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.9,
            tags=tags4 + ["Konkurskosten", "Trade-Off"],
        ),
        card(
            chapter=ch, section="4.2.1 Trade-Off-Theorie",
            question="Was besagt die Trade-Off-Theorie der Kapitalstruktur?",
            answer=(
                "Unternehmen wählen die Kapitalstruktur, die den Barwert des Steuervorteils "
                "gegen den Barwert der erwarteten Konkurskosten abwägt.\n\n"
                "Optimale Kapitalstruktur: Maximiere V = V_U + PV(Steuervorteil) − PV(Konkurskosten)\n\n"
                "Vorhersage: Große, profitable Unternehmen mit sicheren Cashflows → mehr FK; "
                "kleine, wachstumsstarke Unternehmen mit unsicheren Cashflows → weniger FK."
            ),
            card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.9,
            tags=tags4 + ["Trade-Off", "Theorie"],
        ),
        card(
            chapter=ch, section="4.2.2 Agency-Kosten",
            question=(
                "Was ist 'Asset Substitution' und warum entsteht dieser Interessenkonflikt?"
            ),
            answer=(
                "Asset Substitution (Risikoverlagerung): Aktionäre in finanzieller Notlage "
                "bevorzugen riskantere Projekte, auch wenn diese einen negativen Gesamterwartungswert haben.\n\n"
                "Grund: Aktionäre profitieren nur im Erfolgsfall; Verluste tragen weitgehend die Gläubiger. "
                "→ Aktionäre haben Anreiz, riskante Wetten auf Kosten der Gläubiger einzugehen.\n\n"
                "Konsequenz: Antizipierte Agency-Kosten erhöhen FK-Zinsen und mindern Unternehmenswert."
            ),
            card_type="definition", difficulty=4, importance=1.0, exam_relevance=1.0,
            tags=tags4 + ["Asset Substitution", "Agency-Kosten", "Klausurstil"],
        ),
        card(
            chapter=ch, section="4.2.2 Agency-Kosten",
            question=(
                "Klausur (Transfer): Ein Unternehmen ist hoch verschuldet (Kredit fällig: 500 EUR). "
                "Aktueller Unternehmenswert: 400 EUR. Die CFO erwägt eine riskante Strategie "
                "mit 1% Erfolgswahrscheinlichkeit und 1 Mio. EUR Auszahlung bei Erfolg, 0 bei Misserfolg. "
                "Sollten die Anteilseigner zustimmen?"
            ),
            answer=(
                "Ja, aus Sicht der Anteilseigner:\n"
                "Ohne neue Strategie: Sicher in Zahlungsverzug → Auszahlung EK = 0.\n"
                "Mit neuer Strategie: Erwartete Auszahlung EK = 1% × (1.000.000 – 500.000) + 99% × 0 "
                "= 5.000 EUR > 0.\n\n"
                "Auch wenn der Gesamtwert sinkt (Gläubiger verlieren), profitieren Aktionäre – "
                "typisches Beispiel für Asset Substitution."
            ),
            card_type="transfer", difficulty=6, importance=1.0, exam_relevance=1.0,
            solution_steps=[
                "Bestimme EK-Auszahlung ohne Strategiewechsel: 0 (Insolvenz sicher)",
                "Bestimme EK-Auszahlung mit Strategie: p × max(V_Erfolg – D, 0)",
                "1% × (1.000.000 – 500.000) = 5.000 EUR > 0",
                "→ Ja, Aktionäre bevorzugen die Strategie (Asset Substitution)",
            ],
            tags=tags4 + ["Asset Substitution", "Klausurstil", "Transfer"],
        ),
        card(
            chapter=ch, section="4.2.2 Debt Overhang",
            question="Was ist das 'Debt Overhang'-Problem und welche Auswirkung hat es?",
            answer=(
                "Debt Overhang: Unternehmen in finanzieller Notlage unterlässt positive NPV-Projekte, "
                "weil der Großteil des Gewinns an die Gläubiger geht.\n\n"
                "Mechanismus: Aktionäre finanzieren Investition, aber bei hoher Verschuldung "
                "fließen die Gewinne primär an Gläubiger. Netto-Gewinn für Aktionäre < 0 "
                "→ Unterinvestition.\n\n"
                "Konsequenz: FK verzerrt Investitionsentscheidungen → Unternehmenswert sinkt."
            ),
            card_type="definition", difficulty=4, importance=0.9, exam_relevance=0.95,
            tags=tags4 + ["Debt Overhang", "Agency-Kosten"],
        ),
        card(
            chapter=ch, section="4.2.3 Pecking Order",
            question="Was sagt die Pecking Order Theory über die Finanzierungsreihenfolge?",
            answer=(
                "Aufgrund von asymmetrischer Information bevorzugen Unternehmen folgende Reihenfolge:\n"
                "1. Innenfinanzierung (einbehaltene Gewinne) – kein Signalproblem\n"
                "2. Fremdkapital – weniger Informationsproblem als EK\n"
                "3. Eigenkapital – letzter Ausweg (Markt interpretiert EK-Emission als Überbewertsignal)\n\n"
                "Vorhersage: Profitable Unternehmen = weniger FK (wegen ausreichend Innenfinanzierung)."
            ),
            card_type="definition", difficulty=3, importance=0.85, exam_relevance=0.85,
            tags=tags4 + ["Pecking Order", "Asymmetrische Information"],
        ),
        card(
            chapter=ch, section="4.2.3 Signaling",
            question="Was ist Signaling in der Kapitalstruktur und wann ist Verschuldung ein positives Signal?",
            answer=(
                "Signaling: Manager kennen den wahren Unternehmenswert besser als der Markt. "
                "Kapitalstrukturentscheidungen können als Signal genutzt werden.\n\n"
                "Hohe Verschuldung signalisiert: Manager erwartet hohe zukünftige Cashflows "
                "(sonst riskiert er Insolvenz). → Positives Signal.\n"
                "EK-Emission: Oft negatives Signal – Markt vermutet Überbewertung.\n\n"
                "Empirisch: Ankündigung einer EK-Emission → Aktienkurs sinkt i.d.R."
            ),
            card_type="definition", difficulty=3, importance=0.8, exam_relevance=0.8,
            tags=tags4 + ["Signaling", "Asymmetrische Information"],
        ),
        card(
            chapter=ch, section="4.1.3 Steuern auf Investorenebene",
            question=(
                "Wahr oder falsch? Der Steuervorteil des Fremdkapitals entfällt vollständig, "
                "wenn Zinseinkommen beim Investor höher besteuert wird als Dividenden. Begründe kurz."
            ),
            answer=(
                "Falsch (so eindeutig nicht). Der Nettosteuervorteil hängt vom Zusammenspiel "
                "aus Unternehmenssteuer und Investorensteuer ab. Wenn die persönliche Steuer "
                "auf Zinseinkommen deutlich höher ist als auf EK-Renditen, kann der Steuervorteil "
                "auf Unternehmensebene teilweise oder vollständig neutralisiert werden (Miller 1977). "
                "Er entfällt aber nur vollständig unter sehr spezifischen Bedingungen."
            ),
            card_type="trueFalse", difficulty=5, importance=0.75, exam_relevance=0.8,
            tags=tags4 + ["Steuern", "Wahr/Falsch"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 5 – Funktionen von Banken
# ---------------------------------------------------------------------------

def cards_chapter5() -> list[dict]:
    ch = "5. Funktionen von Banken"
    tags5 = ["Banken", "Finanzintermediation"]

    return [
        card(
            chapter=ch, section="Überblick",
            question="Was sind die drei Transformationsfunktionen von Banken?",
            answer=(
                "1. Losgrößentransformation: Bündelt viele kleine Einlagen → große Kredite.\n"
                "2. Fristentransformation: Kurzfristige Einlagen → langfristige Kredite. "
                "Risiko: Liquiditätsrisiko, Bank Runs.\n"
                "3. Risikotransformation: Diversifikation und Monitoring senken Kreditrisiko."
            ),
            card_type="listing", difficulty=2, importance=0.9, exam_relevance=0.9,
            tags=tags5 + ["Transformation"],
        ),
        card(
            chapter=ch, section="5.1 Diamond/Dybvig – Grundmodell",
            question="Beschreibe das Diamond/Dybvig (1983) Modell: Grundstruktur und zentrale Frage.",
            answer=(
                "Drei Perioden (0, 1, 2). Zwei Agenten-Typen:\n"
                "  – Typ 1 (frühe Konsumenten, Anteil π₁): brauchen Konsum in Periode 1\n"
                "  – Typ 2 (späte Konsumenten, Anteil π₂ = 1–π₁): konsumieren in Periode 2\n\n"
                "Technologie: Kurzfristige (L) und langfristige Investition (R > 1, aber L < 1 bei Liquidation).\n\n"
                "Zentrale Frage: Wie organisiert die Bank die Liquiditätsversicherung "
                "besser als Autarkie oder Finanzmärkte?"
            ),
            card_type="definition", difficulty=4, importance=1.0, exam_relevance=1.0,
            tags=tags5 + ["Diamond/Dybvig", "Modell", "Klausurstil"],
        ),
        card(
            chapter=ch, section="5.1 Diamond/Dybvig – Autarkie",
            question=(
                "Diamond/Dybvig: Was ist die Autarkie-Lösung? "
                "Welchen Konsum erhalten frühe und späte Konsumenten?"
            ),
            answer=(
                "In Autarkie optimiert jeder Agent individuell. Wenn die Ecklösung gilt (I = 0):\n"
                "C₁* = C₂* = 1 (kein Investitionsvorteil nutzbar)\n\n"
                "Wenn I > 0 (Ecklösung nicht bindend):\n"
                "C₁ = 1 – ½I; C₂ = 1 + ½I\n"
                "FOC: π₁ · u'(C₁) · ½ = π₂ · ρ · u'(C₂) · ½\n\n"
                "Bei γ = 2: u'(C) = 1/C² → Corner solution I = 0 möglich, wenn Bedingung verletzt."
            ),
            card_type="calculation", difficulty=7, importance=1.0, exam_relevance=1.0,
            solution_steps=[
                "Aufstelle: max_{I} π₁·u(C₁) + π₂·ρ·u(C₂)",
                "mit C₁ = 1 – ½I, C₂ = 1 + ½I",
                "FOC: π₁·u'(C₁)·½ = π₂·ρ·u'(C₂)·½",
                "Einsetzen u'(C) = 1/C² (bei γ=2)",
                "Prüfen ob Ecklösung I=0 bindend ist",
            ],
            formula="C₁ = 1 – (1−π₁)/π₁ · I·L;  C₂ = 1 + I·R",
            tags=tags5 + ["Diamond/Dybvig", "Autarkie", "Rechnen", "Klausurstil"],
        ),
        card(
            chapter=ch, section="5.1 Diamond/Dybvig – Finanzmarkt",
            question=(
                "Diamond/Dybvig: Welche Gleichgewichtsbedingung gilt für den Preis p "
                "eines Wertpapiers, das in Periode 2 eine Einheit auszahlt?"
            ),
            answer=(
                "Im Gleichgewicht: p = 1/R\n\n"
                "Begründung:\n"
                "  – p > 1/R: Wertpapier zu teuer → kein Angebot (Investoren halten lieber kurzfristig)\n"
                "  – p < 1/R: Wertpapier zu billig → keine Nachfrage (alle investieren langfristig)\n"
                "Nur p = 1/R ist ein Gleichgewicht.\n\n"
                "Damit: C₁ = 1, C₂ = R (kein Versicherungsgewinn über Finanzmarkt)"
            ),
            card_type="understanding", difficulty=6, importance=1.0, exam_relevance=1.0,
            formula="p* = 1/R",
            tags=tags5 + ["Diamond/Dybvig", "Finanzmarkt", "Klausurstil"],
        ),
        card(
            chapter=ch, section="5.1 Diamond/Dybvig – First-best",
            question="Diamond/Dybvig: Was ist die First-best-Lösung und warum ist sie besser als der Finanzmarkt?",
            answer=(
                "Die Bank bietet C₁* > 1 und C₂* < R (mit C₁* < C₂*), "
                "indem sie Liquiditätsversicherung anbietet.\n\n"
                "Gleichgewichtssystem:\n"
                "  π₁·C₁ + π₂·(C₂/R) = 1  (Ressourcenbedingung)\n"
                "  u'(C₁) = ρ·R·u'(C₂)   (Optimierungsbedingung)\n\n"
                "Ergebnis: Bank glättet Konsum zwischen frühen und späten Konsumenten. "
                "Vorteil gegenüber Finanzmarkt: C₁* > 1 (Finanzmarkt gibt nur C₁ = 1)."
            ),
            card_type="definition", difficulty=7, importance=1.0, exam_relevance=1.0,
            formula="u'(C₁*) = ρ·R·u'(C₂*)",
            tags=tags5 + ["Diamond/Dybvig", "First-best", "Klausurstil"],
        ),
        card(
            chapter=ch, section="5.2 Delegierte Kontrolle",
            question="Warum ist eine Bank als 'delegierter Kontrolleur' effizienter als viele individuelle Gläubiger?",
            answer=(
                "Kontrollkosten skalieren mit der Anzahl der Gläubiger. "
                "Wenn viele Kleinanleger einen Kreditnehmer überwachen, entstehen Doppelkosten. "
                "Eine Bank übernimmt stellvertretend die Kontrolle (delegierte Kontrolle). "
                "Die Bank diversifiziert über viele Schuldner → fast risikofreie Einlagen → "
                "geringe Kontrollkosten für Einleger → effizienter."
            ),
            card_type="understanding", difficulty=4, importance=0.85, exam_relevance=0.85,
            tags=tags5 + ["Delegierte Kontrolle", "Monitoring"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 6 – Finanzkrisen und systemische Risiken
# ---------------------------------------------------------------------------

def cards_chapter6() -> list[dict]:
    ch = "6. Finanzkrisen und systemische Risiken"
    tags6 = ["Finanzstabilität", "Bank Run", "Systemisches Risiko"]

    return [
        card(
            chapter=ch, section="6.1 Das Grundproblem",
            question="Warum sind Banken strukturell anfällig für Runs (Diamond/Dybvig)?",
            answer=(
                "Banken transformieren kurzfristige Einlagen in langfristige Kredite (Fristentransformation). "
                "Wenn viele Einleger gleichzeitig abheben ('Bank Run'), muss die Bank "
                "langfristige Anlagen frühzeitig und mit Verlust liquidieren (L < 1).\n\n"
                "Sequential Service: Bank bedient Abheber der Reihe nach → wer zu spät kommt, "
                "erhält nichts. Das schafft Anreiz für alle, früh abzuheben → Self-fulfilling Run.\n"
                "→ Stabiles Gleichgewicht (Bank intakt) UND Run-Gleichgewicht existieren nebeneinander."
            ),
            card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0,
            tags=tags6 + ["Diamond/Dybvig", "Self-fulfilling"],
        ),
        card(
            chapter=ch, section="6.2 Narrow Banking",
            question="Was ist Narrow Banking und löst es das Bank-Run-Problem?",
            answer=(
                "Narrow Banking: Banken dürfen nur kurzfristige, sichere Anlagen halten "
                "(kein Fristentransformationsrisiko). "
                "Einlagen wären dann vollständig gedeckt → keine Run-Gefahr.\n\n"
                "Problem: Die Fristentransformation ist die Kernfunktion der Bank "
                "(Liquiditätsversicherung, Diamond/Dybvig). "
                "Narrow Banking beseitigt diese Funktion und damit den gesellschaftlichen Nutzen der Bank."
            ),
            card_type="contrast", difficulty=4, importance=0.85, exam_relevance=0.85,
            tags=tags6 + ["Narrow Banking"],
        ),
        card(
            chapter=ch, section="6.3 Einlagenversicherung",
            question="Wie löst eine Einlagenversicherung das Bank-Run-Gleichgewicht?",
            answer=(
                "Einlagenversicherung garantiert Einlegern die Rückzahlung bis zu einem "
                "bestimmten Betrag (z.B. 100.000 EUR in der EU), unabhängig vom Bankzustand.\n\n"
                "Damit: Es gibt keinen Grund mehr, frühzeitig abzuheben – kein Run-Gleichgewicht.\n"
                "Problem: Moral Hazard – Banken können mehr Risiken eingehen (Einleger überwachen nicht mehr).\n"
                "→ Kombination mit Regulierung (Eigenkapitalanforderungen) nötig."
            ),
            card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.9,
            tags=tags6 + ["Einlagenversicherung", "Moral Hazard"],
        ),
        card(
            chapter=ch, section="6.6 Lender of Last Resort",
            question="Was ist der Lender of Last Resort (LoLR) und welche Bedingung gilt für Kredite?",
            answer=(
                "Der LoLR (typischerweise die Zentralbank) vergibt Kredite an Banken, "
                "die kurzfristig illiquide, aber nicht insolvent sind.\n\n"
                "Bagehot-Prinzip: Kredite nur an illiquide, aber solvente Banken; "
                "zu Strafzinsen; gegen gute Sicherheiten.\n\n"
                "Problem: In der Praxis schwer zu unterscheiden ob illiquide oder insolvent. "
                "LoLR kann Moral Hazard verstärken."
            ),
            card_type="definition", difficulty=4, importance=0.9, exam_relevance=0.9,
            tags=tags6 + ["Lender of Last Resort", "Zentralbank"],
        ),
        card(
            chapter=ch, section="6.7 Too-big-to-fail",
            question=(
                "Wahr oder falsch? Das 'Too-big-to-fail'-Problem führt zu einem "
                "Wettbewerbsvorteil großer Banken gegenüber kleinen. Begründe (max. 2 Sätze)."
            ),
            answer=(
                "Wahr. Große Banken werden von Gläubigern und Gegenparteien als implizit staatlich "
                "garantiert wahrgenommen → günstigere Refinanzierungskonditionen als kleine Banken. "
                "Dies verzerrt den Wettbewerb zugunsten systemisch wichtiger Institute."
            ),
            card_type="trueFalse", difficulty=4, importance=1.0, exam_relevance=1.0,
            tags=tags6 + ["Too-big-to-fail", "Wettbewerb", "Wahr/Falsch", "Klausurstil"],
        ),
        card(
            chapter=ch, section="6.5 Ansteckung",
            question="Über welche Kanäle können Finanzkrisen innerhalb des Bankensystems anstecken?",
            answer=(
                "1. Direkter Interbankenmarkt: Bankforderungen gegen andere Banken → Ausfall pflanzt sich fort.\n"
                "2. Informationskanal: Run auf Bank A löst Run auf Bank B aus "
                "(Einleger schließen auf Qualitätsprobleme im gesamten Sektor).\n"
                "3. Asset-Fire-Sales: Notverkäufe senken Marktpreise → andere Banken erleiden Verluste.\n"
                "4. Liquiditätskanal: Alle Banken ziehen Liquidität gleichzeitig ab."
            ),
            card_type="listing", difficulty=4, importance=0.85, exam_relevance=0.85,
            tags=tags6 + ["Ansteckung", "Contagion"],
        ),
    ]


# ---------------------------------------------------------------------------
# KAPITEL 7 – Bankenregulierung
# ---------------------------------------------------------------------------

def cards_chapter7() -> list[dict]:
    ch = "7. Bankenregulierung"
    tags7 = ["Bankenregulierung", "Eigenkapitalregulierung", "Basel"]

    return [
        card(
            chapter=ch, section="7.1 Gründe für Regulierung",
            question="Warum werden Banken stärker reguliert als andere Unternehmen?",
            answer=(
                "1. Einlagenversicherung schafft Moral Hazard → Regulierung als Gegengewicht.\n"
                "2. Systemisches Risiko: Bankenausfälle haben negative Externalitäten für die Realwirtschaft.\n"
                "3. Informationsasymmetrie: Einleger können Bankqualität nicht effizient überwachen.\n"
                "4. 'Too-big-to-fail': Implizite Staatsgarantie verzerrt Anreize.\n"
                "5. Zahlungsverkehr: Banken sind kritische Infrastruktur."
            ),
            card_type="listing", difficulty=2, importance=0.9, exam_relevance=0.9,
            tags=tags7 + ["Regulierungsgründe"],
        ),
        card(
            chapter=ch, section="7.2 Eigenkapitalregulierung",
            question=(
                "Wahr oder falsch? Aufgrund der Eigenkapitalregulierung sind die "
                "Eigenkapitalquoten der Banken heute viel höher als vor 100 Jahren. Begründe."
            ),
            answer=(
                "Falsch. Eigenkapitalquoten der Banken sind heute viel niedriger als vor 100 Jahren "
                "(historisch 30–50%, heute ca. 8–15%). "
                "Die Eigenkapitalregulierung war eine Reaktion auf den historischen Rückgang "
                "der EK-Quoten, nicht deren Ursache. "
                "Regulierung erhöhte EK-Quoten relativ zum Trend, aber nicht auf historische Niveaus."
            ),
            card_type="trueFalse", difficulty=4, importance=1.0, exam_relevance=1.0,
            tags=tags7 + ["EK-Quote", "Wahr/Falsch", "Klausurstil"],
        ),
        card(
            chapter=ch, section="7.3 Funktionen der EK-Regulierung",
            question=(
                "Wahr oder falsch? Höhere Eigenkapitalanforderungen sind nützlich, "
                "weil sie für Banken einen Puffer gegen unvorhergesehene Schocks darstellen. Begründe."
            ),
            answer=(
                "Wahr (mit Nuance). Höheres EK puffert Verluste und schützt Einleger/Steuerzahler. "
                "Jedoch gilt aus Bankperspektive das Modigliani-Miller-Argument: "
                "Mehr EK senkt zwar die Insolvenzwahrscheinlichkeit, aber EK-Kosten sind höher als FK-Kosten "
                "(vor Steuern äquivalent; mit Steuern: mehr EK teurer). "
                "Gesellschaftlich: Puffernutzen überwiegt private Kosten."
            ),
            card_type="trueFalse", difficulty=5, importance=1.0, exam_relevance=1.0,
            tags=tags7 + ["EK-Puffer", "Wahr/Falsch", "Klausurstil"],
        ),
        card(
            chapter=ch, section="7.2 Basel",
            question="Was sind die Kernelemente der Eigenkapitalregulierung (Basel I → Basel III)?",
            answer=(
                "Basel I (1988): 8% Mindestkapitalquote auf risikogewichtete Aktiva (RWA).\n\n"
                "Basel II (2004): Verfeinerte Risikogewichtung (Standardansatz + interne Modelle); "
                "Marktrisiko + operationelles Risiko.\n\n"
                "Basel III (2010+): Reaktion auf Finanzkrise:\n"
                "  – Höhere Eigenkapitalquoten (Common Equity Tier 1: min. 4,5%)\n"
                "  – Leverage Ratio (ungewichtet, max. 33-facher Hebel)\n"
                "  – Liquidity Coverage Ratio (LCR) und Net Stable Funding Ratio (NSFR)\n"
                "  – Kapitalerhaltungspuffer, antizyklischer Puffer"
            ),
            card_type="listing", difficulty=4, importance=0.9, exam_relevance=0.9,
            tags=tags7 + ["Basel I", "Basel II", "Basel III"],
        ),
        card(
            chapter=ch, section="7.5 Systemisches Risiko",
            question="Was ist systemisches Risiko und wie unterscheidet es sich von individuellem Bankrisiko?",
            answer=(
                "Systemisches Risiko: Risiko eines Zusammenbruchs des gesamten Finanzsystems "
                "oder eines wesentlichen Teils davon, mit schwerwiegenden Folgen für die Realwirtschaft.\n\n"
                "Unterschied zu individuellem Risiko: Banken berücksichtigen bei ihrer Risikoentscheidung "
                "nicht den negativen Effekt auf andere Banken und die Volkswirtschaft "
                "(negative Externalität). Individuelle Rationalität führt zu systemisch übermäßigem Risiko.\n\n"
                "Makroprudenzielle Regulierung zielt darauf ab, dieses Koordinationsversagen zu beheben."
            ),
            card_type="contrast", difficulty=4, importance=0.9, exam_relevance=0.9,
            tags=tags7 + ["Systemisches Risiko", "Makroprudenzielle Regulierung"],
        ),
    ]


# ---------------------------------------------------------------------------
# Flashcards from current exercises (U01–U05_jetzt)
# ---------------------------------------------------------------------------

def cards_from_exercises() -> list[dict]:
    """Generate key flashcards derived from current exercise patterns."""
    ch3 = "3. Kapitalstruktur: vollkommener Markt & MM-Theorem"
    tags = ["Übungsaufgabe", "Rechnen", "Klausurstil", "MM-Theorem"]

    return [
        card(
            chapter=ch3, section="3.1 Rechenbeispiel",
            question=(
                "Übung 1 (Typ): Projekt (EW = 120.000 EUR, Invest = 90.000 EUR). "
                "r_f = 10%, Risikoaufschlag = 10%. Ist das Projekt lohnenswert?"
            ),
            answer=(
                "r_U = r_f + Risikoaufschlag = 10% + 10% = 20%\n"
                "V = EW / (1 + r_U) = 120.000 / 1,20 = 100.000 EUR\n"
                "NPV = V – I = 100.000 – 90.000 = 10.000 EUR > 0\n"
                "→ Ja, das Projekt ist lohnenswert."
            ),
            card_type="calculation", difficulty=4, importance=0.95, exam_relevance=1.0,
            solution_steps=[
                "Diskontierungssatz: r_U = r_f + Risikoaufschlag",
                "Unternehmenswert: V = EW / (1 + r_U)",
                "NPV = V – Investition",
                "NPV > 0 → lohnenswert",
            ],
            formula="NPV = EW/(1+r_U) - I",
            source_current="U01_jetzt.pdf",
            tags=tags,
        ),
        card(
            chapter=ch3, section="3.1 EK-Rendite",
            question=(
                "Ein Projekt zahlt 140.000 EUR (p=50%) oder 100.000 EUR (p=50%). "
                "EK-Wert = 100.000 EUR. Wie hoch ist die erwartete EK-Rendite?"
            ),
            answer=(
                "Rendite hoch = (140.000 – 100.000) / 100.000 = 40%\n"
                "Rendite niedrig = (100.000 – 100.000) / 100.000 = 0%\n"
                "Erwartete Rendite = 0,5 × 40% + 0,5 × 0% = 20%\n\n"
                "Diese entspricht r_U = 20% (vollkommener Markt, vollständige EK-Finanzierung)."
            ),
            card_type="calculation", difficulty=4, importance=0.9, exam_relevance=1.0,
            solution_steps=[
                "Rendite_hoch = (CF_hoch – EK-Wert) / EK-Wert",
                "Rendite_niedrig = (CF_niedrig – EK-Wert) / EK-Wert",
                "Erwartete Rendite = p_hoch × R_hoch + p_niedrig × R_niedrig",
            ],
            source_current="U01_jetzt.pdf",
            tags=tags + ["EK-Rendite"],
        ),
        card(
            chapter=ch3, section="3.3 WACC Berechnung",
            question=(
                "Klausur (Typ): EK = 500 EUR, D = 500 EUR, r_E = 19%, r_D = 5%. "
                "Berechne den WACC. Entspricht das r_U bei vollk. Markt?"
            ),
            answer=(
                "WACC = (E/(E+D)) × r_E + (D/(E+D)) × r_D\n"
                "     = (500/1000) × 19% + (500/1000) × 5%\n"
                "     = 9,5% + 2,5% = 12%\n\n"
                "Ja: WACC = r_U = 12% (MMT I im vollk. Markt)."
            ),
            card_type="calculation", difficulty=4, importance=1.0, exam_relevance=1.0,
            solution_steps=[
                "E/(E+D) = 500/1000 = 0,5",
                "D/(E+D) = 500/1000 = 0,5",
                "WACC = 0,5 × 19% + 0,5 × 5% = 12%",
            ],
            formula="WACC = (E/(E+D))·r_E + (D/(E+D))·r_D",
            numeric_answer=0.12, tolerance=0.001,
            source_current="U01_jetzt.pdf",
            tags=tags + ["WACC"],
        ),
        card(
            chapter=ch3, section="3.2 MMT II Anwendung",
            question=(
                "r_U = 12%, r_D = 5%, D = 800 EUR, E = 200 EUR. "
                "Wie hoch ist r_E laut MMT II?"
            ),
            answer=(
                "MMT II: r_E = r_U + (D/E) × (r_U − r_D)\n"
                "r_E = 12% + (800/200) × (12% − 5%)\n"
                "r_E = 12% + 4 × 7%\n"
                "r_E = 12% + 28% = 40%"
            ),
            card_type="calculation", difficulty=5, importance=1.0, exam_relevance=1.0,
            solution_steps=[
                "Verschuldungsgrad D/E = 800/200 = 4",
                "r_E = r_U + D/E × (r_U – r_D)",
                "r_E = 12% + 4 × (12% – 5%) = 40%",
            ],
            formula="r_E = r_U + (D/E) × (r_U − r_D)",
            numeric_answer=0.40, tolerance=0.001,
            source_current="U01_jetzt.pdf",
            tags=tags + ["MMT II", "Leverage"],
        ),
    ]


# ---------------------------------------------------------------------------
# Deduplication and validation
# ---------------------------------------------------------------------------

def deduplicate(cards: list[dict]) -> list[dict]:
    """Remove near-duplicate cards based on question similarity hash."""
    seen: set[str] = set()
    unique = []
    for c in cards:
        # Normalize and hash first 80 chars of question
        q_key = re.sub(r"\s+", " ", c["question"].lower().strip())[:80]
        h = hashlib.md5(q_key.encode()).hexdigest()[:8]
        if h not in seen:
            seen.add(h)
            unique.append(c)
    return unique


def validate_card(c: dict) -> list[str]:
    issues = []
    if len(c["question"]) < 10:
        issues.append("question_too_short")
    if len(c["answer"]) < 20:
        issues.append("answer_too_short")
    if c["importance"] <= 0:
        issues.append("importance_zero")
    if not c["source"]["current"]:
        issues.append("no_source")
    return issues


def validate_all(cards: list[dict]) -> list[dict]:
    for c in cards:
        issues = validate_card(c)
        c["validation"]["issues"] = issues
        c["validation"]["status"] = "review" if issues else "ok"
    return cards


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phase 4 – Flashcard Generator")
    parser.add_argument("--out", default="flashcards.json")
    args = parser.parse_args()

    print("Generating flashcards...")
    all_cards = (
        cards_chapter1()
        + cards_chapter2()
        + cards_chapter3()
        + cards_chapter4()
        + cards_chapter5()
        + cards_chapter6()
        + cards_chapter7()
        + cards_from_exercises()
    )

    print(f"  Raw cards: {len(all_cards)}")
    all_cards = deduplicate(all_cards)
    print(f"  After deduplication: {len(all_cards)}")
    all_cards = validate_all(all_cards)

    ok = sum(1 for c in all_cards if c["validation"]["status"] == "ok")
    review = sum(1 for c in all_cards if c["validation"]["status"] == "review")
    print(f"  OK: {ok}, Needs review: {review}")

    # Stats by chapter
    from collections import Counter
    ch_counts = Counter(c["chapter"].split(".")[0] for c in all_cards)
    for ch, cnt in sorted(ch_counts.items()):
        print(f"  Chapter {ch}: {cnt} cards")

    output = {
        "meta": {
            "generatedAt": TODAY,
            "generatedBy": "scripts/generate/flashcard_generator.py",
            "primarySource": "Skript FMI SS2026_ jetzt.pdf",
            "totalCards": len(all_cards),
            "byStatus": {"ok": ok, "review": review},
        },
        "flashcards": all_cards,
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFlashcards written to: {out_path}")

    # Also copy to public/data/ for the web app
    public_dir = Path("public/data")
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "flashcards.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Also copied to: {public_dir / 'flashcards.json'}")


if __name__ == "__main__":
    main()
