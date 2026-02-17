import api from './axios'

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  
  register: (email: string, password: string, name: string) =>
    api.post('/auth/register', { email, password, name }),
  
  refresh: (refreshToken: string) =>
    api.post('/auth/refresh', { refreshToken }),
  
  logout: (refreshToken: string) =>
    api.post('/auth/logout', { refreshToken }),
  
  getMe: () =>
    api.get('/auth/me')
}

// Workspace API
export const workspaceAPI = {
  getMyWorkspaces: () =>
    api.get('/workspaces'),
  
  getMembers: (workspaceId: string) =>
    api.get(`/workspaces/${workspaceId}/members`),
  
  inviteMember: (workspaceId: string, email: string, role: string) =>
    api.post(`/workspaces/${workspaceId}/invite`, { email, role }),
  
  changeMemberRole: (workspaceId: string, userId: string, role: string) =>
    api.patch(`/workspaces/${workspaceId}/members/${userId}`, { role }),
  
  removeMember: (workspaceId: string, userId: string) =>
    api.delete(`/workspaces/${workspaceId}/members/${userId}`)
}

// Invitation API
export const invitationAPI = {
  accept: (token: string) =>
    api.post('/invitations/accept', { token })
}

export default api
