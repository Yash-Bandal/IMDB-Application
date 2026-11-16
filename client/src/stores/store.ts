
import { defineStore } from 'pinia'

// Services
import {
  getMovies,
  getMovieById,
  createMovie,
  updateMovie,
  deleteMovie as deleteMovieRequest,
} from '../services/movieService'

import { getActors, createActor } from '../services/actorService'
import { getProducers, createProducer } from '../services/producerService'
import { getGenres } from '../services/genreService'

// Error handling
import { getErrorMessage } from '../services/api'

// Types
import type { Movie, MovieRequest } from '../types/movie'
import type {
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../types/person'
import type { Genre } from '../types/genre'

export const useAppStore = defineStore('app', {
  state: () => ({
    movies: [] as Movie[],
    currentMovie: null as Movie | null,

    actors: [] as Person[],
    producers: [] as Person[],
    genres: [] as Genre[],

    loadingMovies: false,
    loadingPeople: false,
    loadingGenres: false,
    savingMovie: false,

    error: '',
  }),

  getters: {},

  actions: {
    // Fetch all movies
    async fetchMovies() {
      this.loadingMovies = true
      this.error = ''

      try {
        this.movies = await getMovies()
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch movies.')
        throw err
      } finally {
        this.loadingMovies = false
      }
    },

    // Fetch one movie
    async fetchMovieById(id: number) {
      this.error = ''

      try {
        this.currentMovie = await getMovieById(id)
        return this.currentMovie
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch movie.')
        throw err
      }
    },

    // Create movie
    async addMovie(request: MovieRequest) {
      this.savingMovie = true
      this.error = ''

      try {
        return await createMovie(request)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create movie.')
        throw err
      } finally {
        this.savingMovie = false
      }
    },

    // Update movie
    async editMovie(id: number, request: MovieRequest) {
      this.savingMovie = true
      this.error = ''

      try {
        await updateMovie(id, request)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to update movie.')
        throw err
      } finally {
        this.savingMovie = false
      }
    },

    // Delete movie
    async deleteMovie(id: number) {
      this.error = ''

      try {
        await deleteMovieRequest(id)
        this.movies = this.movies.filter(movie => movie.id !== id)
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to delete movie.')
        throw err
      } 
    },

    // Fetch actors and producers
    async fetchPeople() {
      this.loadingPeople = true
      this.error = ''

      try {
        const [actors, producers] = await Promise.all([
          getActors(),
          getProducers(),
        ])

        this.actors = actors
        this.producers = producers
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch people.')
        throw err
      } finally {
        this.loadingPeople = false
      }
    },

    // Create actor
    async addActor(request: PersonRequest): Promise<CreatePersonResponse> {
      this.error = ''

      try {
        const response = await createActor(request)
        await this.fetchPeople()
        return response
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create actor.')
        throw err
      }
    },

    // Create producer
    async addProducer(request: PersonRequest): Promise<CreatePersonResponse> {
      this.error = ''

      try {
        const response = await createProducer(request)
        await this.fetchPeople()
        return response
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create producer.')
        throw err
      }
    },

    // Fetch genres
    async fetchGenres() {
      this.loadingGenres = true
      this.error = ''

      try {
        this.genres = await getGenres()
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch genres.')
        throw err
      } finally {
        this.loadingGenres = false
      }
    },
  },
})
