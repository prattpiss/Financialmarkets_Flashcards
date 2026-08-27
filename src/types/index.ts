export interface FlashcardSource {
  file: string
  page?: number
  section?: string
}

export interface FlashcardLearning {
  repetitions: number
  ease: number        // SM-2 ease factor, starts at 2.5
  interval: number    // days until next review
  due: string         // ISO date string
  lastReviewed: string | null
}

export interface FlashcardValidation {
  status: 'ok' | 'review' | 'error'
  issues: string[]
}

export interface Flashcard {
  id: string
  question: string
  answer: string
  type: CardType
  difficulty: number          // 1–8
  importance: number          // 0.0–1.0
  examRelevance: number       // 0.0–1.0
  chapter: string
  section: string
  tags: string[]
  source: {
    current: FlashcardSource[]
    historical: FlashcardSource[]
  }
  solutionSteps?: string[]
  formula?: string
  variables?: Record<string, string>
  numericAnswer?: number
  tolerance?: number
  note?: string
  validation: FlashcardValidation
  learning: FlashcardLearning
  // New fields (optional, for backward compat)
  slideRef?: string
  difficultyLevel?: string
  chapterNum?: number
  topic?: string
}

export type CardType =
  | 'definition'
  | 'understanding'
  | 'contrast'
  | 'calculation'
  | 'trueFalse'
  | 'transfer'
  | 'listing'
  | 'formula'
  | 'empirical'

export type Rating = 1 | 2 | 3 | 4  // 1=again, 2=hard, 3=good, 4=easy

export interface FlashcardsData {
  meta: {
    generatedAt: string
    totalCards: number
    byStatus: { ok: number; review: number }
  }
  flashcards: Flashcard[]
}

export interface ChapterStats {
  chapter: string
  total: number
  learned: number    // repetitions > 0
  due: number        // due date <= today
  mastered: number   // interval >= 21 days
}

export type ViewMode = 'home' | 'learn' | 'exam'

export interface FilterState {
  chapters: string[]
  types: CardType[]
  minDifficulty: number
  maxDifficulty: number
  minExamRelevance: number
  onlyDue: boolean
  onlyNew: boolean
}

export interface ExamResult {
  cardId: string
  rating: Rating | null
  timeMs: number
}

export interface ExamSession {
  cards: Flashcard[]
  results: ExamResult[]
  startedAt: number
  durationMs: number
}
