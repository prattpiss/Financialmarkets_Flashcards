"""
Comprehensive Flashcard Generator for FMI SS2026
Prof. Farzad Saidi, Universität Bonn
Generates ~400+ cards covering all chapters chronologically.
"""

import json
import uuid
from datetime import datetime


DIFF_MAP = {
    "Wiedergabe": 2,
    "Verständnis": 4,
    "Evaluation": 6,
    "Transfer": 6,
    "Synthese": 8,
}

TYPE_MAP = {
    "concept": "understanding",
    "true_false": "trueFalse",
}


def new_card(chapter, chapter_num, topic, question, answer,
             difficulty_level, slide_ref, card_type="concept",
             formula=None, variables=None, solution_steps=None):
    mapped_type = TYPE_MAP.get(card_type, "understanding")
    difficulty = DIFF_MAP.get(difficulty_level, 4)
    return {
        "id": str(uuid.uuid4()),
        # Core fields (new format)
        "chapter": chapter,
        "chapterNum": chapter_num,
        "topic": topic,
        "question": question,
        "answer": answer,
        "difficultyLevel": difficulty_level,
        "slideRef": slide_ref,
        "type": mapped_type,
        "formula": formula,
        "variables": variables,
        "solutionSteps": solution_steps,
        # Legacy compat fields required by React app
        "difficulty": difficulty,
        "importance": 0.8,
        "examRelevance": 0.85,
        "section": topic,
        "tags": [chapter.split(":")[0].strip(), difficulty_level, slide_ref],
        "source": {
            "current": [{"file": "Skript FMI SS2026", "page": slide_ref}],
            "historical": []
        },
        "validation": {"status": "ok", "issues": []},
        # SM-2 fields (legacy names)
        "learning": {
            "repetitions": 0,
            "ease": 2.5,
            "interval": 0,
            "due": datetime.now().isoformat(),
            "lastReviewed": None
        },
        # SM-2 fields (new names also)
        "easeFactor": 2.5,
        "interval": 0,
        "repetitions": 0,
        "dueDate": datetime.now().isoformat(),
        "lastReviewed": None,
    }


def cards_chapter1():
    ch = "Kapitel 1: Funktionen des Finanzsystems"
    n = 1
    cards = []

    # Akteure
    cards.append(new_card(ch, n, "Akteure des Finanzsystems",
        "Welche drei Hauptkomponenten/Akteure bilden das Finanzsystem?",
        "1. Finanzintermediäre (Banken, Fonds, Versicherungen)\n2. Finanzmärkte\n3. Finanzinfrastruktur (Zahlungssysteme, Aufsicht)\nDazu kommen die Akteure: Haushalte, Unternehmen, Staat.",
        "Wiedergabe", "S. 20"))

    cards.append(new_card(ch, n, "Direkte vs. indirekte Finanzierung",
        "Was ist der Unterschied zwischen direkter und indirekter Finanzierung?",
        "Direkte Finanzierung: Kapitalnehmer und -geber tauschen direkt Wertpapiere auf Finanzmärkten aus.\nIndirekte Finanzierung: Ein Finanzintermediär (z.B. Bank) tritt dazwischen – er nimmt Einlagen entgegen und vergibt Kredite.",
        "Verständnis", "S. 22"))

    cards.append(new_card(ch, n, "Rolle der Akteure",
        "Welche typische Rolle nehmen Haushalte, Unternehmen und der Staat im Finanzsystem ein?",
        "Haushalte: Überschussakteure (Sparer, Nettogläubiger).\nUnternehmen: Defizitakteure (Kreditnehmer, Nettoinvestitoren).\nStaat: Kann beides sein; bei hohen Defiziten Nettokreditnehmer.",
        "Verständnis", "S. 23"))

    cards.append(new_card(ch, n, "Wichtigste Finanzintermediäre",
        "Nennen Sie die drei wichtigsten Typen von Finanzintermediären.",
        "1. Banken (Kreditinstitute)\n2. Investmentfonds / Pensionsfonds\n3. Versicherungen (insb. Lebensversicherungen)",
        "Wiedergabe", "S. 24"))

    cards.append(new_card(ch, n, "Bilanzverknüpfungen",
        "Wie sind Banken, Haushalte und Unternehmen bilanziell miteinander verknüpft?",
        "Bankeinlagen der Haushalte = Passivseite der Bank. Bankkredite an Unternehmen = Aktivseite der Bank. Unternehmensanleihen oder -aktien können von Fonds/Haushalten gehalten werden. Jede Verbindlichkeit ist gleichzeitig eine Forderung.",
        "Verständnis", "S. 25"))

    cards.append(new_card(ch, n, "Drei Hauptfunktionen",
        "Welche drei Hauptfunktionen übernimmt das Finanzsystem?",
        "1. Senkung von Transaktionskosten\n2. Senkung von Informationskosten (adverse Selektion, Moral Hazard)\n3. Risikomanagement (Diversifikation, Liquiditäts-, Risikotransformation)",
        "Wiedergabe", "S. 26"))

    cards.append(new_card(ch, n, "Transaktionskostenreduktion",
        "Wie senkt ein Finanzintermediär Transaktionskosten? Erklären Sie das M×N-Argument.",
        "Ohne Intermediär: M Sparer und N Kreditnehmer brauchen M×N Verträge.\nMit Intermediär: M+N Verträge (jeder schließt nur einen Vertrag mit dem Intermediär).\nErsparnis: M×N − (M+N) Verträge; besonders groß bei vielen Marktteilnehmern.",
        "Verständnis", "S. 27-28",
        formula="Ersparte Verträge = M·N − (M+N)",
        variables={"M": "Anzahl Sparer", "N": "Anzahl Kreditnehmer"}))

    cards.append(new_card(ch, n, "Adverse Selektion",
        "Was versteht man unter adverser Selektion im Finanzsystem und wie kann ein Intermediär helfen?",
        "Adverse Selektion: Vor Vertragsschluss hat der Kreditgeber weniger Informationen als der Kreditnehmer (hidden characteristics) → schlechte Risiken verdrängen gute.\nIntermediär: sammelt Informationen, scrennt Kreditnehmer (Kreditwürdigkeitsprüfung), baut Expertise auf.",
        "Verständnis", "S. 29"))

    cards.append(new_card(ch, n, "Moral Hazard",
        "Was ist Moral Hazard und wie tritt es in Kreditbeziehungen auf?",
        "Moral Hazard: Nach Vertragsschluss verhält sich der Kreditnehmer anders als erwartet, weil der Kreditgeber sein Verhalten nicht vollständig beobachten kann (hidden action).\nBeispiel: Kreditnehmer geht nach Kreditaufnahme höhere Risiken ein als vereinbart.",
        "Verständnis", "S. 30"))

    cards.append(new_card(ch, n, "Risikomanagement – Überblick",
        "Durch welche vier Mechanismen kann das Finanzsystem Risiken managen?",
        "1. Diversifikation: Streuung idiosynkratischer Risiken\n2. Risikotransformation: Weitergabe von Risiken an risikobereitere Anleger\n3. Liquiditätstransformation: Kurzfristige Einlagen → langfristige Kredite\n4. Verbriefungen: Bündelung und Weitergabe von Risiken",
        "Wiedergabe", "S. 31-32"))

    cards.append(new_card(ch, n, "Rolle des Staates",
        "Welche Rollen spielt der Staat im Finanzsystem?",
        "1. Regulierung und Aufsicht (z.B. BaFin, EZB)\n2. Bereitstellung von Infrastruktur (Rechtssystem)\n3. Einlagensicherung und Lender of Last Resort\n4. Selbst Akteur: Staatsanleihen, öffentliche Banken",
        "Verständnis", "S. 33"))

    cards.append(new_card(ch, n, "Warum reguliert?",
        "Nennen Sie die zwei zentralen Gründe für die Regulierung des Finanzsystems.",
        "1. Systemisches Risiko: Zusammenbruch einzelner Finanzinstitute kann das gesamte Finanzsystem und die Realwirtschaft schädigen.\n2. Einlegerschutz: Asymmetrische Information macht es Einlegern schwer, die Risikolage ihrer Bank zu beurteilen.",
        "Verständnis", "S. 34-35"))

    cards.append(new_card(ch, n, "Finanzmarktintegration",
        "Was bedeutet Finanzmarktintegration und welche Vor-/Nachteile hat sie?",
        "Integration = Kapitalmärkte verschiedener Länder wachsen zusammen; Zinsunterschiede werden kleiner.\nVorteile: Bessere Risikostreuung, günstigeres Kapital.\nNachteile: Schnellere Übertragung von Krisen, weniger nationale Geldpolitik wirksam.",
        "Evaluation", "S. 36-37"))

    cards.append(new_card(ch, n, "Finanzsystem und Wirtschaftswachstum",
        "Über welche Kanäle beeinflusst ein gut funktionierendes Finanzsystem das Wirtschaftswachstum?",
        "1. Kapitalakkumulation: Mehr und bessere Investitionen\n2. Produktivität: Bessere Allokation von Kapital zu produktivsten Verwendungen\n3. Innovation: Risikokapital für neue Technologien\nWichtig: Korrelation ≠ Kausalität! Umgekehrte Kausalität möglich.",
        "Verständnis", "S. 38-40"))

    cards.append(new_card(ch, n, "Zu großes Finanzsystem",
        "Kann ein zu großes Finanzsystem schädlich sein? Erklären Sie.",
        "Ja. Ab einer gewissen Größe können negative Effekte dominieren:\n- Ressourcen (Humankapital) werden ineffizient ins Finanzsystem gelenkt\n- Höheres systemisches Risiko\n- Overbanking (z.B. Europa nach der Krise): mangelnde Alternativen zur Bankfinanzierung schwächt Wirtschaft nach Bankkrisen.",
        "Evaluation", "S. 41"))

    cards.append(new_card(ch, n, "Bank- vs. marktbasierte Systeme",
        "Was sind die Argumente für bank- bzw. marktbasierte Finanzsysteme?",
        "Banken (+): Lösung von Informationsproblemen, langfristige Beziehungen, Unternehmensüberwachung.\nMärkte (+): Aggregation disperser Information, Liquidität, mehr Diversifikation.\nEmpirie (Levine/Zervos 1998): Beide sind komplementär, kein System ist überlegen.",
        "Evaluation", "S. 42-50"))

    cards.append(new_card(ch, n, "Komplementarität",
        "Warum sind Finanzmärkte und Finanzintermediäre eher komplementär als substitutiv?",
        "Intermediäre spielen auch auf Märkten eine wichtige Rolle (Market Maker, Emissionsbegleitung, Anlageberatung). Wettbewerb erhöht Effizienz. Grenzen verschwimmen (Verbriefungen). Empirisch fördern beide das Wachstum.",
        "Verständnis", "S. 50"))

    cards.append(new_card(ch, n, "Overbanking",
        "Was bedeutet Overbanking und warum ist es problematisch?",
        "Overbanking: Ein Finanzsystem ist zu stark bankbasiert.\nProblem: Nach Bankenkrisen fehlen alternative Finanzierungsquellen. Unternehmen können sich nicht über Märkte finanzieren.\nIn Europa diskutiert als Argument für Kapitalmarktunion.",
        "Verständnis", "S. 51"))

    cards.append(new_card(ch, n, "Bedeutung des Rechtssystems",
        "Wie beeinflusst das Rechtssystem (La Porta et al. 1997) das Finanzsystem?",
        "Länder mit angelsächsischem Common Law schützen Anteilseigner besser → marktbasierter.\nLänder mit kontinentalem Zivilrecht (z.B. Deutschland) schützen Gläubiger besser → bankbasierter.\nRechtssystem erklärt systematische Unterschiede in der Finanzstruktur.",
        "Verständnis", "S. 52"))

    cards.append(new_card(ch, n, "5 Trends im Finanzsystem",
        "Nennen Sie die 5 wichtigsten Trends im modernen Finanzsystem.",
        "1. Disintermediation: Unternehmensfinanzierung zunehmend über Märkte\n2. Zunehmende Vernetzung: Konsolidierung, Kreditrisikotransfer\n3. Größere Komplexität von Finanzprodukten\n4. Wachstum des Schattenbankensektors (Hedgefonds, Geldmarktfonds)\n5. Digitalisierung bedroht traditionelle Geschäftsmodelle",
        "Wiedergabe", "S. 53-55"))

    cards.append(new_card(ch, n, "Fazit Kap. 1 – Transfer",
        "Warum ist es laut Kapitel 1 falsch zu sagen, marktbasierte Systeme seien grundsätzlich besser als bankbasierte?",
        "Empirische Literatur zeigt: Beide Systeme fördern Wachstum. Sie sind komplementär. Der Nutzen hängt von Institutionen, Rechtssystem, Unternehmensstruktur ab. Wichtig ist die Gesamtgröße und Effizienz des Finanzsystems, nicht die Form.",
        "Transfer", "S. 56"))

    return cards


def cards_chapter2():
    ch = "Kapitel 2: Globale Finanzkrise"
    n = 2
    cards = []

    cards.append(new_card(ch, n, "Stilisierte Fakten über Finanzkrisen",
        "Was sind die wichtigsten stilisierten Fakten über Finanzkrisen?",
        "1. Finanzkrisen treten regelmäßig auf (werden es auch in Zukunft)\n2. Schwerste: Weltwirtschaftskrise 1930er, Finanzkrise 2007-09\n3. Können gleichzeitig viele Länder betreffen\n4. Weitere Beispiele: Savings & Loans (USA 1980er), Japan 1990er, Asienkrise 1997/98, Argentinien 2001",
        "Wiedergabe", "S. 61-62"))

    cards.append(new_card(ch, n, "Bankenkrise – Definition",
        "Wie ist eine Bankenkrise definiert und was sind typische Vorläufer?",
        "Bankenkrise: Gleichzeitiger Zusammenbruch eines signifikanten Teils des Bankensektors (systemische Krise), verbunden mit hohen Verlusten und/oder Bank Runs.\nVorläufer: Kreditboom + Vermögenspreisblasen (v.a. Immobilien).\nWichtig: Zusammenbruch einer einzelnen Bank ≠ Bankenkrise.",
        "Verständnis", "S. 63"))

    cards.append(new_card(ch, n, "Kosten von Bankenkrisen",
        "Welche drei Kostenarten entstehen laut Laeven und Valencia (2013) bei Bankenkrisen?",
        "1. Direkte fiskalische Kosten: Staatliche Bankenrettungen\n2. Outputkosten: BIP fällt dauerhaft unter Vorkrisentrend (wichtigster Posten)\n3. Anstieg der Staatsverschuldung: Durch geringere Einnahmen + höhere Ausgaben",
        "Verständnis", "S. 64-65"))

    cards.append(new_card(ch, n, "Staatsschuldenkrise",
        "Was ist eine Staatsschuldenkrise und wie unterscheidet sie sich von einer normalen Haushaltskrise?",
        "Staatsschuldenkrise: Zahlungsausfall (oder -bereitschaft) eines Staates → Restrukturierung (Laufzeitverlängerung, Schuldenerlass).\nNicht nur Zahlungsfähigkeit, auch Zahlungsbereitschaft relevant (Russland 1998).\nFast alle Länder hatten schon eine (Ausnahmen: USA, Dänemark).",
        "Verständnis", "S. 67"))

    cards.append(new_card(ch, n, "Währungskrise",
        "Was ist eine Währungskrise und welche Länder sind typischerweise betroffen?",
        "Plötzlicher Verfall einer Währung durch spekulative Attacke + sudden stop (Kapitalabflüsse).\nBetrifft v.a. Länder mit festen Wechselkurssystemen.\nFührt zu Abwertung oder Aufgabe des festen Wechselkurses.\nBeispiel: EWS-Krise 1992/93 (UK, Italien).",
        "Verständnis", "S. 68"))

    cards.append(new_card(ch, n, "Twin Crises",
        "Erklären Sie, warum Banken- und Währungskrisen oft gemeinsam auftreten (twin crises).",
        "Bankenkrise → Währungskrise: Ausländische Einleger fliehen aus schwachen Banken ins Ausland (z.B. Deutschland 1931).\nWährungskrise → Bankenkrise: Abwertung trifft Banken/Unternehmen mit Fremdwährungsschulden (z.B. Tequila-Krise Mexiko 1994, Thailand 1997).",
        "Verständnis", "S. 70"))

    cards.append(new_card(ch, n, "Staaten-Banken-Nexus",
        "Was versteht man unter dem Staaten-Banken-Nexus und warum ist er gefährlich?",
        "Wechselseitige Abhängigkeit zwischen Banken und Staatsverschuldung:\n• Banken→Staat: Bankenrettungen belasten Staatsfinanzen (Irland, Spanien)\n• Staat→Banken: Staatsanleihebestände der Banken + schwache staatl. Garantien gefährden Banken (Griechenland)\nVerstärkt durch Home Bias und regulatorische Privilegierung von Staatsanleihen.",
        "Verständnis", "S. 83"))

    cards.append(new_card(ch, n, "Subprime-Krise – Auslöser",
        "Was war der unmittelbare Auslöser der globalen Finanzkrise 2007-2009?",
        "Einbruch der Immobilienpreise in den USA ab 2006 (makroökonomischer Schock).\nDaraufhin massive Kreditausfälle bei Subprime-Krediten (Kredite an hochriskante Schuldner).\nSinkende Immobilienpreise entwerteten Sicherheiten → Schuldner konnten nicht bedienen.",
        "Wiedergabe", "S. 71-72"))

    cards.append(new_card(ch, n, "Makroökonomisches Umfeld 2007",
        "Welches makroökonomische Umfeld begünstigte die Entstehung der Subprime-Krise?",
        "1. Sehr niedrige Leitzinsen in den USA nach Dotcom-Krise\n2. Massive Kapitalzuflüsse aus Asien (insb. China) in die USA\n3. Beides führte zu starker Kreditexpansion im Immobilienbereich\n4. Langsame Zinserhöhungen ab 2004 leiteten Kehrtwende ein",
        "Verständnis", "S. 73"))

    cards.append(new_card(ch, n, "Verbriefung und CDOs",
        "Wie wurde aus einem US-Immobilienproblem eine globale Krise? Erklären Sie die Rolle von CDOs.",
        "Subprime-Kredite wurden gebündelt, tranchiert und als Collateralized Debt Obligations (CDOs) weltweit verkauft.\nHohe Nachfrage: Search for yield (niedrige Zinsen) + hohe Ratings der Senior-Tranchen (AAA).\nRatingagenturen überbewerteten Sicherheit → globale Verteilung des Risikos.",
        "Verständnis", "S. 74-75"))

    cards.append(new_card(ch, n, "Aufbau systemischer Risiken",
        "Welche vier Entwicklungen erhöhten das systemische Risiko vor der Krise?",
        "1. Anstieg der Verschuldung (auch im Schattenbankensektor)\n2. Anstieg der Fristentransformation (SPVs über kurzfristige ABCP finanziert)\n3. Anstieg der Vernetzung (CDS, Gegenparteirisiken)\n4. Anstieg der Korrelationen (ähnliche Risikopositionen)",
        "Verständnis", "S. 76"))

    cards.append(new_card(ch, n, "Illusion der Risikoteilung",
        "Warum erwies sich die verbesserte Risikoteilung durch Verbriefungen als Illusion?",
        "Risiken verblieben weitgehend im Finanzsystem (oft als regulatorische Arbitrage).\nGegenparteirisiken (CDS) waren korreliert mit Grundrisiken: Als Subprime ausfiel, wurden auch viele CDS nicht erfüllt.\nKeine Transparenz darüber, wer welche Risiken trug.",
        "Evaluation", "S. 77"))

    cards.append(new_card(ch, n, "Chronologie der Krise 2007-08",
        "Beschreiben Sie die wichtigsten Ereignisse der Finanzkrise von Juni 2007 bis September 2008.",
        "Juni 2007: Probleme bei US-Hedgefonds\nJuli/Aug 2007: IKB, SachsenLB, WestLB, BayernLB in DE\nSept 2007: Bank Run auf Northern Rock (UK), Verstaatlichung\nMärz 2008: Bear Stearns kollabiert und wird gerettet\n15. Sept 2008: Lehman Brothers bricht zusammen → weltweite systemische Krise",
        "Wiedergabe", "S. 78-80"))

    cards.append(new_card(ch, n, "Lehman Brothers – Bedeutung",
        "Warum war der Zusammenbruch von Lehman Brothers ein Wendepunkt in der Krise?",
        "1. Enttäuschte die Erwartung, Banken würden immer gerettet (moral hazard-Erwartung brach)\n2. Lehman war wichtiger Schuldner, Gegenpartei und Handelspartner\n3. Weltweiter Einbruch der Wertpapierpreise + Einfrieren des Interbankenmarktes\n4. Viele Banken am Rande des Zusammenbruchs",
        "Verständnis", "S. 80"))

    cards.append(new_card(ch, n, "Liquiditätsspiralen",
        "Erklären Sie die Liquiditätsspiralen (Brunnermeier/Pedersen 2009) und ihre Wirkung.",
        "Loss Spiral: Preisverfall → Verluste → erzwungener Verkauf → weitere Preisrückgänge (fire sales).\nMargin Spiral: Höhere Haircuts → mehr Deleveraging → weitere Preisrückgänge.\nBeide Spiralen verstärken sich gegenseitig: Weder funding liquidity noch market liquidity verfügbar.",
        "Verständnis", "S. 81"))

    cards.append(new_card(ch, n, "Akutes Krisenmanagement 2008",
        "Welche Maßnahmen ergriffen Regierungen und Zentralbanken im akuten Krisenmanagement?",
        "1. Massive Liquiditätszuführungen durch Zentralbanken\n2. Staatliche Garantien für Einleger\n3. Eigenkapitalzuführungen für Banken und Versicherungen (AIG, Fortis, Dexia, RBS...)\n2008-12: 413,2 Mrd. Euro an EU-Banken (3,2% des BIP 2012)",
        "Wiedergabe", "S. 82"))

    cards.append(new_card(ch, n, "Eurokrise – Entstehung",
        "Wie begann die Krise im Euroraum im Oktober 2009?",
        "Oktober 2009: Griechenland veröffentlicht revidierte Haushaltszahlen → Staatsfinanzen nicht tragfähig.\nAnstieg der Risikoprämien auf griechische Anleihen (vs. deutsche Bunds).\nMai 2010: Erstes Rettungspaket (110 Mrd. Euro, IWF-Beteiligung, strikte Konditionalität).",
        "Wiedergabe", "S. 84"))

    cards.append(new_card(ch, n, "Ansteckungseffekte im Euroraum",
        "Warum wurden Ansteckungseffekte bei Griechenland so ernst genommen?",
        "Gefahr des Überspringens auf Irland, Portugal, Spanien, Italien (GIIPS).\nAußerdem: Europäische Banken hielten griechische und andere GIIPS-Anleihen.\nGriechenland allein wäre verkraftbar; Ansteckung auf größere Länder hätte den Euro bedroht.",
        "Verständnis", "S. 85-86"))

    cards.append(new_card(ch, n, "Whatever it takes",
        "Was war die Bedeutung von Draghis 'Whatever it takes'-Rede im Juli 2012?",
        "Beruhigung der Eurokrise: EZB würde alles tun, um den Euro zu erhalten.\nSofortiger Rückgang der Risikoprämien.\nAnkündigung des OMT-Programms (Outright Monetary Transactions): Aufkauf von Staatsanleihen, geknüpft an ESM-Programm.\nProgramm wurde nie eingesetzt, allein die Ankündigung reichte.",
        "Verständnis", "S. 88"))

    cards.append(new_card(ch, n, "Krisenmanagement Euroraum",
        "Welche Stützungsmechanismen wurden in der Eurokrise eingerichtet?",
        "Mai 2010: Securities Markets Program (SMP) der EZB\nMai 2011: EFSM und EFSF (temporäre Fazilitäten)\nOkt 2012: Europäischer Stabilitätsmechanismus (ESM, permanent)\nOMT-Programm (Sept 2012): nie eingesetzt",
        "Wiedergabe", "S. 87"))

    cards.append(new_card(ch, n, "Multiple Krisen 2020er",
        "Welche multiplen Krisen stellen seit den 2020ern neue Herausforderungen dar?",
        "Pandemie (COVID-19), hohe Inflation, geopolitische Konflikte, Energiekrise, klimabedingte Investitionsbedarfe.\nBesondere Herausforderung: Simultanität und wechselseitige Verschärfung.\nFiskal- und Geldpolitik geraten in Zielkonflikte.",
        "Wiedergabe", "S. 90"))

    cards.append(new_card(ch, n, "Synthese Finanzkrisen",
        "Warum ist die Regulierung des Finanzsystems nach der Krise von 2007-09 verstärkt worden und was waren die wichtigsten Reformen?",
        "Lehren: Zu wenig Eigenkapital, zu hohe Verschuldung, mangelnde Liquiditätsanforderungen, fehlende makroprudenzielle Perspektive.\nReformen: Basel III (höhere EK-Anforderungen, Liquiditätsregulierung), makroprudenzielle Aufsicht, Solvency II (Versicherungen), stärkere Regulierung von Schattenbanken.",
        "Synthese", "S. 83"))

    return cards


