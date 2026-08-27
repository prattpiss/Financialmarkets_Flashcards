import { useState } from 'react'
import type { Flashcard, Rating } from '@/types'
import { FlashCard } from './FlashCard'
import { applySortMode } from '@/utils/spacedRepetition'
import type { SortMode } from '@/utils/spacedRepetition'
import styles from './LearnMode.module.css'

interface Props {
  cards: Flashcard[]
  sortMode?: SortMode
  onRate: (id: string, rating: Rating) => void
  onBack: () => void
}

export function LearnMode({ cards, sortMode: initialSortMode = 'priority', onRate, onBack }: Props) {
  const [sortMode, setSortMode] = useState<SortMode>(initialSortMode)
  const [index, setIndex] = useState(0)
  const [sessionRatings, setSessionRatings] = useState<Rating[]>([])

  // Re-sort when mode changes; reset index
  const sorted = applySortMode(cards, sortMode)

  if (cards.length === 0) {
    return (
      <div className={styles.empty}>
        <p>Keine Karten für diesen Filter.</p>
        <button className={styles.back} onClick={onBack}>← Zurück</button>
      </div>
    )
  }

  const safeIndex = Math.min(index, sorted.length - 1)
  const card = sorted[safeIndex]
  const done = index >= sorted.length

  function handleRate(rating: Rating) {
    onRate(card.id, rating)
    setSessionRatings((prev) => [...prev, rating])
    setIndex((i) => i + 1)
  }

  function handleSkip() {
    setIndex((i) => i + 1)
  }

  function handleSortChange(mode: SortMode) {
    setSortMode(mode)
    setIndex(0)
    setSessionRatings([])
  }

  if (done) {
    const avg = sessionRatings.length
      ? (sessionRatings.reduce((a, b) => a + b, 0) / sessionRatings.length).toFixed(1)
      : '–'
    return (
      <div className={styles.done}>
        <h2>Sitzung abgeschlossen 🎉</h2>
        <p>{sessionRatings.length} Karten bewertet</p>
        <p>Ø Bewertung: {avg} / 4</p>
        <button className={styles.back} onClick={onBack}>← Zurück</button>
      </div>
    )
  }

  return (
    <div>
      <div className={styles.topBar}>
        <button className={styles.back} onClick={onBack}>← Zurück</button>
        <div className={styles.sortBtns}>
          <button
            className={`${styles.sortBtn} ${sortMode === 'priority' ? styles.sortActive : ''}`}
            onClick={() => handleSortChange('priority')}
            title="Nach Lernpriorität (fällige Karten zuerst)"
          >Priorität</button>
          <button
            className={`${styles.sortBtn} ${sortMode === 'chronological' ? styles.sortActive : ''}`}
            onClick={() => handleSortChange('chronological')}
            title="Kapitel der Reihe nach"
          >Chronologisch</button>
          <button
            className={`${styles.sortBtn} ${sortMode === 'random' ? styles.sortActive : ''}`}
            onClick={() => handleSortChange('random')}
            title="Zufällige Reihenfolge"
          >Zufällig</button>
        </div>
        <span className={styles.hint}>
          <kbd>Space</kbd> zeigen &nbsp; <kbd>1–4</kbd> bewerten &nbsp; <kbd>N / →</kbd> überspringen
        </span>
      </div>
      <FlashCard
        card={card}
        index={index}
        total={sorted.length}
        onRate={handleRate}
        onSkip={handleSkip}
      />
    </div>
  )
}
