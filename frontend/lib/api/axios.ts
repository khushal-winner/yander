import axios from 'axios'

// Create axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// REQUEST INTERCEPTOR
// Runs before every request
api.interceptors.request.use((config) => {
  // Get token from localStorage
  const token = localStorage.getItem('accessToken')
  const workspaceId = localStorage.getItem('activeWorkspaceId')

  if (token) {
    config.headers.Authorization = `Bearer ${token}` 
  }

  if (workspaceId) {
    config.headers['x-workspace-id'] = workspaceId
  }

  return config
})

// RESPONSE INTERCEPTOR
// Runs after every response
let isRefreshing = false
let failedQueue: any[] = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  // Success: just return response
  (response) => response,

  // Error: handle 401
  async (error) => {
    const originalRequest = error.config

    // If 401 and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue this request until refresh completes
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers.Authorization = `Bearer ${token}` 
          return api(originalRequest)
        }).catch(err => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refreshToken')
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/auth/refresh`,
          { refreshToken }
        )

        const { accessToken } = response.data

        // Save new token
        localStorage.setItem('accessToken', accessToken)

        // Process queued requests
        processQueue(null, accessToken)

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${accessToken}` 
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh failed - logout user
        processQueue(refreshError, null)
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api