def cards_chapter3():
    ch = "Kapitel 3: Modigliani-Miller-Theorem"
    n = 3
    cards = []

    cards.append(new_card(ch, n, "Kapitalstruktur – Definition",
        "Was versteht man unter der Kapitalstruktur eines Unternehmens?",
        "Die Kapitalstruktur gibt an, wie die Vermögensgegenstände des Unternehmens finanziert sind (Passivseite der Bilanz): relative Anteile von Eigen- und Fremdkapital.",
        "Wiedergabe", "S. 102"))

    cards.append(new_card(ch, n, "Fremdkapital – Definition",
        "Wie ist Fremdkapital definiert und was passiert bei Nichtzahlung?",
        "Fremdkapital: feste (erfolgsunabhängige) Rückzahlungsverpflichtungen (Zinsen + Nominalbetrag). Fremdkapital muss vor Eigenkapital bedient werden. Kann nicht zurückgezahlt werden → Insolvenz.",
        "Wiedergabe", "S. 104"))

    cards.append(new_card(ch, n, "Eigenkapital – Definition",
        "Was ist das Eigenkapital und warum trägt der Eigenkapitalgeber mehr Risiko?",
        "Eigenkapital: keine festen Rückzahlungspflichten, Anspruch auf Residualertrag nach allen Verpflichtungen (residual claimant).\nHöheres Risiko: Ertrag hängt vom Unternehmenserfolg ab → sehr hohe oder sehr niedrige Renditen.",
        "Verständnis", "S. 104"))

    cards.append(new_card(ch, n, "Kapitalwertformel",
        "Wie berechnet man den Kapitalwert (KW) eines Investitionsprojekts?",
        "KW = −Investition + Barwert der Einzahlungen\nBarwert = Erwartete Einzahlungen / (1 + r), wobei r die gesamten Kapitalkosten (inkl. Risikoprämien) sind.\nKapitalwertregel: Projekte mit KW > 0 durchführen.",
        "Verständnis", "S. 106",
        formula="KW = -I_0 + \\frac{E[CF]}{1+r}",
        variables={"I_0": "Anfangsinvestition", "E[CF]": "Erwarteter Cashflow", "r": "Gesamte Kapitalkosten (inkl. Risikoprämie)"}))

    cards.append(new_card(ch, n, "Eigenkapitalrendite – Beispiel",
        "Wie berechnet sich die erwartete Eigenkapitalrendite bei reiner EK-Finanzierung?",
        "Rendite = (Ertrag − eingesetztes Kapital) / eingesetztes Kapital.\nIm Beispiel (1000 Euro EK, Erfolg: 1400, Misserfolg: 900):\nErfolg: (1400−1000)/1000 = 40%\nMisserfolg: (900−1000)/1000 = −10%\nErwartet: 0,5·40%+0,5·(−10%) = 15%",
        "Verständnis", "S. 107-108",
        formula="r_E = \\frac{Ertrag - EK}{EK}",
        variables={"EK": "Eingesetztes Eigenkapital", "Ertrag": "Auszahlung des Unternehmens"}))

    cards.append(new_card(ch, n, "MMT I – Aussage",
        "Was besagt das Modigliani-Miller-Theorem I (MMT I)?",
        "In einem vollkommenen Kapitalmarkt entspricht der Gesamtwert eines Unternehmens dem Marktwert der Zahlungen seiner Vermögensgegenstände und ist von der Kapitalstruktur unabhängig.\nFolge: Weder Verschuldung noch Eigenkapitalausstattung beeinflussen den Unternehmenswert.",
        "Wiedergabe", "S. 112"))

    cards.append(new_card(ch, n, "Bedingungen MMT",
        "Unter welchen drei Bedingungen gilt das Modigliani-Miller-Theorem?",
        "1. Freie Handelbarkeit: Investoren und Unternehmen handeln Wertpapiere zu Marktpreisen\n2. Keine Steuern oder Transaktionskosten\n3. Keine asymmetrische Information (Finanzierungsentscheidungen generieren keine neue Info)",
        "Verständnis", "S. 113"))

    cards.append(new_card(ch, n, "Homemade Leverage",
        "Was ist Homemade Leverage und warum zeigt es, dass die Kapitalstruktur irrelevant ist?",
        "Investor kann durch eigene Kreditaufnahme (bei gleichem Zinssatz wie Unternehmen) das Auszahlungsprofil eines verschuldeten Unternehmens replizieren.\nFolge: Wenn Investor selbst levern kann, schafft Unternehmensverschuldung keinen Mehrwert → Kapitalstruktur irrelevant.",
        "Verständnis", "S. 115-116"))

    cards.append(new_card(ch, n, "Arbitrageargument",
        "Wie beweist das Arbitrageargument das MMT?",
        "Wenn zwei Unternehmen mit identischen Zahlungsströmen unterschiedliche Gesamtwerte haben, entstehen Arbitragemöglichkeiten.\nKauf des 'billigen', Verkauf des 'teuren' Unternehmens.\nArbitrage treibt Werte zusammen, bis MMT gilt.",
        "Verständnis", "S. 117-118"))

    cards.append(new_card(ch, n, "Marktwertbilanz",
        "Was ist eine Marktwertbilanz und wie bestimmt man darüber den Eigenkapitalwert?",
        "Marktwertbilanz: Alle Positionen zum aktuellen Marktwert.\nMW(EK) = MW(Vermögensgegenstände) − MW(Fremdkapital) − MW(andere Verbindlichkeiten).\nAnwendung: Auch bei komplexeren Wertpapierstrukturen (Optionsscheine etc.).",
        "Verständnis", "S. 119",
        formula="E = A - D - \\text{andere VB}",
        variables={"E": "Marktwert Eigenkapital", "A": "Marktwert Vermögensgegenstände", "D": "Marktwert Fremdkapital"}))

    cards.append(new_card(ch, n, "MMT II – Eigenkapitalkosten",
        "Was besagt das Modigliani-Miller-Theorem II (MMT II) über Eigenkapitalkosten?",
        "Die Eigenkapitalkosten steigen linear mit dem Verschuldungsgrad (D/E).\nFormel: r_E = r_U + (D/E)·(r_U − r_D)\nBegründung: Höhere Verschuldung erhöht Risiko des Eigenkapitals → höhere Rendite gefordert.",
        "Verständnis", "S. 124",
        formula="r_E = r_U + \\frac{D}{E}(r_U - r_D)",
        variables={"r_E": "Eigenkapitalkosten verschuldetes Unternehmen", "r_U": "Eigenkapitalkosten unverschuldetes Unternehmen", "r_D": "Fremdkapitalkosten", "D": "Marktwert Fremdkapital", "E": "Marktwert Eigenkapital"}))

    cards.append(new_card(ch, n, "WACC – Definition und Formel",
        "Was sind die WACC und wie berechnen sie sich?",
        "WACC (Weighted Average Cost of Capital) = gewichtete durchschnittliche Kapitalkosten.\nIn vollkommenem Markt: WACC = r_U = r_A (kapitalstrukturunabhängig).",
        "Verständnis", "S. 125",
        formula="r_{WACC} = \\frac{E}{E+D}\\cdot r_E + \\frac{D}{E+D}\\cdot r_D",
        variables={"r_E": "Eigenkapitalkosten", "r_D": "Fremdkapitalkosten", "E": "Marktwert Eigenkapital", "D": "Marktwert Fremdkapital"}))

    cards.append(new_card(ch, n, "WACC konstant?",
        "Warum bleiben die WACC in einem vollkommenen Markt konstant, obwohl EK-Kosten mit Verschuldung steigen?",
        "Mit steigender Verschuldung steigen r_E und r_D.\nGleichzeitig steigt der Anteil des günstigeren Fremdkapitals.\nDiese beiden Effekte gleichen sich exakt aus → WACC = r_U = konstant.\nMMT: Kapitalstruktur beeinflusst WACC nicht.",
        "Verständnis", "S. 126-128"))

    cards.append(new_card(ch, n, "Beta und Verschuldung",
        "Wie verändert sich das Eigenkapital-Beta mit der Verschuldung?",
        "Asset-Beta (unverschuldetes Unternehmen): β_U = (E/(E+D))·β_E + (D/(E+D))·β_D\nEigenkapital-Beta verschuldetes Unternehmen: β_E = β_U + (D/E)·(β_U − β_D)\nFolge: β_E steigt mit D/E, analog zur erwarteten Rendite.",
        "Verständnis", "S. 131",
        formula="\\beta_E = \\beta_U + \\frac{D}{E}(\\beta_U - \\beta_D)",
        variables={"β_E": "Eigenkapital-Beta", "β_U": "Asset-Beta (unverschuldet)", "β_D": "Fremdkapital-Beta", "D": "Fremdkapital", "E": "Eigenkapital"}))

    cards.append(new_card(ch, n, "Trugschluss EPS",
        "Warum ist es ein Trugschluss zu behaupten, höhere Verschuldung erhöhe den Aktienkurs wegen höherem EPS?",
        "Zwar steigt der erwartete Gewinn je Aktie (EPS) mit Verschuldung.\nAber gleichzeitig steigt das Risiko (Volatilität des EPS).\nHöherer EPS ist exakt die Entschädigung für höheres Risiko → Aktienkurs bleibt unverändert.\nBei niedrigen Gewinnen fällt EPS durch Verschuldung noch stärker.",
        "Evaluation", "S. 138-141"))

    cards.append(new_card(ch, n, "Trugschluss Verwässerung",
        "Warum ist die Behauptung falsch, Aktienemissionen verwässerten den Aktienkurs?",
        "Aktienemission bringt frisches Kapital: Vermögensgegenstände steigen genauso wie die Anzahl der Aktien.\nFolge: Aktienkurs bleibt unverändert.\nNur bei Investments mit negativem KW kann der Aktienkurs fallen.",
        "Evaluation", "S. 142-144"))

    cards.append(new_card(ch, n, "Nettoverschuldung und Barmittel",
        "Wie wirken Barmittel auf die Kapitalstruktur und wie definiert man Nettoverschuldung?",
        "Barmittel wirken wie 'negatives Fremdkapital': Sie reduzieren das Risiko der Aktiva.\nNettoverschuldung = Fremdkapital − risikolose Aktiva.\nFür die WACC/Beta-Berechnung sollte Nettoverschuldung verwendet werden.",
        "Verständnis", "S. 133"))

    cards.append(new_card(ch, n, "Barmittel Cisco-Beispiel",
        "Wie berechnet man das unverschuldete Asset-Beta bei einem Unternehmen mit hohen Barmitteln? (Cisco 2012)",
        "Cisco: Marktkapitalisierung 102,4 Mrd., FK 16,2 Mrd., Barmittel 48,6 Mrd.\nNettoverschuldung = 16,2 − 48,6 = −32,4 Mrd.\nOperativer Unternehmenswert = 102,4 + (−32,4) = 70 Mrd.\nβ_U = (102,4/70)·1,23 + (−32,4/70)·0 ≈ 1,8",
        "Transfer", "S. 133-134",
        formula="\\beta_U = \\frac{E}{E+D_{netto}} \\cdot \\beta_E + \\frac{D_{netto}}{E+D_{netto}} \\cdot \\beta_D",
        variables={"E": "Marktkapitalisierung", "D_netto": "Nettoverschuldung = FK − Barmittel", "β_E": "Eigenkapital-Beta", "β_D": "Fremdkapital-Beta"},
        solution_steps=["Nettoverschuldung = 16,2 − 48,6 = −32,4 Mrd.", "Op. Unternehmenswert = 102,4 − 32,4 = 70 Mrd.", "β_U = (102,4/70)·1,23 = 1,8"]))

    return cards


def cards_chapter4():
    ch = "Kapitel 4: Marktunvollkommenheiten und Kapitalstruktur"
    n = 4
    cards = []

    cards.append(new_card(ch, n, "Steuervorteil Fremdkapital",
        "Warum schafft Fremdkapital in den meisten Steuersystemen einen Steuervorteil?",
        "Zinszahlungen sind steuerlich abzugsfähig → mindern das zu versteuernde Einkommen ('debt bias').\nFremdfinanzierungsbedingter Steuervorteil = Steuersatz × Zinszahlungen.",
        "Verständnis", "S. 148",
        formula="\\text{Steuervorteil} = \\tau \\cdot r_D \\cdot D",
        variables={"τ": "Unternehmensteuersatz", "r_D": "Fremdkapitalzins", "D": "Fremdkapital"}))

    cards.append(new_card(ch, n, "Macy's Beispiel Steuervorteil",
        "Macy's 2012: EBIT 2,5 Mrd. Euro, Zinsaufwand 430 Mio., Steuersatz 35%. Wie hoch ist der Steuervorteil?",
        "Steuervorteil = 0,35 × 430 Mio. = 150,5 Mio. Euro.\nMit Verschuldung: Gesamtauszahlung an Investoren 1.775 Mio.\nOhne Verschuldung: 1.625 Mio.\nDifferenz 150 Mio. = Steuerersparnis.",
        "Transfer", "S. 149-151",
        solution_steps=["Steuervorteil = τ × Zinszahlungen = 0,35 × 430 = 150,5 Mio. Euro"]))

    cards.append(new_card(ch, n, "Barwert des Steuervorteils",
        "Wie berechnet man den Barwert des fremdfinanzierungsbedingten Steuervorteils bei konstanter Verschuldung?",
        "Bei konstanter, risikoloser Verschuldung D:\nBW(Steuervorteil) = τ·D\nEinfache Formel: Barwert der ewigen Steuerersparnis bei Diskontierung mit Fremdkapitalzins.",
        "Transfer", "S. 152",
        formula="BW(\\text{Steuervorteil}) = \\tau \\cdot D",
        variables={"τ": "Körperschaftsteuersatz", "D": "Verschuldung (konstant und risikolos angenommen)"}))

    cards.append(new_card(ch, n, "Steuern auf Investorenebene",
        "Warum reduzieren Steuern auf Investorenebene den Steuervorteil des Fremdkapitals?",
        "Zinserträge (FK) werden auf Investorenebene oft höher besteuert als Dividenden/Kursgewinne (EK).\nEffektiver Steuervorteil τ* < Unternehmensteuersatz τ.\nBei τ_EK = τ_FK macht Investorenbesteuerung keinen Unterschied.",
        "Verständnis", "S. 153"))

    cards.append(new_card(ch, n, "Optimale Kapitalstruktur mit Steuern",
        "Was wäre bei ausschließlicher Berücksichtigung von Steuern die optimale Kapitalstruktur?",
        "Maximale Verschuldung bis EBIT gerade durch Zinsen gedeckt (τ* voll ausschöpfen).\nIn der Realität verhindert dies die Gefahr von Konkurskosten und Agency-Problemen.",
        "Evaluation", "S. 154"))

    cards.append(new_card(ch, n, "Direkte Konkurskosten",
        "Was sind direkte Konkurskosten und wie hoch sind sie typischerweise?",
        "Direkte Konkurskosten: Anwalts-, Gerichts- und Verwaltungskosten im Insolvenzverfahren.\nTypischerweise 3-5% des Unternehmenswerts; bei Großunternehmen oft höher absolut aber geringer relativ.",
        "Wiedergabe", "S. 155"))

    cards.append(new_card(ch, n, "Indirekte Konkurskosten",
        "Was sind indirekte Konkurskosten? Nennen Sie drei Beispiele.",
        "Verluste, die vor der formellen Insolvenz entstehen:\n1. Kunden: Nichteinhaltung von Gewährleistungen\n2. Lieferanten: Aufkündigung von Verträgen\n3. Talentflucht: Schlüsselpersonal verlässt das Unternehmen\nKönnen 10-20% des Unternehmenswerts ausmachen.",
        "Verständnis", "S. 156-157"))

    cards.append(new_card(ch, n, "Trade-Off-Theorie",
        "Was besagt die Trade-Off-Theorie der Kapitalstruktur?",
        "VL = VU + BW(Steuervorteil) − BW(Konkurskosten)\nOptimale Verschuldung D* = Punkt, wo zusätzliche Steuerersparnis = zusätzliche erwartete Konkurskosten.\nJenseits von D*: Unternehmenswert sinkt.",
        "Verständnis", "S. 159",
        formula="V_L = V_U + BW(\\text{Steuervorteil}) - BW(\\text{Konkurskosten})",
        variables={"V_L": "Wert verschuldetes Unternehmen", "V_U": "Wert unverschuldetes Unternehmen"}))

    cards.append(new_card(ch, n, "Wer trägt Konkurskosten?",
        "Wer trägt letztlich die Konkurskosten, wenn das Unternehmen verschuldet ist?",
        "Die Anteilseigner! Obwohl Konkurskosten im Insolvenzfall die Fremdkapitalgeber treffen, antizipieren diese dies und zahlen von Anfang an weniger für das Fremdkapital → Aktionäre tragen Barwert der Konkurskosten.",
        "Verständnis", "S. 160-161"))

    cards.append(new_card(ch, n, "Asset Substitution",
        "Was ist das Asset-Substitution-Problem (Jensen/Meckling 1976)?",
        "Unternehmen in finanzieller Notlage haben Anreiz, riskantere Projekte zu wählen als vereinbart.\nGrund: Aktionäre profitieren von guten Ergebnissen, Verluste tragen im Extremfall Gläubiger.\n'Heads I win, tails you lose' → übermäßige Risikobereitschaft.",
        "Verständnis", "S. 163-165"))

    cards.append(new_card(ch, n, "Schuldenüberhang (Debt Overhang)",
        "Was ist der Schuldenüberhang (Myers 1977) und warum führt er zu Unterinvestition?",
        "Unternehmen in finanzieller Notlage investieren nicht in profitable Projekte (KW > 0), weil der Großteil der Erträge an die Gläubiger geht.\nFolge: Aktionäre investieren nicht → Unterinvestition → Gesamtwert sinkt.",
        "Verständnis", "S. 166-167"))

    cards.append(new_card(ch, n, "Übermäßige Ausschüttung",
        "Was ist die übermäßige Ausschüttung als Agency-Kosten?",
        "Unternehmen in Notlage: Anreiz für Aktionäre, vor Insolvenz möglichst viel Kapital herauszuziehen (z.B. Verkauf von Vermögenswerten unter Wert + Dividende).\nVerluste fallen auf Gläubiger → Cashing out.",
        "Verständnis", "S. 168"))

    cards.append(new_card(ch, n, "Sperrklinkeneffekt der Verschuldung",
        "Was ist der Leverage Ratchet Effect (Admati et al. 2017)?",
        "Wenn Fremdkapital bereits vorhanden ist:\n• Aktionäre haben Anreiz, Verschuldung zu erhöhen (selbst wenn UW sinkt)\n• Kein Anreiz, Verschuldung zu reduzieren (Fremdkapitalgeber profitieren → nicht attraktiv für Aktionäre)\n→ Verschuldung bleibt dauerhaft hoch.",
        "Verständnis", "S. 170"))

    cards.append(new_card(ch, n, "Agency-Nutzen der Verschuldung",
        "Welche positiven Anreizeffekte kann Verschuldung haben (Agency-Nutzen)?",
        "1. Disziplinierung des Managements: Verschuldung zwingt zu Cash-Flow-Generierung (Jensen 1986: Free Cash Flow)\n2. Reduzierung von Overinvestment: Manager können überschüssige Mittel nicht verschwenden\n3. Signalwirkung: Hohe Verschuldung signalisiert Zuversicht des Managements",
        "Verständnis", "S. 171"))

    cards.append(new_card(ch, n, "Covenants",
        "Was sind Covenants und warum sind sie ein zweischneidiges Schwert?",
        "Covenants: Kreditklauseln, die die Handlungsfreiheit des Kreditnehmers einschränken (z.B. Begrenzung von Ausschüttungen, Art der Investitionen).\nVorteil: Reduzieren Agency-Kosten für Gläubiger.\nNachteil: Können profitable Investitionen verhindern, schränken Flexibilität ein.",
        "Evaluation", "S. 172"))

    cards.append(new_card(ch, n, "Adverse Selektion und Kapitalstruktur (Myers/Majluf)",
        "Wie beeinflusst asymmetrische Information die Wahl zwischen EK und FK? (Pecking Order)",
        "Manager wissen mehr als Markt → EK-Emission signalisiert Überbewertung → Kurs fällt.\nFolge: Unternehmen bevorzugen Innenfinanzierung > FK > EK (Pecking Order Theory).\nErklärung: Kapitalstruktur als Resultat von Informationsasymmetrien.",
        "Verständnis", "S. 175"))

    cards.append(new_card(ch, n, "Pecking Order vs. Trade-Off",
        "Vergleichen Sie die Trade-Off-Theorie mit der Pecking Order Theory der Kapitalstruktur.",
        "Trade-Off: Optimales D*, Balance Steuervorteil vs. Konkurskosten → Unternehmen streben Target Leverage an.\nPecking Order: Keine optimale Zielstruktur, Hierarchie der Finanzierungsquellen: intern > FK > EK. Kapitalstruktur als historischer Zufallspfad.",
        "Synthese", "S. 175-176"))

    return cards


