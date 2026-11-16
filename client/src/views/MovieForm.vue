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

    <!-- Error area -->
    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="mb-5"
    >
      {{ error }}
    </v-alert>

    <!-- Form Loading -->
    <div
      v-if="loadingForm"
      class="d-flex justify-center align-center py-10"
    >
      <LoadingSpinner/>
    </div>

    <!-- Movie Form -->
      <v-card
        v-else
        class="form-card"
        variant="flat"
      >

      <v-card-text class="pa-0">
        <v-form  ref="movieForm" @submit.prevent="handleSubmit">

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
                  value => Number(value) >= 0 || 'Enter a valid release year',
                  // value => Number(value) <= new Date().getFullYear() || 'Year cannot be in the future',
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
                  :items="allProducers"
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
                  :items="allActors"
                  item-title="name"
                  item-value="id"
                  label="Actors"
                  variant="outlined"
                  density="comfortable"
                  multiple
                  chips
                  closable-chips
                  class="flex-grow-1"
                  :rules="[value => value?.length > 0 || 'Select at least one actor']"
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
                :items="allGenres"
                item-title="name"
                item-value="id"
                label="Genres"
                variant="outlined"
                density="comfortable"
                multiple
                chips
                closable-chips
                :rules="[value => value?.length > 0 || 'Select at least one genre']"
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

              <input
                type="file"
                accept="image/*"
                class="poster-file-input"
                :disabled="saving"
                @change="handlePosterChange"
              />
              <div v-if="posterError" class="text-error text-caption mt-1">
                {{ posterError }}
              </div>

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
// Dependencies
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'

// Modules
import {
  useMovieStore,
  useActorStore,
  useProducerStore,
  useGenreStore,
} from '../stores'

import type { MovieRequest } from '../types'

// Components
import PersonFormDialog from '../components/shared/PersonFormDialog.vue'
import LoadingSpinner from '../components/shared/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()

// Stores
const movieStore = useMovieStore()
const actorStore = useActorStore()
const producerStore = useProducerStore()
const genreStore = useGenreStore()

// Store State
const { allActors } = storeToRefs(actorStore)
const { allProducers } = storeToRefs(producerStore)
const { allGenres } = storeToRefs(genreStore)
const { selectedMovie } = storeToRefs(movieStore)

const isEditMode = computed(() => route.params.id !== undefined)

const saving = ref(false)
const loadingForm = ref(true)

const showPersonDialog = ref(false)
const personDialogType = ref<'actor' | 'producer'>('actor')

const posterFile = ref<File | null>(null)
const posterPreview = ref('')

const movieForm = ref()

const posterError = ref('')
const error = ref('')

const form = ref<MovieRequest>({
  name: '',
  yearOfRelease: new Date().getFullYear(),
  plot: '',
  coverImage: '',
  producerId: null as number | null,
  actorIds: [],
  genreIds: [],
})

watch(posterFile, (file) => {
  // Clean up the previous preview URL 
  if (posterPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(posterPreview.value)
  }

  posterPreview.value = ''

  // No file selected (Stop callback)
  if (!file){
    return
  } 

  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value =
      'Invalid file. Please select an image (JPG, PNG, GIF, WEBP, etc.).'

    // Reject the invalid file
    posterFile.value = null
    return
  }

  // Valid image selected
  error.value = ''
  posterPreview.value = URL.createObjectURL(file)
})

onUnmounted(() => {
  if (posterPreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(posterPreview.value)
  }
})

onMounted(async () => {
  loadingForm.value = true

  try {
    // Fetch Entities
    await Promise.all([
      actorStore.fetchActors(),
      producerStore.fetchProducers(),
      genreStore.fetchGenres(),
    ])

    // Determine If Edit Mode
    if (isEditMode.value) {
      // get id from route
      const movieId = getValidMovieId()

      if (movieId === null) {
        throw new Error('Invalid movie ID in URL.')
      }

      await movieStore.fetchMovieById(movieId)

      if (!selectedMovie.value) {
        throw new Error('Movie not found.')
      }

      const movie = selectedMovie.value;

      form.value = {
        name: movie.name,
        yearOfRelease: movie.yearOfRelease,
        plot: movie.plot ?? '',
        coverImage: movie.coverImage ?? '',
        producerId: movie.producer?.id ?? null,
        actorIds: movie.actors.map(actor => actor.id),
        genreIds: movie.genres.map(genre => genre.id),
      }

      posterPreview.value = movie.coverImage ?? ''
    }
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to load movie form data.'
  } finally {
    loadingForm.value = false
  }
})

function openPersonDialog(type: 'actor' | 'producer') {
  personDialogType.value = type
  showPersonDialog.value = true
}

// On Adding Actor/Producer Add it to Form -> ActorId[] 
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

function handlePosterChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] ?? null

  posterError.value = ''

  if (!file) {
    posterFile.value = null
    return
  }

  if (!file.type.startsWith('image/')) {
    posterError.value = 'Please select a valid image file.'
    posterFile.value = null

    // Clear the invalid selection from the input
    input.value = ''
    return
  }

  posterFile.value = file
}

async function handleSubmit() {
  // If already saving, cant submit 
  if (saving.value){
    return
  }

  error.value = ''

  // 1. Validate all form fields
  const { valid } = await movieForm.value!.validate()

  if (!valid)
  {
    return
  } 

  saving.value = true

  // If edit mode, perform updation
  try {
    // 1. Upload poster first, if selected
    if (posterFile.value) {
      const imageUrl = await movieStore.uploadMoviePoster(posterFile.value)

      // 2. Add the returned URL to MovieRequest
      form.value.coverImage = imageUrl
    }

    // 3. Create or update movie
    if (isEditMode.value) {
      const movieId = getValidMovieId()

      if (movieId === null) {
        throw new Error('Invalid movie ID in URL.')
      }

      await movieStore.editMovie(movieId, form.value)
    } else {
      await movieStore.addMovie(form.value)
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

.poster-file-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #bdbdbd;
  border-radius: 6px;
  font-size: 14px;
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