

<template>
  <v-container fluid class="movie-form-container">

    <!-- Page Heading -->
    <div class="form-header mb-6">
      <h1 class="text-h5 font-weight-bold">
        {{ isEditMode ? 'Edit Movie' : 'Add Movie' }}
      </h1>

      <p class="text-body-2 text-medium-emphasis mt-2">
        Enter the movie details and select its cast and genres.
      </p>
    </div>

    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="mb-5"
    >
      {{ error }}
    </v-alert>

    <!-- Movie Form -->
    <v-card class="form-card" variant="flat">

      <v-card-text class="pa-0">
        <v-form @submit.prevent="handleSubmit">

          <v-row class="py-2">

            <!-- Movie Name -->
            <v-col cols="12" md="8">
              <v-text-field
                v-model="form.name"
                label="Movie name"
                variant="outlined"
                density="comfortable"
                :rules="[value => !!value?.trim() || 'Movie name is required']"
                required
                :disabled="saving"
              />
            </v-col>

            <!-- Release Year -->
            <v-col cols="12" md="4">
              <v-text-field
                v-model.number="form.yearOfRelease"
                label="Release year"
                type="number"
                variant="outlined"
                density="comfortable"
                :rules="[
                  value => !!value || 'Release year is required',
                  value => Number(value) >= 1888 || 'Enter a valid release year',
                  value => Number(value) <= new Date().getFullYear() || 'Year cannot be in the future',
                ]"
                required
                :disabled="saving"
              />
            </v-col>

            <!-- Plot -->
            <v-col cols="12">
              <v-textarea
                v-model="form.plot"
                label="Plot"
                variant="outlined"
                density="comfortable"
                rows="4"
                auto-grow
                :rules="[value => !!value?.trim() || 'Plot is required']"
                required
                :disabled="saving"
              />
            </v-col>

            <!-- Producer -->
            <v-col cols="12">
              <div class="d-flex align-start ga-2">
                <v-select
                  v-model="form.producerId"
                  :items="producers"
                  item-title="name"
                  item-value="id"
                  label="Producer"
                  variant="outlined"
                  density="comfortable"
                  :rules="[value => !!value || 'Select a producer']"
                  required
                  class="flex-grow-1"
                  :disabled="saving"
                />

                <v-btn
                  color="primary"
                  variant="tonal"
                  density="comfortable"
                  class="add-btn"
                  :disabled="saving"
                  @click="openPersonDialog('producer')"
                >
                  <v-icon>mdi-plus</v-icon>
                  <span class="ml-1">Add</span>
                </v-btn>
              </div>
            </v-col>

            <!-- Actors -->
            <v-col cols="12">
              <div class="d-flex align-start ga-2">
                <v-select
                  v-model="form.actorIds"
                  :items="actors"
                  item-title="name"
                  item-value="id"
                  label="Actors"
                  variant="outlined"
                  density="comfortable"
                  multiple
                  chips
                  closable-chips
                  class="flex-grow-1"
                  :disabled="saving"
                />

                <v-btn
                  color="primary"
                  variant="tonal"
                  density="comfortable"
                  class="add-btn"
                  :disabled="saving"
                  @click="openPersonDialog('actor')"
                >
                  <v-icon>mdi-plus</v-icon>
                  <span class="ml-1">Add</span>
                </v-btn>
              </div>
            </v-col>

            <!-- Genres -->
            <v-col cols="12">
              <v-select
                v-model="form.genreIds"
                :items="genres"
                item-title="name"
                item-value="id"
                label="Genres"
                variant="outlined"
                density="comfortable"
                multiple
                chips
                closable-chips
                :disabled="saving"
              />
            </v-col>

            <!-- Poster Upload -->
            <v-col cols="12">
              <div class="text-subtitle-2 font-weight-medium mb-2">
                Movie poster
                <span class="text-medium-emphasis font-weight-regular">
                  (Optional)
                </span>
              </div>

              <v-file-input
                v-model="posterFile"
                label="Choose poster image"
                accept="image/*"
                prepend-icon="mdi-image-outline"
                variant="outlined"
                density="comfortable"
                show-size
                clearable
                :disabled="saving"
              />

              <v-img
                v-if="posterPreview"
                :src="posterPreview"
                max-height="260"
                max-width="180"
                rounded="lg"
                cover
                class="mt-3"
              />
            </v-col>

          </v-row>

          <!-- Form Actions -->
          <div class="d-flex justify-end ga-3 mt-3 form-actions">

            <v-btn
              to="/movies"
              variant="text"
              color="secondary"
              :disabled="saving"
            >
              Cancel
            </v-btn>

            <v-btn
              type="submit"
              color="primary"
              variant="flat"
              :loading="saving"
              :disabled="saving"
            >
              {{ isEditMode ? 'Update Movie' : 'Create Movie' }}
            </v-btn>

          </div>

        </v-form>
      </v-card-text>
    </v-card>

    <PersonFormDialog
      v-model="showPersonDialog"
      :type="personDialogType"
      @saved="handlePersonSaved"
    />

  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'