def cards_chapter5():
    ch = "Kapitel 5: Funktionen von Banken"
    n = 5
    cards = []

    cards.append(new_card(ch, n, "Irrelevanz von Banken in vollkommenen Märkten",
        "Warum sind Banken in vollkommenen Kapitalmärkten irrelevant?",
        "In vollkommenen Märkten können die Zahlungsströme eines Bankkredits durch den Kauf/Verkauf geeigneter Wertpapiere repliziert werden.\nKredite und Anleihen sind vollständige Substitute.\n→ Existenz von Banken erfordert Marktfriktionen (Transaktions- oder Informationskosten).",
        "Verständnis", "S. 195"))

    cards.append(new_card(ch, n, "Drei Transformationsfunktionen der Banken",
        "Welche drei Transformationsfunktionen erfüllen Banken (Gurley/Shaw 1960)?",
        "1. Losgrößentransformation: Bündelung kleiner Einlagen zu großen Krediten\n2. Fristentransformation: Kurzfristige Einlagen → langfristige Kredite\n3. Risikotransformation: Riskante Kredite → sichere Einlagen",
        "Wiedergabe", "S. 198"))

    cards.append(new_card(ch, n, "Fristentransformation und Risiken",
        "Welche zwei Risiken entstehen aus der Fristentransformation von Banken?",
        "1. Liquiditätsrisiko/Bank-Run-Gefahr: Bank ist illiquide (Diamond/Dybvig 1983)\n2. Zinsänderungsrisiko: Wenn sich kurzfristige Zinsen stärker ändern als langfristige (z.B. Savings & Loans USA 1980er)",
        "Verständnis", "S. 200"))

    cards.append(new_card(ch, n, "Diamond-Dybvig Modell – Grundidee",
        "Was ist die Grundidee des Diamond-Dybvig-Modells (1983) zur Erklärung von Banken?",
        "Haushalte wissen nicht, wann sie konsumieren (Liquiditätsschocks: frühe/späte Konsumenten).\nLangfristige Investitionen: hoher Ertrag R, aber keine vorzeitige Liquidation ohne Verlust.\nBank bietet Einlagenvertrag mit jederzeitiger Abhebemöglichkeit → versichert gegen Liquiditätsrisiko.\n→ Fristentransformation erhöht Wohlfahrt gegenüber Marktlösung.",
        "Verständnis", "S. 203-205"))

    cards.append(new_card(ch, n, "DD-Modell: Drei Perioden",
        "Beschreiben Sie die drei Perioden im Diamond-Dybvig-Modell.",
        "t=0: Konsumenten investieren Anfangsausstattung (1 Einheit)\nt=1: Erfahren Typ (früh/spät); frühe Konsumenten lösen ab\nt=2: Langfristiges Projekt fällig; späte Konsumenten konsumieren\nProduktionen: Lagerung (1→1 in t+1) und Langfristprojekt (1→R>1 in t=2, oder L<1 bei vorzeitiger Liquidation)",
        "Verständnis", "S. 206-207"))

    cards.append(new_card(ch, n, "DD-Modell: Autarkie vs. Markt vs. Bank",
        "Warum ist die Banklösung im DD-Modell besser als Autarkie und Marktlösung?",
        "Autarkie: Ineffiziente Investitionsentscheidungen ex ante, da Typ unbekannt\nMarkt: C1=1, C2=R (keine Konsumglättung)\nBank (First-best): C1*>1, C2*<R (Versicherung gegen Liquiditätsschocks durch Konsumglättung)\nBank besser wegen Risikoaversion der Konsumenten und Gesetz der Großen Zahlen.",
        "Evaluation", "S. 210-214"))

    cards.append(new_card(ch, n, "DD-Modell: Optimalitätsbedingung",
        "Wie lautet die Bedingung erster Ordnung (FOC) für die pareto-optimale Allokation im DD-Modell?",
        "Sozialer Planer maximiert: π1·u(C1) + π2·ρ·u(C2)\nFOC: u'(C1*) = ρ·R·u'(C2*)\nMarktlösung (C1=1, C2=R) verletzt diese Bedingung bei starker Risikoaversion.\n→ C1* > 1, C2* < R: Konsumglättung optimal.",
        "Transfer", "S. 211-212",
        formula="u'(C_1^*) = \\rho R \\cdot u'(C_2^*)",
        variables={"C1*": "Optimaler Konsum früher Typ", "C2*": "Optimaler Konsum später Typ", "ρ": "Diskontfaktor", "R": "Ertrag langfristige Investition"}))

    cards.append(new_card(ch, n, "DD-Modell: Implementierung",
        "Wie implementiert die Bank im DD-Modell die First-best-Lösung?",
        "Bank bietet Einlagenvertrag mit r1 = C1* (Auszahlung in t=1).\nBank investiert π1·C1* in Lagerhaltung (für frühe Konsumenten) und Rest in langfristiges Projekt.\nGutes Gleichgewicht: Typ-1 hebt in t=1 ab, Typ-2 wartet → First-best erreicht.",
        "Verständnis", "S. 215-216"))

    cards.append(new_card(ch, n, "Diamond-Dybvig: Kritik",
        "Was sind die zentralen Schwächen des Diamond-Dybvig-Modells?",
        "1. Aktivseite der Bank nicht modelliert (keine Kreditrisiken)\n2. Projekte risikolos → keine Risikotransformation\n3. Ergebnisse abhängig von fehlenden Wertpapiermärkten (Jacklin 1987)\n4. Einlagen keine Zahlungsmittel → keine Aussage über Zahlungssystemfunktion",
        "Evaluation", "S. 217"))

    cards.append(new_card(ch, n, "Delegierte Kontrolle – Diamond 1984",
        "Was ist die Grundidee der delegierten Kontrolle (Diamond 1984) und warum benötigt man Intermediäre?",
        "Unternehmer können Erträge verbergen (Costly State Verification, Gale/Hellwig 1985).\nKontrolle durch Kapitalgeber nötig, aber kostspielig.\nBank übernimmt stellvertretend die Kontrolle ('delegierte Kontrolle').\nProbleme: Wer kontrolliert den Kontrolleur? → Lösung: Diversifikation reduziert Kontrollkosten gegen null.",
        "Verständnis", "S. 220-222"))

    cards.append(new_card(ch, n, "Delegierte Kontrolle: Informationsproblem",
        "Welches Informationsproblem liegt im Diamond-1984-Modell vor und welche Vertragsform löst es?",
        "Costly State Verification: Kapitalgeber kann Ertrag nur kostenpflichtig beobachten.\nOptimaler Vertrag: Standardkreditvertrag mit nichtmonetären Strafen bei Zahlungsausfall.\nKreditvertrag als anreizkompatible Lösung des Verifikationsproblems.",
        "Verständnis", "S. 223"))

    cards.append(new_card(ch, n, "Losgrößentransformation",
        "Wie erfüllen Banken und Kapitalmärkte die Losgrößentransformation unterschiedlich?",
        "Banken: Pooling kleiner Einlagen zu großen Krediten (Intermediation).\nMärkte: Stückelung in handelbare Wertpapieranteile, aber Mindestgebühren können sehr kleine Beträge unattraktiv machen.",
        "Verständnis", "S. 201"))

    return cards


def cards_chapter6():
    ch = "Kapitel 6: Finanzkrisen und systemische Risiken"
    n = 6
    cards = []

    cards.append(new_card(ch, n, "Das Grundproblem der Banken",
        "Was ist das fundamentale Stabilitätsproblem von Banken, das aus ihrer Struktur entsteht?",
        "Banken sind illiquide (Fristentransformation): Langfristige Aktiva, kurzfristige Passiva.\nSie sind solvent aber illiquide → vulnerable für Bank Runs.\nBank Run = sich selbst erfüllende Erwartung: Wenn alle abziehen, gibt es nicht genug Liquidität.",
        "Verständnis", "S. 230"))

    cards.append(new_card(ch, n, "Bank Run im DD-Modell",
        "Wie entsteht ein Bank Run als schlechtes Gleichgewicht im DD-Modell?",
        "Wenn alle Typ-2-Einleger erwarten, dass alle anderen ebenfalls abziehen, ist es auch für sie optimal abzuziehen.\nBank muss alle Projekte vorzeitig liquidieren → Ertrag L < 1 → nicht genug für alle.\nBank Run = selbsterfüllende Prophezeiung, selbst wenn Bank solvent wäre.",
        "Verständnis", "S. 231"))

    cards.append(new_card(ch, n, "Narrow Banking",
        "Was ist Narrow Banking und wie löst es das Bank-Run-Problem?",
        "Narrow Banking: Trennbanksystem, bei dem Einlagen nur in risikolose Aktiva (z.B. Staatsanleihen) angelegt werden dürfen.\nFolge: Bank kann immer alle Einlagen zurückzahlen → kein Bank Run möglich.\nKritik: Kreditvergabefunktion fehlt → weniger Finanzintermediation.",
        "Evaluation", "S. 232"))

    cards.append(new_card(ch, n, "Einlagenversicherung",
        "Wie löst eine Einlagenversicherung das Bank-Run-Problem und was sind ihre Nachteile?",
        "Versicherung garantiert Einlagen → Einleger haben keinen Anreiz zum Abzug → kein Run-Gleichgewicht mehr.\nVorteil: Eliminiert schlechtes Gleichgewicht.\nNachteile: Moral Hazard (Banken nehmen mehr Risiken, weil Einleger nicht mehr kontrollieren), Finanzierung durch Steuerzahler.",
        "Evaluation", "S. 234"))

    cards.append(new_card(ch, n, "Aufhebung der Konvertibilität",
        "Was ist die Aufhebung der Konvertibilität als Mittel gegen Bank Runs?",
        "Bank kann vorübergehend Abhebungen sperren ('Bankfeiertag') oder begrenzen.\nVorteil: Schlechtes Gleichgewicht wird aufgebrochen.\nNachteil: Erhebliche realwirtschaftliche Kosten (Zahlungsverkehr gesperrt), Vertrauensverlust.",
        "Verständnis", "S. 233"))

    cards.append(new_card(ch, n, "Effiziente Bank Runs",
        "Wann können Bank Runs effizient sein (Gorton/Pennacchi, Calomiris/Kahn)?",
        "Manche Modelle zeigen: Bank Runs können als Disziplinierungsinstrument funktionieren.\nEinleger, die früh Informationen über schlechte Bankperformance erhalten, lösen Run aus → Bank wird diszipliniert.\nProblem: Kontagion trifft auch solvente Banken → systemisches Risiko.",
        "Evaluation", "S. 235"))

    cards.append(new_card(ch, n, "Ansteckungseffekte",
        "Durch welche Kanäle können Bankenprobleme auf andere Banken übergreifen (Ansteckung)?",
        "1. Interbankenmarkt: Direkter Ausfall von Forderungen\n2. Fire Sales: Erzwungener Verkauf → Preisverfall trifft alle mit ähnlichen Aktiva\n3. Informationskontagion: Einleger können nicht unterscheiden, welche Banken gesund sind → Run auf alle\n4. Gegenparteirisiken (z.B. über CDS)",
        "Verständnis", "S. 236-237"))

    cards.append(new_card(ch, n, "Lender of Last Resort (LoLR)",
        "Was ist der Lender of Last Resort und wie begründet Bagehot seine Rolle?",
        "LoLR = Zentralbank als letzte Kreditquelle für illiquide aber solvente Banken.\nBagehot-Regel: In der Krise großzügig leihen, aber gegen gute Sicherheiten und zu Strafzins.\nZweck: Liquiditätspaniken stoppen, ohne Insolvenzbanken zu retten (moral hazard vermeiden).",
        "Verständnis", "S. 238"))

    cards.append(new_card(ch, n, "LoLR in der Praxis",
        "Warum ist die Umsetzung der Bagehot-Regel in Krisen schwierig?",
        "In Krisen schwer zu unterscheiden, ob Bank illiquide oder insolvent ist.\nStrafzins-Bedingung oft nicht umsetzbar (würde geschwächte Banken zusätzlich belasten).\nGute Sicherheiten oft nicht vorhanden → praktisch: Zentralbank muss breiter unterstützen.",
        "Evaluation", "S. 239"))

    cards.append(new_card(ch, n, "Too-big-to-fail (TBTF)",
        "Was versteht man unter dem Too-big-to-fail-Phänomen und welche Probleme erzeugt es?",
        "Große Banken werden im Krisenfall gerettet, weil ihr Zusammenbruch das gesamte System gefährdet.\nProbleme:\n1. Moral Hazard: TBTF-Banken gehen mehr Risiken ein\n2. Wettbewerbsverzerrung: Implizite Staatsgarantie = günstiger Refinanzierungsvorteil\n3. Politisches Problem: Privatisierung der Gewinne, Sozialisierung der Verluste",
        "Verständnis", "S. 240-241"))

    cards.append(new_card(ch, n, "Maßnahmen gegen TBTF",
        "Welche regulatorischen Maßnahmen wurden eingeführt, um das TBTF-Problem zu adressieren?",
        "1. Höhere Eigenkapitalanforderungen für systemrelevante Banken (G-SIBs)\n2. Abwicklungsregime (Bail-in statt Bail-out): Verluste auf Aktionäre und Gläubiger\n3. Abwicklungspläne ('living wills')\n4. Strukturelle Trennung riskanter Aktivitäten",
        "Verständnis", "S. 241"))

    cards.append(new_card(ch, n, "Systemisches Risiko – Definition",
        "Was ist systemisches Risiko und warum ist es ein Marktversagen?",
        "Systemisches Risiko: Risiko des Zusammenbruchs des gesamten Finanzsystems oder wesentlicher Teile davon.\nMarktversagen: Einzelne Institutionen internalisieren die Kosten ihres Zusammenbruchs für andere nicht (negative Externalität).\n→ Begründung für makroprudenzielle Regulierung.",
        "Verständnis", "S. 230"))

    return cards


def cards_chapter7():
    ch = "Kapitel 7: Bankenregulierung"
    n = 7
    cards = []

    cards.append(new_card(ch, n, "Arten der Bankenregulierung",
        "Nennen Sie die wichtigsten Arten der Bankenregulierung in Deutschland/Europa.",
        "1. Marktzutrittsbarrieren (Zulassung, Lizenz)\n2. Eigenkapitalregulierung (Basel I, II, III)\n3. Liquiditätsregulierung (LCR, NSFR)\n4. Begrenzung von Großkrediten\n5. Einlagensicherungssysteme\n6. Spezielle Abwicklungsregime\n7. Verbraucherschutz",
        "Wiedergabe", "S. 248"))

    cards.append(new_card(ch, n, "Aufsichtsbehörden",
        "Welche Behörden beaufsichtigen Banken in Deutschland und Europa?",
        "National: BaFin und Deutsche Bundesbank.\nEuropäisch: EZB (Einheitlicher Aufsichtsmechanismus SSM seit November 2014).\nEZB beaufsichtigt direkt die bedeutenden Banken (significant institutions).",
        "Wiedergabe", "S. 248"))

    cards.append(new_card(ch, n, "Basel I",
        "Was war das Wesentliche von Basel I (1988)?",
        "Erstes internationales Abkommen zur Eigenkapitalregulierung (Basler Ausschuss für Bankenaufsicht).\nMindest-EK-Quote: 8% der risikogewichteten Aktiva (RWA).\nRisikogewichtung: 4 Kategorien (0%, 20%, 50%, 100%).\nKritik: Grobe Risikogewichtung, keine Marktrisiken.",
        "Wiedergabe", "S. 250"))

    cards.append(new_card(ch, n, "Basel II",
        "Was sind die drei Säulen von Basel II?",
        "Säule 1: Mindestkapitalanforderungen (Kredit-, Markt- und operationelle Risiken)\nSäule 2: Aufsichtlicher Überprüfungsprozess (SREP)\nSäule 3: Marktdisziplin (Offenlegungspflichten)\nNeu: Interne Modelle (IRB-Ansatz) für Kreditrisiken.",
        "Wiedergabe", "S. 251"))

    cards.append(new_card(ch, n, "Kritik an Basel II / Prozyklizität",
        "Warum ist Basel II prozyklisch und warum ist das problematisch?",
        "Interne Risikomodelle basieren auf historischen Daten → In Boom-Phase: niedrige PDs, niedrige EK-Anforderungen.\nIn Krise: PDs steigen → EK-Anforderungen steigen → Banken müssen Kredite einschränken → Krise verschärft.\nProzyklizität verstärkt Konjunkturzyklen.",
        "Evaluation", "S. 252"))

    cards.append(new_card(ch, n, "Basel III – Überblick",
        "Was sind die wesentlichen Neuerungen von Basel III im Vergleich zu Basel II?",
        "1. Höhere Qualität des Eigenkapitals (mehr hartes Kernkapital CET1)\n2. Höhere EK-Quote (4,5% CET1, 6% Tier-1, 8% Gesamt)\n3. Kapitalerhaltungspuffer (+2,5%) und antizyklischer Puffer (0-2,5%)\n4. Leverage Ratio (nicht-risikobasiert)\n5. Liquiditätsanforderungen: LCR und NSFR\n6. Systemzuschläge für G-SIBs",
        "Wiedergabe", "S. 253-255"))

    cards.append(new_card(ch, n, "Eigenkapital-Mindestquoten Basel III",
        "Wie hoch sind die Mindest-EK-Quoten unter Basel III?",
        "CET1 (hartes Kernkapital): 4,5% der RWA\nTier-1-Kapital: 6% der RWA\nGesamtkapital: 8% der RWA\n+ Kapitalerhaltungspuffer: 2,5% (CET1) = effektiv 7% CET1\n+ Antizyklischer Puffer: 0-2,5%\n+ G-SIB-Zuschlag: 1-3,5%",
        "Wiedergabe", "S. 254",
        formula="\\text{Eigenkapitalquote} = \\frac{\\text{Eigenkapital}}{\\text{Risikogewichtete Aktiva (RWA)}}",
        variables={"EK": "Eigenkapital (CET1, Tier-1, o. Gesamt)", "RWA": "Risikogewichtete Aktiva"}))

    cards.append(new_card(ch, n, "Leverage Ratio",
        "Was ist die Leverage Ratio und warum wurde sie in Basel III eingeführt?",
        "Leverage Ratio = EK / Gesamtexposition (nicht risikogewichtet).\nMindestwert: 3% (Tier-1-Kapital).\nZweck: Begrenzung des absoluten Verschuldungsgrads, unabhängig von Risikomodellen.\nVerhindert exzessive Verschuldung auch bei formal niedrigen RWA.",
        "Verständnis", "S. 255",
        formula="\\text{Leverage Ratio} = \\frac{\\text{Tier-1-Kapital}}{\\text{Gesamtexposition}} \\geq 3\\%",
        variables={"Tier-1-Kapital": "Hartes und weiches Kernkapital", "Gesamtexposition": "Alle Aktiva inkl. außerbilanzielle Posten (nicht risikogewichtet)"}))

    cards.append(new_card(ch, n, "LCR und NSFR",
        "Was messen LCR und NSFR und warum wurden sie eingeführt?",
        "LCR (Liquidity Coverage Ratio): Kurzfristige Liquidität; Bank muss genug hochliquide Aktiva haben, um 30-Tage-Nettoabflüsse zu decken. ≥ 100%.\nNSFR (Net Stable Funding Ratio): Strukturelle Liquidität; stabile langfristige Refinanzierung für illiquide Aktiva. ≥ 100%.\nZweck: Verhindert übermäßige Fristentransformation.",
        "Verständnis", "S. 256",
        formula="LCR = \\frac{\\text{HQLA}}{\\text{Nettoabflüsse in 30 Tagen}} \\geq 100\\%",
        variables={"HQLA": "High Quality Liquid Assets (hochliquide Aktiva)", "Nettoabflüsse": "Erwartete Abflüsse minus Zuflüsse in Stressszenario"}))

    cards.append(new_card(ch, n, "Makroprudenzielle Regulierung",
        "Was ist makroprudenzielle Regulierung und wie unterscheidet sie sich von mikroprudenzieller?",
        "Mikroprudenziell: Stabilität einzelner Institute (Institution-by-Institution).\nMakroprudenziell: Stabilität des gesamten Finanzsystems; systemische Risiken und Ansteckungseffekte.\nInstrumente: Antizyklischer Kapitalerhaltungspuffer, Systemrisikowarnungen, Begrenzung von LTV-Quoten im Immobilienbereich.",
        "Verständnis", "S. 257"))

    cards.append(new_card(ch, n, "Argumente gegen hohe EK-Anforderungen",
        "Welche Argumente bringen Banken gegen hohe Eigenkapitalanforderungen vor und warum sind sie (teils) falsch?",
        "Argument: Mehr EK → höhere Kapitalkosten → weniger Kreditvergabe.\nGegenargument (Modigliani-Miller): In vollkommenen Märkten keine teuerere Finanzierung durch mehr EK, da r_E sinkt.\nIn der Realität: Steuervorteil FK, implizite Subventionen durch TBTF. Aber MM-Argument zeigt, dass EK nicht prinzipiell teurer ist.",
        "Evaluation", "S. 258"))

    cards.append(new_card(ch, n, "Schattenbanken und Regulierungsarbitrage",
        "Was sind Schattenbanken und warum entstehen sie als Reaktion auf Bankenregulierung?",
        "Schattenbanken: Finanzintermediäre außerhalb der klassischen Bankenregulierung (Hedgefonds, Geldmarktfonds, SPVs).\nEntstehung: Regulierungsarbitrage – Aktivitäten werden in weniger regulierte Bereiche verlagert.\nGefahr: Systemisches Risiko ohne Regulierungsschutz (keine Einlagenversicherung, kein LoLR).",
        "Verständnis", "S. 259"))

    cards.append(new_card(ch, n, "Bankenunion Europa",
        "Was sind die drei Säulen der Europäischen Bankenunion?",
        "1. Einheitlicher Aufsichtsmechanismus (SSM): EZB beaufsichtigt bedeutende Banken\n2. Einheitlicher Abwicklungsmechanismus (SRM): Gemeinsame Abwicklungsregeln und -behörde (SRB) + Fonds (SRF)\n3. Europäische Einlagenversicherung (EDIS): noch nicht vollständig umgesetzt",
        "Verständnis", "S. 260"))

    return cards


def cards_querschnitt():
    """Wahr/Falsch Karten und Klausuraufgaben"""
    ch = "Querschnitt: Wahr/Falsch & Klausuraufgaben"
    n = 99
    cards = []

    wf = [
        ("In einem vollkommenen Kapitalmarkt steigt der Unternehmenswert mit dem Verschuldungsgrad.",
         "FALSCH. Laut MMT I ist der Unternehmenswert in einem vollkommenen Markt unabhängig von der Kapitalstruktur.",
         "S. 112"),
        ("Eine höhere Verschuldung erhöht die Eigenkapitalkosten, lässt aber die WACC unverändert.",
         "WAHR. Nach MMT II steigen r_E mit D/E, aber WACC = r_U = konstant, da der höhere EK-Kostenbeitrag durch den größeren FK-Anteil ausgeglichen wird.",
         "S. 124-126"),
        ("Concurskosten werden letztlich von den Fremdkapitalgebern getragen.",
         "FALSCH. Obwohl Konkurskosten im Insolvenzfall die Gläubiger treffen, antizipieren diese es und zahlen weniger → Aktionäre tragen den Barwert.",
         "S. 160-161"),
        ("Banken sind in vollkommenen Kapitalmärkten irrelevant.",
         "WAHR. In vollkommenen Märkten können alle Zahlungsströme einer Bank durch Wertpapiere repliziert werden (MM-Argument).",
         "S. 195"),
        ("Die LCR misst die strukturelle langfristige Liquidität von Banken.",
         "FALSCH. LCR = kurzfristige Liquidität (30 Tage). NSFR = strukturelle/langfristige Liquidität.",
         "S. 256"),
        ("Der Sperrklinkeneffekt (Leverage Ratchet) erklärt, warum Banken freiwillig Eigenkapital aufbauen.",
         "FALSCH. Der Sperrklinkeneffekt erklärt das Gegenteil: Aktionäre haben keinen Anreiz, Verschuldung zu reduzieren, weil sie den Vorteil primär den Gläubigern zugutekäme.",
         "S. 170"),
        ("Homemade Leverage ist nur dann ein perfekter Ersatz, wenn der Investor zum gleichen Zinssatz leihen kann wie das Unternehmen.",
         "WAHR. Bei unterschiedlichen Zinssätzen (z.B. persönliche Kredite teurer) ist Homemade Leverage kein perfekter Ersatz.",
         "S. 115"),
        ("Das OMT-Programm der EZB wurde während der Eurokrise mehrfach eingesetzt.",
         "FALSCH. Das OMT-Programm wurde angekündigt (Sept 2012), aber nie eingesetzt. Die bloße Ankündigung reichte, um die Märkte zu beruhigen.",
         "S. 88"),
        ("Im Diamond-Dybvig-Modell ist ein Bank Run immer irrational.",
         "FALSCH. Ein Bank Run kann ein rationales Gleichgewicht sein: Wenn alle erwarten, dass andere abziehen, ist es für jeden rational abzuziehen (selbsterfüllende Erwartung).",
         "S. 231"),
        ("Ein Schuldenüberhang führt zur Überinvestition.",
         "FALSCH. Schuldenüberhang (Myers 1977) führt zu UNTERINVESTITION: Aktionäre investieren nicht, weil Erträge primär Gläubigern zugutekommen.",
         "S. 166-167"),
    ]

    for q, a, ref in wf:
        cards.append(new_card(ch, n, "Wahr/Falsch",
            f"Wahr oder Falsch: {q}",
            a, "Evaluation", ref, "true_false"))

    # Rechenaufgaben
    cards.append(new_card(ch, n, "Kapitalwert-Berechnung",
        "Ein Projekt erfordert eine Anfangsinvestition von 1.000 Euro. Es erzielt mit Wahrscheinlichkeit 60% einen Ertrag von 1.500 Euro und mit 40% einen Ertrag von 800 Euro. Der risikolose Zins beträgt 3%, die Risikoprämie 7%. Ist das Projekt lohnend?",
        "Erwarteter Ertrag = 0,6·1500 + 0,4·800 = 900 + 320 = 1.220 Euro\nKapitalkosten = 3% + 7% = 10%\nKW = −1.000 + 1.220/1,10 = −1.000 + 1.109,09 = +109,09 Euro\n→ Projekt lohnend (KW > 0).",
        "Transfer", "S. 106",
        formula="KW = -I_0 + \\frac{E[CF]}{1+r}",
        variables={"I_0": "1.000 Euro", "E[CF]": "1.220 Euro", "r": "10%"},
        solution_steps=["E[CF] = 0,6·1500 + 0,4·800 = 1.220 Euro", "r = 3% + 7% = 10%", "KW = -1000 + 1220/1,10 = 109,09 Euro"]))

    cards.append(new_card(ch, n, "MMT II – Eigenkapitalkosten berechnen",
        "Ein Unternehmen hat einen Verschuldungsgrad D/E = 1, Fremdkapitalkosten von 6% und Eigenkapitalkosten des unverschuldeten Unternehmens von 12%. Wie hoch sind die Eigenkapitalkosten des verschuldeten Unternehmens?",
        "Laut MMT II: r_E = r_U + (D/E)·(r_U − r_D)\nr_E = 12% + 1·(12% − 6%) = 12% + 6% = 18%",
        "Transfer", "S. 124",
        formula="r_E = r_U + \\frac{D}{E}(r_U - r_D)",
        variables={"r_U": "12%", "r_D": "6%", "D/E": "1"},
        solution_steps=["r_E = 12% + 1·(12% − 6%)", "r_E = 12% + 6% = 18%"]))

    cards.append(new_card(ch, n, "WACC berechnen",
        "Eigenkapital E = 600 Mio., Fremdkapital D = 400 Mio., r_E = 15%, r_D = 5%. Berechnen Sie die WACC.",
        "WACC = (E/(E+D))·r_E + (D/(E+D))·r_D\n= (600/1000)·15% + (400/1000)·5%\n= 0,6·15% + 0,4·5%\n= 9% + 2% = 11%",
        "Transfer", "S. 125",
        formula="r_{WACC} = \\frac{E}{E+D} \\cdot r_E + \\frac{D}{E+D} \\cdot r_D",
        variables={"E": "600 Mio.", "D": "400 Mio.", "r_E": "15%", "r_D": "5%"},
        solution_steps=["WACC = (600/1000)·15% + (400/1000)·5%", "= 9% + 2% = 11%"]))

    cards.append(new_card(ch, n, "Steuervorteil berechnen",
        "Ein Unternehmen hat Fremdkapital D = 200 Mio., Fremdkapitalzins r_D = 5%, Körperschaftsteuersatz τ = 30%. Berechnen Sie den jährlichen Steuervorteil und seinen Barwert (bei konstanter Verschuldung).",
        "Jährlicher Steuervorteil = τ·r_D·D = 0,30·0,05·200 = 3 Mio. Euro\nBW(Steuervorteil) = τ·D = 0,30·200 = 60 Mio. Euro",
        "Transfer", "S. 149-152",
        formula="\\text{Jährl. Steuervorteil} = \\tau \\cdot r_D \\cdot D; \\quad BW = \\tau \\cdot D",
        variables={"τ": "0,30", "r_D": "5%", "D": "200 Mio. Euro"},
        solution_steps=["Jährlicher Steuervorteil = 0,30·0,05·200 = 3 Mio.", "BW = τ·D = 0,30·200 = 60 Mio."]))

    cards.append(new_card(ch, n, "Beta entlevern und relevern",
        "CVS hat β_E = 0,8, D/E = 0,1, β_D ≈ 0. Wie hoch ist β_U? Wie hoch wäre β_E wenn D/E auf 0,5 steigt?",
        "β_U = β_E · E/(E+D) = 0,8 · (10/11) ≈ 0,727\nNeues β_E: β_E = β_U + (D/E)·(β_U − β_D) = 0,727 + 0,5·0,727 ≈ 1,09",
        "Transfer", "S. 131",
        formula="\\beta_U = \\frac{E}{E+D}\\beta_E + \\frac{D}{E+D}\\beta_D",
        variables={"β_E": "0,8", "D/E": "0,1 dann 0,5", "β_D": "0"},
        solution_steps=["β_U = 0,8·(10/11) + 0·(1/11) ≈ 0,727", "Neues β_E = 0,727 + 0,5·(0,727−0) ≈ 1,09"]))

    cards.append(new_card(ch, n, "Eigenkapitalkosten CAPM",
        "Ein Wertpapier hat β = 1,5, risikoloser Zins = 2%, Marktrisikoprämie = 5%. Berechnen Sie die erwartete Rendite.",
        "r = risikoloser Zins + β·Marktrisikoprämie = 2% + 1,5·5% = 2% + 7,5% = 9,5%",
        "Transfer", "S. 130",
        formula="r_I = r_f + \\beta_I \\cdot (r_M - r_f)",
        variables={"r_f": "2% (risikoloser Zins)", "β_I": "1,5", "r_M - r_f": "5% (Marktrisikoprämie)"},
        solution_steps=["r = 2% + 1,5·5% = 9,5%"]))

    return cards


