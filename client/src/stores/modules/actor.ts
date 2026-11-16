import { defineStore } from 'pinia'

// Services
import { getActors, createActor, getErrorMessage } from '../../services'

// Types
import type {
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../../types'

export const useActorStore = defineStore('actor', {
  state: () => ({
    actors: [] as Person[],

    actorsLoaded: false,
    loadingActors: false,

    error: '',
  }),

  getters: {
    allActors: (state) => state.actors
  },

  actions: {
    // Fetch actors
    async fetchActors(): Promise<void> {
      if (this.actorsLoaded) return

      this.loadingActors = true
      this.error = ''

      try {
        this.actors = await getActors()
        this.actorsLoaded = true
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch actors.')
        throw err
      } finally {
        this.loadingActors = false
      }
    },

    // Create actor
    async addActor(request: PersonRequest): Promise<CreatePersonResponse> {
      this.error = ''

      try {
        const response = await createActor(request)

        // Refresh actor list
        this.actorsLoaded = false
        await this.fetchActors()

        return response
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create actor.')
        throw err
      }
    },
  },
})
