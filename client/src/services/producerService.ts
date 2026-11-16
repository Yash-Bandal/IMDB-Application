
import { apiGet, apiPost } from './api'

import type { ApiResponse } from '../types/api'
import type {
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../types/person'

export async function getProducers(): Promise<Person[]> {
  const response = await apiGet<ApiResponse<Person[]>>('/producers')
  return response.data
}

export async function createProducer(
  request: PersonRequest,
): Promise<CreatePersonResponse> {
  return apiPost<CreatePersonResponse>('/producers', request)
}