def cards_chapter4_steuern_detail():
    """Kap 4.1.2–4.1.5: Rekapitalisierung, Investorensteuern, Optimale Kapitalstruktur mit Steuern"""
    ch = "Kapitel 4: Marktunvollkommenheiten und Kapitalstruktur"
    n = 4
    cards = []

    # 4.1.2 Rekapitalisierung
    cards.append(new_card(ch, n, "Gehebelte Rekapitalisierung",
        "Was ist eine gehebelte Rekapitalisierung und wie erhöht sie den Unternehmenswert?",
        "Gehebelte Rekapitalisierung: Das Unternehmen nimmt Fremdkapital auf und kauft damit eigene Aktien zurück (Aktienrückkauf).\nDadurch steigt der Verschuldungsgrad, und der fremdfinanzierungsbedingte Steuervorteil erhöht den Unternehmenswert.\nVL = VU + τ·D",
        "Verständnis", "S. 219"))

    cards.append(new_card(ch, n, "Midco-Beispiel: Steuervorteil bei Rekapitalisierung",
        "Midco Industries: VU = 300 Mio. Euro, D = 100 Mio., τ = 35%. Wie hoch ist VL und was erhalten die Aktionäre insgesamt?",
        "BW(Steuervorteil) = τ·D = 0,35·100 = 35 Mio. Euro\nVL = VU + 35 = 335 Mio. Euro\nE = VL − D = 335 − 100 = 235 Mio. Euro\nAktionäre erhalten: 235 Mio. (verbleibende Aktien) + 100 Mio. (Rückkauf) = 335 Mio. Euro\n→ Gesamtgewinn = 35 Mio. Euro = Barwert des Steuervorteils",
        "Transfer", "S. 220-221",
        formula="V_L = V_U + \\tau \\cdot D",
        variables={"V_U": "300 Mio. Euro", "τ": "35%", "D": "100 Mio. Euro"},
        solution_steps=["BW(TV) = 0,35 × 100 = 35 Mio.", "VL = 300 + 35 = 335 Mio.", "E = 335 − 100 = 235 Mio."]))

    cards.append(new_card(ch, n, "Arbitragefreie Bewertung beim Aktienrückkauf",
        "Warum steigt der Aktienkurs bei Ankündigung einer Rekapitalisierung sofort – noch vor dem Rückkauf?",
        "Sobald die Investoren von der Rekapitalisierung erfahren, kaufen sie Aktien (Arbitrage): Sie kaufen für 15 Euro und verkaufen nach dem Rückkauf zu einem höheren Preis.\nFolge: Kurs steigt sofort auf den Wert, der den Steuervorteil einschließt.\nNeuer Kurs = VL / Anzahl Aktien = 335 / 20 = 16,75 Euro (nicht erst nach dem Rückkauf).",
        "Verständnis", "S. 224-226"))

    cards.append(new_card(ch, n, "Mindestpreis beim Aktienrückkauf",
        "Zu welchem Mindestpreis müssen Aktionäre beim Rückkauf bereit sein, ihre Aktien zu verkaufen?",
        "Aktionär verkauft nur, wenn Angebotspreis ≥ Kurs nach dem Rückkauf.\nBei Midco: Mindestpreis = 16,75 Euro (entspricht VL/Aktien = 335/20).\nBei höherem Angebotspreis profitieren die verkaufenden Aktionäre stärker.\n→ Bei fairem Preis profitieren alle Altaktionäre gleichmäßig vom Steuervorteil (1,75 Euro je Aktie × 20 Mio. = 35 Mio.).",
        "Verständnis", "S. 227-229"))

    # 4.1.3 Steuern auf Investorenebene
    cards.append(new_card(ch, n, "Steuern auf Investorenebene – Grundprinzip",
        "Warum reduzieren Steuern auf Investorenebene den Steuervorteil des Fremdkapitals?",
        "Zinserträge (FK) und Dividenden/Kursgewinne (EK) werden auf Investorenebene besteuert.\nWenn Zinsen höher besteuert werden als EK-Erträge (τ_i > τ_e), mindert das den Vorteil der steuerlichen Abzugsfähigkeit von Zinsen auf Unternehmensebene.\nFolge: Effektiver Steuervorteil τ* < Körperschaftsteuersatz τ_c.",
        "Verständnis", "S. 232-234"))

    cards.append(new_card(ch, n, "Cashflows nach Steuern: FK vs. EK",
        "Berechnen Sie die Cashflows nach Steuern für FK und EK bei τ_c = 35%, τ_i = 35%, τ_e = 15%.",
        "An Fremdkapitalgeber: (1 − τ_i) = 1 − 0,35 = 0,65 Euro\nAn Eigenkapitalgeber: (1 − τ_c)·(1 − τ_e) = 0,65·0,85 = 0,5525 Euro\nSteuervorteil FK = 0,65 − 0,5525 = 0,0975, relativ: 0,0975/0,65 ≈ 15%\n→ Effektiver Steuervorteil τ* = 15% (statt 35% ohne Investorensteuern).",
        "Transfer", "S. 235-237",
        solution_steps=["FK-Cashflow: 1 − 0,35 = 0,65", "EK-Cashflow: 0,65 × 0,85 = 0,5525", "τ* = (0,65 − 0,5525)/0,65 ≈ 15%"]))

    cards.append(new_card(ch, n, "Formel effektiver Steuervorteil τ*",
        "Wie lautet die Formel für den effektiven fremdfinanzierungsbedingten Steuervorteil τ* unter Berücksichtigung der Investorensteuern?",
        "τ* = [1 − (1 − τ_c)(1 − τ_e)] / (1 − τ_i) = 1 − (1 − τ_c)(1 − τ_e)/(1 − τ_i)\nSpezialfall: Wenn τ_i = τ_e → τ* = τ_c (Investorensteuern heben sich auf).\nWenn τ_e < τ_i (EK-Erträge günstiger besteuert) → τ* < τ_c.",
        "Verständnis", "S. 240-241",
        formula="\\tau^* = 1 - \\frac{(1-\\tau_c)(1-\\tau_e)}{1-\\tau_i}",
        variables={"τ_c": "Körperschaftsteuersatz", "τ_i": "Steuersatz auf Zinserträge (FK)", "τ_e": "Steuersatz auf EK-Erträge (Dividenden/Kursgewinne)"}))

    cards.append(new_card(ch, n, "Deutsches Steuersystem und τ*",
        "Wie hoch ist der effektive Steuervorteil τ* in Deutschland mit der Abgeltungssteuer?",
        "In Deutschland: Abgeltungssteuer 25% + Solidaritätszuschlag = τ_i = τ_e ≈ 26,38%.\nDa τ_i = τ_e, vereinfacht sich τ* auf: τ* = τ_c = Körperschaftsteuersatz (ca. 30%).\nAber: Beachte die Gewerbesteuer → Gesamtbelastung auf Unternehmensebene ca. 30-33%.\nBerechnung: τ* = 1 − (1 − τ_c)(1 − τ_e)/(1 − τ_i) ≈ 1 − (1 − τ_c) = τ_c ≈ 30%.",
        "Verständnis", "S. 238-239"))

    cards.append(new_card(ch, n, "Unternehmenswert mit Investorensteuern",
        "Wie lautet die Formel für VL mit Investorensteuern und was ändert sich gegenüber VL = VU + τ_c·D?",
        "Mit Investorensteuern: VL = VU + τ*·D\nτ* ≤ τ_c, daher ist der Steuervorteil geringer als ohne Investorensteuern.\nAber typischerweise gilt τ* > 0, d.h. der Steuervorteil verschwindet nicht vollständig.",
        "Verständnis", "S. 243",
        formula="V_L = V_U + \\tau^* \\cdot D",
        variables={"τ*": "Effektiver Steuervorteil (inkl. Investorensteuern)", "D": "Verschuldung (konstant)"}))

    # 4.1.4 Optimale Kapitalstruktur mit Steuern
    cards.append(new_card(ch, n, "Branchenunterschiede in der Kapitalstruktur",
        "Warum gibt es erhebliche Branchenunterschiede in der Nettoverschuldung?",
        "Median Nettoverschuldung (USA): ca. 17,5% des Unternehmenswerts, aber große Varianz.\nHohe Verschuldung: Fluggesellschaften, Immobilien, Versorgungsunternehmen (hohe EBIT, materielle Aktiva).\nGeringe/negative Verschuldung: Biotech, Hightech (geringe EBIT, immaterielles Kapital, hohes Wachstum).\nErklärung: Unterschiedliche Steuervorteil-, Konkurskosten- und Agency-Kosten-Abwägungen.",
        "Verständnis", "S. 254-258"))

    cards.append(new_card(ch, n, "Beschränkungen des Steuervorteils",
        "Warum gibt es eine Obergrenze beim Steuervorteil aus der Verschuldung?",
        "Kein weiterer Steuervorteil, wenn Zinsen das EBIT übersteigen → Unternehmen zahlt keine Steuern mehr.\nBei Zinsen > EBIT: negativer Effektiver Steuervorteil möglich (τ* < 0), da Investorensteuern.\nFolge: Optimale Verschuldung aus Steuersicht = Zinsen ≈ EBIT.",
        "Verständnis", "S. 260-264"))

    cards.append(new_card(ch, n, "Optimale Steuer-Verschuldung",
        "Welches Fremdkapitalniveau ist aus Steuerperspektive optimal und was schränkt es in der Praxis ein?",
        "Optimum: Zinszahlungen = EBIT → maximale Steuerersparnis, kein überflüssiges FK.\nAber: EBIT unsicher → Risiko, dass Zinsen EBIT übersteigen steigt mit Verschuldung.\nMit steigendem Zinsaufwand sinkt die marginale Steuerersparnis, weil die Wahrscheinlichkeit steigt, dass Zinsen das EBIT übersteigen.",
        "Verständnis", "S. 265-267"))

    cards.append(new_card(ch, n, "Wachstum und Fremdkapital",
        "Warum haben Wachstumsunternehmen (z.B. Biotech) aus Steuergründen keine hohe optimale Verschuldung?",
        "Wachstumsunternehmen haben geringe oder keine zu versteuernden Gewinne → kein Steuervorteil aus FK nutzbar.\nZusätzlich: Hohe Konkurskosten (Humankapital, Patente), hohe Agency-Kosten (leichte Risikoerhöhung), geringe freie Cashflows.\n→ Optimales Fremdkapitalniveau niedrig oder null.",
        "Evaluation", "S. 268-270"))

    cards.append(new_card(ch, n, "Das Rätsel der geringen Verschuldung",
        "Was ist das 'Rätsel der geringen Verschuldung' und wie erklärt es sich?",
        "Empirisch haben Unternehmen deutlich weniger FK als steueroptimal wäre.\nMögliche Erklärungen:\n1. Konkurskosten begrenzen Verschuldung (Trade-Off-Theorie)\n2. Agency-Kosten hoher Verschuldung\n3. Asymmetrische Information → Pecking Order\n4. Management-Entrenchment: Manager bevorzugen geringere Verschuldung\nKeine einzelne Erklärung erklärt das Rätsel vollständig.",
        "Evaluation", "S. 271-278"))

    cards.append(new_card(ch, n, "Management-Entrenchment-Theorie",
        "Was besagt die Management-Entrenchment-Theorie der Kapitalstruktur?",
        "Manager wählen Kapitalstruktur nicht um Aktionärswert zu maximieren, sondern um eigene Position zu sichern.\nBevorzugen geringe Verschuldung: Geringeres Insolvenzrisiko schützt ihren Job.\nAber: Mehr Handlungsspielraum (weniger Schuldendisziplin) erhöht ihren Einfluss.\nFolge: Kapitalstruktur spiegelt Management-Interessen wider, nicht Aktionärsoptimum.",
        "Verständnis", "S. 397"))

    return cards


def cards_chapter4_agency_nutzen():
    """Kap 4.2.2: Agency-Theorie der Verschuldung – Agency-Nutzen und Kosten"""
    ch = "Kapitel 4: Marktunvollkommenheiten und Kapitalstruktur"
    n = 4
    cards = []

    cards.append(new_card(ch, n, "3 Arten von Agency-Nutzen der Verschuldung",
        "Welche drei Arten von Agency-Nutzen kann Verschuldung erzeugen (Jensen/Meckling 1976; Jensen 1986)?",
        "(a) Höhere Konzentration des Eigentums: Manager/Eigentümer behält höheren Anteil → bessere Anreize.\n(b) Reduzierung von Fehlinvestitionen: Weniger freie Cashflows → weniger Empire Building und Overconfidence.\n(c) Geringere Handlungsautonomie: Verschuldung diszipliniert Manager durch Insolvenzgefahr und Gläubigerüberwachung.",
        "Wiedergabe", "S. 372"))

    cards.append(new_card(ch, n, "Eigentumskonzentration – Ross-Jackson-Beispiel",
        "Wie beeinflusst die Wahl zwischen FK- und EK-Finanzierung die Eigentumskonzentration und Managementanreize?",
        "Bei FK-Finanzierung: Eigentümer Ross behält 100% → jeder Euro Wertsteigerung kommt ihm vollständig zugute.\nBei EK-Emission (40% abgegeben): Ross erhält nur 60 Cent pro Wertsteigerung → geringerer Arbeitseinsatz.\nFolge: FK-Finanzierung verbessert Managementanreize durch Eigentumskonzentration (Jensen/Meckling 1976).",
        "Verständnis", "S. 373-376"))

    cards.append(new_card(ch, n, "Sachzuwendungen (Perks) bei verdünntem Eigentum",
        "Warum sind übermäßige Sachzuwendungen des Managements bei EK-Emission wahrscheinlicher?",
        "Bei 40% EK-Emission trägt Ross nur 60% der Kosten von Sachzuwendungen (Firmenwagen, Spesenkonto) selbst.\nDie anderen 40% werden von neuen Aktionären getragen.\n→ Anreiz zu übermäßigen Ausgaben steigt mit Eigentumsverw\u00e4sserung.\nFolge: Neue Investoren antizipieren dies und zahlen weniger → Altaktionär trägt Kosten letztlich selbst.",
        "Verständnis", "S. 377-380"))

    cards.append(new_card(ch, n, "Konzentrationsverwässerung bei großen Unternehmen",
        "Warum verringert sich die Eigentumskonzentration bei wachsenden Unternehmen und welche Probleme entstehen?",
        "Wachstumsgründe: Altinhaber gehen in Rente, mehr Kapital über EK nötig, Diversifizierungswunsch.\nFolge: Große Unternehmen haben CEOs mit <1% Anteil → geringe persönliche Anreize.\n→ Potenziell große Interessenkonflikte zwischen Managern und Aktionären.\n→ Stärkere externe Kontrollmechanismen nötig (Aufsichtsrat, aktivistische Aktionäre).",
        "Verständnis", "S. 381-382"))

    cards.append(new_card(ch, n, "Empire Building",
        "Was ist Empire Building und wie verursacht es Fehlinvestitionen?",
        "Empire Building: Manager investieren, um die Unternehmensgröße zu steigern, nicht die Rentabilität.\nMotivation: Größere Unternehmen bringen höhere Gehälter, mehr Prestige und Medienpräsenz.\nFolge: Investitionen mit negativem KW werden durchgeführt, um das Unternehmen zu vergrößern.\nGegenmittel: Fremdkapital entzieht freie Cashflows und verhindert verschwenderische Investitionen.",
        "Verständnis", "S. 385"))

    cards.append(new_card(ch, n, "Overconfidence des Managements",
        "Was ist Overconfidence und wie führt es zu Fehlinvestitionen?",
        "Overconfidence: Manager sind systematisch zu optimistisch über Unternehmensperspektiven.\nFolge:\n1. Neue Geschäftsmöglichkeiten werden überschätzt\n2. Problemhafte Projekte werden nicht beendet ('Projekt-Liebe')\n3. Übernahmen zu überhöhten Preisen (Winner's Curse)\nEvidenz: Akquisitionsstudien zeigen systematische Überrendite-Illusion bei Käuferunternehmen.",
        "Verständnis", "S. 386"))

    cards.append(new_card(ch, n, "Jensen's Free-Cash-Flow-Hypothese (1986)",
        "Was besagt die Free-Cash-Flow-Hypothese und wie reduziert Verschuldung das Problem?",
        "Free Cash Flows = Cash über das hinaus, was für Projekte mit positivem KW und Schuldendienst nötig ist.\nHypothese (Jensen 1986): Unternehmen mit hohen freien Cashflows tendieren zu Fehlinvestitionen.\nLösung: Verschuldung zwingt das Unternehmen, regelmäßige Zinszahlungen zu leisten → weniger freie Mittel für verschwenderische Investitionen.\nEvidenz: Übernahmen finanziert mit FK führen oft zu Effizienzgewinnen.",
        "Verständnis", "S. 387"))

    cards.append(new_card(ch, n, "Geringere Handlungsautonomie durch Verschuldung",
        "Wie reduziert Verschuldung das Management-Entrenchment durch geringere Handlungsautonomie?",
        "Hoch verschuldete Unternehmen: Manager riskieren bei Underperformance Insolvenz und Jobverlust.\n→ Manager haben stärkere Anreize, effizient zu wirtschaften.\nGläubiger überwachen das Management direkt.\nZusätzlich: Insolvenzgefahr zwingt Manager, Strategien konsequenter durchzusetzen (z.B. härtere Lohnverhandlungen).",
        "Verständnis", "S. 388-389"))

    cards.append(new_card(ch, n, "Erweiterte Trade-Off-Theorie mit Agency-Nutzen",
        "Wie lautet die erweiterte Formel für den Unternehmenswert unter Berücksichtigung aller Agency-Effekte?",
        "VL = VU + BW(Steuervorteil) − BW(Konkurskosten) − BW(Agency-Kosten FK) + BW(Agency-Nutzen FK)\nOptimales D*: Grenzkosten (steigende Konkurskosten + Agency-Kosten) = Grenznutzen (Steuervorteil + Agency-Nutzen).",
        "Verständnis", "S. 390-391",
        formula="V_L = V_U + BW(TV) - BW(KK) - BW(AK_{FK}) + BW(AN_{FK})",
        variables={"TV": "Steuervorteil", "KK": "Konkurskosten", "AK_FK": "Agency-Kosten des Fremdkapitals", "AN_FK": "Agency-Nutzen des Fremdkapitals"}))

    cards.append(new_card(ch, n, "Optimales FK für Wachstumsunternehmen (Biotech/Hightech)",
        "Warum ist das optimale Fremdkapitalniveau für R&D-intensive Wachstumsunternehmen gering?",
        "Steuervorteil: Gering (wenig EBIT)\nKonkurskosten: Hoch (Humankapital, intangible Vermögensgegenstände)\nAgency-Kosten FK: Hoch (Risiko der Geschäftsstrategie leicht erhöhbar)\nAgency-Nutzen FK: Gering (wenig freie Cashflows → geringe Fehlinvestitionsgefahr)\n→ Fazit: Sehr geringes optimales Fremdkapitalniveau, oft Nettobargeldhaltung.",
        "Evaluation", "S. 393-394"))

    cards.append(new_card(ch, n, "Optimales FK für reife Unternehmen",
        "Warum haben reife Unternehmen (Immobilien, Versorger, Supermärkte) typischerweise hohe Verschuldung?",
        "Steuervorteil: Hoch (stabile, hohe EBIT)\nKonkurskosten: Gering (materielle Vermögensgegenstände leicht verwertbar)\nAgency-Kosten FK: Gering (Geschäftsrisiko schwer erhöhbar)\nAgency-Nutzen FK: Hoch (hohe freie Cashflows, wenige gute Investitionsgelegenheiten → hohe Fehlinvestitionsgefahr ohne FK-Disziplin)\n→ Fazit: Hohes optimales Fremdkapitalniveau.",
        "Evaluation", "S. 395-396"))

    cards.append(new_card(ch, n, "Covenants als Instrument zur Agency-Kostensenkung",
        "Wie können Covenants Agency-Kosten senken und was sind ihre Grenzen?",
        "Covenants (Kreditklauseln) schränken die Handlungsfreiheit des Schuldners ein:\n• Ausschüttungsbegrenzungen (verhindert Cashing-out)\n• Beschränkung riskanter Investitionen (verhindert Asset Substitution)\n• Verpflichtung zu Mindest-Kennzahlen\nGrenze: Covenants können auch KW > 0-Projekte verhindern → zweischneidiges Schwert.",
        "Evaluation", "S. 369-370"))

    return cards


