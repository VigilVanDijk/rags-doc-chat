// API service for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const queryAPI = async (query, k = 10) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, k }),
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        return data
    } catch (error) {
        console.error('API Error:', error)
        throw error
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

