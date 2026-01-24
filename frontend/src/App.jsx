import { useState } from 'react'
import './App.css'
import QueryInput from './components/QueryInput'
import AnswerDisplay from './components/AnswerDisplay'
import { queryAPI } from './services/api'

function App() {
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [queryHistory, setQueryHistory] = useState([])

  const handleQuery = async (query) => {
    setLoading(true)
    setError(null)
    setAnswer(null)

    try {
      const response = await queryAPI(query, 10)
      setAnswer({
        query: response.query,
        answer: response.answer,
        routing: response.routing
      })
      setQueryHistory(prev => [...prev, query])
    } catch (err) {
      setError(err.message || 'Failed to get response from server. Make sure the backend is running on http://localhost:8000')
      console.error('Query error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎸 Gojira Album Chat</h1>
        <p>Ask questions about The Link and From Mars to Sirius albums</p>
      </header>

      <main className="app-main">
        <QueryInput 
          onQuery={handleQuery} 
          loading={loading}
          placeholder="Try: 'How many songs are in The Link?' or 'Compare technical analysis between both albums'"
        />
        
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching knowledge base...</p>
          </div>
        )}

        {answer && (
          <AnswerDisplay answer={answer} />
        )}

        {queryHistory.length > 0 && (
          <div className="query-history">
            <h3>Recent Queries</h3>
            <ul>
              {queryHistory.slice(-5).reverse().map((q, idx) => (
                <li key={idx} onClick={() => handleQuery(q)}>
                  {q}
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by RAG with automatic query routing</p>
      </footer>
    </div>
  )
}

export default App