def cards_chapter4_asymm_info():
    """Kap 4.2.3: Asymmetrische Information und Kapitalstruktur"""
    ch = "Kapitel 4: Marktunvollkommenheiten und Kapitalstruktur"
    n = 4
    cards = []

    cards.append(new_card(ch, n, "Asymmetrische Information und Kapitalstruktur – Überblick",
        "Welche zwei zentralen Konsequenzen hat asymmetrische Information für die Kapitalstruktur?",
        "1. Signaling-Theorie (Ross 1977): Verschuldung kann als glaubwürdiges Signal positiver Informationen dienen.\n2. Adverse Selektion (Myers/Majluf 1984): EK-Emission signalisiert Überbewertung → Kursabschlag → Pecking Order.\nBeide zeigen: Kapitalstrukturentscheidungen transportieren Information an den Markt.",
        "Verständnis", "S. 398-399"))

    cards.append(new_card(ch, n, "Glaubwürdigkeitsprinzip (Signaling)",
        "Was ist das Glaubwürdigkeitsprinzip und warum ist es die Grundlage der Signaling-Theorie?",
        "Glaubwürdigkeitsprinzip: Behauptungen über die eigene Qualität sind nur dann glaubwürdig, wenn sie durch Handlungen unterstützt werden, die für ein schlechtes Unternehmen zu kostspielig wären.\n'Taten sagen mehr als tausend Worte.'\nAnwendung: Hohe Verschuldung ist nur dann glaubwürdig, wenn das Unternehmen sicher ist, die Zinsen bedienen zu können. Ein schwaches Unternehmen würde in finanzielle Notlage geraten.",
        "Verständnis", "S. 401"))

    cards.append(new_card(ch, n, "Signaling-Theorie des Fremdkapitals (Ross 1977)",
        "Wie erklärt Ross (1977) die Signalwirkung der Verschuldung?",
        "Manager kennen die tatsächliche Profitabilität besser als Investoren.\nHohe Verschuldung = glaubwürdiges Signal zukünftiger Cashflows:\n• Bei wahrem Erfolg: Zinsen problemlos bedienbar\n• Bei falscher Behauptung: Finanzielle Notlage und Jobverlust für Manager\nFolge: Nur starke Unternehmen können hohe Verschuldung glaubwürdig wählen.",
        "Verständnis", "S. 403"))

    cards.append(new_card(ch, n, "Beltran-Beispiel: Mindest-Signal-Verschuldung",
        "Beltran International: Wert entweder 100 oder 50 Mio. (je 50% wahrscheinlich). Manager weiß: Erfolg fast sicher. Bei welcher Verschuldung ist das Signal glaubwürdig?",
        "Bei D ≤ 50 Mio.: Signal nicht glaubwürdig – kein Insolvenzrisiko bei schlechtem Ergebnis.\nBei D > 50 Mio.: Signal glaubwürdig – Manager riskiert bei falscher Aussage seinen Job (Insolvenz).\n→ Mindest-Verschuldung = 50 Mio. Euro für glaubwürdiges Signal.",
        "Transfer", "S. 404-405"))

    cards.append(new_card(ch, n, "Akerlof's Lemons-Problem (1970)",
        "Erklären Sie das Lemons-Problem am Gebrauchtwagenmarkt und warum es zu adverser Selektion führt.",
        "Verkäufer kennt die Qualität des Wagens, Käufer nicht.\nKäufer zahlt nur Durchschnittspreis → Inhaber hochwertiger Autos verkaufen ungern.\n→ Nur unterdurchschnittliche Qualität ('Lemons') wird angeboten.\nLemons-Prinzip: Wenn Verkäufer private Informationen hat, zahlen Käufer nur einen geringen Preis.",
        "Verständnis", "S. 406-408"))

    cards.append(new_card(ch, n, "Adverse Selektion bei Eigenkapitalemission",
        "Warum führt das Lemons-Problem bei der EK-Emission zu einem Kursabschlag?",
        "Manager weiß mehr als Investoren über den wahren Unternehmenswert.\nEmittiert er EK, signalisiert er, dass die Aktien überbewertet sind (sonst würde er FK nutzen).\nInvestoren fordern Preisabschlag → nur Unternehmen mit überbewerteten Aktien emittieren EK.\nFolge: Adverse Selektion = EK-Emittenten haben tendenziell unterdurchschnittliche Qualität.",
        "Verständnis", "S. 409-410"))

    cards.append(new_card(ch, n, "Zycor-Beispiel: Preisverfall bei CEO-Aktienverkauf",
        "Zycor-Aktie: Wert 60/80/100 Euro (gleich wahrscheinlich), Kurs = 80. CEO kündigt Verkauf zum Zweck der Diversifikation an. Warum fällt der Kurs?",
        "CEO verkauft nur, wenn Angebotspreis ≥ 90% des wahren Werts (10% weniger akzeptiert er für Diversifikation).\nBei wahrem Wert 100: CEO akzeptiert 90, aber Marktkurs 80 → kein Verkauf.\nBei wahrem Wert 80 oder 60: CEO verkauft → Kurs fällt auf 70 (Durchschnitt von 60 und 80).\nBei 80 verkauft CEO nicht zu 70 → Kurs fällt auf 60.\n→ Adverse Selektion: Bloße Verkaufsankündigung treibt den Kurs auf 60.",
        "Transfer", "S. 411-413"))

    cards.append(new_card(ch, n, "Gentec-Beispiel: Timing der EK-Emission",
        "Gentec: Marktwert 200 Mio. (10 Euro/Aktie), wahrer Wert 300 Mio. Benötigt 60 Mio. für Labor. Warum sollte Gentec die EK-Emission verzögern?",
        "Sofortige Emission: 6 Mio. neue Aktien zu 10 Euro; nach Bekanntwerden: Kurs 13,85 Euro.\nNach positiven Nachrichten: Nur 4 Mio. neue Aktien zu 15 Euro; Kurs bleibt 15 Euro.\nVorteil der Verzögerung: Altaktionäre halten mehr Anteile am vollen Wert.\nFolge: EK-Emissionen werden verzögert, bis positive Informationen öffentlich werden.",
        "Evaluation", "S. 414-417"))

    cards.append(new_card(ch, n, "Beobachtbare Auswirkungen auf EK-Emissionen",
        "Welche empirischen Auswirkungen der adversen Selektion lassen sich bei EK-Emissionen beobachten?",
        "1. Aktienkurs fällt nach Ankündigung einer EK-Emission: Empirisch ca. −3% (USA).\n   → EK-Emission signalisiert Überbewertung.\n2. Aktienkurs steigt vor EK-Emission: Lucas/McDonald (1990): +50% gegenüber Markt.\n   → Unternehmen emittieren EK nur nach positiven Nachrichten (Asymmetrie ist gering).",
        "Verständnis", "S. 419-420"))

    cards.append(new_card(ch, n, "Die Hackordnung der Finanzierung (Pecking Order)",
        "Was ist die Hackordnung der Finanzierung (Myers/Majluf 1984) und warum entsteht sie?",
        "Hierarchie der Finanzierungsquellen aufgrund adverser Selektion:\n1. Innenfinanzierung (Gewinnrücklagen): keine Adverse-Selektion-Kosten\n2. Fremdkapital: geringe Adverse-Selektion (FK-Preise weniger sensitiv auf private Information)\n3. Eigenkapital: hohe Adverse-Selektion-Kosten → nur als letztes Mittel\nFolge: Keine optimale Zielkapitalstruktur, sondern Hierarchie der Präferenzen.",
        "Verständnis", "S. 421-423"))

    cards.append(new_card(ch, n, "Axon-Beispiel: Kostenvergleich der Finanzierungsquellen",
        "Axon Industries: 10 Mio. Euro benötigt, FK-Kosten 7% (fair: 6%), EK 5% unterbewertet. Wie hoch sind die effektiven Kosten der drei Finanzierungsquellen?",
        "1. Innenfinanzierung: 10 Mio. Euro (keine Adverse-Selektion-Kosten)\n2. Fremdkapital: 10 Mio. × 1,07/1,06 = 10,094 Mio. Euro (Überbewertung 0,94%)\n3. Eigenkapital: 10 Mio. / 0,95 = 10,526 Mio. Euro (Unterbewertung 5%)\n→ Reihenfolge bestätigt Hackordnung: Intern < FK < EK.",
        "Transfer", "S. 424-425",
        solution_steps=["Innen: 10 Mio.", "FK: 10 × 1,07/1,06 = 10,094 Mio.", "EK: 10 / 0,95 = 10,526 Mio."]))

    cards.append(new_card(ch, n, "Pecking Order vs. Trade-Off-Theorie (Vergleich)",
        "Vergleichen Sie die Pecking-Order-Theorie und die Trade-Off-Theorie systematisch.",
        "Trade-Off-Theorie:\n• Optimale Zielkapitalstruktur D*\n• Balance Steuervorteil vs. Konkurs-/Agency-Kosten\n• Unternehmen kehren zu Zielstruktur zurück\nPecking-Order-Theorie:\n• Keine Zielkapitalstruktur\n• Hierarchie: Intern > FK > EK\n• Kapitalstruktur als historischer Zufallspfad\n• Verschuldung ≠ Maß für Qualität, sondern für kumulierten Finanzierungsbedarf",
        "Synthese", "S. 426"))

    return cards


def cards_chapter5_diamond84():
    """Kap 5.2: Diamond (1984) – Delegierte Kontrolle"""
    ch = "Kapitel 5: Funktionen von Banken"
    n = 5
    cards = []

    cards.append(new_card(ch, n, "Diamond 1984 – Überblick und Motivation",
        "Was ist die zentrale Frage des Modells von Diamond (1984) und warum ist es wichtig?",
        "Zweites zentrales Bankenmodell (neben Diamond/Dybvig 1983).\nZentrale Frage: Warum können Banken einen besseren Rendite-Risiko-Trade-off bieten als der Kapitalmarkt?\nModelliert die Risikotransformationsfunktion: Riskante Kredite → nahezu risikolose Einlagen.\nGrundidee: Durch delegierte Kontrolle und Diversifikation werden Kontrollkosten gespart.",
        "Verständnis", "S. 492-493"))

    cards.append(new_card(ch, n, "Grundproblem: Wer kontrolliert den Kontrolleur?",
        "Was ist das zentrale Paradox bei der delegierten Kontrolle und wie löst Diamond es?",
        "Problem: Wenn Einleger die Kontrolle an eine Bank delegieren, entsteht ein neues Informationsproblem (Wer kontrolliert die Bank?).\nLösung durch Diamond: Wenn die Bank viele Projekte finanziert, reduziert Diversifikation das Ausfallrisiko der Bank gegen null.\n→ Einleger müssen Bank kaum mehr kontrollieren (Delegationskosten → 0).",
        "Verständnis", "S. 493-494"))

    cards.append(new_card(ch, n, "Costly State Verification (CSV)",
        "Was ist das Informationsproblem 'Costly State Verification' (Gale/Hellwig 1985) und warum ist es relevant?",
        "CSV: Kapitalgeber können den tatsächlichen Ertrag y eines Projekts nur kostenpflichtig beobachten.\nOhne CSV: Unternehmer gibt wahrheitsgemäß den Ertrag an.\nMit CSV: Unternehmer hat Anreiz, hohe Erträge zu verschweigen (immer y=0 behaupten → keine Rückzahlung).\nFolge: Ohne Mechanismus kommt keine Finanzierung zustande.",
        "Verständnis", "S. 499"))

    cards.append(new_card(ch, n, "Modell-Annahmen bei Diamond (1984)",
        "Beschreiben Sie die Grundannahmen des Diamond-1984-Modells.",
        "N risikoneutrale Unternehmer: je 1 GE benötigt, je 1/m GE von m Investoren.\nKreditangebot > Kreditnachfrage → Investoren werden auf Reservationsnutzen R gedrückt.\nAlternative Geldanlage: R pro GE.\nAsymmetrische Information: Nur Unternehmer beobachtet Projektertrag ỹ.\nE(ỹ) > R → Durchführung effizient bei vollständiger Information.",
        "Wiedergabe", "S. 500-501"))

    cards.append(new_card(ch, n, "Warum funktioniert kein proportionaler Vertrag?",
        "Warum kann die direkte Finanzierung nicht durch einen proportionalen Vertrag (z.B. Gewinnbeteiligung) funktionieren?",
        "Bei einem Vertrag mit prozentualer Rückzahlung:\n→ Unternehmer behauptet immer y = 0 (kein Ertrag)\n→ Rückzahlung = 0\n→ Kapitalgeber antizipieren dies und stellen kein Kapital bereit\n→ Vertrag kommt nicht zustande.\nFolge: Finanzierungsvertrag muss gegen falsches Reporting abgesichert sein.",
        "Verständnis", "S. 502-503"))

    cards.append(new_card(ch, n, "Direktfinanzierung Option 1: Kontrolle (Kosten m·K)",
        "Wie funktioniert direkte Finanzierung mit Kontrolle und was sind ihre Kosten?",
        "Jeder der m Investoren überwacht den Unternehmer zu Kosten K.\nGesamtkosten: m·K (jeder Investor kontrolliert unabhängig → Doppelarbeit).\nBei vielen kleinen Investoren (m groß): sehr hohe Gesamtkontrollkosten.\nVorteil: Kein Anreizproblem, da Ertrag direkt beobachtet wird.",
        "Verständnis", "S. 505"))

    cards.append(new_card(ch, n, "Direktfinanzierung Option 2: Anreizkompatibler Vertrag mit Strafen",
        "Wie funktioniert ein anreizkompatibler Vertrag mit nicht-monetären Strafen und was sind seine Kosten?",
        "Strafe ϕ*(z(y)) = max[h − z(y), 0]: Unternehmer wird bestraft, wenn er weniger als h zurückzahlt.\nFolge: Unternehmer ist indifferent zwischen wahrhaftiger und falscher Angabe.\n→ Zahlt immer z(y) = min[h, y] → Standardkreditvertrag!\nKosten: E[ϕ*(z(y))] = erwartete Strafe (wohlfahrtsmindernd, weil Strafe gezahlt auch wenn wahrheitsgemäß).",
        "Verständnis", "S. 506-511"))

    cards.append(new_card(ch, n, "Optimaler Finanzkontrakt = Standardkreditvertrag",
        "Warum entspricht der optimale Finanzkontrakt bei CSV einem Standardkreditvertrag?",
        "Optimaler Kontrakt: z(y) = min[h, y]\n• Wenn y ≥ h: Unternehmer zahlt h zurück (kein Anreizproblem)\n• Wenn y < h: Unternehmer zahlt alles (y), Strafe = h − y\nDies entspricht exakt einem Kreditvertrag mit festem Rückzahlungsbetrag h und Strafe bei Ausfall!\n→ Erklärt die Existenz von Kreditverträgen als optimale Vertragsform bei CSV.",
        "Verständnis", "S. 510"))

    cards.append(new_card(ch, n, "Wohlfahrtskosten des anreizkompatiblen Vertrags",
        "Was sind die Wohlfahrtskosten des optimalen Finanzkontrakts und wann treten sie auf?",
        "Wohlfahrtskosten = E[ϕ*(z(y))] = erwartete Strafe.\nStrafe fällt an, wenn y < h (Projektertrag unter Rückzahlungsbetrag).\nProblem: Unternehmer wird bestraft, obwohl er die Wahrheit sagt!\nDiese Kosten sind rein wohlfahrtsmindernd (kein Nutzen für Kapitalgeber).\nHöher, je größer die Wahrscheinlichkeit schlechter Projekterträge.",
        "Verständnis", "S. 511"))

    cards.append(new_card(ch, n, "Wann ist Kontrolle besser als anreizkompatibler Vertrag?",
        "Unter welchen Bedingungen ist direkte Kontrolle (m·K) vorzuziehen gegenüber dem anreizkompatiblen Vertrag?",
        "Kontrolle besser wenn: m·K < E[ϕ*(z(y))]\nKontrolle ist teuer bei großem m (vielen Investoren).\nAnreizkomp. Vertrag ist teuer bei hoher Ausfallwahrscheinlichkeit (schlechte Projekterträge wahrscheinlich).\n→ Kontrolle bevorzugt: wenige Investoren + sichere Projekte.\n→ Anreizkontrakt bevorzugt: viele Investoren + sicherer Erfolg.",
        "Evaluation", "S. 512-513"))

    cards.append(new_card(ch, n, "Indirekte Finanzierung: Delegationsidee",
        "Wie reduziert ein Finanzintermediär (FI) die Kontrollkosten von m·K auf K?",
        "Idee: Delegation der Kontrolle an einen FI.\nFI kontrolliert Unternehmer: Kosten = 1·K (statt m·K bei direkter Finanzierung).\nFI gibt Information an die m Investoren weiter via anreizkompatiblem Vertrag.\n→ Gesamtkosten: K (Kontrolle) + Delegationskosten d (für FI-Vertrag mit Investoren).\nAber: Ob K + d < m·K hängt von d ab!",
        "Verständnis", "S. 514-515"))

    cards.append(new_card(ch, n, "Delegationskosten und Diversifikation",
        "Wie löst Diversifikation das Delegationsproblem im Diamond-1984-Modell?",
        "Problem: Wenn FI nur 1 Unternehmer finanziert, sind Delegationskosten ähnlich hoch wie direkte Finanzierung.\nLösung: FI finanziert N Unternehmer mit stochastisch unabhängigen Projekten.\nGesetz der Großen Zahlen: Portfolio-Ertrag (pro Unternehmer) → E(ỹ) für N → ∞.\nFolge: Ausfallwahrscheinlichkeit des FI → 0 → Delegationskosten d → 0.",
        "Verständnis", "S. 517-519"))

    cards.append(new_card(ch, n, "Vorteilhaftigkeit der Finanzintermediation",
        "Wann dominiert die delegierte Kontrolle die direkte Finanzierung?",
        "Kosten Direktfinanzierung: min{m·K, E[ϕ*(z(y))]}\nKosten FI (für großes N): K + d ≈ K\nFI vorteilhaft wenn: K < min{m·K, E[ϕ*(z(y))]} ⟺ K < E[ϕ*(z(y))]\nD.h.: Kontrollkosten geringer als erwartete Strafe bei direktem Vertrag.\nErgebnis: In vielen Fällen dominiert die delegierte Kontrolle über Finanzintermediäre.",
        "Verständnis", "S. 519-521",
        formula="K + d < \\min\\{m \\cdot K,\\; E[\\phi^*(z(\\tilde{y}))]\\}",
        variables={"K": "Kontrollkosten pro FI", "d": "Delegationskosten (→ 0 für N → ∞)", "m": "Anzahl Investoren pro Unternehmer"}))

    cards.append(new_card(ch, n, "Kritische Würdigung Diamond 1984",
        "Was sind die wichtigsten Kritikpunkte am Diamond-1984-Modell?",
        "Stärken:\n• Erklärt Existenz von Banken bei Informationsproblemen\n• Erklärt FK-Finanzierung der Banken (Einlagen)\n• Erklärt relative Sicherheit von Einlagen bei riskanten Krediten\nSchwächen:\n• FI sollte im Ideal unendlich groß sein → Konzentrationsprobleme (TBTF)\n• Kein Bankenwettbewerb modelliert\n• EK-Kapital spielt keine Rolle (wichtig in Realität)\n• CSV ist ein spezielles Informationsproblem (Moral Hazard bei Risikowahl evtl. wichtiger)",
        "Evaluation", "S. 522-525"))

    return cards


def cards_chapter6_dd_detail():
    """Kap 6.1–6.3: Mehr Detail zu Diamond-Dybvig, Narrow Banking, Einlagenversicherung"""
    ch = "Kapitel 6: Finanzkrisen und systemische Risiken"
    n = 6
    cards = []

    cards.append(new_card(ch, n, "Sequential Service Constraint (DD-Modell)",
        "Was ist die Sequential Service Constraint im Diamond-Dybvig-Modell und warum entsteht sie?",
        "SSC: Einleger werden in der Reihenfolge ihrer Ankunft bedient ('First come, first served').\nBank kann nicht sofort wissen, ob Einleger Typ-1 oder Typ-2 ist.\nFolge: Einleger haben Anreiz, früh zu kommen wenn sie einen Run erwarten.\nKoordinationsproblem: Wenn alle kommen, gibt es nicht genug für alle.",
        "Verständnis", "S. 533"))

    cards.append(new_card(ch, n, "Gutes Gleichgewicht im DD-Modell",
        "Wie funktioniert das gute Gleichgewicht im Diamond-Dybvig-Modell?",
        "Nur Typ-1-Einleger heben in t=1 ab (sie brauchen wirklich Liquidität).\nBank weiß: ca. π1·N Einleger kommen in t=1 → hält genau π1·C1* in liquiden Assets.\nTyP-2-Einleger warten bis t=2, erhalten C2* > C1*.\nFirst-best-Gleichgewicht: Bank implementiert die optimale Konsumglättung.",
        "Verständnis", "S. 536-538"))

    cards.append(new_card(ch, n, "Schlechtes Gleichgewicht: Bank Run als Koordinationsproblem",
        "Warum ist ein Bank Run im DD-Modell ein Gleichgewicht und wie unterscheidet er sich vom guten Gleichgewicht?",
        "Wenn ein Typ-2-Einleger erwartet, dass alle anderen in t=1 abziehen:\n→ Er schätzt: Falls er wartet, bleibt nichts mehr übrig\n→ Beste Antwort: auch in t=1 abziehen (obwohl er bis t=2 warten müsste)\nDiese Erwartung ist selbsterfüllend: Alle ziehen ab → Bank liquidiert alle Projekte → L < 1 → nicht genug für alle.\nBeide Gleichgewichte existieren: Welches eintritt, hängt von Erwartungen ab (sunspot).",
        "Verständnis", "S. 539-546"))

    cards.append(new_card(ch, n, "Aggregiertes vs. idiosynkratisches Liquiditätsrisiko",
        "Was ist der Unterschied zwischen aggregiertem und idiosynkratischem Liquiditätsrisiko und warum ist das für Bank Runs wichtig?",
        "Idiosynkratisches Risiko: Individuelle Schocks (z.B. ein Einleger braucht zufällig früh Geld).\n→ Durch Gesetz der Großen Zahlen im Durchschnitt vorhersagbar → Bank kann perfekt planen.\nAggregiertes Risiko: Alle Einleger wollen gleichzeitig abziehen (z.B. bei Rezession).\n→ Nicht durch Diversifikation eliminierbar → Bank kann nicht alle bedienen.\nBank Run = Extremfall eines aggregierten Liquiditätsschocks.",
        "Verständnis", "S. 555"))

    cards.append(new_card(ch, n, "Einlagenversicherung und Moral Hazard",
        "Wie löst die Einlagenversicherung das Bank-Run-Problem und was sind die Nachteile?",
        "Lösung: Einleger werden geschützt → kein Anreiz zum Abziehen → schlechtes Gleichgewicht existiert nicht mehr.\nNachteil 1 – Moral Hazard der Bank: Einleger kontrollieren die Bank nicht mehr → Bank kann mehr Risiken eingehen.\nNachteil 2 – Prämiengestaltung: Wenn Prämie nicht risikoadjustiert, subventioniert sichere Bank riskante Bank.\nNachteil 3 – Fiskalische Kosten: Bei vielen Bankinsolvenzen: Steuerzahler haftet.",
        "Evaluation", "S. 557-560"))

    cards.append(new_card(ch, n, "Kritische Würdigung DD-Modell als Regulierungsmodell",
        "Was sind die Grenzen des Diamond-Dybvig-Modells als Grundlage für Bankenregulierung?",
        "Schwächen:\n1. Nur idiosynkratische Schocks modelliert: Aggregierte Schocks nicht erfasst\n2. Keine Aktivseite der Bank: Kreditrisiken nicht modelliert\n3. Gleichgewicht hängt von Erwartungen ab (sunspot): Regulierung kann Erwartungen beeinflussen, aber wie?\n4. Einlagenversicherung löst Problem, schafft aber Moral Hazard → separate Regulierung nötig\n5. Jacklin (1987): Bei freiem Aktienhandel verschwindet das Bank-Run-Gleichgewicht",
        "Evaluation", "S. 561-565"))

    return cards


