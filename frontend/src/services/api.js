// API service for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Log the API URL being used (helpful for debugging)
console.log('API Base URL:', API_BASE_URL)

export const queryAPI = async (query, k = 10) => {
    try {
        const url = `${API_BASE_URL}/api/query`
        console.log('Making request to:', url)

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, k }),
        })

        // Check content type before parsing
        const contentType = response.headers.get('content-type')
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text()
            console.error('Non-JSON response received:', text.substring(0, 200))
            throw new Error(
                `Server returned HTML instead of JSON. This usually means:\n` +
                `1. The API URL (${API_BASE_URL}) is incorrect\n` +
                `2. The API server is not running or not accessible\n` +
                `3. There's a CORS or routing issue\n\n` +
                `Response preview: ${text.substring(0, 100)}...`
            )
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        return data
    } catch (error) {
        console.error('API Error:', error)
        // If it's already our custom error, throw it as-is
        if (error.message && error.message.includes('Server returned HTML')) {
            throw error
        }
        // Otherwise, wrap it with more context
        throw new Error(error.message || 'Failed to connect to API server')
    }
}

export const healthCheck = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`)
        if (!response.ok) {
            throw new Error('Health check failed')
        }
        return await response.json()
    } catch (error) {
        console.error('Health check error:', error)
        throw error
    }
}

