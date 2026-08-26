import { useState } from 'react'
import type { Flashcard, Rating } from '@/types'
import { StudyCard } from './StudyCard'
import { FlashCard } from './FlashCard'
import { sortChronologically } from '@/utils/spacedRepetition'
import styles from './StudyThenQuizMode.module.css'

type Phase = 'study' | 'quiz' | 'done'

interface Props {
  cards: Flashcard[]
  onRate: (id: string, rating: Rating) => void
  onBack: () => void
}

export function StudyThenQuizMode({ cards, onRate, onBack }: Props) {
  // Always present in chronological order
  const ordered = sortChronologically(cards)
  const [phase, setPhase] = useState<Phase>('study')
  const [studyIndex, setStudyIndex] = useState(0)
  const [quizIndex, setQuizIndex] = useState(0)
  const [ratings, setRatings] = useState<Rating[]>([])

  if (ordered.length === 0) {
    return (
      <div className={styles.empty}>
        <p>Keine Karten ausgewählt.</p>
        <button className={styles.back} onClick={onBack}>← Zurück</button>
      </div>
    )
  }

  // ── Study phase ──────────────────────────────
  if (phase === 'study') {
    return (
      <div>
        <div className={styles.topBar}>
          <button className={styles.back} onClick={onBack}>← Zurück</button>
          <div className={styles.phaseBadge}>📖 Lernphase</div>
          <span className={styles.hint}>Lies alle Karten durch, dann folgt die Abfrage.</span>
        </div>
        <StudyCard
          card={ordered[studyIndex]}
          index={studyIndex}
          total={ordered.length}
          onNext={() => setStudyIndex((i) => i + 1)}
          onDone={() => { setPhase('quiz') }}
        />
      </div>
    )
  }

  // ── Quiz phase ───────────────────────────────
  if (phase === 'quiz') {
    if (quizIndex >= ordered.length) {
      const avg = ratings.length
        ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1)
        : '–'
      return (
        <div className={styles.done}>
          <div className={styles.doneIcon}>🎉</div>
          <h2>Lern & Abfrage abgeschlossen!</h2>
          <div className={styles.doneStats}>
            <div className={styles.doneStat}>
              <span>{ordered.length}</span>
              <small>Karten gelernt</small>
            </div>
            <div className={styles.doneStat}>
              <span>{ratings.length}</span>
              <small>Bewertet</small>
            </div>
            <div className={styles.doneStat}>
              <span>{avg} / 4</span>
              <small>Ø Bewertung</small>
            </div>
          </div>
          <button className={styles.back} onClick={onBack}>← Zurück zur Übersicht</button>
        </div>
      )
    }

    return (
      <div>
        <div className={styles.topBar}>
          <button className={styles.back} onClick={onBack}>← Abbrechen</button>
          <div className={`${styles.phaseBadge} ${styles.quizBadge}`}>✏️ Abfragephase</div>
          <span className={styles.hint}>
            <kbd>Space</kbd> zeigen &nbsp; <kbd>1–4</kbd> bewerten
          </span>
        </div>
        <FlashCard
          card={ordered[quizIndex]}
          index={quizIndex}
          total={ordered.length}
          onRate={(r) => {
            onRate(ordered[quizIndex].id, r)
            setRatings((prev) => [...prev, r])
            setQuizIndex((i) => i + 1)
          }}
          onSkip={() => setQuizIndex((i) => i + 1)}
        />
      </div>
    )
  }

  return null
}
