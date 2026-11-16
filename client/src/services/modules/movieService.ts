import {
  apiGet,
  apiPost,
  apiPut,
  apiDelete,
  apiUpload,
} from './api'

import type { ApiResponse, Movie, MovieRequest, CreateMovieResponse } from '../../types'

// Get all movies
// Immediately return promise object pending that would be resolved to Movies array on success
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
// Immediately return promise object pending that would be resolved to any type, int/string/etc on success
export async function createMovie(movie: MovieRequest): Promise<CreateMovieResponse> {
  return apiPost<CreateMovieResponse>('/movies', movie)
}

// Update movie
export async function updateMovie(id: number, movie: MovieRequest, ): Promise<void> {
  await apiPut<void>(`/movies/${id}`, movie)
}

// Delete movie
export async function deleteMovie(id: number): Promise<void> {
  await apiDelete(`/movies/${id}`)
}

// Upload or replace movie poster
export async function updateMoviePoster(movieId: number, file: File, ): Promise<string> {
  const formData = new FormData()
  formData.append('file', file)

  return apiUpload<string>(`/movies/${movieId}/poster`, formData)
}

export async function uploadMoviePoster(file: File): Promise<string> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiUpload<ApiResponse<string>>(
    '/movies/poster',
    formData,
  )

  return response.data
}