import { useEffect } from 'react'

type KeyMap = Record<string, () => void>

export function useKeyboard(keyMap: KeyMap, active = true) {
  useEffect(() => {
    if (!active) return
    function handler(e: KeyboardEvent) {
      // Ignore when typing in inputs
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      const fn = keyMap[e.key]
      if (fn) {
        e.preventDefault()
        fn()
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [keyMap, active])
}
