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


def build_all_cards():
    all_cards = []
    all_cards.extend(cards_chapter1())
    all_cards.extend(cards_chapter2())
    all_cards.extend(cards_chapter3())
    all_cards.extend(cards_chapter4())
    all_cards.extend(cards_chapter5())
    all_cards.extend(cards_chapter6())
    all_cards.extend(cards_chapter7())
    all_cards.extend(cards_querschnitt())
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
        # Kapitel 6
        {"term": "Lender of Last Resort (LoLR)", "definition": "Zentralbank als letzte Kreditquelle für illiquide aber solvente Banken in Krisen.", "chapter": 6, "slideRef": "S. 238"},
        {"term": "Bagehot-Regel", "definition": "In Krisen: großzügig leihen, aber zu Strafzins und gegen gute Sicherheiten.", "chapter": 6, "slideRef": "S. 238"},
        {"term": "Too-big-to-fail (TBTF)", "definition": "Systemrelevante Banken werden gerettet, weil ihr Zusammenbruch das gesamte System gefährdet.", "chapter": 6, "slideRef": "S. 240"},
        {"term": "Narrow Banking", "definition": "Trennbanksystem: Einlagen nur in risikolose Aktiva anlegen → kein Bank Run möglich.", "chapter": 6, "slideRef": "S. 232"},
        {"term": "Einlagenversicherung", "definition": "Staatliche/privatwirtschaftliche Garantie für Bankeinlagen bis zu einem Limit.", "chapter": 6, "slideRef": "S. 234"},
        {"term": "Selbsterfüllende Erwartung", "definition": "Erwartungen, die, wenn sie von genug Akteuren geteilt werden, ihr eigenes Eintreten bewirken (z.B. Bank Run).", "chapter": 6, "slideRef": "S. 231"},
        # Kapitel 7
        {"term": "RWA (Risikogewichtete Aktiva)", "definition": "Summe aller Aktiva gewichtet nach Risikogehalt; Grundlage für EK-Anforderungen.", "chapter": 7, "slideRef": "S. 250"},
        {"term": "CET1 (Common Equity Tier 1)", "definition": "Hartes Kernkapital: Stammaktien + einbehaltene Gewinne; höchste Qualität im Basel-III-Kapital.", "chapter": 7, "slideRef": "S. 254"},
        {"term": "LCR (Liquidity Coverage Ratio)", "definition": "Kurzfristige Liquiditätsanforderung: HQLA / 30-Tage-Nettoabflüsse ≥ 100%.", "chapter": 7, "slideRef": "S. 256"},
        {"term": "NSFR (Net Stable Funding Ratio)", "definition": "Strukturelle Liquiditätsanforderung: stabile Refinanzierung für illiquide Aktiva ≥ 100%.", "chapter": 7, "slideRef": "S. 256"},
        {"term": "Leverage Ratio", "definition": "Nicht-risikobasierte EK-Quote: Tier-1-Kapital / Gesamtexposition ≥ 3%.", "chapter": 7, "slideRef": "S. 255"},
        {"term": "Makroprudenzielle Regulierung", "definition": "Regulierung zum Schutz des gesamten Finanzsystems (systemische Perspektive), z.B. antizyklische Puffer.", "chapter": 7, "slideRef": "S. 257"},
        {"term": "SSM (Single Supervisory Mechanism)", "definition": "Einheitlicher Aufsichtsmechanismus: EZB beaufsichtigt direkt bedeutende Banken der Eurozone.", "chapter": 7, "slideRef": "S. 248"},
        {"term": "Regulierungsarbitrage", "definition": "Verlagerung von Bankaktivitäten in weniger regulierte Bereiche (→ Schattenbanken).", "chapter": 7, "slideRef": "S. 259"},
        {"term": "G-SIB (Global Systemically Important Bank)", "definition": "Global systemrelevante Bank; unterliegt zusätzlichen EK-Anforderungen und Aufsicht.", "chapter": 7, "slideRef": "S. 254"},
        {"term": "Bail-in", "definition": "Verlustbeteiligung der Gläubiger bei Bankabwicklung, als Alternative zum staatlichen Bail-out.", "chapter": 7, "slideRef": "S. 241"},
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
