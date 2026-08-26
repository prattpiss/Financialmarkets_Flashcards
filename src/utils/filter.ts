import type { Flashcard, FilterState } from '@/types'

export const DEFAULT_FILTER: FilterState = {
  chapters: [],
  types: [],
  minDifficulty: 1,
  maxDifficulty: 8,
  minExamRelevance: 0,
  onlyDue: false,
  onlyNew: false,
}

const TODAY = new Date().toISOString().split('T')[0]

export function applyFilter(cards: Flashcard[], filter: FilterState): Flashcard[] {
  return cards.filter((c) => {
    if (filter.chapters.length > 0) {
      const chNum = c.chapter.split('.')[0].trim()
      if (!filter.chapters.includes(chNum)) return false
    }
    if (filter.types.length > 0 && !filter.types.includes(c.type)) return false
    if (c.difficulty < filter.minDifficulty || c.difficulty > filter.maxDifficulty) return false
    if (c.examRelevance < filter.minExamRelevance) return false
    if (filter.onlyDue && c.learning.due > TODAY) return false
    if (filter.onlyNew && c.learning.repetitions > 0) return false
    return true
  })
}

export function getChapters(cards: Flashcard[]): string[] {
  const seen = new Set<string>()
  cards.forEach((c) => seen.add(c.chapter))
  return Array.from(seen).sort()
}

export function getChapterStats(cards: Flashcard[], chapter: string) {
  const cc = cards.filter((c) => c.chapter === chapter)
  return {
    total: cc.length,
    due: cc.filter((c) => c.learning.due <= TODAY).length,
    learned: cc.filter((c) => c.learning.repetitions > 0).length,
    mastered: cc.filter((c) => c.learning.interval >= 21).length,
  }
}