def cards_chapter6_eff_runs():
    """Kap 6.4: Effiziente Bank Runs (Calomiris/Kahn 1991)"""
    ch = "Kapitel 6: Finanzkrisen und systemische Risiken"
    n = 6
    cards = []

    cards.append(new_card(ch, n, "Effiziente Bank Runs – Grundidee",
        "Wann können Bank Runs (oder die Möglichkeit von Bank Runs) effizient sein?",
        "Bei Diamond/Dybvig: Bank Runs sind immer ineffizient (Koordinationsversagen).\nCalomiris/Kahn (1991): Bank Runs können effizient sein als Disziplinierungsinstrument:\n→ Möglichkeit eines Runs hält die Bank davon ab, mit Einlegergeldern zu 'fliehen' (Moral Hazard).\nNur weil ein Run droht, sind Einleger bereit, das Kapital überhaupt einzulegen.",
        "Verständnis", "S. 568"))

    cards.append(new_card(ch, n, "Calomiris/Kahn 1991: Moral Hazard der Bank",
        "Was ist das Moral-Hazard-Problem auf Seiten der Bank im Calomiris/Kahn-Modell?",
        "Moral-Hazard: Der Banker kann die eingelegten Gelder nehmen und 'weglaufen' (absconden).\nOhne Drohung eines Runs: Kein Anreiz, Gelder zurückzuzahlen.\nMit jederzeit abhebbaren Einlagen (demand deposits): Einleger können sofort abziehen wenn Fehlverhalten vermutet.\n→ Drohung des Runs verhindert Fehlverhalten und ermöglicht erst die Finanzierung effizienter Projekte.",
        "Verständnis", "S. 569"))

    cards.append(new_card(ch, n, "Sequential Service Constraint als Kontrollmechanismus",
        "Wie löst die Sequential Service Constraint (SSC) das Trittbrettfahrerproblem bei der Bankenüberwachung?",
        "Problem: Kontrollkosten fallen beim Überwachenden an, Nutzen genießen alle Einleger.\n→ Niemand kontrolliert (Trittbrettfahrerproblem).\nLösung mit SSC: Wer zuerst kommt (frühzeitig Fehlverhalten entdeckt und abzieht), erhält als erster volle Rückzahlung.\n→ SSC schafft Anreiz zur Überwachung: Als Kompensation für Kontrollkosten erhält der Überwachende einen vorderen Platz in der Schlange.",
        "Verständnis", "S. 570"))

    cards.append(new_card(ch, n, "Diamond/Rajan 2001: Fragile Bankstruktur als Commitment",
        "Wie erklärt Diamond/Rajan (2001) die Fragilitätsfunktion von Bankeinlagen?",
        "Banker kennt die optimale Verwendung der Investitionen (private Information).\nEinleger können FK nicht zurückfordern → Banker könnte Gelder zurückhalten.\nLösung: Einlagen als täglich fälliges FK → Drohung des Runs zwingt Banker, sein spezifisches Wissen nicht zur Erpressung zu nutzen.\nFragilität = Commitment-Gerät: Die Möglichkeit eines Runs macht die Bank glaubwürdig.",
        "Verständnis", "S. 568"))

    cards.append(new_card(ch, n, "Marktdisziplin als Regulierungssubstitut",
        "Wie kann Marktdisziplin als Ersatz für staatliche Bankenregulierung dienen?",
        "Idee: Informierte Gläubiger (nicht: Kleineinleger) überwachen Banken besser als Regulierungsbehörden.\nVoraussetzungen: Transparenz, Offenlegungspflichten, Abwesenheit impliziter Staatsgarantien.\nSäule 3 Basel: Marktdisziplin als ergänzendes Regulierungsprinzip.\nProblem: Wer ist der 'Markt'? Private Einleger zu klein und uninformiert.",
        "Evaluation", "S. 573-574"))

    cards.append(new_card(ch, n, "Nachrangige Schulden als Marktdisziplininstrument",
        "Was ist der Vorschlag von Calomiris zur Schaffung von Marktdisziplin durch nachrangige Schulden?",
        "Vorschlag: Jede Bank muss einen bestimmten Anteil über nachrangige Schulden (subordinated debt) finanzieren.\nNachrangige Gläubiger werden bei Insolvenz als letzte bedient (senior debt geht vor).\nFolge: Nachrangige Gläubiger haben starken Anreiz zur Überwachung → informierter als Kleineinleger.\nÖffentlich gehandelt: Risikoprämien liefern Informationen über Bankstabilität → Aufseher können nutzen.",
        "Verständnis", "S. 575"))

    cards.append(new_card(ch, n, "TLAC und MREL: Regulatorische Umsetzung",
        "Was sind TLAC und MREL und wie setzen sie die Idee bail-in-fähiger Schulden um?",
        "TLAC (Total Loss Absorbing Capacity): FSB-Standard für G-SIBs; mindestens 16-18% RWA als bail-in-fähige Verbindlichkeiten.\nMREL (Minimum Requirement for Own Funds and Eligible Liabilities): EU-Äquivalent für alle Institute.\nIdee: Im Krisenfall werden diese Schulden in EK umgewandelt oder abgeschrieben → Bail-in statt Bail-out.\nOffene Frage: Wird Bail-in in einer Systemkrise tatsächlich durchgesetzt?",
        "Verständnis", "S. 576"))

    cards.append(new_card(ch, n, "Bail-outs untergraben Marktdisziplin",
        "Warum untergraben staatliche Bail-outs die Marktdisziplin durch nachrangige Gläubiger?",
        "In der globalen Finanzkrise wurden auch nachrangige Gläubiger gerettet.\n→ Diese antizipieren künftige Rettung → kein Anreiz zur Überwachung.\nFolge: Marktdisziplin funktioniert nur, wenn Bail-outs glaubwürdig ausgeschlossen sind.\nGlaubwürdigkeit: Erfordert ex ante festgelegte Abwicklungsregime und politischen Willen zur Umsetzung.",
        "Evaluation", "S. 576"))

    return cards


def cards_chapter6_ansteckung():
    """Kap 6.5: Ansteckungseffekte im Finanzsystem"""
    ch = "Kapitel 6: Finanzkrisen und systemische Risiken"
    n = 6
    cards = []

    cards.append(new_card(ch, n, "Systemisches Risiko und Bankenkrisen",
        "Was ist der Unterschied zwischen einem Bank Run bei einer einzelnen Bank und systemischem Risiko?",
        "Bank Run (einzelne Bank): Probleme einer Bank → Run auf diese Bank.\nSystemisches Risiko: Probleme im gesamten Bankensystem (banking panic).\nBankenkrise (banking panic): Simultaner Zusammenbruch eines signifikanten Teils des Bankensystems.\nSystemisches Risiko = Risiko des Zusammenbruchs des gesamten Finanzsystems.",
        "Verständnis", "S. 578-579"))

    cards.append(new_card(ch, n, "Zwei Arten von Bankenkrisen",
        "Welche zwei grundlegend verschiedenen Ursachen können Bankenkrisen haben?",
        "(a) Makroökonomische Schocks: Alle Banken werden gleichzeitig vom selben Schock getroffen (Rezession, Zinsanstieg, Währungskrise).\n(b) Ansteckung (Contagion): Probleme bei einer einzelnen Bank weiten sich auf das gesamte Bankensystem aus.\nBeide Arten erhöhen systemisches Risiko → zentrale Begründung für Bankenregulierung.",
        "Verständnis", "S. 579"))

    cards.append(new_card(ch, n, "Kanal 1: Informationsansteckung (Chen 1999)",
        "Wie können Informationseffekte Ansteckung im Bankensystem verursachen (Chen, JPE 1999)?",
        "Bankerträge sind zwischen verschiedenen Banken positiv korreliert.\nZusammenbruch einer Bank = Signal über Zustand anderer Banken.\nUninformierte Einleger können nicht unterscheiden, welche Banken noch solvent sind.\nReaktion: Einleger ziehen bei anderen Banken ab (Sicherheitshalber), um in der SSC-Schlange vorne zu sein.\n→ Run auf solvente Banken möglich, obwohl diese gesund sind.",
        "Verständnis", "S. 584-585"))

    cards.append(new_card(ch, n, "Kanal 2: Allen/Gale (2000) – Interbankenverbindlichkeiten",
        "Wie können Interbankenverbindlichkeiten Ansteckung verursachen (Allen/Gale, JPE 2000)?",
        "Banken sind über Interbankenmärkte miteinander vernetzt (gegenseitige Forderungen).\nFunktion: Versicherung gegen regionale Liquiditätsschocks.\nProblem: Aggregierter Schock → eine Bank muss liquidieren → Verluste für verbundene Banken → Dominoeffekte.\nWichtigstes Ergebnis: Vollständige Vernetzung (alle mit allen) stabiler als unvollständige (Kettenstruktur).",
        "Verständnis", "S. 586-591"))

    cards.append(new_card(ch, n, "Interbankenmarkt: Funktion und Risiko",
        "Welche positive Funktion erfüllt der Interbankenmarkt und warum ist er gleichzeitig ein Ansteckungskanal?",
        "Positive Funktion: Umverteilung von Liquidität zwischen Banken mit Überschuss und Defizit → regionale Liquiditätsschocks ausgeglichen.\nRisiko: Vernetzung bedeutet, dass Probleme einer Bank Verluste bei Gläubigerbanken verursachen.\nKeine Ansteckung: Nur idiosynkratische Schocks → Interbankenmarkt löst das Problem.\nAnsteckung: Bei aggregierten Schocks → Interbankenmarkt überträgt den Schock.",
        "Verständnis", "S. 586"))

    cards.append(new_card(ch, n, "Vollständige vs. unvollständige Interbanken-Marktstruktur",
        "Warum ist eine vollständige Interbankenmarktstruktur stabiler als eine unvollständige (Allen/Gale 2000)?",
        "Vollständig: Jede Bank hält Forderungen gegen alle anderen Banken → Verluste werden gleichmäßig verteilt → keine einzelne Bank geht unter.\nUnvollständig (Kettenstruktur): Jede Bank ist nur mit wenigen verbunden → Verluste konzentrieren sich → Dominoeffekt möglich.\nErgebnis: Vernetzung kann stabilisieren ODER destabilisieren, abhängig von der Struktur.",
        "Verständnis", "S. 589-591"))

    cards.append(new_card(ch, n, "Kanal 3: Fire Sales und makroökonomische Rückkopplungen",
        "Wie entstehen Ansteckungseffekte über Fire Sales (Notverkäufe)?",
        "Bank muss Assets schnell verkaufen (fire sales) → Preise fallen unter Fundamentalwert.\nDa viele Banken ähnliche Assets halten, trifft Preisverfall alle gleichzeitig.\nVerstärkungseffekte: Mark-to-market-Bilanzierung zwingt weitere Banken zu Abschreibungen → weiterer Verkaufsdruck.\nErgebnis: Intrinsisch solvente Banken können durch Marktpreisverfall insolvent werden.",
        "Verständnis", "S. 592-594"))

    cards.append(new_card(ch, n, "Deleveraging und finanzieller Akzelerator",
        "Was ist Deleveraging und wie wirkt es als finanzieller Akzelerator?",
        "Deleveraging: Banken reduzieren in Rezessionen ihre Bilanzen, um Eigenkapitalquoten zu halten.\nMechanismus: Kreditvergabe sinkt → abhängige Unternehmen (bes. KMU) können nicht investieren → gesamtwirtschaftliche Nachfrage sinkt → Rezession verschärft sich.\nFinanzieller Akzelerator: Rückkopplungseffekte verstärken den ursprünglichen Schock.\nZusätzlich: Deleveraging im Interbankenmarkt = Run durch andere Banken.",
        "Verständnis", "S. 595-596"))

    cards.append(new_card(ch, n, "Wirtschaftspolitische Relevanz der Ansteckungsangst",
        "Welche wirtschaftspolitische Bedeutung haben Ansteckungseffekte und was ist das Zombie-Banken-Problem?",
        "Ansteckungsangst wird genutzt, um staatliche Rettungsmaßnahmen zu rechtfertigen.\nProblem: Selbst insolvente Banken werden gerettet 'wegen Ansteckungsgefahr'.\nFolge: Zombie-Banken (nicht-profitable Banken) bleiben am Leben und verringern die Kreditvergabe an profitable Unternehmen.\n→ Marktmechanismus außer Kraft gesetzt, Ressourcenfehlallokation.",
        "Evaluation", "S. 597"))

    cards.append(new_card(ch, n, "Empirische Evidenz zu Ansteckungseffekten",
        "Wie stark ist die empirische Evidenz für die drei Ansteckungskanäle?",
        "Informationsansteckung: Relativ schwache Evidenz; Einleger können oft zwischen Banken unterscheiden.\nInterbankenverbindlichkeiten: Ansteckung nachgewiesen, aber Größenordnung erklärt nicht Schwere realer Krisen.\nMakroökonmische Rückkopplungen (Fire Sales): Zunehmende Evidenz; erklärt am besten Ausmaß von Krisen.\nGlobale Finanzkrise 2007-09: Alle drei Kanäle aktiv, v.a. Makro-Rückkopplungen über strukturierte Produkte.",
        "Evaluation", "S. 598-599"))

    cards.append(new_card(ch, n, "Ansteckungseffekte in der globalen Finanzkrise 2007-09",
        "Welche Ansteckungskanäle waren in der globalen Finanzkrise 2007-09 aktiv?",
        "Makroschock: Einbruch US-Immobilienpreise.\nInformationsansteckung: Ja, bes. im Interbankenmarkt (Misstrauen über Subprime-Exposition).\nInterbankenverbindlichkeiten: Ja, aber weniger traditionelle Kredite, eher Kreditderivate (CDS), Repos, AIG als zentrale Gegenpartei.\nFire Sales / Makro: Ja, vor allem bei strukturierten Produkten (CDOs, MBS).\nFazit: Alle drei Kanäle aktiv, aber Makro-Rückkopplungen dominierten.",
        "Verständnis", "S. 599"))

    return cards


def cards_chapter6_lolr_detail():
    """Kap 6.6: Lender of Last Resort – Vertiefte Analyse"""
    ch = "Kapitel 6: Finanzkrisen und systemische Risiken"
    n = 6
    cards = []

    cards.append(new_card(ch, n, "Bagehot (1873): 4 Bedingungen des LoLR",
        "Welche vier Bedingungen formuliert Bagehot (1873) für den Lender of Last Resort?",
        "1. Nur an illiquide, aber solvente Finanzinstitutionen leihen (nicht an insolvente).\n2. Strafzins verlangen: Verhindert, dass Banken sich regelmäßig bei LoLR refinanzieren.\n3. Gute Sicherheiten fordern (zu Vorkrisenpreisen bewertet).\n4. Im Vorfeld ankündigen: Banken wissen ex ante, unter welchen Bedingungen Hilfe kommt.",
        "Wiedergabe", "S. 602"))

    cards.append(new_card(ch, n, "Problem 1: Illiquidität vs. Insolvenz",
        "Warum ist die Unterscheidung zwischen Illiquidität und Insolvenz das zentrale Problem des LoLR in der Praxis?",
        "In Krisenzeiten schwer zu unterscheiden, ob Bank illiquide oder insolvent ist.\nAsymmetrische Information: Zentralbank hat keinen vollständigen Zugang zu Bankbuchhaltung.\nZusätzlich: Illiquidität kann zu Insolvenz führen (fire sales erzwingen Unterwertverkäufe).\nFolge: Praktisch kaum möglich, nur illiquide Banken zu unterstützen → Bail-out-Risiko.",
        "Evaluation", "S. 605-606"))

    cards.append(new_card(ch, n, "Problem 2: Moral Hazard – Lender of First Resort",
        "Was ist das Moral-Hazard-Problem beim LoLR und was ist 'konstruktive Ambiguität'?",
        "Banken verlassen sich darauf, im Krisenfall unterstützt zu werden.\n→ Banken halten zu wenig Liquidität (Lender of First Resort statt Last Resort).\nLösung 1: Bagehot-Regel: Strafzins (teuer für die Bank).\nLösung 2: Konstruktive Ambiguität: LoLR gibt ex ante keine Garantie → Unsicherheit erhält Vorsicht.\nProbleme: Konstruktive Ambiguität widerspricht Bagehot-Kriterium 4 (Vorangbekanntmachung).",
        "Evaluation", "S. 607-608"))

    cards.append(new_card(ch, n, "Problem 3: Widerspruch zur Preisstabilität",
        "Warum kann LoLR-Politik mit anderen wirtschaftspolitischen Zielen in Konflikt geraten?",
        "Widerspruch Preisstabilität: In Krisen oft kein Problem (deflationäre Tendenzen), aber lockere Geldpolitik → zukünftige Inflation.\nWechselkursstabilität: Bei festem Wechselkurssystem → expansive Geldpolitik kann Währungskrise auslösen (twin crises).\nFinanzielle Instabilität: Liquiditätszuführungen können Vermögenspreisblasen begünstigen.",
        "Verständnis", "S. 609-610"))

    cards.append(new_card(ch, n, "Warum Interbankenmarkt in Krisen versagt",
        "Warum reicht es nicht aus, Liquidität über den Interbankenmarkt bereitzustellen, wenn einzelne Banken in Not sind?",
        "In Krisenzeiten ist niemand bereit, einer angeschlagenen Bank zu leihen.\nGrund: Asymmetrische Information → Adverse Selektion: Wer Geld leiht, könnte das Risiko übernehmen.\nBanken halten lieber Überschussliquidität (liquidity hoarding).\nHöhere Zinsangebote helfen nicht (adverse Selektion verschlimmert sich).\n→ Nur die Zentralbank kann in aggregierten Liquiditätskrisen effektiv eingreifen.",
        "Verständnis", "S. 603-604"))

    cards.append(new_card(ch, n, "LoLR in der globalen Finanzkrise: EZB-Handeln",
        "Wie handelte die EZB als LoLR in der globalen Finanzkrise und wie wich sie von Bagehots Prinzipien ab?",
        "Massive Liquiditätszuführungen (quantitativ unbegrenzt).\nSelbst insolvente Banken erhielten Liquidität (keine scharfe Trennung möglich).\nSicherheiten: akzeptiert, aber Qualitätsanforderungen gesenkt (höhere Haircuts).\nKein Strafzins (im Gegenteil: Leitzins auf historisches Tief gesenkt).\nAusweitung auf Nicht-Banken (Investmentbanken).\n→ Pragmatische Anpassung der Bagehot-Prinzipien an die Realität einer Systemkrise.",
        "Verständnis", "S. 613-614"))

    cards.append(new_card(ch, n, "Nullzinsgrenze und Quantitative Easing (QE)",
        "Was ist die Nullzinsgrenze und wie reagierte die EZB mit Quantitative Easing (QE)?",
        "Nullzinsgrenze (Zero Lower Bound): Leitzins kann nicht unter null gesenkt werden (begrenzte Wirkung konventioneller Geldpolitik).\nEZB-Reaktion (ab 2014-2016): QE = Aufkauf von Staatsanleihen und anderen Wertpapieren.\nZiel: Zinsen für längere Laufzeiten senken, Bilanzen ausweiten, Kreditvergabe anregen.\nKritik: Risiken für Finanzstabilität (Suche nach Rendite, Vermögenspreisblasen).",
        "Verständnis", "S. 615-616"))

    cards.append(new_card(ch, n, "Empirische Evidenz für LoLR-Wirksamkeit",
        "Was zeigt die empirische Evidenz über die Wirksamkeit der LoLR-Politik?",
        "Positiv: Unbestritten, dass Zentralbanken in der globalen Finanzkrise den Zusammenbruch des Systems abgewandt haben.\nHistorisch: USA 1929-1933: Keine LoLR-Politik → schwere Depression; Gegen-Evidenz für Wirksamkeit.\nNegativ: In Währungskrisen (fester Wechselkurs) hilft LoLR kaum (Deutschland 1931, Thailand 1997).\nRisiko: Lockere Geldpolitik kann zukünftige Krisen begünstigen (Blasenbildung).",
        "Evaluation", "S. 611-612"))

    return cards


