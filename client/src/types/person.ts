export interface PersonRequest {
  name: string
  bio: string
  dob: string
  gender: string
}

export interface Person {
  id: number
  name: string
  bio?: string | null
  dob?: string | null
  gender?: string | null
}

export interface CreatePersonResponse {
  id: number
}