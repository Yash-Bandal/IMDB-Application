import { apiGet } from './api'

import type { ApiResponse } from '../types/api'
import type { Genre } from '../types/genre'

export async function getGenres(): Promise<Genre[]> {
  const response = await apiGet<ApiResponse<Genre[]>>('/genres')
  return response.data
}