import { useAppStore } from '../stores/store'
import { uploadMoviePoster } from '../services/movieService'

import type { MovieRequest } from '../types/movie'

import PersonFormDialog from '../components/shared/PersonFormDialog.vue'

const route = useRoute()
const router = useRouter()
const store = useAppStore()

const {
  actors,
  producers,
  genres,
  error,
  savingMovie,
} = storeToRefs(store)

const isEditMode = computed(() => route.params.id !== undefined)

const saving = ref(false)

const showPersonDialog = ref(false)
const personDialogType = ref<'actor' | 'producer'>('actor')

const posterFile = ref<File | null>(null)
const posterPreview = ref('')

const form = ref<MovieRequest>({
  name: '',
  yearOfRelease: new Date().getFullYear(),
  plot: '',
  coverImage: '',
  producerId: 0,
  actorIds: [],
  genreIds: [],
})

watch(posterFile, (file) => {
  if (posterPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(posterPreview.value)
  }

  posterPreview.value = file
    ? URL.createObjectURL(file)
    : ''
})

onUnmounted(() => {
  if (posterPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(posterPreview.value)
  }
})

onMounted(async () => {
  try {
    await Promise.all([
      store.fetchPeople(),
      store.fetchGenres(),
    ])

    if (isEditMode.value) {
      const movieId = getValidMovieId()

      if (movieId === null) {
        throw new Error('Invalid movie ID in URL.')
      }

      const movie = await store.fetchMovieById(movieId)

      form.value = {
        name: movie.name,
        yearOfRelease: movie.yearOfRelease,
        plot: movie.plot ?? '',
        coverImage: movie.coverImage ?? '',
        producerId: movie.producer?.id ?? 0,
        actorIds: movie.actors.map(actor => actor.id),
        genreIds: movie.genres.map(genre => genre.id),
      }

      posterPreview.value = movie.coverImage ?? ''
    }
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to load movie form data.'
  }
})

function openPersonDialog(type: 'actor' | 'producer') {
  personDialogType.value = type
  showPersonDialog.value = true
}

function handlePersonSaved(personId: number) {
  if (personDialogType.value === 'actor') {
    if (!form.value.actorIds.includes(personId)) {
      form.value.actorIds.push(personId)
    }
  } else {
    form.value.producerId = personId
  }
}

function getValidMovieId(): number | null {
  const id = Number(route.params.id)

  if (!Number.isInteger(id) || id <= 0) {
    return null
  }

  return id
}

async function handleSubmit() {
  if (saving.value) return

  error.value = ''

  if (!form.value.name.trim()) {
    error.value = 'Movie name is required.'
    return
  }

  if (!form.value.yearOfRelease || form.value.yearOfRelease < 1888 ||
      form.value.yearOfRelease > new Date().getFullYear()) {
    error.value = 'Please enter a valid release year.'
    return
  }

  if (!form.value.plot.trim()) {
    error.value = 'Movie plot is required.'
    return
  }

  if (!form.value.producerId) {
    error.value = 'Please select a producer.'
    return
  }

  if (posterFile.value && !posterFile.value.type.startsWith('image/')) {
    error.value = 'Please select a valid image file.'
    return
  }

  saving.value = true

  try {
    if (isEditMode.value) {
      const movieId = getValidMovieId()

      if (movieId === null) {
        throw new Error('Invalid movie ID in URL.')
      }

      await store.editMovie(movieId, form.value)

      if (posterFile.value) {
        await uploadMoviePoster(movieId, posterFile.value)
      }
    } else {
      const createdMovie = await store.addMovie(form.value)

      if (posterFile.value) {
        const result = createdMovie as {
          data?: { id?: number }
          id?: number
        }

        const movieId = result?.data?.id ?? result?.id

        if (movieId === undefined) {
          throw new Error('Movie created, but ID was not returned.')
        }

        await uploadMoviePoster(movieId, posterFile.value)
      }
    }

    await router.push('/movies')
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to save the movie.'
  } finally {
    saving.value = false
  }
}
</script>


<style setup>

.movie-form-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 32px;
}

.form-header h1 {
  color: #222;
}

.form-card {
  background: transparent;
  border: none !important;
  box-shadow: none !important;
}

.add-btn {
  margin-top: 2px;
  min-width: 76px;
  height: 48px;
  text-transform: none;
  letter-spacing: 0;
}

.form-actions .v-btn {
  text-transform: none;
  letter-spacing: 0;
}


/* Tablet */
@media (max-width: 960px) {
  .movie-form-container {
    padding: 20px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .movie-form-container {
    padding: 16px 8px;
  }

  .form-header {
    margin-bottom: 20px !important;
  }

  .form-actions {
    margin-top: 8px;
  }

  .add-btn {
    min-width: 40px;
    padding: 0 10px;
  }
}

</style>