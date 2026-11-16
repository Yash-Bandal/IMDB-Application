import { apiGet, apiPost } from './api'

import type { ApiResponse } from '../types/api'
import type {
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../types/person'

export async function getActors(): Promise<Person[]> {
  const response = await apiGet<ApiResponse<Person[]>>('/actors')
  return response.data
}

export async function createActor(
  request: PersonRequest,
): Promise<CreatePersonResponse> {
  return apiPost<CreatePersonResponse>('/actors', request)
}
