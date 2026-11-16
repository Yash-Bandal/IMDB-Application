import { defineStore } from 'pinia'

// Services
import {
  getMovies,
  getMovieById,
  createMovie,
  updateMovie,
  uploadMoviePoster as uploadMoviePosterRequest,
  deleteMovie as deleteMovieRequest,
  getErrorMessage } from '../../services'

// Types
import type { Movie, MovieRequest, CreateMovieResponse } from '../../types'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    movies: [] as Movie[],
    currentMovie: null as Movie | null,

    moviesLoaded: false,

    loadingMovies: false,
    savingMovie: false,

    error: '',
  }),

  getters: {
    allMovies: (state) => state.movies,
    selectedMovie : (state) => state.currentMovie,
  },

  actions: {
    // Fetch all movies
    async fetchMovies(): Promise<void> {
      // dont fetch if already movies loaded  
      if (this.moviesLoaded){
          return
      } 

      this.loadingMovies = true
      this.error = ''

      try {
        this.movies = await getMovies()
        this.moviesLoaded = true
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch movies.')
        throw err
      } finally {
        this.loadingMovies = false
      }
    },

    // Fetch one movie
    async fetchMovieById(id: number): Promise<void> {
      this.error = ''

      try {
        this.currentMovie = await getMovieById(id)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch movie.')
        throw err
      }
    },

    // Create movie
    async addMovie(request: MovieRequest): Promise<CreateMovieResponse> {
      this.savingMovie = true
      this.error = ''

      try {
        const response = await createMovie(request)
        // Movie list is now outdated
        this.moviesLoaded = false

        return response
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create movie.')
        throw err
      } finally {
        this.savingMovie = false
      }
    },

    // Update movie
    async editMovie(id: number, request: MovieRequest): Promise<void> {
      this.savingMovie = true
      this.error = ''

      try {
        await updateMovie(id, request)

        // Movie list is now outdated
        this.moviesLoaded = false
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to update movie.')
        throw err
      } finally {
        this.savingMovie = false
      }
    },

    // Upload movie poster
    async uploadMoviePoster(file: File): Promise<string> {
      this.savingMovie = true
      this.error = ''

      try {
        return await uploadMoviePosterRequest(file)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to upload movie poster.')
        throw err
      } finally {
        this.savingMovie = false
      }
    },

    // Delete movie
    async deleteMovie(id: number): Promise<void> {
      this.error = ''

      try {
        await deleteMovieRequest(id)

        // Update local list without another API call (avoid refetching of movies)
        this.movies = this.movies.filter(movie => movie.id !== id)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to delete movie.')
        throw err
      }
    },
  },
})
