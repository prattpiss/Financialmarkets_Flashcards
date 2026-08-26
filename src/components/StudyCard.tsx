import type { Flashcard } from '@/types'
import styles from './StudyCard.module.css'

interface Props {
  card: Flashcard
  index: number
  total: number
  onNext: () => void
  onDone: () => void
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

export function StudyCard({ card, index, total, onNext, onDone }: Props) {
  const isLast = index === total - 1

  return (
    <div className={styles.wrapper}>
      <div className={styles.meta}>
        <span className={styles.progress}>{index + 1} / {total}</span>
        <span className={styles.type}>{TYPE_LABELS[card.type] ?? card.type}</span>
        <span className={styles.chapter}>{card.chapter.split('.')[0]}</span>
      </div>

      <div className={styles.card}>
        {/* Question */}
        <div className={styles.block}>
          <span className={styles.label}>Frage</span>
          <pre className={styles.pre}>{card.question}</pre>
        </div>

        <div className={styles.divider} />

        {/* Answer – always visible in study mode */}
        <div className={styles.block}>
          <span className={styles.label}>Antwort</span>
          <pre className={styles.pre}>{card.answer}</pre>
        </div>

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
      </div>

      <div className={styles.actions}>
        {isLast ? (
          <button className={styles.doneBtn} onClick={onDone}>
            Abfrage starten →
          </button>
        ) : (
          <button className={styles.nextBtn} onClick={onNext}>
            Weiter →
          </button>
        )}
      </div>

      <div className={styles.tags}>
        {card.tags.slice(0, 4).map((t) => (
          <span key={t} className={styles.tag}>{t}</span>
        ))}
      </div>
    </div>
  )
}
