<template>
  <v-container fluid class="movies-container">

    <!-- Page Heading -->
    <div class="movies-header d-flex align-center justify-space-between flex-wrap ga-4">

      <!-- Heading -->
      <div>
        <div class="d-flex align-center ga-2">
          <h1 class="movies-heading">Movies</h1>

          <v-icon
            icon="mdi-movie-open-outline"
            size="30"
            color="#333"
          />
        </div>

        <p class="movies-subheading">
          Explore and manage your movie collection
        </p>
      </div>

      <!-- Add Movie Button -->
      <v-btn
        to="/movies/create"
        variant="outlined"
        color="black"
        append-icon="mdi-plus"
        class="add-movie-btn"
      >
        Add Movie
      </v-btn>

    </div>

    <!-- API Error -->
    <v-alert
      v-if="error"
      type="error"
      variant="tonal"
      class="mb-4"
    >
      {{ error }}

      <div class="mt-2">
        Check that your backend is running and its HTTPS certificate is trusted.
      </div>
    </v-alert>

    <!-- Loading State -->
    <div
      v-else-if="loadingMovies"
      class="d-flex justify-center py-12"
    >
      <LoadingMovies />
    </div>

    <!-- Empty State -->
    <v-alert
      v-else-if="allMovies.length === 0"
      type="info"
      variant="tonal"
    >
      No movies found.
    </v-alert>

    <!-- Movie Grid -->
    <v-row v-else class="movie-grid">

      <v-col
        v-for="movie in allMovies"
        :key="movie.id"
        cols="12"
        sm="6"
        md="4"
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

    <!-- Movie Details Dialog -->
    <MovieDetailModal
      v-model="modelValue"
      :movie="ModalMovie"
    />

  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref , computed} from 'vue'
import { storeToRefs } from 'pinia'
import { useMovieStore } from '../stores'
import type { Movie } from '../types'
import Swal from 'sweetalert2'

// Components
import MovieCard from '../components/movies/MovieCard.vue'
import MovieDetailModal from '../components/movies/MovieDetailModal.vue'
import LoadingMovies from '../components/shared/LoadingMovies.vue'

// Store and Router
const movieStore = useMovieStore()
const router = useRouter()

const {
  allMovies,
  loadingMovies,
  error,
} = storeToRefs(movieStore)

// Local UI State
const modelValue = ref(false)
const ModalMovie = ref<Movie | null>(null)

// Fetch movies
onMounted(() => {
  movieStore.fetchMovies()
})

// Delete Movie Confirmation
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
        await movieStore.deleteMovie(movie.id)
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

// Open Movie Details
function handleView(movie: Movie) {
  modelValue.value = true
  ModalMovie.value = movie
}

// Navigate to Edit Movie
function handleEdit(movie: Movie) {
  router.push(`/movies/${movie.id}/edit`)
}

</script>

<style scoped>
.movies-container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 24px 28px;
}

.movie-grid {
  row-gap: 18px;
}

.movies-header {
  margin-bottom: 28px;
}

.movies-heading {
  font-size: 30px;
  font-weight: 750;
  line-height: 1.2;
  letter-spacing: -0.8px;
  color: #171717;
  margin: 0;
}

.movies-subheading {
  font-size: 14px;
  color: #777;
  margin: 5px 0 0;
  line-height: 1.4;
}

.add-movie-btn {
  text-transform: none;
  letter-spacing: 0;
  font-size: 14px;
  font-weight: 600;
  height: 42px;
  padding: 0 18px;
  border: 1px solid #222 !important;
  border-radius: 8px;
  background: transparent !important;
  box-shadow: none !important;
  transition: all 0.2s ease;
}

.add-movie-btn:hover {
  background: #f5f5f5 !important;
}

@media (max-width: 600px) {
  .movies-heading {
    font-size: 25px;
  }

  .movies-header {
    margin-bottom: 22px;
  }

  .movies-subheading {
    font-size: 12px;
  }
}

/* .movies-heading {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 20px;
} */

/* Tablet */
@media (max-width: 960px) {
  .movies-container {
    padding: 20px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .movies-container {
    padding: 16px 12px;
  }

  .movies-heading {
    font-size: 26px;
  }
}
</style>
