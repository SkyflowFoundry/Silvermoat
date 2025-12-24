import { useState, useEffect } from 'react'
import { getQuote } from '../services/api'
import './QuoteList.css'

function QuoteList({ quotes, apiBase, onError }) {
  const [expandedQuote, setExpandedQuote] = useState(null)
  const [quoteDetails, setQuoteDetails] = useState({})
  const [loading, setLoading] = useState({})

  const handleExpand = async (quoteId) => {
    if (expandedQuote === quoteId) {
      setExpandedQuote(null)
      return
    }

    setExpandedQuote(quoteId)
    
    // If we already have the details, don't fetch again
    if (quoteDetails[quoteId]) {
      return
    }

    setLoading(prev => ({ ...prev, [quoteId]: true }))
    onError(null)

    try {
      if (!apiBase) {
        throw new Error('API base URL not configured')
      }

      const details = await getQuote(apiBase, quoteId)
      setQuoteDetails(prev => ({ ...prev, [quoteId]: details }))
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load quote details'
      onError(errorMessage)
      console.error('Quote fetch error:', err)
    } finally {
      setLoading(prev => ({ ...prev, [quoteId]: false }))
    }
  }

  if (quotes.length === 0) {
    return (
      <div className="quote-list-empty">
        <p>No quotes created yet. Create one using the form on the left.</p>
      </div>
    )
  }

  return (
    <div className="quote-list">
      {quotes.map((quote) => {
        const quoteId = quote.id || quote.item?.id
        const isExpanded = expandedQuote === quoteId
        const details = quoteDetails[quoteId]
        const isLoading = loading[quoteId]

        return (
          <div key={quoteId} className="quote-item">
            <div 
              className="quote-item-header"
              onClick={() => handleExpand(quoteId)}
            >
              <div className="quote-item-id">
                <strong>Quote ID:</strong> {quoteId}
              </div>
              <div className="quote-item-toggle">
                {isExpanded ? '▼' : '▶'}
              </div>
            </div>
            
            {isExpanded && (
              <div className="quote-item-details">
                {isLoading ? (
                  <div className="loading">Loading details...</div>
                ) : details ? (
                  <pre className="quote-json">
                    {JSON.stringify(details, null, 2)}
                  </pre>
                ) : (
                  <div className="error">Failed to load details</div>
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default QuoteList

