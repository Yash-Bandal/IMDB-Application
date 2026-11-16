import {
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  apiUpload,
} from './api'

import type { ApiResponse } from '../types/api'
import type { Movie, MovieRequest } from '../types/movie'

// Get all movies
export async function getMovies(): Promise<Movie[]> {
  const response = await apiGet<ApiResponse<Movie[]>>('/movies')
  return response.data
}

// Get movie by ID
export async function getMovieById(id: number): Promise<Movie> {
  const response = await apiGet<ApiResponse<Movie>>(`/movies/${id}`)
  return response.data
}

// Create movie
export async function createMovie(movie: MovieRequest): Promise<unknown> {
  return apiPost<unknown>('/movies', movie)
}

// Update movie
export async function updateMovie(
  id: number,
  movie: MovieRequest,
): Promise<void> {
  await apiPut<void>(`/movies/${id}`, movie)
}

// Delete movie
export async function deleteMovie(id: number): Promise<void> {
  await apiDelete(`/movies/${id}`)
}

// Upload or replace movie poster
export async function uploadMoviePoster(
  movieId: number,
  file: File,
): Promise<unknown> {
  const formData = new FormData()
  formData.append('file', file)

  return apiUpload<unknown>(`/movies/${movieId}/poster`, formData)
}

