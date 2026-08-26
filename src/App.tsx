import { useState, useMemo } from 'react'
import { useFlashcards } from '@/hooks/useFlashcards'
import { ChapterCard } from '@/components/ChapterCard'
import { LearnMode } from '@/components/LearnMode'
import { StudyThenQuizMode } from '@/components/StudyThenQuizMode'
import { getChapters, applyFilter, DEFAULT_FILTER } from '@/utils/filter'
import { isDue, isNew, isMastered } from '@/utils/spacedRepetition'
import type { SortMode } from '@/utils/spacedRepetition'
import styles from './App.module.css'

type View = 'home' | 'learn' | 'studyquiz'

export default function App() {
  const { allCards, loading, error, rateCard, resetProgress } = useFlashcards()
  const [view, setView] = useState<View>('home')
  const [activeChapter, setActiveChapter] = useState<string | null>(null)
  const [minExamRel, setMinExamRel] = useState(0)
  const [onlyDue, setOnlyDue] = useState(false)
  const [showReset, setShowReset] = useState(false)
  const [sortMode, setSortMode] = useState<SortMode>('priority')

  const chapters = useMemo(() => getChapters(allCards), [allCards])

  const learnCards = useMemo(() => {
    const filter = {
      ...DEFAULT_FILTER,
      chapters: activeChapter ? [activeChapter.split('.')[0]] : [],
      minExamRelevance: minExamRel,
      onlyDue,
    }
    return applyFilter(allCards, filter)
  }, [allCards, activeChapter, minExamRel, onlyDue])

  const totalDue = useMemo(() => allCards.filter(isDue).length, [allCards])
  const totalNew = useMemo(() => allCards.filter(isNew).length, [allCards])
  const totalMastered = useMemo(() => allCards.filter(isMastered).length, [allCards])

  if (loading) return <div className={styles.loading}>Lade Karteikarten…</div>
  if (error) return <div className={styles.error}>Fehler: {error}</div>

  if (view === 'learn') {
    return (
      <div className={styles.app}>
        <LearnMode
          cards={learnCards}
          sortMode={sortMode}
          onRate={rateCard}
          onBack={() => { setView('home'); setActiveChapter(null) }}
        />
      </div>
    )
  }

  if (view === 'studyquiz') {
    return (
      <div className={styles.app}>
        <StudyThenQuizMode
          cards={learnCards}
          onRate={rateCard}
          onBack={() => { setView('home'); setActiveChapter(null) }}
        />
      </div>
    )
  }

  return (
    <div className={styles.app}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <div>
            <h1 className={styles.title}>Finanzmärkte & Institutionen</h1>
            <p className={styles.subtitle}>SS2026 · Prof. Farzad Saidi · Universität Bonn</p>
          </div>
          <button
            className={styles.resetBtn}
            onClick={() => setShowReset(true)}
            title="Lernfortschritt zurücksetzen"
          >
            ↺
          </button>
        </div>
      </header>

      {/* Global progress */}
      <section className={styles.globalStats}>
        <div className={styles.statBox}>
          <span className={styles.statNum}>{allCards.length}</span>
          <span className={styles.statLabel}>Gesamt</span>
        </div>
        <div className={styles.statBox}>
          <span className={`${styles.statNum} ${styles.due}`}>{totalDue}</span>
          <span className={styles.statLabel}>Fällig</span>
        </div>
        <div className={styles.statBox}>
          <span className={`${styles.statNum} ${styles.new}`}>{totalNew}</span>
          <span className={styles.statLabel}>Neu</span>
        </div>
        <div className={styles.statBox}>
          <span className={`${styles.statNum} ${styles.mastered}`}>{totalMastered}</span>
          <span className={styles.statLabel}>Beherrscht</span>
        </div>
      </section>

      {/* Quick filter bar */}
      <section className={styles.filterBar}>
        <label className={styles.filterLabel}>
          <input
            type="checkbox"
            checked={onlyDue}
            onChange={(e) => setOnlyDue(e.target.checked)}
          />
          Nur fällige
        </label>
        <label className={styles.filterLabel}>
          Klausurrelevanz ≥
          <select
            value={minExamRel}
            onChange={(e) => setMinExamRel(Number(e.target.value))}
            className={styles.select}
          >
            <option value={0}>Alle</option>
            <option value={0.7}>Hoch (≥ 70%)</option>
            <option value={0.9}>Sehr hoch (≥ 90%)</option>
            <option value={1.0}>Klausurpflicht</option>
          </select>
        </label>
        <label className={styles.filterLabel}>
          Reihenfolge
          <select
            value={sortMode}
            onChange={(e) => setSortMode(e.target.value as SortMode)}
            className={styles.select}
          >
            <option value="priority">Priorität (fällig zuerst)</option>
            <option value="chronological">Chronologisch (Kapitelreihenfolge)</option>
            <option value="random">Zufällig</option>
          </select>
        </label>
        <div className={styles.actionGroup}>
          <button
            className={styles.studyQuizBtn}
            onClick={() => { setActiveChapter(null); setView('studyquiz') }}
            title="Erst lesen, dann abgefragt werden"
          >
            📖 Lern & Abfragen ({learnCards.length})
          </button>
          <button
            className={styles.learnAllBtn}
            onClick={() => { setActiveChapter(null); setView('learn') }}
          >
            Direkt lernen ({learnCards.length})
          </button>
        </div>
      </section>

      {/* Chapters */}
      <section className={styles.chapters}>
        <h2 className={styles.sectionTitle}>Kapitel</h2>
        <div className={styles.grid}>
          {chapters.map((ch) => (
            <ChapterCard
              key={ch}
              chapter={ch}
              cards={allCards}
              onClick={() => { setActiveChapter(ch); setView('learn') }}
              onStudyQuiz={() => { setActiveChapter(ch); setView('studyquiz') }}
            />
          ))}
        </div>
      </section>

      {/* Keyboard hints */}
      <footer className={styles.footer}>
        <kbd>Space</kbd> Antwort zeigen &nbsp;
        <kbd>1</kbd>–<kbd>4</kbd> Bewerten &nbsp;
        <kbd>N</kbd> Überspringen
      </footer>

      {/* Reset dialog */}
      {showReset && (
        <div className={styles.overlay} onClick={() => setShowReset(false)}>
          <div className={styles.dialog} onClick={(e) => e.stopPropagation()}>
            <h3>Fortschritt zurücksetzen?</h3>
            <p>Alle Bewertungen und Intervalle werden gelöscht.</p>
            <div className={styles.dialogActions}>
              <button onClick={() => setShowReset(false)}>Abbrechen</button>
              <button
                className={styles.danger}
                onClick={() => { resetProgress(); setShowReset(false) }}
              >
                Zurücksetzen
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
