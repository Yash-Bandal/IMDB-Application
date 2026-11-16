import type { Genre } from "./genre";
import type { Person } from "./person";

export interface Movie {
  id: number
  name: string
  yearOfRelease: number
  plot?: string | null
  coverImage?: string | null
  producer: Person | null
  actors: Person[]
  genres: Genre[]
}

export interface MovieRequest {
  name: string
  yearOfRelease: number
  plot: string
  coverImage: string
  producerId: number | null
  actorIds: number[]
  genreIds: number[]
}

export interface CreateMovieResponse {
  id: number
}

