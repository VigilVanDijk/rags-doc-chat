import { useState } from 'react'
import { ImageList, ImageListItem } from '@mui/material'
import './App.css'
import QueryInput from './components/QueryInput'
import AnswerDisplay from './components/AnswerDisplay'
import { queryAPI } from './services/api'

function App() {
  const bannerImages = [
    {
      title: 'Terra Incognita',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/TerraIncognita.jpg'
    },
    {
      title: 'The Link',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/TheLink.jpg'
    },
    {
      title: 'From Mars to Sirius',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/FromMarsToSirius.jpg'
    },
    {
      title: 'The Way of All Flesh',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/TheWayOfAllFlesh.jpg'
    },
    {
      title: 'LEnfant Sauvage',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/LeEnfantSauvage.jpg'
    },
    {
      title: 'Magma',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/Magma.jpg'
    },
    {
      title: 'Fortitude',
      src: 'https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/Fortitude.jpg'
    }
  ]

  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [queryHistory, setQueryHistory] = useState([])
  const [verboseToggle, setVerboseToggle] = useState(false)
  const [query, setQuery] = useState('')
  const vvd = `https://github.com/VigilVanDijk`;
  const vvd_assets = `https://github.com/VigilVanDijk/vvd-assets`

  const handleQuery = async (queryText) => {
    setLoading(true)
    setError(null)
    setAnswer(null)

    try {
      const response = await queryAPI(queryText, 10)
      setAnswer({
        query: response.query,
        answer: response.answer,
        routing: response.routing
      })
      setQueryHistory(prev => [...prev, queryText])
      setQuery('') // Clear input only after answer is received
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
        <div className="header-content" >
          <img
            className="header-logo"
            src="https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/gojira_logo.png"
            alt="Gojira logo"
            loading="lazy"
          />
          <h1>Knowledge Engine</h1>
        </div>
        <div className="banner">
          <div className="banner-scroll" role="region" aria-label="Gojira album art scroll">
            <div className="banner-track">
              {[0, 1].map((dupIndex) => (
                <ImageList
                  className="banner-list"
                  cols={bannerImages.length}
                  rowHeight={200}
                  gap={16}
                  key={`banner-set-${dupIndex}`}
                >
                  {bannerImages.map((image) => (
                    <ImageListItem className="banner-card" key={`${image.title}-${dupIndex}`}>
                      <img src={image.src} alt={`${image.title} album art`} loading="lazy" />
                    </ImageListItem>
                  ))}
                </ImageList>
              ))}
            </div>
          </div>
        </div>
      </header>

      <main className="app-main">
        <QueryInput
          onQuery={handleQuery}
          loading={loading}
          query={query}
          setQuery={setQuery}
          placeholder="Try: 'How many songs are in The Link?' or 'Compare technical analysis between both albums'"
        />

        <div className="toggle-container">
          <label className="toggle-label">
            <input
              type="checkbox"
              checked={verboseToggle}
              onChange={(e) => setVerboseToggle(e.target.checked)}
              className="toggle-input"
            />
            <span className="toggle-slider"></span>
            <span className="toggle-text">Verbose</span>
          </label>
          <span className={`toggle-hint ${verboseToggle ? 'visible' : 'hidden'}`}>
            Hover a tag for details
          </span>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <img
              src="https://cdn.jsdelivr.net/gh/VigilVanDijk/vvd-assets@rags-doc-chat/gojira_album_arts/assets/gojirafortitudeslipmat.png"
              alt="Loader"
              className="spinner"
            />
            <p>Searching knowledge base...</p>
          </div>
        )}

        {answer && (
          <AnswerDisplay answer={answer} verboseToggle={verboseToggle} />
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
        <p>Powered by RAG with automatic query routing | <a href={vvd} target="_blank" rel="noopener noreferrer" className="vvd-link">VigilVanDijk</a> | <a href={vvd_assets} target="_blank" rel="noopener noreferrer" className="vvd-link">VigilVanDijk Assets</a></p>
      </footer>
    </div>
  )
}

export default App