# fmi-flashcards

KI-gestützte Karteikarten-Lernplattform für VWL – **Finanzmärkte und Institutionen**

---

## Projektidee

Dieses Projekt liest alle Kursmaterialien (Skripte, Übungen, Probeklausuren) automatisch ein, extrahiert das Wissen und generiert eine hochwertige, klausurnahe Karteikarten-Datenbank. Diese wird in einer modernen React-Lern-App über GitHub Pages bereitgestellt.

---

## Architektur

```
Kursmaterialien (PDF)
        ↓
Phase 1 – Document Classifier     →  document_inventory.json
        ↓
Phase 2 – Knowledge Extraction    →  knowledge_base.json
        ↓
Phase 3 – Exam Pattern Analysis   →  exam_profile.json
        ↓
Phase 4 – Flashcard Generation    →  flashcards.json
        ↓
Phase 5 – Validation & Dedup      →  flashcards.json (bereinigt)
        ↓
Phase 6–8 – React App             →  GitHub Pages
```

---

## Quellenhierarchie

| Priorität | Kennzeichen | Bedeutung |
|-----------|-------------|-----------|
| **1** | Dateiname enthält `jetzt` | Aktueller Kurs (SS2026) – maßgeblich |
| **2** | Kein `jetzt` im Dateinamen | Vergangenes Jahr – ergänzend |

> Wenn Inhalte nur in historischen Quellen vorkommen, werden sie als `historical_context` markiert und **nicht** als aktueller Prüfungsstoff behandelt.

---

## Dateiformate

Version 1 arbeitet mit PDF (via `pdfplumber`). Spätere Versionen sollen unterstützen:

- PDF, PPTX, DOCX, TXT, Markdown

---

## Generator (Python)

```
scripts/
├── requirements.txt
├── classify/
│   └── run_classifier.py      # Phase 1 – Dokumentklassifikation
├── extract/                   # Phase 2 – Wissensbasis
├── generate/                  # Phase 4 – Karteikarten
├── validate/                  # Phase 5 – Validierung
└── output/
    ├── text_cache/            # Extrahierte PDF-Texte
    └── ...
```

### Karten generieren

```bash
# 1. Abhängigkeiten installieren
pip install -r scripts/requirements.txt

# 2. Phase 1: Dokumente analysieren
python scripts/classify/run_classifier.py --source-dir . --out document_inventory.json

# 3. Alle weiteren Phasen (nach Implementierung)
python scripts/run_pipeline.py
```

---

## Datenmodell – Karteikarte

```json
{
  "id": "fmfi-001",
  "question": "Was ist direkte Finanzierung?",
  "answer": "...",
  "type": "definition",
  "difficulty": 1,
  "importance": 0.95,
  "examRelevance": 0.90,
  "chapter": "1. Funktionen des Finanzsystems",
  "tags": ["Finanzierung"],
  "source": {
    "current": [{ "file": "Skript FMI SS2026_ jetzt.pdf", "page": 22 }],
    "historical": []
  },
  "learning": {
    "repetitions": 0,
    "ease": 2.5,
    "interval": 0,
    "due": "2026-08-27",
    "lastReviewed": null
  },
  "validation": {
    "status": "ok",
    "issues": []
  }
}
```

---

## Kartentypen / Schwierigkeitsgrade

| Level | Typ | Beispiel |
|-------|-----|---------|
| 1 | Recall | Was ist ein ETF? |
| 2 | Verständnis | Warum verbessern Intermediäre die Kapitalallokation? |
| 3 | Zusammenhänge | Wie hängen Finanzintermediation und Wachstum zusammen? |
| 4 | Abgrenzung | Direkte vs. indirekte Finanzierung |
| 5 | Transfer | Szenario → Finanzierungsform bestimmen |
| 6 | Rechnen | Formel, Rechenweg, Ergebnis |
| 7 | Klausurniveau | Wahr/Falsch + Begründung, mehrteilige Aufgabe |
| 8 | Empirie | Evidenz, Korrelation vs. Kausalität |

---

## Lern-App

**Stack:** React + TypeScript + Vite

**Features:**
- Hauptseite: Kapitelübersicht + Gesamtfortschritt
- Lernmodus: Spaced Repetition (fällige Karten zuerst)
- Filter: Kapitel, Schwierigkeit, Typ, Relevanz
- Klausurmodus: zeitlich begrenzt, Punkte, Auswertung
- Tastatursteuerung: `Space` zeigen, `1–4` bewerten, `N` nächste

---

## Spaced Repetition

Basiert auf SM-2-Algorithmus. Fortschritt wird in `localStorage` gespeichert.

```json
{
  "repetitions": 0,
  "ease": 2.5,
  "interval": 0,
  "due": "2026-08-27",
  "lastReviewed": null
}
```

---

## Klausurmodus

Simuliert echte Klausurbedingungen. Struktur wird aus den Probeklausuren abgeleitet:
- Zeitlimit
- Aufgabentypen (Wahr/Falsch, Berechnung, Transfer, Begründung)
- Punkteverteilung
- Auswertung: Stärken/Schwächen nach Kapitel und Aufgabentyp

---

## Lokale Entwicklung

```bash
# Lern-App
npm install
npm run dev

# Generator
cd scripts
pip install -r requirements.txt
python classify/run_classifier.py
```

---

## GitHub Pages Deployment

```bash
git push origin main
# GitHub Actions baut automatisch und deployed auf GitHub Pages
```

---

## Qualitätsziel

Lieber **300 sehr gute Karten** als 1500 schlechte. Jede Karte muss:
- durch eine Quelle gedeckt sein
- einen echten Lernnutzen haben
- nicht redundant sein

---

## Zukünftige Features

- KI-Feedback: Nutzer schreibt freie Antwort → KI bewertet Vollständigkeit
- PDF/PPTX/DOCX Parser
- Serverless KI-Verarbeitung (z.B. via GitHub Actions)
- Mehrere Kurse / Fächer
- Lerngruppen-Modus
