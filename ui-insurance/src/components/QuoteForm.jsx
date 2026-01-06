import { useState } from 'react'
import { createQuote } from '../services/api'
import './QuoteForm.css'

function QuoteForm({ apiBase, onQuoteCreated, onError }) {
  const [formData, setFormData] = useState({
    name: '',
    zip: '',
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    onError(null)

    try {
      if (!apiBase) {
        throw new Error('API base URL not configured. Please set VITE_API_BASE_URL or window.API_BASE_URL')
      }

      const result = await createQuote(apiBase, formData)
      onQuoteCreated(result.item || result)
      
      // Reset form
      setFormData({ name: '', zip: '' })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create quote'
      onError(errorMessage)
      console.error('Quote creation error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="quote-form">
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          placeholder="Jane Doe"
        />
      </div>

      <div className="form-group">
        <label htmlFor="zip">ZIP Code</label>
        <input
          type="text"
          id="zip"
          name="zip"
          value={formData.zip}
          onChange={handleChange}
          required
          placeholder="33431"
          pattern="[0-9]{5}"
          maxLength="5"
        />
      </div>

      <button type="submit" disabled={loading} className="submit-button">
        {loading ? 'Creating...' : 'Create Quote'}
      </button>
    </form>
  )
}

export default QuoteForm

