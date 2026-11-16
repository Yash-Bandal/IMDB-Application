import { defineStore } from 'pinia'

// Services
import { getGenres, getErrorMessage } from '../../services'

// Types
import type { Genre } from '../../types'

export const useGenreStore = defineStore('genre', {
  state: () => ({
    genres: [] as Genre[],

    genresLoaded: false,
    loadingGenres: false,

    error: '',
  }),

  getters: {
    allGenres: (state) => state.genres,
  },

  actions: {
    // Fetch genres
    async fetchGenres(): Promise<void> {
      if (this.genresLoaded) return

      this.loadingGenres = true
      this.error = ''

      try {
        this.genres = await getGenres()
        this.genresLoaded = true
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch genres.')
        throw err
      } finally {
        this.loadingGenres = false
      }
    },
  },
})
