'use client'

import { useAuth } from '@/lib/context/auth.context'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login')
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  if (!user) {
    return null
  }

  return (
    <div className="flex h-screen">
      {/* Sidebar will go here */}
      <div className="w-64 bg-gray-900 text-white p-4">
        <h2 className="text-xl font-bold mb-6">Yander</h2>
        <nav className="space-y-2">
          <a href="/dashboard" className="block py-2 px-3 rounded hover:bg-gray-800">
            Dashboard
          </a>
          <a href="/workspaces" className="block py-2 px-3 rounded hover:bg-gray-800">
            Workspaces
          </a>
          <a href="/settings" className="block py-2 px-3 rounded hover:bg-gray-800">
            Settings
          </a>
        </nav>
      </div>
      
      <main className="flex-1 overflow-auto p-6">
        {children}
      </main>
    </div>
  )
}
