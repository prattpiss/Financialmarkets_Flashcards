import { useState, useEffect, useCallback } from 'react'
import type { Flashcard, FlashcardsData } from '@/types'
import { computeNextReview } from '@/utils/spacedRepetition'
import type { Rating } from '@/types'

const STORAGE_KEY = 'fmi-flashcards-progress'

type ProgressMap = Record<string, Flashcard['learning']>

function loadProgress(): ProgressMap {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as ProgressMap) : {}
  } catch {
    return {}
  }
}

function saveProgress(progress: ProgressMap) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
}

function mergeProgress(cards: Flashcard[], progress: ProgressMap): Flashcard[] {
  return cards.map((c) =>
    progress[c.id] ? { ...c, learning: progress[c.id] } : c,
  )
}

export function useFlashcards() {
  const [allCards, setAllCards] = useState<Flashcard[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('./data/flashcards.json')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json() as Promise<FlashcardsData>
      })
      .then((data) => {
        const progress = loadProgress()
        setAllCards(mergeProgress(data.flashcards, progress))
        setLoading(false)
      })
      .catch((e: unknown) => {
        setError(String(e))
        setLoading(false)
      })
  }, [])

  const rateCard = useCallback((cardId: string, rating: Rating) => {
    setAllCards((prev) => {
      const next = prev.map((c) => {
        if (c.id !== cardId) return c
        const newLearning = computeNextReview(c.learning, rating)
        return { ...c, learning: newLearning }
      })
      // Persist
      const progress = loadProgress()
      const updated = next.find((c) => c.id === cardId)
      if (updated) progress[cardId] = updated.learning
      saveProgress(progress)
      return next
    })
  }, [])

  const resetProgress = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setAllCards((prev) =>
      prev.map((c) => ({
        ...c,
        learning: {
          repetitions: 0,
          ease: 2.5,
          interval: 0,
          due: new Date().toISOString().split('T')[0],
          lastReviewed: null,
        },
      })),
    )
  }, [])

  return { allCards, loading, error, rateCard, resetProgress }
}
