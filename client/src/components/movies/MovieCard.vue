<script setup lang="ts">
import type { Movie } from '../../types'
import { ref } from 'vue';

interface Props {
  movie: Movie,
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (event: 'edit', movie: Movie): void
  (event: 'delete', movie: Movie): void
  (event: 'view', movie: Movie): void
}>()  

</script>

<template>
  <v-card
    class="movie-card"
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

    <!-- Poster Placeholder -->
    <div
      v-else
      class="movie-poster poster-placeholder d-flex align-center justify-center"
    >
      <v-icon
        icon="mdi-movie-open-outline"
        size="64"
        color="grey-lighten-1"
      />
    </div>

    <!-- Gradient Overlay and Content -->
    <div class="movie-overlay">

      <div class="movie-content">

        <!-- Movie Title -->
        <h3 class="movie-title">
          {{ movie.name }}
        </h3>
        
        <!-- Movie Details: Visible on Hover -->
        <div class="movie-details">
          <p class="movie-year">
            {{ movie.yearOfRelease }}
          </p>

          <!-- <p class="movie-description">
            {{ movie.plot || 'No description available.' }}
          </p> -->
        </div>

        <!-- Action Buttons -->
      <div class="movie-actions">

        <!-- Edit and Delete: Bottom Left -->
        <div class="management-actions">
          <v-btn
            icon="mdi-pencil-outline"
            variant="text"
            color="white"
            size="small"
            aria-label="Edit movie"
            @click.stop="emit('edit', movie)"
          />

          <v-btn
            icon="mdi-delete-outline"
            variant="text"
            color="white"
            size="small"
            aria-label="Delete movie"
            @click.stop="emit('delete', movie)"
          />
        </div>

        <!-- Explore Arrow: Bottom Right -->
        <v-btn
          class="explore-arrow"
          icon="mdi-arrow-right"
          variant="text"
          color="white"
          size="large"
          aria-label="Explore movie"
          @click.stop="emit('view', movie)"
        />

      </div>
      </div>
    </div>
  </v-card>
</template>



<style scoped>
.movie-card {
  position: relative;
  width: 100%;
  aspect-ratio: 1.08 / 1;
  min-height: 300px;
  overflow: hidden;
  /* background: #171717; */
  cursor: default;
}

/* Poster */
.movie-poster {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  transition: transform 0.55s ease;
}

.poster-placeholder {
  background: #5f5f5f;
}

/* Gradient overlay */
.movie-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  padding: 20px;
  color: white;

  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.75) 0%,
    rgba(0, 0, 0, 0.65) 18%,
    rgba(0, 0, 0, 0.12) 35%,
    transparent 100%
  );
}

.movie-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;

  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.88) 0%,
    rgba(0, 0, 0, 0.60) 35%,
    rgba(0, 0, 0, 0.10) 80%
  );

  transition: opacity 0.40s ease;
}

.movie-content {
  position: relative;
  z-index: 1;
  width: 100%;
}

/* Title */
.movie-title {
  font-size: 21px;
  font-weight: 700;
  line-height: 1.3;
  color: white;
  margin: 0;
  padding: 0;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

/* Movie details */
.movie-details {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transform: translateY(10px);

  transition:
    max-height 0.45s ease,
    opacity 0.4s ease,
    transform 0.4s ease;
}

.movie-year {
  font-size: 14px;
  font-weight: 600;
  margin-top: 6px;
  margin-bottom: 4px;
  color: #e5e5e5;
}

.movie-description {
  font-size: 11px;
  line-height: 1.35;
  color: #e5e5e5;

  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

/* Action area */
.movie-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;

  max-height: 0;
  opacity: 0;
  overflow: hidden;
  margin-top: 0;

  transition:
    max-height 0.4s ease,
    opacity 0.35s ease,
    margin 0.35s ease;
}

/* Edit and Delete group: bottom left */
.management-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Remove all default Vuetify button backgrounds */
.movie-actions :deep(.v-btn) {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  color: white !important;
  letter-spacing: 0;
  min-width: 36px;
  width: 36px;
  height: 36px;
  opacity: 0.85;
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

/* Subtle icon hover */
.movie-actions :deep(.v-btn:hover) {
  opacity: 1;
  transform: scale(1.12);
}

/* Explore arrow: bottom right */
.explore-arrow {
  margin-left: auto;
}

/* Arrow moves slightly right on hover */

/* Smooth arrow movement when hovering over the arrow */
.explore-arrow {
  background: transparent !important;
  box-shadow: none !important;
  transition: none !important;
}

/* Remove Vuetify's hover background */
.explore-arrow :deep(.v-btn__overlay),
.explore-arrow :deep(.v-btn__underlay) {
  opacity: 0 !important;
  background: transparent !important;
}

/* Keep only the arrow animated */
.explore-arrow :deep(.v-icon) {
  transition: transform 0.3s ease !important;
}

.explore-arrow:hover :deep(.v-icon) {
  transform: translateX(6px);
}

/* .movie-card:hover .explore-arrow {
  transform: translateX(5px);
  opacity: 1;
} */

/* Poster zoom */
.movie-card:hover .movie-poster {
  transform: scale(1.06);
}

/* Gradient reveal */
.movie-card:hover .movie-overlay::before {
  opacity: 1;
}

/* Details reveal */
.movie-card:hover .movie-details {
  max-height: 150px;
  opacity: 1;
  transform: translateY(0);
}

/* Actions reveal */
.movie-card:hover .movie-actions {
  max-height: 48px;
  opacity: 1;
  margin-top: 12px;
}

/* Touch devices */
@media (hover: none) {
  .movie-overlay::before {
    opacity: 1;
  }

  .movie-details {
    max-height: 150px;
    opacity: 1;
    transform: none;
  }

  .movie-actions {
    max-height: 48px;
    opacity: 1;
    margin-top: 12px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .movie-card {
    aspect-ratio: 1.15 / 1;
    min-height: 260px;
  }

  .movie-overlay {
    padding: 16px;
  }

  .movie-title {
    font-size: 18px;
  }

  .movie-description {
    font-size: 13px;
  }
}
</style>