def cards_chapter7_detail():
    """Kap 7.1, 7.3, 7.4, 7.5, 7.6: Vertiefte Bankenregulierung"""
    ch = "Kapitel 7: Bankenregulierung"
    n = 7
    cards = []

    # 7.1 Gründe für Bankenregulierung
    cards.append(new_card(ch, n, "Systemisches Risiko als negativer Externalitätseffekt",
        "Warum ist systemisches Risiko ein Marktversagen, das staatliche Regulierung erfordert?",
        "Banken internalisieren die Kosten ihres Zusammenbruchs für andere Banken und die Realwirtschaft nicht vollständig.\nNegative Externalitäten: Zusammenbruch einer Bank schadet anderen (Ansteckung, Fire Sales, Kreditklemme).\nMarktversagen: Banken gehen daher zu hohe systemische Risiken ein.\n→ Staatliche Regulierung soll diese Externalitäten internalisieren (Pigou-Regulierung).",
        "Verständnis", "S. 637-641"))

    cards.append(new_card(ch, n, "Einlegerschutz: Warum Einleger Risiken nicht beurteilen können",
        "Warum ist Einlegerschutz ein eigenständiger Regulierungsgrund neben systemischem Risiko?",
        "Informationsasymmetrie: Einleger können die tatsächliche Risikolage ihrer Bank kaum beurteilen.\nKleineinleger: Zu wenig Ressourcen für Bankanalyse, zu kleines Engagement für Monitoring.\nFolge: Ohne staatlichen Schutz wären Einleger schutzlos.\nZusätzlich: Einlagen erfüllen Zahlungssystemfunktion → Stabilität besonders wichtig.",
        "Verständnis", "S. 642"))

    cards.append(new_card(ch, n, "Warum werden Banken stärker reguliert als Nicht-Banken?",
        "Vergleichen Sie die Regulierungsintensität von Banken mit der von Nicht-Banken und erklären Sie die Unterschiede.",
        "Nicht-Banken (z.B. Einzelhändler): Insolvenz schadet primär Gläubigern und Aktionären.\nBanken: Insolvenz schadet auch unbeteiligten Dritten:\n1. Zahlungssystem: Einlagen = Zahlungsmittel → Systemstörung\n2. Ansteckung: Interbankenverbindlichkeiten → andere Banken\n3. Kreditklemme: Realwirtschaft leidet unter Kreditentzug\n4. Einlagensicherung: Staatliche Garantien → Moral Hazard erfordert Regulierung",
        "Verständnis", "S. 641"))

    # 7.3 Funktionen der EK-Regulierung
    cards.append(new_card(ch, n, "3 Funktionen der Eigenkapitalregulierung – Überblick",
        "Welche drei Funktionen erfüllt die Eigenkapitalregulierung von Banken?",
        "(1) Puffer gegen Verluste: Schutz der Gläubiger, Einlagensicherung und Steuerzahler.\n(2) Frühzeitige Eingriffsmöglichkeit: Wenn EK unter Minimum fällt, kann Aufsicht eingreifen bevor alle Werte vernichtet sind.\n(3) Anreizeffekte (Skin in the game): Banken mit eigenem EK treffen effizientere Risikoentscheidungen.",
        "Wiedergabe", "S. 661"))

    cards.append(new_card(ch, n, "Funktion 1: Puffer gegen Verluste – Wer ist geschützt?",
        "Für wen schafft Eigenkapital einen Verlustpuffer und warum ist die regulatorische EK-Quote kein Puffer für die Bank selbst?",
        "EK schützt: Gläubiger, Einlagenversicherung, Steuerzahler.\nAber: EK ist kein Puffer für die Bank selbst!\nBank darf regulatorisches Minimum nicht unterschreiten → muss sofort Maßnahmen ergreifen.\nNur EK oberhalb des Minimums ist echter Puffer.\nBasel III: Kapitalerhaltungspuffer (+2,5%) und antizyklischer Puffer (0-2,5%) als echte Puffer eingeführt.",
        "Verständnis", "S. 662"))

    cards.append(new_card(ch, n, "Funktion 2: Frühzeitige Eingriffsmöglichkeit",
        "Wie ermöglicht die Eigenkapitalregulierung frühzeitige Eingriffe der Bankenaufsicht?",
        "Wenn EK die regulatorischen Anforderungen unterschreitet: Aufsicht kann eingreifen.\nStufenweise Reaktion: Zunächst Geschäftspolitikbeschränkungen, dann ggf. Abwicklung.\nWichtigkeit des 'Früh': Eingriff bevor alle Werte vernichtet → Insolvenz kostet weniger.\nProblem: Regulatorische EK-Quote spiegelt nicht immer das tatsächliche Risiko wider (Basel-II-Kritik).",
        "Verständnis", "S. 663"))

    cards.append(new_card(ch, n, "Funktion 3: Anreizeffekte – Skin in the Game",
        "Wie verbessern Eigenkapitalanforderungen die Risikoentscheidungen von Banken?",
        "Asset Substitution: Banken mit beschränkter Haftung tendieren zu übermäßiger Risikoübernahme (Verluste begrenzt, Gewinne ungekürzt).\nLösung: EK-Anforderungen erhöhen den 'Skin in the Game' → Bank trägt mehr Verluste selbst.\nFolge: Banken wählen effizientere (risikoärmere) Projekte.\nProblem: Falsche Risikogewichte können trotzdem zu falschen Anreizen führen (Basel I).",
        "Verständnis", "S. 664-666"))

    cards.append(new_card(ch, n, "Asset Substitution bei Banken mit beschränkter Haftung",
        "Wie entsteht Asset Substitution bei Banken und welche Regulierung bekämpft es?",
        "Mechanismus: Hohe Renditen im guten Zustand gehen an Bank; Verluste im schlechten Zustand tragen Gläubiger/Steuerzahler.\n→ Banken bevorzugen riskante Projekte (hohe Streuung) gegenüber sicheren bei gleicher Renditeerwartung.\nBeispiel: Investment in nachrangige CDO-Tranchen statt sichere Staatsanleihen.\nLösung: EK-Anforderungen reduzieren Anreiz, da Bank eigene Verluste trägt.",
        "Verständnis", "S. 665"))

    # 7.4 Schwächen Vorkrisen-Regulierung
    cards.append(new_card(ch, n, "Drei Schwächen der Vorkrisen-Regulierung",
        "Was sind die drei zentralen Schwächen der Vorkrisen-Bankenregulierung (vor 2008)?",
        "(1) Keine hinreichende Berücksichtigung des systemischen Risikos: Individuelle Sicherheit ≠ Systemsicherheit.\n(2) Prozyklizität der EK-Regulierung: In Booms niedrige EK-Anforderungen, in Krisen erhöhte → verstärkt Zyklen.\n(3) Starke Betonung der Aktivseite: Kreditausfallrisiko und Marktrisiko erfasst, aber Refinanzierungsrisiken ignoriert.",
        "Wiedergabe", "S. 667"))

    cards.append(new_card(ch, n, "Schwäche 1: Banken individuell sicher ≠ System sicher",
        "Warum kann ein Bankensystem instabil sein, auch wenn jede einzelne Bank sicher erscheint?",
        "Paradox der Sicherheit: Der Versuch einer Bank, ihr eigenes Risiko zu reduzieren, kann das Systemrisiko erhöhen.\nBeispiel 1: Notverkäufe → Preisverfall trifft andere Banken.\nBeispiel 2: Kreditvergabeeinschränkung → Kreditklemme und Rezession → schadet allen Banken.\nFolge: Mikroprudenzielle Regulierung (eine Bank sicher) reicht nicht → makroprudenzielle Perspektive nötig.",
        "Verständnis", "S. 668"))

    cards.append(new_card(ch, n, "Mikro- vs. makroprudenzielle Regulierung",
        "Was ist der Unterschied zwischen mikro- und makroprudenzieller Regulierung?",
        "Mikroprudenziell: Fokus auf Stabilität einzelner Institute (institution-by-institution).\nMakroprudenziell: Fokus auf Stabilität des gesamten Finanzsystems; berücksichtigt Externalitäten und Vernetzung.\nInstrumente (makro): Antizyklische Puffer, systemische Risikopuffer, LTV-Begrenzungen im Immobilienbereich, Stresstests.\nBasel II: Fast ausschließlich mikroprudenziell → Schwäche erkannt durch Krise.",
        "Verständnis", "S. 668-669"))

    cards.append(new_card(ch, n, "Schwäche 2: Prozyklizität der EK-Regulierung",
        "Erklären Sie den Prozyklizitätsmechanismus bei risikogewichteter EK-Regulierung.",
        "Mechanismus:\n1. Boom: Kreditwürdigkeit steigt, Risikogewichte (PD) fallen → EK-Anforderungen sinken → mehr Kreditvergabe → verstärkt Boom.\n2. Krise: Kreditwürdigkeit fällt, Risikogewichte steigen → EK-Anforderungen steigen → Kreditvergabe sinkt → verschlimmert Krise.\nVerstärkt durch interne Modelle (Basel II): Historische Daten aus Boomphasen unterschätzen Risiken.\nLösung (Basel III): Antizyklische Puffer und Kapitalerhaltungspuffer.",
        "Verständnis", "S. 670-672"))

    cards.append(new_card(ch, n, "Schwäche 3: Aktivseite-Betonung – Refinanzierungsrisiken",
        "Welche Risiken wurden unter Basel II vernachlässigt und wie löst Basel III das Problem?",
        "Basel II erfasste: Kreditausfallrisiko, Marktrisiko, operationelle Risiken → alles Aktivseite.\nVernachlässigt: Refinanzierungsrisiken (Liquiditätsrisiken) = Passivseitenrisiken.\nRefinanzierungsrisiken: Wenn kurzfristige Verbindlichkeiten nicht mehr verlängert werden (funding run).\nProblem: Aktivseiten- und Passivseiten-Risiken interagieren stark.\nLösung Basel III: LCR (kurzfristig) und NSFR (strukturell) als Liquiditätsanforderungen.",
        "Verständnis", "S. 673"))

    # 7.5 Regulierung des systemischen Risikos
    cards.append(new_card(ch, n, "Operationalisierung systemischen Risikos",
        "Wie kann systemisches Risiko gemessen/operationalisiert werden?",
        "Dimensionen:\n• Größe: Zu-groß-zum-Scheitern (Assets, Marktanteile)\n• Vernetzung: Too-interconnected-to-fail (Interbanken-Netzwerke)\n• Korrelation: Too-correlated-to-fail (ähnliche Portfolios)\n• Kontext: Situationsabhängig (in Krise systemisch, in normalem Umfeld nicht)\nZusätzlich: Statistische Maße wie CoVaR.",
        "Verständnis", "S. 674-675"))

    cards.append(new_card(ch, n, "SIFIs: 4 Kategorien (Geneva Report 2009)",
        "Welche vier Kategorien von SIFIs (systemically important financial institutions) werden unterschieden?",
        "1. Individuell systemisch: Too big/interconnected/important/complex to fail.\n2. In der Gruppe systemisch: Too many to fail (viele ähnliche kleine Banken gleichzeitig).\n3. Kontextuell systemisch: Werden in einer Krise systemisch, obwohl sie es normal nicht sind.\n4. Nie systemisch: Deren Ausfall keine systemischen Auswirkungen hätte.",
        "Wiedergabe", "S. 675"))

    cards.append(new_card(ch, n, "CoVaR: Statistisches Maß für systemisches Risiko",
        "Was ist der CoVaR (Adrian/Brunnermeier 2016) und was misst er?",
        "CoVaR = Conditional Value at Risk.\nMisst: Wie stark erhöht sich das Risiko des gesamten Finanzsystems, wenn eine bestimmte Bank in Schwierigkeiten ist?\nVorteil: Stetige Messung der Systemrelevanz, differenziertere Einschätzung als binäre SIFI-Klassifizierung.\nNachteil: Prozyklisch (in Krisen hohe CoVaR-Werte, in Booms niedrig) und unterschiedliche Rankings je nach Methode.",
        "Verständnis", "S. 676"))

    cards.append(new_card(ch, n, "Ziele der Regulierung systemrelevanter Banken",
        "Welche fünf möglichen Regulierungsziele für systemrelevante Banken werden im Skript genannt?",
        "1. Senkung des systemischen Risikos (durch Anreize oder Beschränkungen)\n2. Schaffung eines Puffers für zukünftige Krisen\n3. Finanzierung der Kosten von Krisen (Bankenabgabe)\n4. Reduzierung der Anreize, systemisch zu werden (level playing field)\n5. Beseitigung von Wettbewerbsverzerrungen\nZielsetting wichtig: Maßnahmen müssen auf konkretes Ziel ausgerichtet sein; Ziele können in Konflikt stehen.",
        "Verständnis", "S. 677"))

    cards.append(new_card(ch, n, "Pigou-Steuer auf systemisches Risiko",
        "Was ist eine 'Systemic Risk Tax' (Pigou-Steuer) und warum ist sie schwierig umzusetzen?",
        "Idee: Steuer auf systemisches Risiko = Banken zahlen für die Externalitäten, die sie für andere verursachen.\nVorteil: Internalisierung der Externalitäten ohne direkte Beschränkung der Geschäftstätigkeit.\nNachteil: Sehr schwierig zu kalibrieren (wie hoch ist der soziale Schaden durch systemisches Risiko einer Bank?).\nUmsetzung: Bankenabgabe in Deutschland und EU als Annäherung (nicht risikoadjustiert genug).",
        "Evaluation", "S. 678"))

    cards.append(new_card(ch, n, "Höhere EK-Anforderungen für SIFIs (G-SIB-Zuschlag)",
        "Warum sind höhere EK-Anforderungen für systemrelevante Banken sinnvoll (Admati et al. 2013)?",
        "Vorteile höherer EK-Anforderungen:\n• Puffer für systemische Krisen → absorbiert Verluste ohne Staatshilfe\n• Bessere Anreize: weniger asset substitution, mehr Skin in the Game\n• Verringert Prozyklizität\nAdmati et al. (2013): Argumente gegen mehr EK sind meist falsch oder volkswirtschaftlich irrelevant.\nIn Basel III: G-SIB-Zuschlag 1-3,5% CET1 je nach Systemrelevanz.",
        "Evaluation", "S. 678"))

    cards.append(new_card(ch, n, "Geschäftsmodellregulierung: Volcker-Regel und Trennbanken",
        "Was ist die Volcker-Regel und was ist das Trennbankensystem?",
        "Volcker-Regel (USA, Dodd-Frank 2010): Verbot des Eigenhandels (proprietary trading) für Einlagenbanken.\nTrennbankensystem: Vollständige Trennung von Einlagengeschäft und Investmentbanking.\nVorteil: Verhindert, dass riskante Investmentbankaktivitäten mit staatlich gesicherten Einlagen finanziert werden.\nNachteil: Grenzen zwischen Aktivitäten schwer zu ziehen; kann Diversifikationsvorteile zerstören.",
        "Verständnis", "S. 679"))

    cards.append(new_card(ch, n, "Abwicklungsmechanismus: Ziel und Funktionsweise",
        "Was ist das Ziel eines effektiven Bankabwicklungsregimes (FSB 2011)?",
        "FSB-Definition: 'Abwicklung möglich machen ohne schwere systemische Störung und ohne Steuerbelastung; Schutz lebensnotwendiger Funktionen durch Mechanismen, die Verluste auf Aktionäre und ungesicherte Gläubiger abwälzen.'\nIdee: Spezielles Regime ermöglicht Bankschließung ohne Systemkrise.\nZeitinkonsistenz-Problem: Glaubwürdige ex-ante Bindung, nicht zu retten → verhindert Moral Hazard.",
        "Verständnis", "S. 680-681"))

    cards.append(new_card(ch, n, "Bail-in vs. Bail-out",
        "Was ist der Unterschied zwischen Bail-in und Bail-out und warum wurde Bail-in eingeführt?",
        "Bail-out: Staatliche Rettung der Bank mit Steuermitteln → moralisches Hazard, Privatisierung der Gewinne/Sozialisierung der Verluste.\nBail-in: Verluste werden auf Aktionäre und Gläubiger abgewälzt (Schuldenabschreibung oder Umwandlung in EK).\nVorteil Bail-in: Kein Steuergeld nötig, Moral Hazard reduziert, Gläubigerhierarchie respektiert.\nProblem: In einer Systemkrise kann selbst Bail-in destabilisierend sein.",
        "Verständnis", "S. 681"))

    cards.append(new_card(ch, n, "Contingent Capital / Bail-in-fähige Schulden",
        "Was sind Contingent Capital / bail-in-fähige Schulden und was sind ihre Vor- und Nachteile?",
        "Contingent Capital (CoCos): Schulden, die bei Unterschreiten einer EK-Schwelle automatisch in EK umgewandelt oder abgeschrieben werden.\nVorteil aus Bankperspektive: Steuerliche Abzugsfähigkeit der Zinsen.\nKritik:\n• EK erfüllt Pufferfunktion mindestens ebenso gut\n• Anreizeffekte schwächer als direkte EK-Erhöhung\n• In einer Krise: Konversion könnte Anleger verunsichern und Panik auslösen\n• Unsicher ob Bail-in bei Systemkrise tatsächlich durchgesetzt wird.",
        "Evaluation", "S. 683"))

    # 7.6 Herausforderungen
    cards.append(new_card(ch, n, "Herausforderung: Bankenunion vervollständigen",
        "Was sind die wesentlichen ungelösten Probleme bei der Europäischen Bankenunion?",
        "1. Banken-Staaten-Nexus: Konzentrierte Staatsanleihenbestände der Banken → Regulierung nötig.\n2. Zielkonflikt SSM: EZB gleichzeitig für Geldpolitik und Bankenaufsicht zuständig → Interessenkonflikt.\n3. Glaubwürdigkeit SRM: Einheitlicher Abwicklungsmechanismus muss gestärkt werden.\n4. EDIS: Europäische Einlagenversicherung noch nicht vollständig umgesetzt (fehlendes drittes Säule der Bankenunion).",
        "Verständnis", "S. 685"))

    cards.append(new_card(ch, n, "Regulatory Capture",
        "Was ist Regulatory Capture und warum ist es eine Herausforderung für die Bankenregulierung?",
        "Regulatory Capture: Regulierungsbehörden werden von den regulierten Industrien übermäßig beeinflusst.\nMechanismen: Drehtür (Wechsel zwischen Behörde und Industrie), Lobby, Informationsasymmetrie.\nFolge: Regulierung dient Industrie-Interessen statt öffentlichem Interesse.\nRisiko: Neue Deregulierungswelle durch Banklobby nach Krisenmemoiren.",
        "Verständnis", "S. 686"))

    cards.append(new_card(ch, n, "Regulierung von Nicht-Banken / Schattenbanken und Fintechs",
        "Welche neuen regulatorischen Herausforderungen entstehen durch Schattenbanken und Fintechs?",
        "Schattenbanken: Starkes Wachstum seit der Krise (Investmentfonds, ETFs, Geldmarktfonds).\nRegulierungsarbitrage: Bankaktivitäten verlagern sich in weniger regulierte Bereiche.\nFintechs: Neue Marktteilnehmer mit disruptiven Geschäftsmodellen.\nBigtechs (Amazon, Google, Apple): Eintreten ins Finanzgeschäft → systemisch relevant ohne Bankzulassung?\nHerausforderung: Gleiche Regeln für gleiche Risiken ('same risk, same rules').",
        "Verständnis", "S. 686"))

    cards.append(new_card(ch, n, "Fazit Bankenregulierung: Kernprinzipien",
        "Was sind die zwei Kerninstrumente der modernen Bankenregulierung und welche offene Herausforderung bleibt?",
        "Zwei Kerninstrumente:\n1. Höhere Eigenkapitalanforderungen: Schafft Puffer, verbessert Anreize, ermöglicht Frühintervention.\n2. Glaubwürdige Abwicklungsmechanismen: Reduziert Rettungserwartungen, ermöglicht geordnete Insolvenz.\nOffene Herausforderung: Systemisches Risiko angemessen regulieren, insbes. für G-SIBs.\nAusblick: EK-Anforderungen sollten weiter erhöht werden; Abwicklungsregime muss glaubwürdiger werden.",
        "Synthese", "S. 687-689"))

    return cards


def cards_querschnitt_erweitert():
    """Weitere Wahr/Falsch-Karten und Rechenaufgaben"""
    ch = "Querschnitt: Wahr/Falsch & Klausuraufgaben"
    n = 99
    cards = []

    wf = [
        ("Die Pecking-Order-Theorie sagt eine optimale Ziel-Kapitalstruktur voraus.",
         "FALSCH. Die Pecking-Order-Theorie sagt keine Ziel-Kapitalstruktur voraus. Sie beschreibt eine Finanzierungshierarchie: Innenfinanzierung > FK > EK. Die Kapitalstruktur ist ein historischer Zufallspfad.",
         "S. 421-426"),
        ("Der effektive Steuervorteil τ* ist immer kleiner als der Körperschaftsteuersatz τ_c.",
         "FALSCH. Wenn τ_i = τ_e (z.B. im deutschen Steuersystem mit Abgeltungssteuer), dann τ* = τ_c. τ* < τ_c nur wenn EK-Erträge günstiger besteuert werden als FK-Erträge (τ_e < τ_i).",
         "S. 241"),
        ("Im Diamond-1984-Modell ist ein anreizkompatibler Vertrag immer besser als direkte Kontrolle.",
         "FALSCH. Direktkontrolle (Kosten m·K) ist besser, wenn m klein und schlechte Projekterträge unwahrscheinlich sind. Anreizkompatibler Vertrag besser bei großem m (vielen Investoren).",
         "S. 512-513"),
        ("Calomiris und Kahn (1991) zeigen, dass Bank Runs immer ineffizient sind.",
         "FALSCH. Calomiris/Kahn (1991) zeigen, dass Bank Runs effizient sein können: Sie disziplinieren das Management und verhindern Moral Hazard auf Seiten der Bank.",
         "S. 568-572"),
        ("Ein vollständig vernetztes Interbanken-System (alle Banken mit allen verbunden) ist stabiler als ein unvollständiges (Kettenstruktur).",
         "WAHR. Laut Allen/Gale (2000) sind vollständige Strukturen stabiler, weil Verluste gleichmäßig auf alle Banken verteilt werden. Bei Kettenstruktur konzentrieren sich Verluste und können zu Dominoeffekten führen.",
         "S. 589"),
        ("Eigenkapital schützt eine Bank selbst als Puffer gegen Verluste.",
         "FALSCH. Eigenkapital schützt Gläubiger, Einlagensicherung und Steuerzahler. Für die Bank selbst ist das regulatorische Minimum kein Puffer, weil es nicht unterschritten werden darf. Nur EK über dem Minimum ist ein Puffer.",
         "S. 662"),
        ("Konstruktive Ambiguität widerspricht dem 4. Kriterium von Bagehot.",
         "WAHR. Bagehot verlangt, dass LoLR im Vorfeld die Bedingungen seiner Hilfe ankündigt. Konstruktive Ambiguität (absichtliche Unklarheit über Rettungsbereitschaft) widerspricht dieser Transparenzforderung.",
         "S. 607-608"),
        ("Das Rätsel der geringen Verschuldung besagt, dass Unternehmen sich mehr verschulden als steueroptimal wäre.",
         "FALSCH. Das Rätsel ist, dass Unternehmen WENIGER Fremdkapital halten als steueroptimal wäre. Die Erklärung liegt in Konkurskosten, Agency-Kosten und anderen Friktionen.",
         "S. 271"),
        ("Empire Building bezieht sich auf das Problem, dass Manager Unternehmen in anderen Branchen kaufen wollen.",
         "FALSCH. Empire Building = Manager bevorzugen große Unternehmen (gleiche Branche), um ihr Prestige und Gehalt zu steigern. Es geht um Größe, nicht um Diversifikation.",
         "S. 385"),
        ("Die globale Finanzkrise 2007-09 zeigt, dass makroökonomische Rückkopplungen (Fire Sales, Deleveraging) ein wichtigerer Ansteckungskanal waren als direkte Interbankenverbindlichkeiten.",
         "WAHR. Empirische Evidenz zeigt, dass makroökonomische Rückkopplungen über strukturierte Produkte (CDOs, MBS) die Krise stärker verbreiteten als direkte Interbankenverbindlichkeiten.",
         "S. 599"),
    ]

    for q, a, ref in wf:
        cards.append(new_card(ch, n, "Wahr/Falsch",
            f"Wahr oder Falsch: {q}",
            a, "Evaluation", ref, "true_false"))

    # Weitere Rechenaufgaben
    cards.append(new_card(ch, n, "τ* Berechnung – Effektiver Steuervorteil",
        "Ein Unternehmen hat τ_c = 30%, τ_i = 26%, τ_e = 26% (deutsche Abgeltungssteuer). Berechnen Sie τ* und vergleichen Sie mit τ_c.",
        "τ* = 1 − (1 − τ_c)(1 − τ_e)/(1 − τ_i)\n= 1 − (1 − 0,30)(1 − 0,26)/(1 − 0,26)\n= 1 − (0,70 × 0,74)/0,74\n= 1 − 0,70 = 0,30 = τ_c\nWeil τ_i = τ_e: τ* = τ_c (Investorensteuern heben sich auf).",
        "Transfer", "S. 240-241",
        formula="\\tau^* = 1 - \\frac{(1-\\tau_c)(1-\\tau_e)}{1-\\tau_i}",
        variables={"τ_c": "30%", "τ_i": "26%", "τ_e": "26%"},
        solution_steps=["τ* = 1 − (0,70 × 0,74)/0,74", "= 1 − 0,70 = 30%", "τ* = τ_c da τ_i = τ_e"]))

    cards.append(new_card(ch, n, "Trade-Off-Theorie: Optimaler Unternehmenswert",
        "VU = 400 Mio., τ* = 25%, D = 200 Mio. BW(Konkurskosten) = 15 Mio., BW(Agency-Kosten) = 10 Mio., BW(Agency-Nutzen) = 8 Mio. Berechnen Sie VL.",
        "VL = VU + τ*·D − BW(KK) − BW(AK) + BW(AN)\n= 400 + 0,25·200 − 15 − 10 + 8\n= 400 + 50 − 15 − 10 + 8\n= 433 Mio. Euro",
        "Transfer", "S. 390",
        formula="V_L = V_U + \\tau^* D - BW(KK) - BW(AK) + BW(AN)",
        variables={"V_U": "400 Mio.", "τ*": "25%", "D": "200 Mio.", "BW(KK)": "15 Mio.", "BW(AK)": "10 Mio.", "BW(AN)": "8 Mio."},
        solution_steps=["τ*·D = 0,25 × 200 = 50 Mio.", "VL = 400 + 50 − 15 − 10 + 8 = 433 Mio."]))

    cards.append(new_card(ch, n, "LCR berechnen",
        "Eine Bank hat HQLA von 500 Mio. Euro und erwartet Nettoabflüsse in einem 30-Tage-Stressszenario von 400 Mio. Euro. Ist die LCR-Anforderung erfüllt?",
        "LCR = HQLA / Nettoabflüsse = 500 / 400 = 1,25 = 125%\nMindestanforderung: LCR ≥ 100%\n→ Anforderung erfüllt. Bank hat 25% Puffer.",
        "Transfer", "S. 256",
        formula="LCR = \\frac{HQLA}{\\text{Nettoabflüsse (30 Tage)}} \\geq 100\\%",
        variables={"HQLA": "500 Mio. Euro", "Nettoabflüsse": "400 Mio. Euro"},
        solution_steps=["LCR = 500/400 = 1,25 = 125%", "125% ≥ 100% → Anforderung erfüllt"]))

    cards.append(new_card(ch, n, "Risikogewichtete Eigenkapitalquote",
        "Eine Bank hat Tier-1-EK von 8 Mrd. Euro und risikogewichtete Aktiva (RWA) von 80 Mrd. Euro. Wie hoch ist die Tier-1-EK-Quote und ist die Basel-III-Mindestanforderung erfüllt?",
        "Tier-1-EK-Quote = Tier-1-EK / RWA = 8 / 80 = 10%\nMindesanforderung Basel III: Tier-1 ≥ 6% (+ 2,5% Kapitalerhaltungspuffer = 8,5% effektiv)\n→ 10% > 8,5% → Anforderung (inkl. Puffer) erfüllt.",
        "Transfer", "S. 254",
        formula="\\text{Tier-1-Quote} = \\frac{\\text{Tier-1-EK}}{RWA}",
        variables={"Tier-1-EK": "8 Mrd. Euro", "RWA": "80 Mrd. Euro"},
        solution_steps=["Tier-1-Quote = 8/80 = 10%", "10% > Mindestandforderung 6% (+ 2,5% = 8,5%)"]))

    return cards


def build_all_cards():
    all_cards = []
    all_cards.extend(cards_chapter1())
    all_cards.extend(cards_chapter2())
    all_cards.extend(cards_chapter3())
    all_cards.extend(cards_chapter4())
    all_cards.extend(cards_chapter4_steuern_detail())
    all_cards.extend(cards_chapter4_agency_nutzen())
    all_cards.extend(cards_chapter4_asymm_info())
    all_cards.extend(cards_chapter5())
    all_cards.extend(cards_chapter5_diamond84())
    all_cards.extend(cards_chapter6())
    all_cards.extend(cards_chapter6_dd_detail())
    all_cards.extend(cards_chapter6_eff_runs())
    all_cards.extend(cards_chapter6_ansteckung())
    all_cards.extend(cards_chapter6_lolr_detail())
    all_cards.extend(cards_chapter7())
    all_cards.extend(cards_chapter7_detail())
    all_cards.extend(cards_querschnitt())
    all_cards.extend(cards_querschnitt_erweitert())
    return all_cards


