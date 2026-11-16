import { defineStore } from 'pinia'

// Services
import { getProducers, createProducer } from '../../services/modules/producerService'

// Error handling
import { getErrorMessage } from '../../services/modules/api'

// Types
import type {
  Person,
  PersonRequest,
  CreatePersonResponse,
} from '../../types'

export const useProducerStore = defineStore('producer', {
  state: () => ({
    producers: [] as Person[],

    producersLoaded: false,
    loadingProducers: false,

    error: '',
  }),

  getters: {
    allProducers: (state) => state.producers,
  },

  actions: {
    // Fetch producers
    async fetchProducers(): Promise<void> {
      if (this.producersLoaded) return

      this.loadingProducers = true
      this.error = ''

      try {
        this.producers = await getProducers()
        this.producersLoaded = true
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to fetch producers.')
        throw err
      } finally {
        this.loadingProducers = false
      }
    },

    // Create producer
    async addProducer(request: PersonRequest): Promise<CreatePersonResponse> {
      this.error = ''

      try {
        const response = await createProducer(request)

        // Refresh producer list
        this.producersLoaded = false
        await this.fetchProducers()

        return response
      } catch (err) {
        this.error = getErrorMessage(err, 'Failed to create producer.')
        throw err
      }
    },
  },
})
