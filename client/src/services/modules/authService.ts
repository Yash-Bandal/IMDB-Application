import { reactive } from 'vue'
import { apiPost, getErrorMessage } from './api'
import type { ApiResponse } from '../../types'
import { setAccessToken, clearAccessToken } from './authToken'

interface AuthResponse {
  accessToken: string
}

const DEMO_USER = {
  emailId: 'yb.testing@gmail.com',
  password: 'Yash@1234',
}

export const authStatus = reactive({
  isLoading: true,
  isAuthenticated: false,
  error: '',
})

export async function login(): Promise<void> {
  const response = await apiPost<ApiResponse<AuthResponse>>(
    '/auth/login',
    DEMO_USER,
  )

  setAccessToken(response.data.accessToken)
}

export async function initializeAuth(): Promise<void> {
  authStatus.isLoading = true
  authStatus.error = ''

  try {
    await login()
    authStatus.isAuthenticated = true
  } catch (error) {
    clearAccessToken()
    authStatus.isAuthenticated = false
    authStatus.error = getErrorMessage(error, 'Authentication failed.')
  } finally {
    authStatus.isLoading = false
  }
}