def build_glossary():
    """Glossar mit wichtigen Begriffen, geordnet nach Kapitel."""
    glossary = [
        # Kapitel 1
        {"term": "Finanzintermediation", "definition": "Vermittlung zwischen Kapitalgebern (Sparern) und Kapitalnehmern durch eine dritte Partei (Finanzintermediär wie Banken).", "chapter": 1, "slideRef": "S. 22"},
        {"term": "Direkte Finanzierung", "definition": "Kapitalnehmer und -geber tauschen direkt Wertpapiere auf Finanzmärkten aus, ohne Intermediär.", "chapter": 1, "slideRef": "S. 22"},
        {"term": "Indirekte Finanzierung", "definition": "Finanzierung über einen Zwischenhändler (Intermediär), der Einlagen entgegennimmt und Kredite vergibt.", "chapter": 1, "slideRef": "S. 22"},
        {"term": "Adverse Selektion", "definition": "Phänomen, bei dem Informationsasymmetrien vor Vertragsschluss dazu führen, dass schlechte Risiken gute verdrängen.", "chapter": 1, "slideRef": "S. 29"},
        {"term": "Moral Hazard", "definition": "Verhaltensunsicherheit nach Vertragsschluss: informierte Partei verhält sich anders als erwartet (hidden action).", "chapter": 1, "slideRef": "S. 30"},
        {"term": "Diversifikation", "definition": "Streuung von Investments über verschiedene Anlagen, um idiosynkratische Risiken zu eliminieren.", "chapter": 1, "slideRef": "S. 31"},
        {"term": "Liquiditätstransformation", "definition": "Umwandlung kurzfristiger Einlagen in langfristige Kredite durch Finanzintermediäre.", "chapter": 1, "slideRef": "S. 31"},
        {"term": "Systemisches Risiko", "definition": "Risiko des Zusammenbruchs des gesamten Finanzsystems oder wesentlicher Teile davon.", "chapter": 1, "slideRef": "S. 34"},
        {"term": "Disintermediation", "definition": "Trend zur direkten Unternehmensfinanzierung über Märkte, unter Umgehung von Finanzintermediären.", "chapter": 1, "slideRef": "S. 53"},
        {"term": "Schattenbankensektor", "definition": "Finanzintermediäre außerhalb der klassischen Bankenregulierung (Hedgefonds, Geldmarktfonds, SPVs).", "chapter": 1, "slideRef": "S. 54"},
        {"term": "Corporate Governance", "definition": "Mechanismen, die sicherstellen, dass das Management im Sinne der Investoren handelt.", "chapter": 1, "slideRef": "S. 47"},
        {"term": "Overbanking", "definition": "Zu stark bankbasiertes Finanzsystem, das nach Bankenkrisen Unternehmen ohne alternative Finanzierungsquellen lässt.", "chapter": 1, "slideRef": "S. 51"},
        # Kapitel 2
        {"term": "Bankenkrise", "definition": "Gleichzeitiger Zusammenbruch eines signifikanten Teils des Bankensektors (systemische Krise).", "chapter": 2, "slideRef": "S. 63"},
        {"term": "Bank Run", "definition": "Massenabhebung von Einlagen bei einer Bank, ausgelöst durch (berechtigte oder unberechtigte) Solvenzbedenken.", "chapter": 2, "slideRef": "S. 63"},
        {"term": "Subprime-Kredite", "definition": "Kredite an hochriskante Schuldner mit geringer Kreditwürdigkeit; Hauptauslöser der Krise 2007-09.", "chapter": 2, "slideRef": "S. 72"},
        {"term": "CDO (Collateralized Debt Obligation)", "definition": "Strukturiertes Kreditprodukt, das Bündel von Krediten in Tranchen unterschiedlicher Seniorität aufteilt.", "chapter": 2, "slideRef": "S. 74"},
        {"term": "Fire Sales", "definition": "Erzwungener Notverkauf von Vermögenswerten in fallenden Märkten, der Preise weiter drückt.", "chapter": 2, "slideRef": "S. 81"},
        {"term": "Staaten-Banken-Nexus", "definition": "Wechselseitige Abhängigkeit zwischen Bankensolvenz und Staatsfinanzen, die Krisen verschärft.", "chapter": 2, "slideRef": "S. 83"},
        {"term": "Contagion (Ansteckung)", "definition": "Übertragung von Finanzproblemen von einer Institution/einem Land auf andere.", "chapter": 2, "slideRef": "S. 85"},
        {"term": "Search for yield", "definition": "Verhalten von Investoren in Niedrigzinsumfeld, die zur Renditesteigerung höhere Risiken eingehen.", "chapter": 2, "slideRef": "S. 74"},
        {"term": "OMT-Programm", "definition": "Outright Monetary Transactions: EZB-Anleihekaufprogramm (Sept 2012), an ESM-Konditionalität geknüpft, nie aktiviert.", "chapter": 2, "slideRef": "S. 88"},
        {"term": "ESM (Europäischer Stabilitätsmechanismus)", "definition": "Permanenter Krisenfonds der Eurozone (ab Okt 2012), Nachfolger von EFSF.", "chapter": 2, "slideRef": "S. 87"},
        # Kapitel 3
        {"term": "Kapitalstruktur", "definition": "Relative Anteile von Eigen- und Fremdkapital an der Passivseite der Unternehmensbilanz.", "chapter": 3, "slideRef": "S. 102"},
        {"term": "Residual Claimant", "definition": "Eigenkapitalgeber als Restanspruchsinhaber nach Bedienung aller anderen Verpflichtungen.", "chapter": 3, "slideRef": "S. 104"},
        {"term": "Modigliani-Miller-Theorem", "definition": "In vollkommenen Märkten ist der Unternehmenswert unabhängig von der Kapitalstruktur.", "chapter": 3, "slideRef": "S. 112"},
        {"term": "Homemade Leverage", "definition": "Replikation des Auszahlungsprofils eines verschuldeten Unternehmens durch persönliche Kreditaufnahme eines Investors.", "chapter": 3, "slideRef": "S. 115"},
        {"term": "WACC (Weighted Average Cost of Capital)", "definition": "Gewichtete durchschnittliche Kapitalkosten = gewichteter Durchschnitt aus EK- und FK-Kosten.", "chapter": 3, "slideRef": "S. 125"},
        {"term": "Beta-Faktor", "definition": "Maß des systematischen Risikos: Sensitivität der Wertpapierrendite gegenüber Marktrendite.", "chapter": 3, "slideRef": "S. 130"},
        {"term": "Asset-Beta (β_U)", "definition": "Beta des unverschuldeten Unternehmens; misst das Marktrisiko der zugrundeliegenden Vermögensgegenstände.", "chapter": 3, "slideRef": "S. 131"},
        {"term": "Leverage (Verschuldungsgrad)", "definition": "D/E: Verhältnis von Fremdkapital zu Eigenkapital.", "chapter": 3, "slideRef": "S. 124"},
        {"term": "Marktwertbilanz", "definition": "Bilanz, in der alle Positionen zu aktuellen Marktwerten bewertet sind.", "chapter": 3, "slideRef": "S. 119"},
        {"term": "Kapitalverwässerung", "definition": "Angeblicher Rückgang des Aktienkurses durch Ausgabe neuer Aktien – oft ein Trugschluss.", "chapter": 3, "slideRef": "S. 142"},
        # Kapitel 4
        {"term": "Steuerlicher Debt Bias", "definition": "Verzerrung des Steuersystems zugunsten von Fremdkapital, da Zinsen steuerlich abzugsfähig sind.", "chapter": 4, "slideRef": "S. 148"},
        {"term": "Trade-Off-Theorie", "definition": "Optimale Kapitalstruktur durch Abwägung von Steuervorteil (FK) und Konkurskosten.", "chapter": 4, "slideRef": "S. 159"},
        {"term": "Asset Substitution", "definition": "Ersetzen risikoarmer durch risikoreichere Projekte in Notlage (Agency-Kosten), zum Nachteil der Gläubiger.", "chapter": 4, "slideRef": "S. 163"},
        {"term": "Schuldenüberhang (Debt Overhang)", "definition": "Unterinvestitionsproblem bei hoch verschuldeten Unternehmen (Myers 1977): Profitable Projekte werden abgelehnt.", "chapter": 4, "slideRef": "S. 166"},
        {"term": "Leverage Ratchet Effect", "definition": "Sperrklinkeneffekt: Aktionäre erhöhen Verschuldung, reduzieren sie aber nicht (Admati et al. 2017).", "chapter": 4, "slideRef": "S. 170"},
        {"term": "Covenant", "definition": "Kreditklausel, die die Handlungsfreiheit des Schuldners einschränkt (z.B. Ausschüttungsbegrenzungen).", "chapter": 4, "slideRef": "S. 172"},
        {"term": "Pecking Order Theory", "definition": "Hierarchie der Finanzierungsquellen: Innenfinanzierung > Fremdkapital > Eigenkapital.", "chapter": 4, "slideRef": "S. 175"},
        {"term": "VL = VU + BW(TV) - BW(KK)", "definition": "Wert verschuldetes Unternehmen = Wert unverschuldet + Barwert Steuervorteil − Barwert Konkurskosten.", "chapter": 4, "slideRef": "S. 159"},
        # Kapitel 5
        {"term": "Diamond-Dybvig-Modell", "definition": "Modell zur Erklärung der Existenz von Banken als Liquiditätsversicherung und der Fragilität durch Bank Runs.", "chapter": 5, "slideRef": "S. 203"},
        {"term": "Costly State Verification", "definition": "Annahme, dass Kapitalgeber Erträge nur kostenpflichtig beobachten können (Gale/Hellwig 1985).", "chapter": 5, "slideRef": "S. 223"},
        {"term": "Delegierte Kontrolle", "definition": "Bank übernimmt stellvertretend für viele Einleger die Überwachung der Kreditnehmer (Diamond 1984).", "chapter": 5, "slideRef": "S. 220"},
        {"term": "Losgrößentransformation", "definition": "Bündelung kleiner Einlagen zu großen Krediten durch den Finanzintermediär.", "chapter": 5, "slideRef": "S. 201"},
        {"term": "Fristentransformation", "definition": "Umwandlung kurzfristiger Verbindlichkeiten (Einlagen) in langfristige Forderungen (Kredite).", "chapter": 5, "slideRef": "S. 200"},
        {"term": "Früher/Später Konsument (DD)", "definition": "Im DD-Modell: Typ 1 = früher Konsument (braucht Liquidität in t=1), Typ 2 = später (konsumiert in t=2).", "chapter": 5, "slideRef": "S. 207"},
        {"term": "First-best-Lösung", "definition": "Pareto-optimale Allokation eines allwissenden sozialen Planers; oft nicht direkt implementierbar.", "chapter": 5, "slideRef": "S. 212"},
        {"term": "Standardkreditvertrag", "definition": "Optimaler Finanzkontrakt bei Costly State Verification: fester Rückzahlungsbetrag h; Strafe bei Unterschreiten (= Kreditvertrag).", "chapter": 5, "slideRef": "S. 510"},
        {"term": "Delegationskosten", "definition": "Kosten der Übertragung der Kontrollfunktion auf einen Finanzintermediär; gegen null für große N durch Diversifikation.", "chapter": 5, "slideRef": "S. 514"},
        {"term": "Diversifikation (Diamond 1984)", "definition": "Finanzierung vieler unkorrelierter Projekte durch die Bank; lässt Delegationskosten gegen null konvergieren (Gesetz der Großen Zahlen).", "chapter": 5, "slideRef": "S. 517"},
        # Kapitel 6 – erweitert
        {"term": "Sequential Service Constraint", "definition": "Einleger werden in Reihenfolge der Ankunft bedient (first come, first served); Anreiz zur frühen Kontrolle.", "chapter": 6, "slideRef": "S. 533"},
        {"term": "Lender of Last Resort (LoLR)", "definition": "Zentralbank als letzte Kreditquelle für illiquide aber solvente Banken in Krisen.", "chapter": 6, "slideRef": "S. 601"},
        {"term": "Bagehot-Regel", "definition": "LoLR-Prinzipien: Nur an solvente illiquide Banken leihen; zu Strafzins; gegen gute Sicherheiten; ex ante ankündigen.", "chapter": 6, "slideRef": "S. 602"},
        {"term": "Too-big-to-fail (TBTF)", "definition": "Systemrelevante Banken werden gerettet, weil ihr Zusammenbruch das gesamte System gefährdet.", "chapter": 6, "slideRef": "S. 240"},
        {"term": "Narrow Banking", "definition": "Trennbanksystem: Einlagen nur in risikolose Aktiva anlegen → kein Bank Run möglich.", "chapter": 6, "slideRef": "S. 232"},
        {"term": "Einlagenversicherung", "definition": "Staatliche/privatwirtschaftliche Garantie für Bankeinlagen bis zu einem Limit; eliminiert schlechtes Gleichgewicht (Bank Run).", "chapter": 6, "slideRef": "S. 234"},
        {"term": "Selbsterfüllende Erwartung", "definition": "Erwartungen, die, wenn sie von genug Akteuren geteilt werden, ihr eigenes Eintreten bewirken (z.B. Bank Run).", "chapter": 6, "slideRef": "S. 231"},
        {"term": "Ansteckung (Contagion)", "definition": "Ausbreitung von Bankproblemen auf andere Institute über Information, Interbanken-Verbindlichkeiten oder makroök. Rückkopplungen.", "chapter": 6, "slideRef": "S. 578"},
        {"term": "Bankenkrise (Banking Panic)", "definition": "Simultaner Zusammenbruch eines signifikanten Teils des Bankensystems; geht über einzelne Bank Run hinaus.", "chapter": 6, "slideRef": "S. 578"},
        {"term": "Deleveraging", "definition": "Bilanzsummenreduktion durch Banken in Krisenzeiten; kann Kreditklemme und Rezession verschärfen (finanzieller Akzelerator).", "chapter": 6, "slideRef": "S. 595"},
        {"term": "Konstruktive Ambiguität", "definition": "Absichtliche Unklarheit der Zentralbank über Rettungsbereitschaft; soll Moral Hazard begrenzen, widerspricht Bagehot-Kriterium 4.", "chapter": 6, "slideRef": "S. 607"},
        {"term": "Quantitative Easing (QE)", "definition": "Aufkauf langfristiger Wertpapiere durch Zentralbank bei Nullzinsgrenze; unkonventionelles Instrument der Geldpolitik.", "chapter": 6, "slideRef": "S. 615"},
        {"term": "Marktdisziplin", "definition": "Überwachung von Banken durch informierte Gläubiger (z.B. nachrangige Anleihegläubiger) als Ergänzung staatlicher Regulierung.", "chapter": 6, "slideRef": "S. 574"},
        {"term": "Nachrangige Schulden (Subordinated Debt)", "definition": "FK, das erst nach vorrangigen Gläubigern bedient wird; Träger haben Anreiz zur Bankenüberwachung (Calomiris-Vorschlag).", "chapter": 6, "slideRef": "S. 575"},
        # Kapitel 7 – erweitert
        {"term": "RWA (Risikogewichtete Aktiva)", "definition": "Summe aller Aktiva gewichtet nach Risikogehalt; Grundlage für EK-Anforderungen.", "chapter": 7, "slideRef": "S. 250"},
        {"term": "CET1 (Common Equity Tier 1)", "definition": "Hartes Kernkapital: Stammaktien + einbehaltene Gewinne; höchste Qualität im Basel-III-Kapital; mind. 4,5% RWA.", "chapter": 7, "slideRef": "S. 254"},
        {"term": "LCR (Liquidity Coverage Ratio)", "definition": "Kurzfristige Liquiditätsanforderung: HQLA / 30-Tage-Nettoabflüsse ≥ 100%.", "chapter": 7, "slideRef": "S. 256"},
        {"term": "NSFR (Net Stable Funding Ratio)", "definition": "Strukturelle Liquiditätsanforderung: stabile Refinanzierung für illiquide Aktiva ≥ 100%.", "chapter": 7, "slideRef": "S. 256"},
        {"term": "Leverage Ratio", "definition": "Nicht-risikobasierte EK-Quote: Tier-1-Kapital / Gesamtexposition ≥ 3%.", "chapter": 7, "slideRef": "S. 255"},
        {"term": "Makroprudenzielle Regulierung", "definition": "Regulierung zum Schutz des gesamten Finanzsystems (systemische Perspektive), z.B. antizyklische Puffer.", "chapter": 7, "slideRef": "S. 257"},
        {"term": "Mikroprudenzielle Regulierung", "definition": "Regulierung auf Ebene einzelner Institute; berücksichtigt keine Externalitäten auf das Gesamtsystem.", "chapter": 7, "slideRef": "S. 668"},
        {"term": "SSM (Single Supervisory Mechanism)", "definition": "Einheitlicher Aufsichtsmechanismus: EZB beaufsichtigt direkt bedeutende Banken der Eurozone (ab Nov. 2014).", "chapter": 7, "slideRef": "S. 248"},
        {"term": "SRM (Single Resolution Mechanism)", "definition": "Einheitlicher Abwicklungsmechanismus: gemeinsame Abwicklungsregeln + Behörde (SRB) + Fonds (SRF) für EU-Banken.", "chapter": 7, "slideRef": "S. 260"},
        {"term": "EDIS (European Deposit Insurance Scheme)", "definition": "Geplante europäische Einlagenversicherung als dritte Säule der Bankenunion; noch nicht vollständig umgesetzt.", "chapter": 7, "slideRef": "S. 685"},
        {"term": "Regulierungsarbitrage", "definition": "Verlagerung von Bankaktivitäten in weniger regulierte Bereiche (→ Schattenbanken).", "chapter": 7, "slideRef": "S. 259"},
        {"term": "G-SIB (Global Systemically Important Bank)", "definition": "Global systemrelevante Bank; unterliegt zusätzlichen EK-Anforderungen (G-SIB-Zuschlag 1-3,5% CET1) und Aufsicht.", "chapter": 7, "slideRef": "S. 254"},
        {"term": "Bail-in", "definition": "Verlustbeteiligung der Gläubiger bei Bankabwicklung durch Schuldenabschreibung oder -umwandlung in EK.", "chapter": 7, "slideRef": "S. 681"},
        {"term": "Bail-out", "definition": "Staatliche Rettung einer Bank mit Steuermitteln; schafft Moral Hazard und sozialisiert Verluste.", "chapter": 7, "slideRef": "S. 681"},
        {"term": "Contingent Capital (CoCos)", "definition": "Bedingte Pflichtwandelanleihen: werden bei Unterschreiten einer EK-Schwelle automatisch in EK umgewandelt.", "chapter": 7, "slideRef": "S. 683"},
        {"term": "TLAC/MREL", "definition": "Total Loss Absorbing Capacity / Minimum Requirement for Own Funds and Eligible Liabilities: Mindestanforderungen für bail-in-fähige Verbindlichkeiten.", "chapter": 7, "slideRef": "S. 576"},
        {"term": "SIFI (Systemically Important Financial Institution)", "definition": "Systemrelevantes Finanzinstitut, dessen Ausfall das gesamte Finanzsystem gefährden kann (too big/interconnected/complex to fail).", "chapter": 7, "slideRef": "S. 675"},
        {"term": "CoVaR (Conditional Value at Risk)", "definition": "Statistisches Maß für systemisches Risiko: Risiko des Gesamtsystems gegeben, dass eine bestimmte Bank in Schwierigkeiten ist (Adrian/Brunnermeier 2016).", "chapter": 7, "slideRef": "S. 676"},
        {"term": "Prozyklizität", "definition": "EK-Regulierung, die in Booms Kreditexpansion fördert und in Krisen Kreditvergabe einschränkt → verstärkt Konjunkturzyklen.", "chapter": 7, "slideRef": "S. 670"},
        {"term": "Antizyklischer Kapitalpuffer", "definition": "Basel-III-Instrument: 0-2,5% CET1 zusätzlich in Boomzeiten; gibt Puffer für Krisenzeiten und dämpft Prozyklizität.", "chapter": 7, "slideRef": "S. 653"},
        {"term": "Regulatory Capture", "definition": "Übermäßige Einflussnahme der regulierten Industrie auf Regulierungsbehörden; gefährdet Effektivität der Regulierung.", "chapter": 7, "slideRef": "S. 686"},
        {"term": "Volcker-Regel", "definition": "US-Regulierung (Dodd-Frank 2010): Verbietet Eigenhandel (proprietary trading) bei Einlagenbanken.", "chapter": 7, "slideRef": "S. 679"},
        {"term": "Kapitalerhaltungspuffer", "definition": "Basel III: 2,5% CET1 über Mindestquote; bei Unterschreiten: Ausschüttungsbeschränkungen; schafft echten Puffer.", "chapter": 7, "slideRef": "S. 653"},
        # Kapitel 4 – zusätzliche Begriffe
        {"term": "Hackordnung (Pecking Order)", "definition": "Finanzierungshierarchie aufgrund adverser Selektion: Innenfinanzierung > Fremdkapital > Eigenkapital (Myers/Majluf 1984).", "chapter": 4, "slideRef": "S. 422"},
        {"term": "Signaling-Theorie (Ross 1977)", "definition": "Verschuldung als glaubwürdiges Signal zukünftiger Cashflows: nur erfolgreiche Unternehmen können sich hohe Schulden leisten.", "chapter": 4, "slideRef": "S. 403"},
        {"term": "Lemons-Problem (Akerlof 1970)", "definition": "Adverse Selektion durch Informationsasymmetrie: schlechte Qualitäten verdrängen gute vom Markt; gilt auch für Kapitalmärkte.", "chapter": 4, "slideRef": "S. 406"},
        {"term": "Empire Building", "definition": "Managerverhalten: Unternehmen vergrößern für persönliches Prestige/Gehalt, unabhängig von Rentabilität.", "chapter": 4, "slideRef": "S. 385"},
        {"term": "Overconfidence", "definition": "Systematischer Optimismus von Managern, der zu Überinvestitionen und schlechten Akquisitionen führt.", "chapter": 4, "slideRef": "S. 386"},
        {"term": "Free Cash Flow (Jensen 1986)", "definition": "Cash über dem hinaus, was für positive KW-Projekte und Schuldendienst nötig ist; kann zu Fehlinvestitionen führen.", "chapter": 4, "slideRef": "S. 387"},
        {"term": "Management Entrenchment", "definition": "Manager nutzen ihre Position, um sich zu 'verschanzen' und zu eigenem Vorteil, nicht im Aktionärsinteresse zu handeln.", "chapter": 4, "slideRef": "S. 371"},
        {"term": "Gehebelte Rekapitalisierung", "definition": "Aufnahme von Fremdkapital zur Finanzierung eines Aktienrückkaufs; erhöht Verschuldungsgrad und realisiert Steuervorteil.", "chapter": 4, "slideRef": "S. 219"},
        {"term": "Effektiver Steuervorteil (τ*)", "definition": "Steuervorteil des Fremdkapitals nach Berücksichtigung der Investorenbesteuerung: τ* = 1 − (1−τ_c)(1−τ_e)/(1−τ_i).", "chapter": 4, "slideRef": "S. 240"},
    ]
    return glossary


def validate(cards):
    required = ["id", "chapter", "chapterNum", "topic", "question", "answer",
                "difficultyLevel", "slideRef", "type", "learning"]
    errors = []
    ids = set()
    for i, card in enumerate(cards):
        for field in required:
            if field not in card:
                errors.append(f"Card {i}: missing field '{field}'")
        if card["id"] in ids:
            errors.append(f"Card {i}: duplicate ID {card['id']}")
        ids.add(card["id"])
    return errors


def main():
    print("Generating comprehensive FMI flashcards...")
    cards = build_all_cards()
    
    errors = validate(cards)
    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        return
    
    print(f"Generated {len(cards)} cards")
    
    # Count by chapter
    from collections import Counter
    ch_counts = Counter(c["chapterNum"] for c in cards)
    for ch_num, count in sorted(ch_counts.items()):
        ch_name = next(c["chapter"] for c in cards if c["chapterNum"] == ch_num)
        print(f"  Kapitel {ch_num}: {count} Karten ({ch_name[:45]})")
    
    # Count by difficulty
    diff_counts = Counter(c["difficultyLevel"] for c in cards)
    print("\nNach Schwierigkeitsgrad:")
    for d, count in sorted(diff_counts.items()):
        print(f"  {d}: {count}")
    
    # Write flashcards – format for React app (flashcards key)
    out = {
        "cards": cards,
        "flashcards": cards,  # legacy key some components might use
        "meta": {
            "generatedAt": datetime.now().isoformat(),
            "generated": datetime.now().isoformat(),
            "total": len(cards),
            "totalCards": len(cards),
            "course": "Finanzmärkte und -institutionen SS2026",
            "professor": "Prof. Farzad Saidi",
            "university": "Universität Bonn",
            "byStatus": {"ok": len(cards), "review": 0}
        }
    }
    
    import os
    root = os.path.join(os.path.dirname(__file__), "..", "..")
    
    for path in [
        os.path.join(root, "flashcards.json"),
        os.path.join(root, "public", "data", "flashcards.json")
    ]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\nWrote: {path}")
    
    # Write glossary
    glossary = build_glossary()
    gout = {"terms": glossary, "meta": {
        "generated": datetime.now().isoformat(),
        "total": len(glossary)
    }}
    
    for path in [
        os.path.join(root, "glossary.json"),
        os.path.join(root, "public", "data", "glossary.json")
    ]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(gout, f, ensure_ascii=False, indent=2)
        print(f"Wrote: {path}")
    
    print(f"\n✓ Done. {len(cards)} Karten und {len(glossary)} Glossareinträge geschrieben.")


if __name__ == "__main__":
    main()
