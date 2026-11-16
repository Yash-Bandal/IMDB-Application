<script setup lang="ts">
import type { Movie } from '../../types/movie'

defineProps<{
  movie: Movie
}>()

const emit = defineEmits<{
  (event: 'edit', movie: Movie): void
  (event: 'delete', movie: Movie): void
  (event: 'view', movie: Movie): void
}>()
</script>

<template>
  <v-card
    class="movie-card d-flex flex-column"
    height="100%"
    rounded="lg"
    elevation="0"
  >
    <!-- Movie Poster -->
    <v-img
      v-if="movie.coverImage"
      :src="movie.coverImage"
      class="movie-poster"
      cover
      alt="Movie poster"
    />

    <div
      v-else
      class="movie-poster poster-placeholder d-flex align-center justify-center"
    >
      <v-icon
        icon="mdi-movie-open-outline"
        size="56"
        color="grey"
      />
    </div>

    <!-- Movie Title -->
    <v-card-title class="movie-title">
      {{ movie.name }}
    </v-card-title>

    <!-- Movie Description -->
    <v-card-text class="movie-description">
      {{ movie.plot || 'No description available.' }}
    </v-card-text>

    <!-- Action Buttons -->
    <v-card-actions class="movie-actions">
      <v-btn
        color="primary"
        variant="text"
        size="small"
        append-icon="mdi-arrow-right"
        @click="emit('view', movie)"
      >
        Explore
      </v-btn>

      <v-spacer />

      <v-btn
        icon="mdi-pencil-outline"
        color="primary"
        variant="text"
        size="small"
        aria-label="Edit movie"
        @click="emit('edit', movie)"
      />

      <v-btn
        icon="mdi-delete-outline"
        color="error"
        variant="text"
        size="small"
        aria-label="Delete movie"
        @click="emit('delete', movie)"
      />
    </v-card-actions>
  </v-card>
</template>


<style scoped>
.movie-card {
  background-color: #f3f6fd;
  border: none;
  min-height: 408px;
  padding: 18px;
  overflow: hidden;
}

.movie-poster {
  width: 100%;
  aspect-ratio: 5/4;
  object-fit: cover;
}

.poster-placeholder {
  background-color: #e9edf5;
}

.movie-title {
  min-height: 72px;
  padding: 22px 4px 12px;
  align-items: flex-start;

  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
  white-space: normal;
  overflow-wrap: anywhere;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.movie-description {
  min-height: 78px;
  padding: 0 4px;

  font-size: 16px;
  line-height: 1.5;
  color: #555e6d;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.movie-actions {
  min-height: 52px;
  margin-top: auto;
  padding: 8px 0 0;
}

.movie-actions :deep(.v-btn) {
  letter-spacing: 0;
  text-transform: none;
  min-width: 32px;
  height: 32px;
  font-size: 13px;
}

/* Explore button */
.movie-actions :deep(.v-btn--variant-text:not(.v-btn--icon)) {
  padding: 0 10px;
}

/* Icon buttons */
.movie-actions :deep(.v-btn--icon) {
  width: 32px;
  height: 32px;
}


/* buttons */
@media (max-width: 600px) {
  .movie-actions :deep(.v-btn) {
    font-size: 12px;
    height: 28px;
    min-width: 28px;
  }

  .movie-actions :deep(.v-btn--icon) {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 600px) {
  .movie-card {
    min-height: 440px;
  }

  .movie-poster {
    height: 210px;
  }
}
</style>