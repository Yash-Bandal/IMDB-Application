<template>
<v-container fluid class="movies-container">
    <div class="d-flex flex-wrap align-center justify-space-between ga-3">
      <h1 class="movies-heading">Movies</h1>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
      {{ error }}
      <div class="mt-2">
        Check that your backend is running and its HTTPS certificate is trusted.
      </div>
    </v-alert>

<div v-else-if="loadingMovies" class="d-flex justify-center py-12">
  <LoadingMovies />
</div>

    <v-alert v-else-if="movies.length === 0" type="info" variant="tonal">
      No movies found.
    </v-alert>

    <v-row v-else class="movie-grid">
      <v-col
        v-for="movie in movies"
        :key="movie.id"
        cols="12"
        sm="6"
        lg="3"
      >
        <MovieCard
          :movie="movie"
          @view="handleView"
          @edit="handleEdit"
          @delete="confirmDelete"
        />
      </v-col>
    </v-row>

    <MovieDetailModal
      v-model="detailsDialog"
      :movie="detailMovie"
    />

  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAppStore } from '../stores/store'
import type { Movie } from '../types/movie'
import MovieDetailModal from '../components/movies/MovieDetailModal.vue'
import MovieCard from '../components/movies/MovieCard.vue'
import Swal from 'sweetalert2'
import LoadingMovies from '../components/shared/LoadingSpinner.vue'
// import LoadingMovies from '../components/shared/LoadingMovies.vue'
import LoadingSpinner from '../components/shared/LoadingSpinner.vue'

const store = useAppStore()
const router = useRouter()

const {
  movies,
  loadingMovies,
  error,
} = storeToRefs(store)

// Local UI state

const detailsDialog = ref(false)
const detailMovie = ref<Movie | null>(null)

onMounted(() => {
  store.fetchMovies()
})

async function confirmDelete(movie: Movie) {
  const result = await Swal.fire({
    title: 'Are you sure?',
    text: `Do you want to delete "${movie.name}"?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'Yes, delete it',
    cancelButtonText: 'Cancel',
    showLoaderOnConfirm: true,

    preConfirm: async () => {
      try {
        await store.deleteMovie(movie.id)
      } catch {
        Swal.showValidationMessage(
          'Unable to delete the movie. Please try again.'
        )
        return false
      }
    },

    allowOutsideClick: () => !Swal.isLoading(),
  })

  if (result.isConfirmed) {
    await Swal.fire({
      title: 'Deleted!',
      text: 'The movie has been deleted.',
      icon: 'success',
      confirmButtonColor: '#3085d6',
    })
  }
}

function handleView(movie: Movie) {
  detailMovie.value = movie
  detailsDialog.value = true
}

function handleEdit(movie: Movie) {
  router.push(`/movies/${movie.id}/edit`)
}

</script>

<style scoped>
.movies-container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 12px 12px;
}

.movie-grid {
  row-gap: 12px;
}

.movies-heading {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

/* Tablets */
@media (max-width: 960px) {
  .movies-container {
    padding: 20px 20px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .movies-container {
    padding: 16px 8px;
  }

  .movie-grid {
    row-gap: 8px;
  }
}
</style>