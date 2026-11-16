import { apiGet, apiPost } from '../modules/api'

import type { 
  ApiResponse,
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../../types'

export async function getActors(): Promise<Person[]> {
  const response = await apiGet<ApiResponse<Person[]>>('/actors')
  return response.data
}

export async function createActor(request: PersonRequest, ): Promise<CreatePersonResponse> {
  return apiPost<CreatePersonResponse>('/actors', request)
}
