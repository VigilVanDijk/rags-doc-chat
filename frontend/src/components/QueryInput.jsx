import { useState } from 'react'

function QueryInput({ onQuery, loading, placeholder }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !loading) {
      onQuery(query.trim())
      setQuery('')
    }
  }

  return (
    <form className="query-input-form" onSubmit={handleSubmit}>
      <div className="input-wrapper">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className="query-input"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="submit-button"
        >
          <img
            src="https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/whale_loader-1.png"
            alt="Submit"
            className={loading ? 'submit-whale spinning' : 'submit-whale'}
          />
        </button>
      </div>
    </form>
  )
}

export default QueryInput