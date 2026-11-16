import { apiGet } from './api'

import type { ApiResponse, Genre } from '../../types'

export async function getGenres(): Promise<Genre[]> {
  const response = await apiGet<ApiResponse<Genre[]>>('/genres')
  return response.data
}
