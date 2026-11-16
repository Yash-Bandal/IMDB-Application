import axios, { type AxiosError } from 'axios'
import { getAccessToken } from './authToken'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptors
// centralized request handling.
api.interceptors.request.use(config => {
  const token = getAccessToken()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  // Success case
  response => response,

  // Error case - Normalize all Axios errors
  (error: AxiosError) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      const details = error.response?.data

      const message =
        getBackendErrorMessage(details) ??
        (status
          ? `Request failed with status ${status}.`
          : error.message || 'Unable to connect to the server.')

      return Promise.reject(
        new ApiError(message, status, details),
      )
    }

    return Promise.reject(error)
  },
)

// Standard structure for API errors
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly details?: unknown,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

// Extract a useful error message from the backend response 
function getBackendErrorMessage(data: unknown): string | undefined {
  if (typeof data === 'string' && data.trim()) {
    return data
  }

  if (typeof data !== 'object' || data === null) {
    return undefined
  }

  const body = data as Record<string, unknown>

  if (typeof body.message === 'string') return body.message
  if (typeof body.Message === 'string') return body.Message
  if (typeof body.title === 'string') return body.title
  if (typeof body.detail === 'string') return body.detail

  return undefined
}

// Helper for displaying consistent error messages
export function getErrorMessage(error: unknown, fallback = 'Something went wrong.', ): string 
{
  if (error instanceof ApiError) {
    return error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return fallback
}

// API Methods
// GET
export async function apiGet<T>(endpoint: string): Promise<T> 
{
  const response = await api.get<T>(endpoint)
  return response.data
}

// POST
export async function apiPost<T>(endpoint: string, body: object, ): Promise<T> 
{
  const response = await api.post<T>(endpoint, body)
  return response.data
}

// PUT
export async function apiPut<T>(endpoint: string, body: object, ): Promise<T> 
{
  const response = await api.put<T>(endpoint, body)
  return response.data
}

// DELETE
export async function apiDelete(endpoint: string): Promise<void> 
{
  await api.delete(endpoint)
}

// File upload (will be used for update/ dont remove keep it)
export async function apiUpdate<T>(endpoint: string, formData: FormData, ): Promise<T> 
{
  const response = await api.put<T>(endpoint, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export async function apiUpload<T>(endpoint: string, formData: FormData, ): Promise<T> 
{
  const response = await api.post<T>(endpoint, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export default api
