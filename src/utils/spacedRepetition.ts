import type { Flashcard, FlashcardLearning, Rating } from '@/types'

export type SortMode = 'priority' | 'chronological' | 'random'

const TODAY = new Date().toISOString().split('T')[0]

function addDays(isoDate: string, days: number): string {
  const d = new Date(isoDate)
  d.setDate(d.getDate() + days)
  return d.toISOString().split('T')[0]
}

/**
 * SM-2 algorithm adapted for 4-button rating.
 * Rating mapping:
 *   1 = Again (< 3 in SM-2)
 *   2 = Hard  (3)
 *   3 = Good  (4)
 *   4 = Easy  (5)
 */
export function computeNextReview(
  learning: FlashcardLearning,
  rating: Rating,
): FlashcardLearning {
  const { repetitions, ease, interval } = learning
  const sm2Grade = [0, 3, 4, 5][rating - 1]  // map 1→0, 2→3, 3→4, 4→5

  let newRep = repetitions
  let newInterval = interval
  let newEase = ease

  if (sm2Grade < 3) {
    // Failed: reset
    newRep = 0
    newInterval = 1
  } else {
    newRep = repetitions + 1
    if (repetitions === 0) {
      newInterval = 1
    } else if (repetitions === 1) {
      newInterval = 6
    } else {
      newInterval = Math.round(interval * ease)
    }
    newEase = Math.max(1.3, ease + 0.1 - (5 - sm2Grade) * (0.08 + (5 - sm2Grade) * 0.02))
  }

  return {
    repetitions: newRep,
    ease: Math.round(newEase * 100) / 100,
    interval: newInterval,
    due: addDays(TODAY, newInterval),
    lastReviewed: TODAY,
  }
}

export function isDue(card: Flashcard): boolean {
  return card.learning.due <= TODAY
}

export function isNew(card: Flashcard): boolean {
  return card.learning.repetitions === 0
}

export function isMastered(card: Flashcard): boolean {
  return card.learning.interval >= 21
}

/**
 * Priority order for card selection:
 * 1. Due today  2. Poor ease  3. High examRelevance  4. New cards
 */
export function sortByPriority(cards: Flashcard[]): Flashcard[] {
  return [...cards].sort((a, b) => {
    const aDue = isDue(a) ? 0 : 1
    const bDue = isDue(b) ? 0 : 1
    if (aDue !== bDue) return aDue - bDue

    // Lower ease = needs more practice
    const aEase = a.learning.ease
    const bEase = b.learning.ease
    if (Math.abs(aEase - bEase) > 0.2) return aEase - bEase

    // Higher exam relevance first
    const relDiff = b.examRelevance - a.examRelevance
    if (Math.abs(relDiff) > 0.05) return relDiff

    // New cards last (after due + struggling)
    const aNew = isNew(a) ? 0 : -1
    const bNew = isNew(b) ? 0 : -1
    return aNew - bNew
  })
}

/** Chronological: chapter order → section → difficulty */
export function sortChronologically(cards: Flashcard[]): Flashcard[] {
  return [...cards].sort((a, b) => {
    const aNum = parseInt(a.chapter.split('.')[0]) || 99
    const bNum = parseInt(b.chapter.split('.')[0]) || 99
    if (aNum !== bNum) return aNum - bNum
    if (a.section !== b.section) return a.section.localeCompare(b.section, 'de')
    return a.difficulty - b.difficulty
  })
}

/** Fisher–Yates shuffle */
export function shuffleCards(cards: Flashcard[]): Flashcard[] {
  const arr = [...cards]
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
}

export function applySortMode(cards: Flashcard[], mode: SortMode): Flashcard[] {
  if (mode === 'chronological') return sortChronologically(cards)
  if (mode === 'random') return shuffleCards(cards)
  return sortByPriority(cards)
}
