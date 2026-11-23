import { useEffect, useState } from 'react'
import { validatePortfolioData } from './portfolioData.js'

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

export function useAppData(initialData) {
  const [data, setData] = useState(initialData || null)
  const [loading, setLoading] = useState(!initialData)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (initialData) return

    const controller = new AbortController()
    const apiUrl = `${API_BASE_URL.replace(/\/+$/, '')}/api/`

    fetch(apiUrl, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`)
        }
        return response.json()
      })
      .then((json) => {
        setData(validatePortfolioData(json))
        setLoading(false)
      })
      .catch((err) => {
        if (err.name === 'AbortError') return
        setError(err.message)
        setLoading(false)
      })

    return () => controller.abort()
  }, [initialData])

  return { data, loading, error }
}
