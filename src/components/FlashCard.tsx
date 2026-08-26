import { useState } from 'react'
import type { Flashcard, Rating } from '@/types'
import { useKeyboard } from '@/hooks/useKeyboard'
import styles from './FlashCard.module.css'

interface Props {
  card: Flashcard
  index: number
  total: number
  onRate: (rating: Rating) => void
  onSkip: () => void
}

const TYPE_LABELS: Record<string, string> = {
  definition: 'Definition',
  understanding: 'Verständnis',
  contrast: 'Abgrenzung',
  calculation: 'Rechnen',
  trueFalse: 'Wahr/Falsch',
  transfer: 'Transfer',
  listing: 'Aufzählung',
  formula: 'Formel',
  empirical: 'Empirie',
}

const DIFFICULTY_COLORS = ['', '#4ade80', '#86efac', '#fde047', '#fb923c', '#f87171', '#ef4444', '#dc2626', '#b91c1c']

const RATINGS: { value: Rating; label: string; hint: string; key: string }[] = [
  { value: 1, label: 'Nochmal', hint: 'Key 1', key: '1' },
  { value: 2, label: 'Schwer', hint: 'Key 2', key: '2' },
  { value: 3, label: 'Gut', hint: 'Key 3', key: '3' },
  { value: 4, label: 'Sehr gut', hint: 'Key 4', key: '4' },
]

export function FlashCard({ card, index, total, onRate, onSkip }: Props) {
  const [revealed, setReveal] = useState(false)

  useKeyboard({
    ' ': () => { if (!revealed) setReveal(true) },
    '1': () => { if (revealed) { onRate(1); setReveal(false) } },
    '2': () => { if (revealed) { onRate(2); setReveal(false) } },
    '3': () => { if (revealed) { onRate(3); setReveal(false) } },
    '4': () => { if (revealed) { onRate(4); setReveal(false) } },
    'n': () => onSkip(),
    'N': () => onSkip(),
  })

  function handleRate(r: Rating) {
    onRate(r)
    setReveal(false)
  }

  return (
    <div className={styles.wrapper}>
      {/* Progress */}
      <div className={styles.meta}>
        <span className={styles.progress}>{index + 1} / {total}</span>
        <span className={styles.type}>{TYPE_LABELS[card.type] ?? card.type}</span>
        <span
          className={styles.diff}
          style={{ color: DIFFICULTY_COLORS[card.difficulty] }}
          title={`Schwierigkeit ${card.difficulty}/8`}
        >
          {'●'.repeat(card.difficulty)}{'○'.repeat(8 - card.difficulty)}
        </span>
        <span className={styles.chapter}>{card.chapter.split('.')[0]}</span>
      </div>

      {/* Exam relevance bar */}
      <div className={styles.relBar}>
        <div className={styles.relFill} style={{ width: `${card.examRelevance * 100}%` }} />
      </div>

      {/* Card */}
      <div className={`${styles.card} ${revealed ? styles.revealed : ''}`}>
        <div className={styles.question}>
          <pre className={styles.pre}>{card.question}</pre>
        </div>

        {revealed && (
          <div className={styles.answer}>
            <div className={styles.divider} />
            <pre className={styles.pre}>{card.answer}</pre>

            {card.formula && (
              <div className={styles.formula}>
                <span className={styles.formulaLabel}>Formel:</span>
                <code>{card.formula}</code>
              </div>
            )}

            {card.solutionSteps && card.solutionSteps.length > 0 && (
              <div className={styles.steps}>
                <span className={styles.stepsLabel}>Lösungsweg:</span>
                <ol>
                  {card.solutionSteps.map((s, i) => <li key={i}>{s}</li>)}
                </ol>
              </div>
            )}

            {card.source.current.length > 0 && (
              <div className={styles.source}>
                📄 {card.source.current[0].file}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Actions */}
      {!revealed ? (
        <div className={styles.actions}>
          <button className={styles.showBtn} onClick={() => setReveal(true)}>
            Antwort zeigen <kbd>Space</kbd>
          </button>
          <button className={styles.skipBtn} onClick={onSkip} title="Überspringen (N)">
            Überspringen
          </button>
        </div>
      ) : (
        <div className={styles.ratings}>
          {RATINGS.map((r) => (
            <button
              key={r.value}
              className={`${styles.ratingBtn} ${styles['rating' + r.value]}`}
              onClick={() => handleRate(r.value)}
            >
              {r.label}
              <kbd>{r.key}</kbd>
            </button>
          ))}
        </div>
      )}

      {/* Tags */}
      <div className={styles.tags}>
        {card.tags.slice(0, 4).map((t) => (
          <span key={t} className={styles.tag}>{t}</span>
        ))}
      </div>
    </div>
  )
}
