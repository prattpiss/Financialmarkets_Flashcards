"""
Phase 4 – Flashcard Generator (VOLLSTÄNDIG)
Erzeugt ~400+ Lernkarten für alle 7 Kapitel des FMI-Skripts SS2026.

Chapters:
  1 – Funktionen des Finanzsystems
  2 – Die globale Finanzkrise
  3 – MM-Theorem (vollkommener Markt)
  4 – Marktunvollkommenheiten & Kapitalstruktur
  5 – Funktionen von Banken (Diamond-Dybvig)
  6 – Finanzkrisen & systemische Risiken
  7 – Bankenregulierung

Usage:
    python scripts/generate/flashcard_generator.py [--out flashcards.json]
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Optional

TODAY = date.today().isoformat()
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
    card_type: str,
    difficulty: int,
    importance: float,
    exam_relevance: float,
    tags: list[str],
    source_current: Optional[str] = "Skript FMI SS2026_ jetzt.pdf",
    solution_steps: Optional[list[str]] = None,
    formula: Optional[str] = None,
    variables: Optional[dict] = None,
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
            "historical": [],
        },
        **({"solutionSteps": solution_steps} if solution_steps else {}),
        **({"formula": formula} if formula else {}),
        **({"variables": variables} if variables else {}),
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


# ===========================================================================
# KAPITEL 1
# ===========================================================================

def cards_chapter1() -> list[dict]:
    ch = "1. Funktionen des Finanzsystems"
    t = ["Finanzsystem", "Grundlagen"]
    return [
        card(chapter=ch, section="Akteure", question="Welche drei Kerngruppen von Akteuren sind im Finanzsystem aktiv?",
             answer="1. Finanzmärkte & Finanzintermediäre (Banken, Versicherungen, Fonds)\n2. Endnutzer: Haushalte, Unternehmen, Regierungen\n3. Finanzinfrastruktur: Börsen, Zahlungssysteme, Ratingagenturen",
             card_type="listing", difficulty=1, importance=0.85, exam_relevance=0.8, tags=t+["Akteure"]),
        card(chapter=ch, section="Direkte vs. indirekte Finanzierung", question="Was ist direkte Finanzierung? Nenne ein Beispiel.",
             answer="Kapitalnehmer tritt direkt mit Kapitalanleger in Kontakt, ohne Intermediär.\nBeispiel: Haushalt kauft Unternehmensanleihe am Kapitalmarkt.",
             card_type="definition", difficulty=1, importance=0.9, exam_relevance=0.85, tags=t+["Finanzierung"]),
        card(chapter=ch, section="Direkte vs. indirekte Finanzierung", question="Was ist indirekte Finanzierung? Nenne ein Beispiel.",
             answer="Ein Finanzintermediär (z.B. Bank) steht zwischen Anleger und Kapitalnehmer.\nBeispiel: Haushalt legt bei Bank an → Bank vergibt Kredit an Unternehmen.",
             card_type="definition", difficulty=1, importance=0.9, exam_relevance=0.85, tags=t+["Finanzierung"]),
        card(chapter=ch, section="Direkte vs. indirekte Finanzierung", question="Was ist der zentrale Vorteil indirekter Finanzierung gegenüber direkter?",
             answer="Intermediäre reduzieren Transaktions- und Informationskosten durch:\n• Skaleneffekte (große Volumina)\n• Spezialisierung in Risikobewertung und Monitoring\n• Fristentransformation\n• Risikodiversifikation über viele Kreditnehmer",
             card_type="understanding", difficulty=2, importance=0.9, exam_relevance=0.85, tags=t+["Intermediäre"]),
        card(chapter=ch, section="Funktionen", question="Welche 5 Hauptfunktionen übernimmt das Finanzsystem?",
             answer="1. Kapitalallokation (Ersparnisse → Investitionen)\n2. Reduktion von Transaktionskosten\n3. Reduktion von Informationskosten\n4. Risikomanagement (Diversifikation, Hedging)\n5. Corporate Governance (Kontrolle der Unternehmensführung)",
             card_type="listing", difficulty=2, importance=0.95, exam_relevance=0.85, tags=t+["Funktionen"]),
        card(chapter=ch, section="Transaktionskosten", question="Wie reduzieren Finanzintermediäre Transaktionskosten?",
             answer="• Standardisierung von Verträgen\n• Spezialisierung und Lernkurveneffekte\n• Skaleneffekte (Fixkosten verteilen)\n• Bündelung kleiner Transaktionen",
             card_type="understanding", difficulty=2, importance=0.85, exam_relevance=0.75, tags=t+["Transaktionskosten"]),
        card(chapter=ch, section="Informationskosten", question="Welche zwei Arten von Informationsproblemen lösen Finanzintermediäre?",
             answer="1. Adverse Selektion (ex ante): Screening vor Vertragsschluss (Kreditprüfung)\n2. Moral Hazard (ex post): Monitoring nach Vertragsschluss",
             card_type="contrast", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Informationskosten", "Adverse Selektion", "Moral Hazard"]),
        card(chapter=ch, section="Informationskosten", question="Was ist das 'Free-Rider-Problem' bei der Finanzmarkt-Informationsproduktion?",
             answer="Ein Investor beschafft kostspielig Informationen, andere nutzen sie kostenlos (z.B. durch Preisbeobachtung). Dadurch wird zu wenig in Informationsproduktion investiert. Finanzintermediäre lösen dies durch private Kreditverträge.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.75, tags=t+["Informationskosten", "Free Rider"]),
        card(chapter=ch, section="Risikomanagement", question="Welche drei Hauptformen des Risikomanagements bietet das Finanzsystem?",
             answer="1. Diversifikation (Risiko über viele Anlagen streuen)\n2. Liquiditätsbereitstellung (Umwandlung illiquider in liquide Anlagen)\n3. Hedging / Absicherung (Derivate: Futures, Optionen, Swaps)",
             card_type="listing", difficulty=2, importance=0.85, exam_relevance=0.75, tags=t+["Risikomanagement"]),
        card(chapter=ch, section="Corporate Governance", question="Warum ist Corporate Governance eine Funktion des Finanzsystems?",
             answer="EK-Geber delegieren Entscheidungen an Manager. Das Finanzsystem schafft Kontrollanreize:\n• Vergütungsstruktur (Aktienoptionen)\n• FK-Disziplinierung (Konkursdrohung)\n• Aktionärsrechte, Hauptversammlung\n• Markt für Unternehmenskontrolle (Übernahmen)",
             card_type="understanding", difficulty=3, importance=0.8, exam_relevance=0.7, tags=t+["Corporate Governance"]),
        card(chapter=ch, section="Schattenbankensystem", question="Was ist das Schattenbankensystem und warum ist es entstanden?",
             answer="Finanzintermediäre mit bankenähnlichen Funktionen, aber ohne Bankenregulierung.\nEntstanden als Reaktion auf:\n• Verschärfte Bankenregulierung\n• Suche nach höheren Renditen\nBeispiele: Money-Market-Fonds, Hedge-Fonds, SPVs",
             card_type="definition", difficulty=3, importance=0.8, exam_relevance=0.75, tags=t+["Schattenbankensystem"]),
        card(chapter=ch, section="Schattenbankensystem", question="Welche Risiken birgt das Schattenbankensystem für die Finanzstabilität?",
             answer="• Keine Einlagensicherung → anfällig für Runs\n• Keine Zentralbankunterstützung\n• Weniger transparent → systemisches Risiko\n• Verflechtung mit regulärem Bankensystem\n• Regulierungsarbitrage",
             card_type="understanding", difficulty=4, importance=0.75, exam_relevance=0.65, tags=t+["Schattenbankensystem", "Systemisches Risiko"]),
        card(chapter=ch, section="Trends", question="Welche drei wesentlichen aktuellen Trends prägen das Finanzsystem?",
             answer="1. Wachstum des Schattenbankensystems\n2. Digitalisierung (FinTech, Krypto) bedroht traditionelle Geschäftsmodelle\n3. Größere Komplexität von Finanzprodukten",
             card_type="listing", difficulty=2, importance=0.75, exam_relevance=0.65, tags=t+["Trends", "FinTech"]),
        card(chapter=ch, section="Finanzmarktinstrumente", question="Unterschied zwischen Geldmarkt und Kapitalmarkt?",
             answer="Geldmarkt: Laufzeit ≤ 1 Jahr, sehr liquide und risikoarm (z.B. Schatzwechsel, Overnight-Einlagen).\nKapitalmarkt: Laufzeit > 1 Jahr (z.B. Aktien, Anleihen). Höheres Risiko, höhere Renditeerwartung.",
             card_type="contrast", difficulty=2, importance=0.8, exam_relevance=0.7, tags=t+["Geldmarkt", "Kapitalmarkt"]),
        card(chapter=ch, section="Finanzmarktinstrumente", question="Was ist Fristentransformation und warum ist sie riskant?",
             answer="Banken nehmen kurzfristige Einlagen und vergeben langfristige Kredite. Profitabel wegen positiver Zinsstrukturkurve.\nRisiko: Bei Run wollen alle Geld zurück, aber Kredite sind illiquide → Liquiditätskrise.",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Fristentransformation", "Bank Run"]),
        card(chapter=ch, section="Akteure", question="Welche Rolle spielen Ratingagenturen im Finanzsystem?",
             answer="Reduzieren Informationsasymmetrien durch Kreditwürdigkeitsbewertung von Schuldnern.\nKritik: Interessenkonflikt (bezahlt vom Emittenten), Versagen vor der Finanzkrise 2007-09.",
             card_type="understanding", difficulty=3, importance=0.75, exam_relevance=0.7, tags=t+["Ratingagenturen"]),
        card(chapter=ch, section="Recht der großen Zahlen", question="Warum ermöglicht das Gesetz der großen Zahlen Risikodiversifikation durch Banken?",
             answer="Bei n Einlegern konvergiert der Anteil π der Typ-1-Konsumenten in Wahrscheinlichkeit zu seinem Erwartungswert. Die Bank kann exakt π als Reserve halten und den Rest langfristig investieren – ohne auf individuelle Nachfrage warten zu müssen.",
             card_type="understanding", difficulty=4, importance=0.9, exam_relevance=0.85, tags=t+["Gesetz der großen Zahlen", "Liquidität"]),
        card(chapter=ch, section="Vergleich", question="Vergleiche: Banken vs. Kapitalmärkte als Unternehmensfinanzierungskanäle.",
             answer="Banken:\n• Private Beziehung, enge Überwachung\n• Günstiger für kleine/junge Unternehmen\n\nKapitalmärkte:\n• Breite Investorenbasis, öffentliche Informationen\n• Günstiger für große, transparente Unternehmen\n• Ermöglicht breite Risikostreuung",
             card_type="contrast", difficulty=3, importance=0.8, exam_relevance=0.7, tags=t+["Banken", "Kapitalmärkte"]),
    ]


# ===========================================================================
# KAPITEL 2
# ===========================================================================

def cards_chapter2() -> list[dict]:
    ch = "2. Die globale Finanzkrise und ihre Auswirkungen"
    t = ["Finanzkrise", "Makroökonomie"]
    return [
        card(chapter=ch, section="Arten von Finanzkrisen", question="Welche vier Arten von Finanzkrisen unterscheidet die Literatur?",
             answer="1. Bankenkrisen\n2. Währungskrisen\n3. Staatsverschuldungskrisen\n4. Kombinationen (Zwillings-/Drillingskrisen)",
             card_type="listing", difficulty=2, importance=0.75, exam_relevance=0.6, tags=t+["Krisentypen"]),
        card(chapter=ch, section="Stilisierte Fakten", question="Nenne 4 stilisierte Fakten über Finanzkrisen.",
             answer="1. Finanzkrisen sind wiederkehrend und unvermeidlich\n2. Bankenkrisen treten oft zusammen mit Währungskrisen auf\n3. Kreditbooms gehen Krisen typischerweise voraus\n4. Krisen verursachen hohe Kosten: BIP-Verlust, Schuldenanstieg, Arbeitslosigkeit",
             card_type="listing", difficulty=3, importance=0.7, exam_relevance=0.55, tags=t+["Stilisierte Fakten"]),
        card(chapter=ch, section="Finanzkrise 2007-2009", question="Was waren die wesentlichen Ursachen der globalen Finanzkrise 2007-2009?",
             answer="• Kreditboom im US-Hypothekenmarkt (Subprime)\n• Verbriefung: Hypotheken → MBS → CDOs\n• Originate-to-distribute: keine Haftung der Kreditvergeber\n• Zu niedrige Zinsen fördern Risikobereitschaft\n• Übermäßiger Leverage im Schattenbankensystem\n• Versagen der Ratingagenturen und Regulatoren",
             card_type="listing", difficulty=3, importance=0.8, exam_relevance=0.65, tags=t+["Subprime", "Verbriefung"]),
        card(chapter=ch, section="Verbriefung", question="Was ist Verbriefung und welche Rolle spielte sie in der Finanzkrise?",
             answer="Verbriefung: Bündeln von Krediten und Ausgabe von Wertpapieren (MBS, CDO) an externe Investoren.\nRolle: Originate-to-distribute senkte Vergabestandards (Risiko weitergegeben). Komplexe CDO-Strukturen verschleierten Risikokonzentration. Bei Preisrückgängen implodierte das System.",
             card_type="understanding", difficulty=4, importance=0.8, exam_relevance=0.65, tags=t+["Verbriefung", "MBS", "CDO"]),
        card(chapter=ch, section="Finanzkrise 2007-2009", question="Was ist das 'Originate-to-Distribute'-Modell und welches Anreizproblem erzeugt es?",
             answer="Banken vergeben Kredite ('originate') und verkaufen sie sofort weiter ('distribute') durch Verbriefung.\nProblem (Moral Hazard): Kreditgeber haben keinen Anreiz zur Kreditprüfung, da sie das Ausfallrisiko nicht tragen. Resultat: Sinkende Vergabestandards.",
             card_type="understanding", difficulty=3, importance=0.8, exam_relevance=0.65, tags=t+["Moral Hazard", "Verbriefung"]),
        card(chapter=ch, section="Zweckgesellschaften", question="Was sind Special Purpose Vehicles (SPVs)?",
             answer="Rechtlich selbstständige Einheiten, die Verbriefungsgeschäfte durchführen. Finanzieren sich über kurzfristige Verbindlichkeiten (ABCP) und halten langfristige Aktiva.\nFunktion: Auslagerung aus der Bankbilanz (Regulierungsarbitrage). In der Krise: Banken mussten SPVs stützen → Rückübertragung der Risiken.",
             card_type="understanding", difficulty=4, importance=0.75, exam_relevance=0.6, tags=t+["SPV", "Regulierungsarbitrage"]),
        card(chapter=ch, section="Eurokrise", question="Was waren die Kernursachen der Euroraumkrise ab 2010?",
             answer="• Staatsschuldenkrisen (GR, IE, PT, ES, IT)\n• Home Bias: Banken halten zu viele heimische Staatsanleihen → Doom Loop\n• Doom Loop: schwache Banken → Staatsrettungen → schlechtere Staatsfinanzen → Bankenverluste\n• Fehlende gemeinsame Fiskalpolitik im Euroraum",
             card_type="listing", difficulty=4, importance=0.7, exam_relevance=0.55, tags=t+["Eurokrise", "Staatsschulden", "Doom Loop"]),
        card(chapter=ch, section="Eurokrise", question="Was ist der 'Doom Loop' / Teufelskreis zwischen Banken und Staaten?",
             answer="1. Banken halten viele Staatsanleihen des Heimatlandes\n2. Staatliche Probleme → Anleihewert sinkt → Bankenverluste\n3. Schwache Banken brauchen Staatsrettung → Staatsschulden steigen\n4. Schlechtere Staatsfinanzen → Anleihepreise fallen → zurück zu Schritt 2",
             card_type="understanding", difficulty=4, importance=0.75, exam_relevance=0.6, tags=t+["Doom Loop"]),
        card(chapter=ch, section="Home Bias", question="Was ist 'Home Bias' bei Banken und warum ist er problematisch?",
             answer="Banken halten unverhältnismäßig viele Staatsanleihen des eigenen Heimatlandes statt diversifiziert.\nProblem: Verstärkt den Doom Loop – wenn das eigene Land in eine Schuldenkrise gerät, leiden heimische Banken besonders.",
             card_type="understanding", difficulty=3, importance=0.7, exam_relevance=0.55, tags=t+["Home Bias"]),
        card(chapter=ch, section="Reaktionen", question="Welche regulatorischen Reformen wurden nach der Finanzkrise 2007-2009 eingeleitet?",
             answer="• Basel III: Höhere EK- und Liquiditätsanforderungen\n• Dodd-Frank (USA): Volcker Rule, Derivate-Clearing, Stresstests\n• Bankenunion EU (SSM, SRM)\n• TLAC/MREL: Bail-in-fähiges Kapital\n• Stärkere Schattenbanken-Aufsicht",
             card_type="listing", difficulty=3, importance=0.75, exam_relevance=0.65, tags=t+["Basel III", "Regulierung"]),
        card(chapter=ch, section="2020er", question="Welche finanzmarktrelevanten Entwicklungen prägten die 2020er Jahre?",
             answer="• COVID-19 (2020): Massive staatliche Hilfen, Zentralbankliquidität\n• Inflationsschock 2021-23: Zinswende\n• Zinsanstieg → Bankturbulenzen 2023 (SVB, Credit Suisse)\n• Krypto-Boom und -Crash\n• Geopolitische Risiken (Ukraine, Energie)",
             card_type="listing", difficulty=2, importance=0.7, exam_relevance=0.5, tags=t+["COVID-19", "Inflation", "SVB"]),
        card(chapter=ch, section="Kapitalstruktur Kontext", question="Warum ist Leverage im Bankensektor besonders gefährlich für die Finanzstabilität?",
             answer="Banken operieren mit sehr hohem Leverage (30-50x vor der Krise). Schon kleine Verluste können das gesamte EK aufzehren → Insolvenz. Durch Vernetzung des Bankensystems können Ausfälle schnell auf andere Banken übergreifen → systemisches Risiko.",
             card_type="understanding", difficulty=3, importance=0.8, exam_relevance=0.7, tags=t+["Leverage", "Systemisches Risiko"]),
        card(chapter=ch, section="Savings & Loan", question="Was war die Savings-and-Loan-Krise der 1980er Jahre?",
             answer="US-Sparkassen (S&Ls) hatten langfristige Hypotheken zu festen Zinsen, aber kurzfristige Refinanzierung. Als Zinsen Ende 1970er stiegen, wurden Refinanzierungskosten höher als Erträge.\nVerschärfung durch Deregulierung → riskantere Investments → Verluste, Pleiten. Kosten: ca. 130 Mrd. USD.",
             card_type="understanding", difficulty=3, importance=0.6, exam_relevance=0.5, tags=t+["S&L-Krise"]),
    ]


# ===========================================================================
# KAPITEL 3
# ===========================================================================

def cards_chapter3() -> list[dict]:
    ch = "3. Kapitalstruktur im vollkommenen Markt (MM-Theorem)"
    t = ["MM-Theorem", "Kapitalstruktur"]
    return [
        card(chapter=ch, section="EK vs. FK Grundlagen", question="Was ist der Unterschied zwischen EK und FK aus Sicht der Ansprüche?",
             answer="EK: Residualanspruch – Eigentümer erhalten, was nach allen anderen Zahlungen bleibt. Beschränkte Haftung (GmbH/AG).\nFK: Prioritätsanspruch – Gläubiger erhalten feste Zahlungen (Zinsen + Tilgung). Bei Ausfall Vorrang vor Eigentümern.",
             card_type="contrast", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["EK", "FK"]),
        card(chapter=ch, section="EK vs. FK Grundlagen", question="Was sind die Rechte der Eigenkapitalgeber einer AG?",
             answer="Rechte:\n• Stimmrecht (Hauptversammlung)\n• Dividendenanspruch (wenn ausgeschüttet)\n• Anteil am Liquidationserlös (nachrangig)\nPflichten:\n• Beschränkte Haftung (max. Einlage)\n• Keine festen Zahlungsansprüche",
             card_type="listing", difficulty=2, importance=0.85, exam_relevance=0.8, tags=t+["Eigenkapital", "Aktie"]),
        card(chapter=ch, section="EK vs. FK Grundlagen", question="Was ist der Verschuldungsgrad und wie wird er berechnet?",
             answer="Verschuldungsgrad = D/E (FK/EK) oder D/(E+D) (FK-Quote).\nHöherer Verschuldungsgrad bedeutet: mehr Risiko für EK-Geber, mögliche höhere EK-Renditen (Leverage-Effekt), höheres Ausfallrisiko.",
             card_type="definition", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["Verschuldungsgrad"],
             formula="D/E oder D/(E+D)"),
        card(chapter=ch, section="EK vs. FK Grundlagen", question="Was versteht man unter 'Homemade Leverage'?",
             answer="Anleger können selbst FK aufnehmen und in EK investieren (oder umgekehrt), um denselben Auszahlungsstrom zu replizieren wie eine verschuldete/unverschuldete Firma. Kernargument für MM: Wenn Anleger die Kapitalstruktur selbst replizieren können, hat sie für den Firmenwert keinen Einfluss.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.95, tags=t+["Homemade Leverage"]),
        card(chapter=ch, section="MM I", question="Formuliere das Modigliani-Miller-Theorem I (ohne Steuern).",
             answer="Auf einem vollkommenen Kapitalmarkt ist der Marktwert eines Unternehmens unabhängig von seiner Kapitalstruktur:\nV_U = V_L = E + D\n\nEine verschuldete Firma hat denselben Gesamtwert wie eine identische unverschuldete Firma.",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["MM I"],
             formula="V_U = V_L",
             variables={"V_U": "Wert unverschuldetes Unternehmen", "V_L": "Wert verschuldetes Unternehmen"}),
        card(chapter=ch, section="MM I", question="Beweis-Logik für MM I: Wie zeigt man per Arbitrage, dass V_L = V_U sein muss?",
             answer="Angenommen V_L > V_U:\n→ Investor kauft α·V_U + leiht selbst α·D auf\n→ Repliziert damit Auszahlung des EK der verschuldeten Firma\n→ Kostet aber nur α·(V_U - D) < α·E_L\n→ Arbitragegewinn → Preise passen sich an bis V_L = V_U\nAngenommen V_L < V_U: analoges Argument.",
             card_type="understanding", difficulty=5, importance=1.0, exam_relevance=1.0, tags=t+["MM I", "Arbitrage"]),
        card(chapter=ch, section="MM I", question="Welche Annahmen eines 'vollkommenen Kapitalmarkts' setzt MM I voraus?",
             answer="1. Keine Steuern\n2. Keine Transaktionskosten\n3. Keine Informationsasymmetrien\n4. Keine Konkurskosten\n5. Anleger und Unternehmen können zu gleichen Konditionen FK aufnehmen",
             card_type="listing", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Annahmen"]),
        card(chapter=ch, section="MM II", question="Formuliere das Modigliani-Miller-Theorem II (ohne Steuern).",
             answer="Die erwartete EK-Rendite steigt linear mit dem Verschuldungsgrad:\nr_E = r_U + (D/E) · (r_U - r_D)\n\nMit zunehmender Verschuldung steigt das Risiko des EK → Aktionäre fordern höhere Rendite.",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["MM II"],
             formula="r_E = r_U + (D/E) · (r_U - r_D)",
             variables={"r_E": "EK-Rendite", "r_U": "Rendite unverschuldet", "r_D": "FK-Zins", "D/E": "Verschuldungsgrad"}),
        card(chapter=ch, section="MM II", question="Warum steigt nach MM II die EK-Rendite mit dem Verschuldungsgrad, obwohl der Gesamtwert gleich bleibt?",
             answer="Mit höherem D trägt das EK mehr finanzielles Risiko (on top of Business Risk). Aktionäre fordern daher höhere Risikoprämie.\nDas billigere FK wird exakt durch teureres EK kompensiert → WACC = r_U = konstant.\nKonsistent mit MM I: kein Vorteil der Kapitalstrukturoptimierung.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["MM II", "WACC"]),
        card(chapter=ch, section="WACC", question="Was ist der WACC und wie berechnet er sich ohne Steuern?",
             answer="WACC = gewichtete durchschnittliche Kapitalkosten:\nWACC = (E/(E+D))·r_E + (D/(E+D))·r_D\n\nOhne Steuern gilt nach MM: WACC = r_U = konstant (unabhängig von D/E).",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["WACC"],
             formula="WACC = (E/(E+D))·r_E + (D/(E+D))·r_D"),
        card(chapter=ch, section="WACC", question="Wie ändert sich der WACC, wenn das Unternehmen mehr FK aufnimmt (ohne Steuern)?",
             answer="WACC bleibt konstant (= r_U).\nZwar sinkt der Anteil des teuren EK und steigt der des günstigeren FK, aber durch MM II steigt gleichzeitig r_E genau so, dass der WACC unverändert bleibt.\nUnter MM-Annahmen gibt es keine 'günstigere' Kapitalstruktur.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["WACC"]),
        card(chapter=ch, section="Beta und Leverage", question="Wie hängen Equity-Beta und Asset-Beta mit dem Verschuldungsgrad zusammen?",
             answer="β_E = β_A · (1 + D/E)  (bei risikolosem FK)\n\nDas Equity-Beta steigt linear mit dem Verschuldungsgrad, weil das EK das gesamte systematische Risiko der Aktiva trägt plus das finanzielle Risiko.",
             card_type="formula", difficulty=4, importance=0.95, exam_relevance=0.95, tags=t+["Beta", "Leverage"],
             formula="β_E = β_A · (1 + D/E)"),
        card(chapter=ch, section="Gewinn pro Aktie", question="Wie beeinflusst Leverage den Gewinn pro Aktie (EPS)?",
             answer="Leverage verstärkt die EPS-Schwankungen:\n• Gutes Ergebnis: EPS steigt stärker (weniger Aktien, Zinsen festgelegt)\n• Schlechtes Ergebnis: EPS sinkt stärker (evtl. negativ)\nEPS = (EBIT - r_D·D) / n_Aktien",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["EPS", "Leverage"],
             formula="EPS = (EBIT - r_D·D) / n"),
        card(chapter=ch, section="Gehebelte Rekapitalisierung", question="Was ist eine gehebelte Rekapitalisierung?",
             answer="Das Unternehmen gibt neues FK aus und kauft damit eigene Aktien zurück oder zahlt Sonderdividende. EK schrumpft, FK wächst → höherer Verschuldungsgrad.\nNach MM I (ohne Steuern): Gesamtwert bleibt gleich, EK-Wert pro Aktie bleibt gleich.",
             card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["Rekapitalisierung"]),
        card(chapter=ch, section="Trugschlüsse", question="Was ist der 'EPS-Trugschluss' bei der Kapitalstruktur?",
             answer="Trugschluss: Mehr FK erhöht EPS → FK ist besser.\nWiderlegung: Höherer EPS geht mit höherem Risiko einher → KGV sinkt. Aktienkurs bleibt nach MM konstant.",
             card_type="understanding", difficulty=4, importance=0.9, exam_relevance=0.9, tags=t+["Trugschlüsse", "EPS"]),
        card(chapter=ch, section="Trugschlüsse", question="Ist Fremdkapital wirklich 'billiger' als Eigenkapital? Was sagt MM?",
             answer="Trugschluss: FK hat niedrigeren Zinssatz → FK senkt Kapitalkosten.\nMM-Antwort: Nein. Mit mehr FK steigt r_E (MM II) genau so, dass WACC = r_U = konstant bleibt. FK ist günstiger in Zinssatz, aber ändert das Risiko des EK.",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Trugschlüsse", "WACC"]),
        card(chapter=ch, section="Rechenbeispiel", question="Beispiel: Unverschuldetes Unternehmen, EBIT=200 (konstant), r_U=10%, 1000 Aktien. Firmenwert und EK-Rendite?",
             answer="V_U = EBIT/r_U = 200/0,10 = 2.000\nAktienkurs = 2.000/1.000 = 2,00\nr_E = r_U = 10%\nEPS = 200/1.000 = 0,20",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Rechenbeispiel"],
             solution_steps=["V_U = 200/0,10 = 2.000", "Kurs = 2.000/1.000 = 2,00", "r_E = 10%"]),
        card(chapter=ch, section="Rechenbeispiel", question="Rekapitalisierung: Das Unternehmen nimmt D=800 FK zu r_D=5% auf und kauft Aktien zurück. Restaktien? r_E?",
             answer="V_L = V_U = 2.000 (MM I)\nE = 2.000-800 = 1.200\nKurs = 2,00 (unverändert)\nAktien = 1.200/2,00 = 600\nr_E = 10% + (800/1.200)·(10%-5%) = 10% + 3,33% = 13,33%",
             card_type="calculation", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Rekapitalisierung"],
             solution_steps=["V_L = 2.000 (MM I)", "E = 1.200", "Aktien = 600", "r_E = 13,33%"]),
        card(chapter=ch, section="Rechenbeispiel", question="Verifiziere: D=800, r_D=5%, r_E=13,33%, E=1200 → WACC = r_U = 10%?",
             answer="WACC = (1200/2000)·13,33% + (800/2000)·5%\n= 0,6·13,33% + 0,4·5%\n= 8,00% + 2,00%\n= 10% ✓",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["WACC"],
             solution_steps=["0,6·13,33% = 8,00%", "0,4·5% = 2,00%", "WACC = 10% ✓"]),
        card(chapter=ch, section="Aktienemission", question="Was passiert zum Aktienkurs, wenn ein Unternehmen neue Aktien ausgibt (vollkommener Markt)?",
             answer="Keine Verwässerung bei fairer Bewertung: Neue Aktien werden zum fairen Wert ausgegeben, alter Aktienkurs bleibt konstant. Erlös erhöht Firmenwert um genau den Emissionserlös.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.85, tags=t+["Aktienemission", "Verwässerung"]),
        card(chapter=ch, section="Portfolioreplikation", question="Wie repliziert ein Investor per 'Homemade Leverage' das EK einer verschuldeten Firma?",
             answer="Ziel: α-Anteil am EK der verschuldeten Firma\nReplikation:\n1. Kaufe α-Anteil am EK der UNVERSCHULDETEN Firma\n2. Nimm selbst FK α·D auf\nAuszahlung identisch, Kosten: α·(V_U-D) = α·E_L (nach MM)\n→ Kein Arbitragegewinn möglich.",
             card_type="understanding", difficulty=5, importance=0.95, exam_relevance=0.95, tags=t+["Homemade Leverage"]),
        card(chapter=ch, section="Kapitalwert", question="Wie berechnet man den Kapitalwert (NPV) bei vollkommenem Markt?",
             answer="NPV = -I + PV(zukünftige Cashflows)\n= -I + CF_1/(1+r) + CF_2/(1+r)² + ...\n\nNPV ist unabhängig von der Finanzierungsstruktur (MM I).",
             card_type="formula", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["Kapitalwert"],
             formula="NPV = -I + Σ CF_t/(1+r)^t"),
        card(chapter=ch, section="Interpretation", question="Was ist die ökonomische Intuition hinter MM I und II zusammen?",
             answer="MM I: Der 'Kuchen' (Gesamtwert) ändert sich nicht durch seine Aufteilung (EK vs. FK).\nMM II: Wer einen größeren Anteil bekommt (EK bei hohem Leverage), trägt auch mehr Risiko und verlangt mehr Rendite. Die Renditen passen sich an, sodass der Gesamtwert konstant bleibt.",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["MM I", "MM II"]),
        card(chapter=ch, section="Break-even EBIT", question="Was ist der Break-even-EBIT und wie wird er berechnet?",
             answer="Der EBIT, bei dem EPS des verschuldeten und unverschuldeten Unternehmens gleich sind:\n\n(EBIT_BE - 0) / n_U = (EBIT_BE - r_D·D) / n_L\n\nUnterhalb des Break-even: weniger FK besser (höheres EPS). Oberhalb: mehr FK besser (höheres EPS). Nach MM ist EPS-Vergleich aber irreführend (Risikounterschied!).",
             card_type="formula", difficulty=4, importance=0.85, exam_relevance=0.85, tags=t+["Break-even EBIT"]),
    ]


# ===========================================================================
# KAPITEL 4
# ===========================================================================

def cards_chapter4() -> list[dict]:
    ch = "4. Kapitalstruktur mit Marktunvollkommenheiten"
    t = ["Kapitalstruktur", "Marktunvollkommenheiten"]
    return [
        card(chapter=ch, section="4.1 Steuervorteil FK", question="Was ist der fremdfinanzierungsbedingte Steuervorteil und warum entsteht er?",
             answer="Zinszahlungen auf FK sind steuerlich absetzbar, Dividenden auf EK nicht.\nSteuervorteil pro Periode = τ_C · r_D · D\nBei permanenter Verschuldung: PV(Steuervorteil) = τ_C · D",
             card_type="understanding", difficulty=2, importance=1.0, exam_relevance=1.0, tags=t+["Steuervorteil"],
             formula="PV(Steuervorteil) = τ_C · D"),
        card(chapter=ch, section="4.1 Steuervorteil FK", question="Formuliere MM I mit Steuern.",
             answer="V_L = V_U + PV(fremdfinanzierungsbedingter Steuervorteil)\n\nBei dauerhafter risikoloser Verschuldung:\nV_L = V_U + τ_C · D",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["MM I mit Steuern"],
             formula="V_L = V_U + τ_C · D"),
        card(chapter=ch, section="4.1 Steuervorteil FK", question="Wie berechnet sich der WACC mit Körperschaftsteuer?",
             answer="WACC = (E/(E+D))·r_E + (D/(E+D))·r_D·(1-τ_C)\n\nFK-Kosten werden mit (1-τ_C) multipliziert (Zinsen steuerlich absetzbar).\nWACC < r_U → WACC sinkt mit steigendem FK.",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["WACC mit Steuern"],
             formula="WACC = (E/(E+D))·r_E + (D/(E+D))·r_D·(1-τ_C)"),
        card(chapter=ch, section="4.1 Steuervorteil FK", question="Wie hoch ist der Steuervorteil: D=500, r_D=5%, τ_C=30%?",
             answer="Zinsen = 0,05·500 = 25\nSteuervorteil/Periode = 0,30·25 = 7,50\nPV (dauerhafte Verschuldung) = τ_C·D = 0,30·500 = 150",
             card_type="calculation", difficulty=2, importance=0.95, exam_relevance=0.95,
             tags=t+["Steuervorteil", "Rechnung"],
             solution_steps=["Zinsen = 25", "Steuervorteil/Periode = 7,50", "PV = 150"]),
        card(chapter=ch, section="4.1 Rekapitalisierung", question="Was passiert bei einer Rekapitalisierung zur Nutzung des Steuervorteils?",
             answer="Unternehmen nimmt neues FK auf, kauft Aktien zurück.\nV_L steigt um τ_C·ΔD.\nAktienkurs steigt bei Ankündigung (Einpreisung des PV der Steuervorteile).\nAlte Aktionäre profitieren voll.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.95, tags=t+["Rekapitalisierung"]),
        card(chapter=ch, section="4.1 Rekapitalisierung", question="Warum steigt der Aktienkurs bei Ankündigung einer Rekapitalisierung (FK-Aufnahme)?",
             answer="Ankündigung signalisiert zukünftige Steuervorteile. Markt diskontiert sofort PV der Steuervorteile.\nAnkündigungseffekt = τ_C·ΔD / n_Aktien (vor Rückkauf)\nDanach: Rückkauf zum gestiegenen Kurs → alte Aktionäre profitieren voll.",
             card_type="understanding", difficulty=4, importance=0.9, exam_relevance=0.9, tags=t+["Ankündigungseffekt"]),
        card(chapter=ch, section="4.1 Steuern Investorenebene", question="Wie berechnet sich der effektive Steuervorteil von FK bei Berücksichtigung von Investorensteuern?",
             answer="τ* = 1 - (1-τ_C)(1-τ_E)/(1-τ_D)\n\nτ_C = Körperschaftsteuersatz, τ_E = Steuer auf EK-Erträge, τ_D = Steuer auf Zinserträge.\nWenn τ_D > τ_E: τ* < τ_C (Steuervorteil reduziert sich)\nWenn (1-τ_C)(1-τ_E) = (1-τ_D): τ* = 0",
             card_type="formula", difficulty=5, importance=0.85, exam_relevance=0.8, tags=t+["Investorensteuern"],
             formula="τ* = 1 - (1-τ_C)(1-τ_E)/(1-τ_D)"),
        card(chapter=ch, section="4.1 Optimale Kapitalstruktur", question="Welche optimale Kapitalstruktur folgt aus dem reinen Steuermodell?",
             answer="Rein aus dem Steuermodell: 100% FK-Finanzierung optimal, da PV(Steuervorteil) = τ_C·D mit D maximiert.\nIn der Realität: keine 100% FK-Finanzierung → Konkurskosten und Agency-Kosten begrenzen D.",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["optimale Kapitalstruktur"]),
        card(chapter=ch, section="4.2 Konkurskosten", question="Was sind direkte Konkurskosten?",
             answer="Direkte Kosten bei Insolvenz:\n• Anwalts- und Gerichtskosten\n• Verwaltungskosten des Insolvenzverfahrens\n• Beraterhonorare\nTypischerweise 3-5% des Unternehmenswerts.",
             card_type="definition", difficulty=2, importance=0.9, exam_relevance=0.9, tags=t+["Konkurskosten"]),
        card(chapter=ch, section="4.2 Konkurskosten", question="Was sind indirekte Konkurskosten? Warum sind sie größer als direkte?",
             answer="Kosten durch finanzielle Notlage, auch ohne formellen Konkurs:\n• Verlust von Kunden/Lieferanten\n• Verlust wichtiger Mitarbeiter\n• Verpassen profitabler Projekte (Underinvestment)\n• Notverkauf von Assets (Fire Sales)\n• Erhöhte Refinanzierungskosten\nTypischerweise 10-20% des Unternehmenswerts.",
             card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["Konkurskosten", "indirekt"]),
        card(chapter=ch, section="4.2 Trade-Off", question="Formuliere MM I mit Steuern UND Konkurskosten (Trade-Off-Theorie).",
             answer="V_L = V_U + PV(Steuervorteil) - PV(Konkurskosten)\n\nOptimales D* wo Grenzsteuervorteil = Grenz-Konkurskosten.",
             card_type="formula", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["Trade-Off-Theorie"],
             formula="V_L = V_U + τ_C·D - PV(Konkurskosten)"),
        card(chapter=ch, section="4.2 Trade-Off", question="Was sagt die Trade-Off-Theorie über den optimalen Verschuldungsgrad?",
             answer="• Bei D < D*: höheres FK lohnt (Steuervorteil überwiegt)\n• Bei D > D*: weiteres FK schadet (Konkurskosten überwiegen)\n\nProblem: Profitable Firmen haben empirisch oft geringe FK-Quoten → Pecking Order passt besser.",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Trade-Off-Theorie"]),
        card(chapter=ch, section="4.2 Trade-Off", question="Was bestimmt die Höhe der Konkurskosten eines Unternehmens?",
             answer="• Art der Vermögenswerte: immateriell (F&E, Marken) → hohe Kosten; physisch (Immobilien) → gering\n• Branche: technologieintensiv → höhere indirekte Kosten\n• Kundenbindung: Langfristbeziehungen → hohe Verluste bei Konkurs",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.85, tags=t+["Konkurskosten"]),
        card(chapter=ch, section="4.2 Agency-Theorie", question="Was versteht man unter Agency-Kosten des Fremdkapitals?",
             answer="Kosten durch Interessenkonflikte zwischen EK- und FK-Gebern:\n1. Übermäßige Risikobereitschaft (Asset Substitution)\n2. Underinvestment (Debt Overhang)\n3. Cashing Out (Dividendenentnahme vor Konkurs)\n4. Gambles bei drohender Insolvenz",
             card_type="listing", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["Agency-Kosten"]),
        card(chapter=ch, section="4.2 Asset Substitution", question="Was ist das Asset-Substitution-Problem?",
             answer="Bei hoher Verschuldung: EK-Geber gewinnen stark bei riskanten Projekten (upside), FK-Geber tragen den Verlust (downside).\n→ EK-Geber wählen riskantere Projekte als sozial optimal (evtl. NPV < 0).\nLösung: Covenants verbieten riskante Investments.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Asset Substitution"]),
        card(chapter=ch, section="4.2 Asset Substitution", question="Warum ist Asset Substitution ein Problem für FK-Geber?",
             answer="FK-Geber haben beschränkten Upside (feste Zinsen), aber vollen Downside-Verlust bei Ausfall.\nRisikoerhöhung durch EK-Geber verschiebt Wert von FK zu EK – auf Kosten der FK-Geber.\nFK-Geber antizipieren dies → verlangen ex ante höhere Zinsen → ex-ante Unternehmenswert sinkt.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.95, tags=t+["Asset Substitution"]),
        card(chapter=ch, section="4.2 Underinvestment", question="Was ist das Underinvestment-Problem (Debt Overhang)?",
             answer="Bei sehr hoher Verschuldung (Firma nahe Insolvenz): Neue profitable Projekte (NPV>0) kommen hauptsächlich FK-Gebern zugute, nicht EK-Gebern. EK-Geber verzichten, weil sie Kosten tragen, aber Gewinn nicht erhalten.\nFolge: Wertvernichtende Unterinvestition.\nLösung: FK-Restrukturierung (Schulden reduzieren).",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Underinvestment", "Debt Overhang"]),
        card(chapter=ch, section="4.2 Cashing Out", question="Was ist 'Cashing Out' als Agency-Problem?",
             answer="Vor absehbarer Insolvenz zahlen EK-Geber sich selbst Dividenden aus oder verkaufen Unternehmensvermögen, was FK-Gebern schadet.\nVerfügbares Vermögen zur Schuldendeckung sinkt.\nLösung: Covenants, die Dividendenzahlungen beschränken.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.85, tags=t+["Cashing Out"]),
        card(chapter=ch, section="4.2 Covenants", question="Was sind Covenants und wie lösen sie Agency-Probleme?",
             answer="Vertragsklauseln in Kreditverträgen:\n• Positive Covenants: Schuldner muss Kennzahlen einhalten (Mindest-EK-Quote)\n• Negative Covenants: Keine riskanten Akquisitionen, keine übermäßigen Dividenden\n\nLösen Asset Substitution und Cashing Out, erzeugen aber Monitoring-Kosten.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.85, tags=t+["Covenants"]),
        card(chapter=ch, section="4.2 Asymm. Information", question="Was ist das Problem der adversen Selektion bei Aktienemissionen (Lemon Problem)?",
             answer="Manager wissen mehr als Investoren.\nAktienemission = Signal: Aktien überbewertet (Manager emittieren bei hohem Kurs).\nInvestoren antizipieren → Kurs fällt bei Ankündigung.\nUnterbewertet Firmen: Emission zu teuer → verzichten auf gute Projekte.\n\nNach Myers & Majluf (1984): Announcement-Effekt der Aktienemission ist negativ (~-3%).",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.9, tags=t+["Adverse Selektion", "Lemon"]),
        card(chapter=ch, section="4.2 Pecking Order", question="Was ist die Pecking-Order-Theorie der Kapitalstruktur?",
             answer="Myers & Majluf (1984): Firmen bevorzugen Finanzierungsquellen in Reihenfolge:\n1. Interne Mittel (einbehaltene Gewinne) – keine Informationsasymmetrie\n2. Fremdkapital – geringe Informationsasymmetrie\n3. Eigenkapital – nur als letzte Option (negativer Announcement-Effekt)\n\nKein Ziel-Verschuldungsgrad, sondern Finanzierungshierarchie.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.9, tags=t+["Pecking Order"]),
        card(chapter=ch, section="4.2 Signaling", question="Was ist die Signaling-Theorie der Kapitalstruktur (Ross 1977)?",
             answer="Manager können über Kapitalstruktur private Information signalisieren:\n• Hohe Verschuldung = Signal für Qualität (nur starke Firmen leisten hohe Zinszahlungen)\n• FK-Aufnahme → positiver Kurseffekt\nGlaubwürdiges Signal, weil schwache Firmen bei hohem D Konkurs riskieren.",
             card_type="understanding", difficulty=4, importance=0.85, exam_relevance=0.8, tags=t+["Signaling"]),
        card(chapter=ch, section="4.2 Announcement-Effekte", question="Welche Ankündigungseffekte auf den Aktienkurs erwartet die Theorie bei EK vs. FK Emission?",
             answer="Aktienemission: Negativ (~-3%). Signal: Aktien überbewertet.\nFK-Emission: Leicht positiv oder neutral. Signal: Qualität oder Steuervorteil.\nAktienrückkauf: Positiv. Signal: Aktien unterbewertet.",
             card_type="contrast", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Announcement-Effekte"]),
        card(chapter=ch, section="Vergleich Theorien", question="Vergleiche Trade-Off-Theorie vs. Pecking-Order-Theorie für profitable Firmen.",
             answer="Trade-Off: Profitable Firmen → hohes Einkommen → großer Steuervorteil → höheres optimales D.\n\nPecking Order: Profitable Firmen → viele interne Mittel → nutzen diese zuerst → geringeres D.\n\nEmpirie: Profitable Firmen haben typischerweise geringe FK-Quoten → Pecking Order passt besser.",
             card_type="contrast", difficulty=4, importance=0.9, exam_relevance=0.85, tags=t+["Trade-Off", "Pecking Order"]),
        card(chapter=ch, section="Rechenbeispiel Steuern", question="Beispiel: V_U=100, τ_C=30%, D=40 (dauerhaft). V_L?",
             answer="V_L = V_U + τ_C·D = 100 + 0,30·40 = 100 + 12 = 112\nEK = V_L - D = 112 - 40 = 72",
             card_type="calculation", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["Rechnung"],
             solution_steps=["V_L = 100 + 12 = 112", "EK = 72"]),
        card(chapter=ch, section="Rechenbeispiel Konkurs", question="Beispiel: V_U=100, τ_C=25%, D=60, PV(Konkurskosten)=8. V_L?",
             answer="V_L = V_U + τ_C·D - PV(Konkurskosten)\n= 100 + 0,25·60 - 8\n= 100 + 15 - 8 = 107",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Konkurskosten", "Rechnung"],
             solution_steps=["PV(Steuervorteil) = 15", "V_L = 100 + 15 - 8 = 107"]),
        card(chapter=ch, section="WACC Rechenbeispiel", question="Berechne WACC: E=1200, D=800, r_E=14%, r_D=5%, τ_C=30%.",
             answer="WACC = (1200/2000)·14% + (800/2000)·5%·0,70\n= 0,60·14% + 0,40·3,50%\n= 8,40% + 1,40%\n= 9,80%",
             card_type="calculation", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["WACC"],
             solution_steps=["FK-Kosten n.St. = 5%·0,70 = 3,50%", "WACC = 8,40% + 1,40% = 9,80%"]),
        card(chapter=ch, section="Finanzielle Notlage", question="Was ist 'finanzielle Notlage' und wann tritt sie auf?",
             answer="Situation, in der ein Unternehmen Schwierigkeiten hat, Verbindlichkeiten zu erfüllen, ohne notwendigerweise insolvent zu sein.\nTritt auf, wenn EBIT < Zinsen.\nIndirekte Kosten entstehen bereits vor formalem Konkurs.",
             card_type="definition", difficulty=2, importance=0.9, exam_relevance=0.9, tags=t+["finanzielle Notlage"]),
        card(chapter=ch, section="Sanierung vs. Liquidation", question="Was ist der Unterschied zwischen Sanierung und Liquidation im Insolvenzverfahren?",
             answer="Sanierung: Weiterführung unter Insolvenzschutz (Chapter 11 USA). Schulden restrukturieren.\nLiquidation: Zerschlagung, Erlös nach Gläubigerrangfolge verteilt.\n\nSanierung optimal wenn Fortführungswert > Liquidationswert.",
             card_type="contrast", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Insolvenz"]),
        card(chapter=ch, section="MM II mit Steuern", question="Wie lautet MM II mit Steuern (EK-Rendite des verschuldeten Unternehmens)?",
             answer="r_E = r_U + (D/E)·(r_U - r_D)·(1-τ_C)\n\nMit Steuern ist der Leverage-Effekt etwas geringer, weil FK durch Steuerersparnis günstiger ist.",
             card_type="formula", difficulty=4, importance=0.9, exam_relevance=0.9, tags=t+["MM II mit Steuern"],
             formula="r_E = r_U + (D/E)·(r_U - r_D)·(1-τ_C)"),
        card(chapter=ch, section="Optimale Kapitalstruktur", question="Welche Faktoren bestimmen laut Trade-Off-Theorie den optimalen Verschuldungsgrad?",
             answer="FK-fördernd (höheres D*):\n• Hohe Profitabilität, Tangible Assets, stabile Cashflows\n\nFK-hemmend (geringeres D*):\n• Wachstumsunternehmen, intangible Assets, volatile Cashflows, hohe Branchenkonkurskosten",
             card_type="listing", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Trade-Off"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Da FK günstiger ist als EK, sollten Unternehmen möglichst viel FK aufnehmen.'",
             answer="Falsch. Nach MM II (ohne Steuern) kompensiert steigendes r_E den FK-Kostenvorteil vollständig → WACC konstant. Mit Steuern gibt es Steuervorteil, aber Konkurskosten und Agency-Kosten begrenzen D*.",
             card_type="trueFalse", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Wahr/Falsch"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Die Emission neuer Aktien erhöht den Wert je Aktie für bestehende Aktionäre.'",
             answer="Falsch. Bei fairer Preisgestaltung ist die Emission wertneutral. Nur wenn Aktien unter fairem Wert emittiert werden, sinkt der Kurs. Asymmetrische Information kann zu negativen Ankündigungseffekten führen.",
             card_type="trueFalse", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["Verwässerung", "Wahr/Falsch"]),
        card(chapter=ch, section="Kapitalstruktur & Branche", question="Warum unterscheiden sich Kapitalstrukturen stark zwischen Branchen?",
             answer="Pharmaunternehmen: Wenig FK (F&E-Risiken, intangible Assets)\nAirlines: Viel FK (Flugzeuge als Sicherheiten)\nFinanzinstitute: Sehr viel FK (Einlagen = FK)\nTechnikfirmen: Wenig FK (Wachstum, intangible)\n\nHauptdeterminanten: Vermögensstruktur, Cashflow-Stabilität, Konkurskosten.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Branche"]),
    ]


# ===========================================================================
# KAPITEL 5
# ===========================================================================

def cards_chapter5() -> list[dict]:
    ch = "5. Funktionen von Banken"
    t = ["Banken", "Diamond-Dybvig"]
    return [
        card(chapter=ch, section="Bankfunktionen", question="Was sind die wesentlichen wirtschaftlichen Funktionen von Banken?",
             answer="1. Liquiditätsversicherung (Diamond-Dybvig 1983)\n2. Delegierte Überwachung (Diamond 1984)\n3. Fristentransformation\n4. Zahlungsverkehr\n5. Risikodiversifikation",
             card_type="listing", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["Bankfunktionen"]),
        card(chapter=ch, section="Diamond-Dybvig Modell", question="Beschreibe die Grundstruktur des Diamond-Dybvig-Modells (1983).",
             answer="3 Perioden: t=0, 1, 2\nn Konsumenten, je 1 Einheit Endowment.\nInvestition: langfristig (R>1 in t=2) oder Liquidation (=1 in t=1).\nKonsumenten unsicher über eigenen Typ:\n• Typ 1 (Anteil π): braucht Konsum in t=1 (impatient)\n• Typ 2 (Anteil 1-π): kann bis t=2 warten (patient)\nTyp ist private Information.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Modell"]),
        card(chapter=ch, section="Diamond-Dybvig Autarkie", question="Was passiert ohne Finanzintermediation (Autarkie) im Diamond-Dybvig-Modell?",
             answer="Jeder investiert selbst:\n• Typ 1: liquidiert in t=1 → erhält 1\n• Typ 2: hält bis t=2 → erhält R\n\nProblem: Typ-1 hat keine Liquiditätsversicherung → ineffizient.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Autarkie"]),
        card(chapter=ch, section="Diamond-Dybvig First Best", question="Was ist die 'First-best'-Lösung im Diamond-Dybvig-Modell?",
             answer="Sozialer Planer mit vollständiger Information:\nC1* > 1 (Typ 1 mehr als Liquidationswert)\nC2* < R (Typ 2 weniger als vollen Ertrag)\nOptimale Bedingung: u'(C1*) = ρ·R·u'(C2*)\n\nBedingung für Anreizkompatibilität: C2* ≥ C1*.",
             card_type="understanding", difficulty=5, importance=1.0, exam_relevance=1.0, tags=t+["First Best"],
             formula="u'(C1*) = ρ·R·u'(C2*)"),
        card(chapter=ch, section="Diamond-Dybvig Bank", question="Wie implementiert eine Bank die First-best-Allokation im Diamond-Dybvig-Modell?",
             answer="Bank bietet Sichteinlagen-Vertrag:\n• Rückzahlung C1* in t=1\n• Rückzahlung C2* = R(1-π·C1*)/(1-π) in t=2\n\nBank hält Reserve π·C1* liquide, investiert Rest langfristig.\nDurch Gesetz der großen Zahlen: genau π·n heben in t=1 ab → Reserven exakt richtig.",
             card_type="understanding", difficulty=5, importance=1.0, exam_relevance=1.0, tags=t+["Bank", "Sichteinlagen"]),
        card(chapter=ch, section="Bank Run", question="Wie entsteht ein Bank Run im Diamond-Dybvig-Modell?",
             answer="Neben dem guten Gleichgewicht existiert ein schlechtes:\nWenn Typ-2 glaubt, andere rennen:\n→ Er zieht in t=1 ab (um nicht leer auszugehen)\n→ Bank muss Langfrist-Investments liquidieren\n→ Wenn alle rennen: Bank bricht zusammen\n\nBank Run = selbsterfüllende Prophezeiung / Koordinationsversagen.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Bank Run"]),
        card(chapter=ch, section="Bank Run Gleichgewichte", question="Welche zwei Nash-Gleichgewichte existieren im Diamond-Dybvig-Modell?",
             answer="1. Gutes Gleichgewicht ('No Run'): Nur Typ-1 hebt ab. Bank zahlt C1* und C2*.\n\n2. Schlechtes Gleichgewicht ('Run'): Alle heben ab. Bank ist bankrott. Typ-2 verliert.\n\nWelches eintritt ist unbestimmt (Sunspot-Gleichgewichte). Panik ist self-fulfilling.",
             card_type="understanding", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Nash-Gleichgewicht"]),
        card(chapter=ch, section="Gesetz der großen Zahlen", question="Welche Rolle spielt das Gesetz der großen Zahlen für die Bankenfunktion?",
             answer="Mit vielen Einlegern (n → ∞): Anteil der Typ-1-Konsumenten konvergiert zu π.\nStandardabweichung ≈ 0\n\nBank kann sicher π als Reserve halten, ohne zu viel oder zu wenig liquide Mittel. Diversifikation des individuellen Liquiditätsrisikos.",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Gesetz der großen Zahlen"]),
        card(chapter=ch, section="Delegierte Überwachung", question="Was versteht man unter 'delegierter Überwachung' (Diamond 1984)?",
             answer="Direkte Finanzierung: Jeder Anleger überwacht selbst → hohe Kosten n·c.\nBank als Intermediär: Einleger delegieren Überwachung.\n• Skalenvorteil: Bank überwacht einmal für alle\n• Bank hat Anreiz (haftet mit EK)\n• Gesamtkosten-Ersparnis rechtfertigt Bankenexistenz.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.9, tags=t+["Delegierte Überwachung"]),
        card(chapter=ch, section="Delegierte Überwachung", question="Warum ist delegierte Überwachung durch eine Bank kosteneffizienter?",
             answer="Direkte Überwachung: n Anleger × Kosten c = n·c.\nBank: überwacht einmal → Kosten = c (durch Diversifikation über viele Kredite).\nBank kann Einleger fast sicher zurückzahlen → Strafandrohung wirkt → zuverlässiges Monitoring.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.9, tags=t+["Delegierte Überwachung"]),
        card(chapter=ch, section="Delegierte Überwachung", question="Was ist die Strafe im Diamond-Modell der delegierten Überwachung und warum ist sie wichtig?",
             answer="Die Strafe ist die Konsequenz für die Bank bei Nichterfüllung der versprochenen Rückzahlung an Einleger. Hoch genug, damit Bank Anreiz hat zu überwachen (Moral Hazard der Bank gelöst).\nOhne Strafe: kein Anreiz zu überwachen.",
             card_type="understanding", difficulty=5, importance=0.85, exam_relevance=0.8, tags=t+["Strafe", "Moral Hazard"]),
        card(chapter=ch, section="Banktypen", question="Was ist der Unterschied zwischen Universal- und Investmentbank?",
             answer="Universalbank: Einlagen-/Kreditgeschäft + Investmentbanking.\nInvestmentbank: Fokus auf Kapitalmarktgeschäfte (Emission, M&A, Handel), kein Einlagengeschäft.\nTrennbankensystem (Glass-Steagall 1933-1999): gesetzliche Trennung.",
             card_type="contrast", difficulty=2, importance=0.7, exam_relevance=0.65, tags=t+["Universalbank"]),
        card(chapter=ch, section="Fristentransformation", question="Was ist Fristentransformation und warum ist sie für Banken charakteristisch?",
             answer="Kurzfristige Einlagen → langfristige Kredite.\nProfitabel: Langfristige Zinsen > kurzfristige (normale Zinsstrukturkurve).\nRisiko: Bei Run → Liquiditätsproblem (Aktiva illiquide, Passiva fällig).\nExakte Darstellung im Diamond-Dybvig-Modell.",
             card_type="understanding", difficulty=2, importance=0.9, exam_relevance=0.85, tags=t+["Fristentransformation"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Im Diamond-Dybvig-Modell ist ein Bank Run immer ineffizient.'",
             answer="Falsch. Im Grundmodell ist der Run ineffizient (Koordinationsproblem). Es gibt aber 'Efficient Bank Runs' (Erweiterungen), in denen Runs informationsbasiert sind (schlechte Bankqualität bekannt) und dann effizient sind – sie erzwingen Liquidation einer tatsächlich schlechten Bank.",
             card_type="trueFalse", difficulty=4, importance=0.9, exam_relevance=0.85, tags=t+["Bank Run", "Wahr/Falsch"]),
        card(chapter=ch, section="Finanzmarkt vs. Bank", question="Wann ist direkte Marktfinanzierung vorteilhafter als Bankfinanzierung?",
             answer="Direkte Marktfinanzierung besser bei:\n• Großen, bekannten Unternehmen (öffentliche Information)\n• Standardisierten Kreditnehmern\n• Wenn Anleger Liquidität brauchen (handelbare Papiere)\n\nBankfinanzierung besser bei:\n• KMUs, Wachstumsunternehmen (enge Beziehung)\n• Beziehungskredite (Relationship Banking)",
             card_type="contrast", difficulty=3, importance=0.8, exam_relevance=0.75, tags=t+["Marktfinanzierung"]),
    ]


# ===========================================================================
# KAPITEL 6
# ===========================================================================

def cards_chapter6() -> list[dict]:
    ch = "6. Finanzkrisen und systemische Risiken"
    t = ["Finanzkrisen", "Systemisches Risiko"]
    return [
        card(chapter=ch, section="Grundproblem", question="Was ist das 'Grundproblem' im Diamond-Dybvig-Bankenmodell für Finanzstabilität?",
             answer="Banken produzieren Liquidität durch Fristentransformation (wertvolle Funktion), aber: Multiple Gleichgewichte (Run / No-Run). Das schlechte Gleichgewicht ist selbsterfüllend und exogen (Sunspot). Kein Fundamentalgrund für den Run nötig.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.85, tags=t+["Grundproblem"]),
        card(chapter=ch, section="Narrow Banking", question="Was ist 'Narrow Banking' als Lösung für Bank Runs?",
             answer="Einlagen zu 100% durch sichere, liquide Assets gedeckt (Staatsanleihen). Keine Fristentransformation.\n\nVorteil: Kein Run möglich.\nNachteil: Liquiditätsversicherungsfunktion geht verloren. Kreditvergabe muss durch teures EK finanziert werden.",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.8, tags=t+["Narrow Banking"]),
        card(chapter=ch, section="Aufhebung der Konvertibilität", question="Was ist 'Aufhebung der Konvertibilität' als Lösung für Bank Runs?",
             answer="Bank setzt vorübergehend aus, Einlagen in Bargeld zu tauschen (Suspension of Convertibility).\n\nVorteil: Bricht Runlogik, Typ-2 hat Anreiz zu warten.\nNachteil: Echte Typ-1-Konsumenten kommen nicht an Geld → politisch schwer durchsetzbar.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.75, tags=t+["Konvertibilität"]),
        card(chapter=ch, section="Einlagenversicherung", question="Wie löst eine Einlagenversicherung das Bank-Run-Problem?",
             answer="Staat garantiert Einlagen bis zu Betrag (EU: 100.000 €).\n\nMechanismus: Typ-2 hat keinen Anreiz zu rennen (bekommt Geld auf jeden Fall) → nur Typ-1 hebt ab → gutes Gleichgewicht eindeutig.\n\nProblem: Moral Hazard – Banken nehmen mehr Risiko (Verluste trägt Einlagensicherungsfonds).",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Einlagenversicherung"]),
        card(chapter=ch, section="Einlagenversicherung Moral Hazard", question="Welches Moral-Hazard-Problem erzeugt die Einlagenversicherung für Banken?",
             answer="Mit Einlagenversicherung:\n• Einleger meiden risikoreiche Banken nicht (kein Marktdisziplin)\n• Banken können riskant anlegen, Gewinne privatisieren, Verluste sozialisieren\n• 'Gambling for Resurrection': Fast-insolvente Banken setzen alles auf eine Karte\n\nLösung: Risikobasierte Prämien + strenge EK-Regulierung.",
             card_type="understanding", difficulty=4, importance=0.95, exam_relevance=0.9, tags=t+["Moral Hazard"]),
        card(chapter=ch, section="Effiziente Bank Runs", question="Was sind 'effiziente Bank Runs'?",
             answer="Jacklin & Bhattacharya (1988): Wenn Bankaktiva-Qualität öffentlich bekannt, können Runs rational und effizient sein.\n• Schlechte Aktiva → Run erzwingt Liquidation einer schlechten Bank (ex post effizient)\n\nUnterschied zu DD: Basiert auf Fundamentaldaten, nicht Koordinationsversagen.\nNicht alle Bank Runs sind pathologisch.",
             card_type="understanding", difficulty=4, importance=0.8, exam_relevance=0.75, tags=t+["Effiziente Runs"]),
        card(chapter=ch, section="Systemisches Risiko", question="Was ist systemisches Risiko?",
             answer="Gefahr, dass der Ausfall eines oder mehrerer Finanzinstitute eine Kettenreaktion auslöst, die das gesamte Finanzsystem destabilisiert.\n\nKanäle:\n1. Interbanken-Verbindlichkeiten (direkte Ansteckung)\n2. Makroökonomische Rückkopplungen (Asset-Preisspirale)\n3. Informationsansteckung",
             card_type="definition", difficulty=3, importance=0.95, exam_relevance=0.85, tags=t+["Systemisches Risiko"]),
        card(chapter=ch, section="Ansteckungseffekte", question="Erkläre Ansteckungseffekte über Interbankenverbindlichkeiten.",
             answer="Banken leihen sich gegenseitig Geld. Bei Ausfall von Bank A:\n• Bank B hat Forderung gegen A → Verlust\n• Bank B könnte selbst in Schieflage geraten\n• Domino-Effekt auf Bank C usw.\n\nVernetzungsgrad bestimmt Ansteckungsrisiko.",
             card_type="understanding", difficulty=4, importance=0.9, exam_relevance=0.8, tags=t+["Ansteckung", "Interbanken"]),
        card(chapter=ch, section="Ansteckungseffekte", question="Was sind makroökonomische Rückkopplungen als Ansteckungskanal?",
             answer="Banken in Schieflage → Kreditklemme → Investitionen sinken → Konjunktur schwächt → Ausfälle steigen → Bankenverluste.\n\nZusätzlich: Fire-Sale-Spirale: Banken verkaufen Assets → Preise fallen → andere Banken erleiden Verluste → weitere Verkäufe.",
             card_type="understanding", difficulty=4, importance=0.85, exam_relevance=0.75, tags=t+["Makro-Rückkopplungen", "Fire Sale"]),
        card(chapter=ch, section="Lender of Last Resort", question="Was ist ein 'Lender of Last Resort' und Bagehots Prinzip?",
             answer="LoLR: Zentralbank als letzte Kreditinstanz für illiquide, aber solvente Banken.\n\nBagehots Prinzip (1873):\n1. Nur illiquide (aber solvente) Banken\n2. Zu Strafzinssätzen (über Marktrate)\n3. Gegen gute Sicherheiten\n\nProblem: Unterscheidung illiquide vs. insolvent in Krisenzeiten sehr schwierig.",
             card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.8, tags=t+["Lender of Last Resort"]),
        card(chapter=ch, section="Lender of Last Resort", question="Welches Moral-Hazard-Problem erzeugt ein Lender of Last Resort?",
             answer="Banken wissen, dass sie im Notfall gerettet werden → nehmen mehr Risiko.\n'Too Big to Fail': Große Banken wissen, dass sie immer gerettet werden → extreme Risikobereitschaft.\n\nLösung: Strafzinsen (Bagehot), strenge Regulierung, Bail-in.",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.8, tags=t+["Moral Hazard", "LoLR"]),
        card(chapter=ch, section="Too Big to Fail", question="Was ist das 'Too-Big-to-Fail'-Problem?",
             answer="Systemrelevante Banken (SIFIs) sind so groß/verflochten, dass ihr Ausfall das Finanzsystem gefährdet.\n→ Staat muss retten → Banken haben implizite Staatsgarantie → günstigere Refinanzierung + Anreiz zu Risikoübernahme.\n\nLösung: Höhere EK-Anforderungen für SIFIs, Bail-in (TLAC/MREL), Abwicklungsplanung.",
             card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Too Big to Fail", "SIFI"]),
        card(chapter=ch, section="Too Big to Fail", question="Warum ist das Zeitinkonsistenzproblem zentral für Too-Big-to-Fail?",
             answer="Ex ante: Staat kündigt an 'Wir retten keine Banken' → verhindert Moral Hazard.\nEx post: Kosten des Nichtrettens (systemische Krise) so hoch, dass Rettung optimal ist.\n\n→ Drohung 'nicht zu retten' ist zeitinkonsistent → Markt erwartet Rettung → Anreizproblem.",
             card_type="understanding", difficulty=4, importance=0.85, exam_relevance=0.8, tags=t+["Zeitinkonsistenz"]),
        card(chapter=ch, section="Netzwerkstruktur", question="Welche Netzwerkstruktur des Interbankensystems ist stabiler: vollständig vernetzt oder Stern?",
             answer="Allen & Gale (2000):\n• Vollständig vernetzt: Verluste werden auf viele Banken verteilt → robust gegen kleine Schocks, aber bei großen Schocks unvermeidliche Ansteckung.\n• Stern-Netz: Weniger Kanäle, aber wenn Zentrum ausfällt → katastrophal.\n\nAllgemein: Vernetzung stabilisiert bei kleinen, destabilisiert bei großen Schocks.",
             card_type="understanding", difficulty=5, importance=0.8, exam_relevance=0.7, tags=t+["Netzwerk", "Allen Gale"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Eine Einlagenversicherung löst das Bank-Run-Problem vollständig ohne Nebenwirkungen.'",
             answer="Falsch. Einlagenversicherung verhindert Runs effektiv, erzeugt aber Moral Hazard: Banken übernehmen mehr Risiko, da Einleger nicht mehr disziplinieren. Daher immer mit starker Regulierung zu kombinieren.",
             card_type="trueFalse", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Wahr/Falsch"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Narrow Banking würde Banken sicherer machen, ohne Kosten zu verursachen.'",
             answer="Falsch. Narrow Banking verhindert Runs, eliminiert aber die Liquiditätsversicherungsfunktion. Die gesellschaftlichen Wohlfahrtsgewinne aus der Liquiditätsbereitstellung (Diamond-Dybvig) gingen verloren.",
             card_type="trueFalse", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Narrow Banking", "Wahr/Falsch"]),
    ]


# ===========================================================================
# KAPITEL 7
# ===========================================================================

def cards_chapter7() -> list[dict]:
    ch = "7. Bankenregulierung"
    t = ["Regulierung", "Basel"]
    return [
        card(chapter=ch, section="Gründe", question="Warum werden Banken reguliert? Nenne 3 Hauptgründe.",
             answer="1. Einlagenversicherung erzeugt Moral Hazard → Regulierung nötig\n2. Negative Externalitäten: Bankausfall schadet dem System (systemisches Risiko)\n3. Informationsasymmetrien: Einleger können Bankqualität nicht beurteilen",
             card_type="listing", difficulty=2, importance=0.9, exam_relevance=0.85, tags=t+["Gründe"]),
        card(chapter=ch, section="Eigenkapitalregulierung", question="Was ist die Eigenkapitalquote einer Bank und warum ist sie reguliert?",
             answer="EK-Quote = Eigenkapital / Risikogewichtete Aktiva (RWA)\n\nMindestquoten Basel III: 4,5% CET1, 6% Tier-1, 8% Gesamtkapital.\n\nHöheres EK = größerer Verlustpuffer → geringeres Konkurs- und systemisches Risiko.",
             card_type="understanding", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["EK-Quote", "Basel"]),
        card(chapter=ch, section="RWA", question="Was sind risikogewichtete Aktiva (RWA) und wie funktioniert das Prinzip?",
             answer="RWA = Σ (Aktiva_i × Risikogewicht_i)\n\nRisikogewichte nach Aktivaklasse:\n• Staatsanleihen (Basel I): 0%\n• Hypotheken: 35-50%\n• Unternehmenskredite: 100%\n• Aktien: 100-300%\n\nProblem: Standardisierte Gewichte können tatsächliche Risiken verzerren.",
             card_type="understanding", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["RWA"]),
        card(chapter=ch, section="Basel I", question="Was waren die wesentlichen Merkmale von Basel I (1988)?",
             answer="• Erste internationale EK-Vereinbarung (Basler Ausschuss)\n• Mindest-EK-Quote: 8% der RWA\n• Nur 4 grobe Risikogewichtsklassen (0%, 20%, 50%, 100%)\n• Nur Kreditrisiko berücksichtigt\n\nProbleme: Zu grob, Regulierungsarbitrage, kein Markt-/operationelles Risiko.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Basel I"]),
        card(chapter=ch, section="Basel II", question="Welche Neuerungen brachte Basel II (2004)?",
             answer="3 Säulen:\n1. Mindestkapitalanforderungen: feinere Risikogewichte, interne Modelle (IRB), Markt- + operationelles Risiko\n2. Aufsichtlicher Überprüfungsprozess (ICAAP)\n3. Marktdisziplin (Offenlegungspflichten)\n\nProblem: IRB erlaubt RWA-Optimierung durch Modellwahl → Unterkapitalisierung.",
             card_type="listing", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Basel II", "3 Säulen"]),
        card(chapter=ch, section="Basel III", question="Was sind die wesentlichen Neuerungen von Basel III (ab 2010)?",
             answer="• Höhere EK-Anforderungen: CET1 4,5%, Tier-1 6%, Gesamt 8%\n• Kapitalpuffer: Erhaltungspuffer 2,5%, antizyklischer Puffer 0-2,5%\n• Leverage Ratio: 3% (ohne Risikogewichtung)\n• Liquiditätsanforderungen: LCR + NSFR\n• Höhere Anforderungen für SIFIs",
             card_type="listing", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Basel III", "CET1"]),
        card(chapter=ch, section="CET1", question="Was ist CET1 und warum ist es die wichtigste Kapitalklasse?",
             answer="CET1 = Common Equity Tier 1 = hartes Kernkapital:\n• Gewöhnliche Stammaktien + einbehaltene Gewinne\n• Höchste Verlustabsorptionsfähigkeit (going concern)\n• Mindest-Basel-III: 4,5% der RWA\n\nTier 1 = CET1 + AT1 (z.B. CoCo-Bonds)\nTier 2 = nachrangige Anleihen (gone concern)",
             card_type="definition", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["CET1"]),
        card(chapter=ch, section="Leverage Ratio", question="Was ist die Leverage Ratio (Basel III) und welchen Vorteil hat sie?",
             answer="Leverage Ratio = Tier-1-Kapital / Gesamtexposure (ungewichtet)\nMindestwert: 3%\n\nVorteil: Nicht manipulierbar durch Risikomodelle. Einfach und transparent. Verhindert übermäßige Bilanzhebel.\nNachteil: Kein Anreiz zur Risikoreduzierung innerhalb erlaubter Kategorie.",
             card_type="contrast", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Leverage Ratio"]),
        card(chapter=ch, section="LCR", question="Was ist die LCR (Liquidity Coverage Ratio)?",
             answer="LCR = HQLA / Netto-Liquiditätsabflüsse (30-Tage-Stressphase)\nMindest-LCR: 100%\n\nHQLA = hochliquide Aktiva (Bargeld, Staatsanleihen).\nZiel: Bank soll 30 Tage einen Run/Stress ohne Zentralbankhilfe überstehen.",
             card_type="definition", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["LCR", "Liquidität"]),
        card(chapter=ch, section="NSFR", question="Was ist die NSFR (Net Stable Funding Ratio)?",
             answer="NSFR = Verfügbare stabile Refinanzierung / Erforderliche stabile Refinanzierung\nMindest-NSFR: 100%\n\nZiel: Langfristige Refinanzierungsstruktur – langfristige Aktiva mit stabilen Passiva finanzieren.\nAdressiert strukturelles Fristentransformationsrisiko (nicht nur 30-Tage wie LCR).",
             card_type="definition", difficulty=3, importance=0.8, exam_relevance=0.75, tags=t+["NSFR"]),
        card(chapter=ch, section="Antizyklischer Puffer", question="Was ist der antizyklische Kapitalpuffer (CCB)?",
             answer="Zusätzliche CET1-Anforderung 0-2,5%, festgesetzt von nationalen Behörden.\n• Aufgebaut in Boom-Phasen (überdurchschnittliches Kreditwachstum)\n• Abgebaut in Krisen (um Kreditvergabe aufrechtzuerhalten)\n\nZiel: Prozyklizität des Bankensystems mildern.",
             card_type="understanding", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Antizyklischer Puffer"]),
        card(chapter=ch, section="Funktionen EK-Regulierung", question="Welche drei Funktionen erfüllt Eigenkapitalregulierung aus ökonomischer Sicht?",
             answer="1. Verlustpuffer: EK absorbiert Verluste\n2. Anreizsetzung: mehr EK → weniger Moral Hazard\n3. Systemische Stabilität: weniger Leverage im System → geringere Ansteckungsgefahr",
             card_type="listing", difficulty=2, importance=0.9, exam_relevance=0.85, tags=t+["EK-Regulierung"]),
        card(chapter=ch, section="Vorkrisen-Schwächen", question="Welche Schwächen der Vorkrisen-Regulierung (Basel I/II) offenbarte die Finanzkrise?",
             answer="• Zu niedrige EK-Anforderungen (Leverage 30-50x möglich)\n• Keine Liquiditätsanforderungen\n• IRB ermöglichte massive RWA-Reduktion (Prozyklizität)\n• Schattenbankensystem nicht reguliert (Off-Balance-Sheet)\n• Staatsanleihen mit 0% Risikogewicht → Home Bias\n• Keine Leverage Ratio",
             card_type="listing", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Vorkrisen-Schwächen"]),
        card(chapter=ch, section="Systemisches Risiko Regulierung", question="Welche Instrumente gibt es zur Regulierung des systemischen Risikos?",
             answer="• SIFI-Aufschläge: G-SIBs, D-SIBs brauchen mehr Kapital\n• TLAC/MREL: Bail-in-fähiges Kapital\n• Resolution Framework: geordnete Abwicklung\n• Makroprudenzielle Aufsicht (ESRB)\n• Stresstests\n• Strukturelle Trennung (Volcker Rule)",
             card_type="listing", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["SIFI", "TLAC"]),
        card(chapter=ch, section="Bail-in vs. Bail-out", question="Was ist der Unterschied zwischen 'Bail-in' und 'Bail-out'?",
             answer="Bail-out: Steuerzahler retten Bank (staatliche Kapitalzuführung). Verluste sozialisiert.\n\nBail-in: Gläubiger und Aktionäre absorbieren Verluste (Umwandlung Schulden → EK oder Haircut).\n\nBail-in schützt Steuerzahler, erhöht Marktdisziplin. Problem: kann Ansteckung auslösen.",
             card_type="contrast", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Bail-in", "Bail-out"]),
        card(chapter=ch, section="CoCo-Bonds", question="Was sind CoCo-Bonds und wie funktionieren sie?",
             answer="CoCo-Bonds = bedingte Pflichtwandelanleihen:\n• Werden wie FK behandelt (Zinsen steuerlich absetzbar)\n• Wandeln automatisch in EK um, wenn Kapitalquote unter Trigger fällt (z.B. CET1 < 5,125%)\n\nVorteil: Stärken Kapital automatisch in Krisenzeiten.\nRisiko: Verlust genau dann, wenn Markt schlecht ist.\nZählen zu AT1 (Additional Tier 1).",
             card_type="definition", difficulty=4, importance=0.85, exam_relevance=0.8, tags=t+["CoCo-Bonds", "AT1"]),
        card(chapter=ch, section="Herausforderungen", question="Welche Herausforderungen stellen sich der Bankenregulierung in Zukunft?",
             answer="• FinTech / Krypto: neue Anbieter ohne gleiche Regulierung\n• Schattenbanken weiterhin schwer regulierbar\n• Climate Risk: Übergangs- und physische Risiken\n• Globale Fragmentierung: Regulierungsarbitrage\n• Zinswende: stille Lasten bei zinsempfindlichen Banken (SVB)\n• Cybersicherheit als operationelles Risiko",
             card_type="listing", difficulty=2, importance=0.75, exam_relevance=0.7, tags=t+["Herausforderungen"]),
        card(chapter=ch, section="Prozyklizität", question="Was ist Prozyklizität im Bankensystem und wie verstärkt Regulierung sie?",
             answer="Prozyklizität: Banken verstärken den Konjunkturzyklus.\n• Boom: niedrige Ausfallraten → niedrige RWA → viel Kredit\n• Rezession: hohe Ausfallraten → hohe RWA → Kreditklemme\n\nRWA-basierte Regulierung verstärkt dies.\nLösung: antizyklischer Puffer, Forward-looking Provisioning.",
             card_type="understanding", difficulty=4, importance=0.85, exam_relevance=0.8, tags=t+["Prozyklizität"]),
        card(chapter=ch, section="Wahr/Falsch", question="Wahr oder Falsch: 'Höhere EK-Anforderungen machen Banken teurer ohne Vorteile.'",
             answer="Falsch. Vorteile: geringeres Konkursrisiko, weniger Moral Hazard, geringeres systemisches Risiko. Nach MM (ohne Marktunvollkommenheiten): EK-Anforderungen neutral (höheres EK senkt r_E). Nettokosten daher geringer als oft angenommen (Admati & Hellwig Argument).",
             card_type="trueFalse", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["EK-Regulierung", "Wahr/Falsch"]),
    ]


# ===========================================================================
# QUERSCHNITT: WAHR/FALSCH-SAMMLUNG (Klausurformat)
# ===========================================================================

def cards_true_false_exam() -> list[dict]:
    ch = "Querschnitt: Klausur-Wahr/Falsch"
    t = ["Wahr/Falsch", "Klausur"]
    return [
        card(chapter=ch, section="MM I", question="Wahr oder Falsch: 'Nach MM I (ohne Steuern) erhöht FK-Aufnahme den Unternehmenswert.'",
             answer="Falsch. Nach MM I ist der Unternehmenswert unabhängig von der Kapitalstruktur: V_L = V_U. Erst mit Steuern entsteht ein Steuervorteil: V_L = V_U + τ_C·D.",
             card_type="trueFalse", difficulty=2, importance=1.0, exam_relevance=1.0, tags=t+["MM I"]),
        card(chapter=ch, section="WACC", question="Wahr oder Falsch: 'Nach MM II steigt der WACC mit dem Verschuldungsgrad.'",
             answer="Falsch. WACC = r_U = konstant (ohne Steuern). Steigendes r_E kompensiert den FK-Vorteil exakt. Mit Steuern sinkt WACC (Steuervorteil).",
             card_type="trueFalse", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["WACC"]),
        card(chapter=ch, section="EK-Rendite", question="Wahr oder Falsch: 'Ein Unternehmen mit mehr Schulden hat höhere erwartete EK-Rendite.'",
             answer="Wahr. MM II: r_E = r_U + (D/E)·(r_U-r_D). Mit D>0 und r_U>r_D gilt r_E > r_U. Erhöhtes finanzielles Risiko der EK-Geber.",
             card_type="trueFalse", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["MM II"]),
        card(chapter=ch, section="Steuervorteil", question="Wahr oder Falsch: 'Je mehr FK, desto besser – der Steuervorteil gilt unbegrenzt.'",
             answer="Falsch. Im reinen Steuermodell wäre 100% FK optimal. In der Realität begrenzen Konkurskosten und Agency-Kosten das optimale D*. Zudem: Zinsen nur bis Höhe des EBIT absetzbar.",
             card_type="trueFalse", difficulty=2, importance=0.95, exam_relevance=0.95, tags=t+["Steuervorteil"]),
        card(chapter=ch, section="Asset Substitution", question="Wahr oder Falsch: 'Asset Substitution ist für FK-Geber vorteilhaft.'",
             answer="Falsch. Asset Substitution schadet FK-Gebern: beschränkter Upside (feste Zinsen), aber voller Downside. Risikoerhöhung verschiebt Wert von FK zu EK.",
             card_type="trueFalse", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["Asset Substitution"]),
        card(chapter=ch, section="Underinvestment", question="Wahr oder Falsch: 'Beim Debt Overhang verweigern EK-Geber profitable Projekte (NPV>0).'",
             answer="Wahr. Bei hohem Leverage profitieren FK-Geber von NPV>0-Projekten (Konkursrisiko sinkt). EK-Geber zahlen Investment, erhalten aber nur geringe Restrendite → Unterinvestition rational, gesellschaftlich ineffizient.",
             card_type="trueFalse", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["Underinvestment"]),
        card(chapter=ch, section="Bank Run", question="Wahr oder Falsch: 'Im Diamond-Dybvig-Modell tritt ein Bank Run nur auf, wenn die Bank tatsächlich insolvent ist.'",
             answer="Falsch. Im DD-Modell ist ein Run als selbsterfüllende Prophezeiung auch bei fundamental solventer Bank möglich. Rein als Koordinationsversagen (schlechtes Nash-Gleichgewicht), kein Fundamentalgrund nötig.",
             card_type="trueFalse", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["Bank Run"]),
        card(chapter=ch, section="Einlagenversicherung", question="Wahr oder Falsch: 'Eine Einlagenversicherung kann ohne weitere Regulierung eingeführt werden.'",
             answer="Falsch. Einlagenversicherung allein erzeugt Moral Hazard. Banken nehmen mehr Risiko, da Einleger nicht mehr disziplinieren → strenge EK-Regulierung und Aufsicht unbedingt nötig.",
             card_type="trueFalse", difficulty=2, importance=0.95, exam_relevance=0.9, tags=t+["Einlagenversicherung"]),
        card(chapter=ch, section="Homemade Leverage", question="Wahr oder Falsch: 'Homemade Leverage setzt voraus, dass Anleger zu gleichen Konditionen wie Unternehmen FK aufnehmen können.'",
             answer="Wahr. Das Arbitrage-Argument für MM I funktioniert nur bei gleichen Kreditkonditionen. In der Realität zahlen Privatpersonen oft höhere Zinsen → leichte Einschränkung des MM-Arguments.",
             card_type="trueFalse", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Homemade Leverage"]),
        card(chapter=ch, section="WACC mit Steuern", question="Wahr oder Falsch: 'Mit Körperschaftsteuer sinkt der WACC bei steigendem Verschuldungsgrad.'",
             answer="Wahr. WACC = (E/(E+D))·r_E + (D/(E+D))·r_D·(1-τ_C). FK-Kosten mit (1-τ_C) reduziert. Steuervorteil wird nicht vollständig durch r_E-Anstieg kompensiert → WACC sinkt.",
             card_type="trueFalse", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["WACC", "Steuern"]),
        card(chapter=ch, section="Pecking Order", question="Wahr oder Falsch: 'Die Pecking-Order-Theorie sagt vorher, dass profitable Unternehmen hohe FK-Quoten haben.'",
             answer="Falsch. Pecking Order: Profitable Firmen haben viele interne Mittel und nutzen diese zuerst → geringe FK-Quoten. Gegenteilige Vorhersage zur Trade-Off-Theorie.",
             card_type="trueFalse", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Pecking Order"]),
        card(chapter=ch, section="Too-big-to-fail", question="Wahr oder Falsch: 'Too-big-to-fail-Banken haben einen Wettbewerbsnachteil.'",
             answer="Falsch. TBTF-Banken haben einen Vorteil: implizite Staatsgarantie → günstigere Refinanzierung. Dies ist eine wettbewerbsverzerrende Subvention gegenüber kleineren Banken.",
             card_type="trueFalse", difficulty=3, importance=0.9, exam_relevance=0.85, tags=t+["Too Big to Fail"]),
        card(chapter=ch, section="Delegierte Überwachung", question="Wahr oder Falsch: 'Delegierte Überwachung durch Banken ist nur sinnvoll, wenn Überwachungskosten gleich null sind.'",
             answer="Falsch. Delegierte Überwachung lohnt sich, wenn die Gesamtkosten der Banküberwachung (c für alle Kredite) geringer sind als die Summe der Überwachungskosten aller Einzelanleger (n·c). Selbst bei positiven Kosten: Skalenvorteile rechtfertigen Bankenexistenz.",
             card_type="trueFalse", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Delegierte Überwachung"]),
        card(chapter=ch, section="Fristentransformation", question="Wahr oder Falsch: 'Fristentransformation ist für Banken nur möglich, weil sie eine Zentralbankgarantie haben.'",
             answer="Falsch. Fristentransformation ist grundsätzlich profitabel wegen der normalen Zinsstrukturkurve (langfristige Zinsen > kurzfristige). Das Diamond-Dybvig-Modell zeigt, dass Banken diese auch ohne explizite Staatsgarantie durchführen. Das Liquiditätsrisiko bleibt aber real.",
             card_type="trueFalse", difficulty=3, importance=0.85, exam_relevance=0.8, tags=t+["Fristentransformation"]),
    ]


# ===========================================================================
# RECHENAUFGABEN (Klausurformat)
# ===========================================================================

def cards_exam_calculations() -> list[dict]:
    ch = "Klausuraufgaben: Rechenübungen"
    t = ["Rechenaufgabe", "Klausur"]
    return [
        card(chapter=ch, section="EK-Rendite", question="EK=800, FK=200 (r_D=4%), E[EBIT]=90, r_U=10%. Berechne r_E via MM II.",
             answer="MM II: r_E = r_U + (D/E)·(r_U - r_D)\n= 10% + (200/800)·(10%-4%)\n= 10% + 0,25·6%\n= 10% + 1,5%\n= 11,5%",
             card_type="calculation", difficulty=3, importance=1.0, exam_relevance=1.0, tags=t+["EK-Rendite", "MM II"],
             solution_steps=["D/E = 200/800 = 0,25", "r_E = 10% + 0,25·6% = 11,5%"]),
        card(chapter=ch, section="Rekapitalisierung", question="500 Aktien, Kurs=20, r_U=10%, τ_C=25%. Rekapitalisierung: D=2.000. (a) V_U? (b) Kurs nach Ankündigung? (c) V_L? (d) Neue Aktienanzahl?",
             answer="(a) V_U = 500·20 = 10.000\n(b) PV(Steuervorteil) = 0,25·2.000 = 500\n    V_L = 10.500 → Kurs = 10.500/500 = 21,00\n(c) V_L = 10.500\n(d) Rückkauf: 2.000/21 ≈ 95,2 Aktien\n    Restaktien ≈ 500 - 95,2 = 404,8",
             card_type="calculation", difficulty=5, importance=1.0, exam_relevance=1.0, tags=t+["Rekapitalisierung"],
             solution_steps=["V_U = 10.000", "PV(TV) = 500 → Kurs = 21", "Rückkauf ≈ 95,2 Aktien", "Restaktien ≈ 404,8"]),
        card(chapter=ch, section="Diamond-Dybvig", question="D-D: n=1000, π=0,3, R=1,5, C1*=1,1. Wie viel investiert Bank langfristig? C2*?",
             answer="Reserve = n·π·C1* = 1000·0,3·1,1 = 330\nLangfristige Investition = 1000 - 330 = 670\n\nC2* = R·(1-π·C1*)/(1-π)\n= 1,5·(1-0,3·1,1)/(1-0,3)\n= 1,5·(1-0,33)/0,7\n= 1,5·0,67/0,7\n= 1,5·0,957...\n≈ 1,436",
             card_type="calculation", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["Diamond-Dybvig"],
             solution_steps=["Reserve = 330", "Langfristig = 670", "C2* = 1,5·0,67/0,7 ≈ 1,44"]),
        card(chapter=ch, section="Agency-Rechnung", question="FK=100 fällig. Projekt A: CF=130 (sicher). Projekt B: CF=160 (P=0,5) oder CF=80 (P=0,5). Welches wählen EK-Geber?",
             answer="Projekt A:\nE[CF_A] = 130 → FK erhält 100, EK erhält 30 (sicher)\n\nProjekt B:\nE[CF_B] = 0,5·160 + 0,5·80 = 120\nEK(B) = 0,5·max(160-100,0) + 0,5·max(80-100,0)\n= 0,5·60 + 0,5·0 = 30\n\nHier indifferent. Bei höheren Upside-Werten für B → EK bevorzugt B (Asset Substitution).",
             card_type="calculation", difficulty=5, importance=1.0, exam_relevance=1.0, tags=t+["Asset Substitution"],
             solution_steps=["EK(A) = 30 sicher", "EK(B) = 0,5·60 = 30", "Indifferent hier; Asset Substitution bei höherem Upside"]),
        card(chapter=ch, section="WACC", question="Berechne WACC: E=60, D=40, r_E=15%, r_D=6%, τ_C=35%.",
             answer="WACC = (60/100)·15% + (40/100)·6%·0,65\n= 0,6·15% + 0,4·3,9%\n= 9,0% + 1,56%\n= 10,56%",
             card_type="calculation", difficulty=2, importance=1.0, exam_relevance=1.0, tags=t+["WACC"],
             solution_steps=["FK n.St. = 6%·0,65 = 3,9%", "WACC = 9,0% + 1,56% = 10,56%"]),
        card(chapter=ch, section="Beta Entlevering", question="β_E=1,8, D/E=0,5, β_D=0. Berechne β_A.",
             answer="β_E = β_A·(1+D/E)\n1,8 = β_A·1,5\nβ_A = 1,8/1,5 = 1,2",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.9, tags=t+["Beta"],
             solution_steps=["β_A = β_E/(1+D/E) = 1,8/1,5 = 1,2"]),
        card(chapter=ch, section="Beta Relevering", question="β_A=1,0, D/E=1,5. Wie hoch ist β_E nach Rekapitalisierung?",
             answer="β_E = β_A·(1+D/E) = 1,0·(1+1,5) = 2,5\n\nInterpretation: EK trägt 2,5x das systematische Marktrisiko.",
             card_type="calculation", difficulty=3, importance=0.9, exam_relevance=0.9, tags=t+["Beta"],
             solution_steps=["β_E = 1,0·2,5 = 2,5"]),
        card(chapter=ch, section="Insolvenz EK/FK", question="FK=200 fällig in t=1. CF = 250 (P=0,6) oder 140 (P=0,4). Was bekommen EK und FK je Zustand?",
             answer="Z1 (CF=250): FK=200, EK=50\nZ2 (CF=140): FK=140 (Insolvenz!), EK=0\n\nE[FK] = 0,6·200 + 0,4·140 = 120+56 = 176\nE[EK] = 0,6·50 + 0,4·0 = 30\nE[gesamt] = 206 = E[CF] ✓",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Insolvenz"],
             solution_steps=["Z1: FK=200, EK=50", "Z2: FK=140, EK=0", "E[FK]=176, E[EK]=30"]),
        card(chapter=ch, section="Steuervorteil Rekapitalisierung", question="V_U=50 Mio., τ_C=30%, neues FK=10 Mio. Wie viel steigt V_L und der Aktienkurs (vor Rückkauf, 500.000 Aktien)?",
             answer="PV(Steuervorteil) = 0,30·10 = 3 Mio.\nV_L = 50 + 3 = 53 Mio.\nKursanstieg = 3 Mio. / 500.000 Aktien = 6 €/Aktie\nNeuer Kurs = alter Kurs + 6",
             card_type="calculation", difficulty=3, importance=0.95, exam_relevance=0.95, tags=t+["Steuervorteil"],
             solution_steps=["PV(TV) = 3 Mio.", "Kursanstieg = 6 €"]),
        card(chapter=ch, section="MM II Verifikation", question="EK=3.600, FK=2.400, V=6.000, r_U=8%, r_D=4%. Berechne r_E (MM II) und prüfe WACC.",
             answer="MM II: r_E = 8% + (2.400/3.600)·(8%-4%)\n= 8% + 0,667·4%\n= 8% + 2,667%\n= 10,667%\n\nWACC = (3.600/6.000)·10,667% + (2.400/6.000)·4%\n= 0,6·10,667% + 0,4·4%\n= 6,4% + 1,6%\n= 8% = r_U ✓",
             card_type="calculation", difficulty=4, importance=1.0, exam_relevance=1.0, tags=t+["MM II", "WACC"],
             solution_steps=["r_E = 8% + 0,667·4% = 10,667%", "WACC = 6,4% + 1,6% = 8% ✓"]),
    ]


# ===========================================================================
# HAUPTPROGRAMM
# ===========================================================================

def build_all_cards() -> list[dict]:
    all_cards = []
    for fn in [
        cards_chapter1,
        cards_chapter2,
        cards_chapter3,
        cards_chapter4,
        cards_chapter5,
        cards_chapter6,
        cards_chapter7,
        cards_true_false_exam,
        cards_exam_calculations,
    ]:
        all_cards.extend(fn())
    return all_cards


def validate(cards: list[dict]) -> dict:
    issues = []
    ids_seen: set[str] = set()
    for c in cards:
        if c["id"] in ids_seen:
            issues.append(f"Duplicate ID: {c['id']}")
        ids_seen.add(c["id"])
        if not c["question"].strip():
            issues.append(f"Empty question: {c['id']}")
        if not c["answer"].strip():
            issues.append(f"Empty answer: {c['id']}")
    return {"ok": len(issues) == 0, "issues": issues}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="flashcards.json")
    args = parser.parse_args()

    global _counter
    _counter = 0

    cards = build_all_cards()
    result = validate(cards)

    payload = {
        "meta": {
            "generatedAt": TODAY,
            "generatedBy": "scripts/generate/flashcard_generator.py",
            "primarySource": "Skript FMI SS2026_ jetzt.pdf",
            "totalCards": len(cards),
            "byStatus": {"ok": len([c for c in cards if c["validation"]["status"] == "ok"]), "review": 0},
        },
        "flashcards": cards,
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {len(cards)} Karten generiert → {out_path}")

    web_path = Path("public/data/flashcards.json")
    if web_path.parent.exists():
        web_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✓ Kopiert → {web_path}")

    if not result["ok"]:
        print(f"⚠ Validierungsprobleme: {result['issues']}")
    else:
        print("✓ Validierung OK")

    from collections import Counter
    per_ch = Counter(c["chapter"] for c in cards)
    print("\nKarten pro Kapitel:")
    for ch, n in sorted(per_ch.items()):
        print(f"  {n:3d}  {ch}")


if __name__ == "__main__":
    main()
