import type { Flashcard } from '@/types'
import { getChapterStats } from '@/utils/filter'
import styles from './ChapterCard.module.css'

interface Props {
  chapter: string
  cards: Flashcard[]
  onClick: () => void
  onStudyQuiz: () => void
}

export function ChapterCard({ chapter, cards, onClick, onStudyQuiz }: Props) {
  const stats = getChapterStats(cards, chapter)
  const progress = stats.total > 0 ? Math.round((stats.learned / stats.total) * 100) : 0
  // Handle "Kapitel X: Title" format
  const colonIdx = chapter.indexOf(':')
  const num = colonIdx >= 0 ? chapter.slice(0, colonIdx).trim() : chapter
  const shortTitle = colonIdx >= 0 ? chapter.slice(colonIdx + 1).trim() : chapter

  return (
    <button className={styles.card} onClick={onClick}>
      <div className={styles.header}>
        <span className={styles.num}>{num}</span>
        <span className={styles.title}>{shortTitle}</span>
      </div>
      <div className={styles.stats}>
        <span className={styles.stat}>{stats.total} Karten</span>
        {stats.due > 0 && (
          <span className={`${styles.stat} ${styles.due}`}>{stats.due} fällig</span>
        )}
        {stats.mastered > 0 && (
          <span className={`${styles.stat} ${styles.mastered}`}>{stats.mastered} beherrscht</span>
        )}
      </div>
      <div className={styles.bar}>
        <div className={styles.barFill} style={{ width: `${progress}%` }} />
      </div>
      <div className={styles.cardActions}>
        <span className={styles.pct}>{progress}%</span>
        <button
          className={styles.studyBtn}
          onClick={(e) => { e.stopPropagation(); onStudyQuiz() }}
          title="Erst lesen, dann abgefragt werden"
        >
          📖 Lern & Abfragen
        </button>
      </div>
    </button>
  )
}
