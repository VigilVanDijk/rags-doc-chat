import { useState } from 'react'
import './App.css'
import QueryInput from './components/QueryInput'
import AnswerDisplay from './components/AnswerDisplay'

function App() {
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [queryHistory, setQueryHistory] = useState([])

  const handleQuery = async (query) => {
    setLoading(true)
    setError(null)
    setAnswer(null)

    // TODO: Replace with actual API call when backend is ready
    // For now, using placeholder
    setTimeout(() => {
      setAnswer({
        query: query,
        answer: `This is a placeholder response for: "${query}". The backend API will be connected soon!`,
        routing: {
          type: "single",
          sections: ["overview"],
          albums: ["The Link"],
          confidence: 0.9
        }
      })
      setQueryHistory(prev => [...prev, query])
      setLoading(false)
    }, 1000)
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

        {answer ? (
          <AnswerDisplay answer={answer} />
        ) : (
          <div className="no-answer">
            <p>No answer found. Please try a different query.</p>
          </div>
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