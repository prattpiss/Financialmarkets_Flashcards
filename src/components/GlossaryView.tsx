import { useState, useEffect } from 'react'
import styles from './GlossaryView.module.css'

interface GlossaryTerm {
  term: string
  definition: string
  chapter: number
  slideRef: string
}

interface Props {
  onBack: () => void
}

const CHAPTER_NAMES: Record<number, string> = {
  1: 'Kap. 1: Funktionen des Finanzsystems',
  2: 'Kap. 2: Globale Finanzkrise',
  3: 'Kap. 3: Modigliani-Miller-Theorem',
  4: 'Kap. 4: Marktunvollkommenheiten',
  5: 'Kap. 5: Funktionen von Banken',
  6: 'Kap. 6: Finanzkrisen & systemische Risiken',
  7: 'Kap. 7: Bankenregulierung',
}

export function GlossaryView({ onBack }: Props) {
  const [terms, setTerms] = useState<GlossaryTerm[]>([])
  const [search, setSearch] = useState('')
  const [filterChapter, setFilterChapter] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('./data/glossary.json')
      .then((r) => r.json())
      .then((data) => {
        setTerms(data.terms ?? [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const filtered = terms.filter((t) => {
    const matchSearch =
      !search ||
      t.term.toLowerCase().includes(search.toLowerCase()) ||
      t.definition.toLowerCase().includes(search.toLowerCase())
    const matchChapter = filterChapter === null || t.chapter === filterChapter
    return matchSearch && matchChapter
  })

  const chapters = [...new Set(terms.map((t) => t.chapter))].sort((a, b) => a - b)

  return (
    <div className={styles.wrapper}>
      <header className={styles.header}>
        <button className={styles.backBtn} onClick={onBack}>← Zurück</button>
        <h2 className={styles.title}>📚 Fachbegriff-Glossar</h2>
        <span className={styles.count}>{filtered.length} Begriffe</span>
      </header>

      <div className={styles.controls}>
        <input
          className={styles.search}
          type="text"
          placeholder="Begriff oder Definition suchen…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className={styles.chapterSelect}
          value={filterChapter ?? ''}
          onChange={(e) => setFilterChapter(e.target.value ? Number(e.target.value) : null)}
        >
          <option value="">Alle Kapitel</option>
          {chapters.map((ch) => (
            <option key={ch} value={ch}>{CHAPTER_NAMES[ch] ?? `Kapitel ${ch}`}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className={styles.loading}>Glossar wird geladen…</div>
      ) : (
        <div className={styles.list}>
          {filtered.map((term, i) => (
            <div key={i} className={styles.item}>
              <div className={styles.itemHeader}>
                <strong className={styles.term}>{term.term}</strong>
                <span className={styles.slideRef}>📄 {term.slideRef}</span>
              </div>
              <p className={styles.definition}>{term.definition}</p>
              <span className={styles.chapterBadge}>{CHAPTER_NAMES[term.chapter] ?? `Kap. ${term.chapter}`}</span>
            </div>
          ))}
          {filtered.length === 0 && (
            <div className={styles.empty}>Keine Begriffe gefunden.</div>
          )}
        </div>
      )}
    </div>
  )
}
