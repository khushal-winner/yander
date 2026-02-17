'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import api from '../api/axios'

interface User {
  id: string
  email: string
  name: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  register: (data: RegisterData) => Promise<void>
}

interface RegisterData {
  email: string
  password: string
  name: string
  workspaceName: string
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // On mount: check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      // Verify token by fetching user
      api.get('/auth/me')
        .then(res => setUser(res.data))
        .catch(() => {
          localStorage.clear()
          setUser(null)
        })
        .finally(() => setIsLoading(false))
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const res = await api.post('/auth/login', { email, password })

    // Store tokens
    localStorage.setItem('accessToken', res.data.accessToken)
    localStorage.setItem('refreshToken', res.data.refreshToken)

    // Set active workspace (first one)
    if (res.data.user) {
      setUser(res.data.user)
    }
  }

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      await api.post('/auth/logout', { refreshToken })
    } finally {
      localStorage.clear()
      setUser(null)
    }
  }

  const register = async (data: RegisterData) => {
    const res = await api.post('/auth/register', data)

    localStorage.setItem('accessToken', res.data.accessToken)
    localStorage.setItem('refreshToken', res.data.refreshToken)

    if (res.data.workspace) {
      localStorage.setItem('activeWorkspaceId', res.data.workspace.id)
    }

    setUser(res.data.user)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
