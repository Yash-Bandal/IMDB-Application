<script setup lang="ts">
import type { Movie } from '../../types'

interface Props {
  modelValue: boolean
  movie: Movie | null
}

defineProps<Props>()

// emit func definition (Typescript signature func taking 2 params)
const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
}>()

// calls the above sinature func to emit event closedialog  
function closeDialog() {
  emit('update:modelValue', false)
}
</script>

<template>
  <!-- Listen event update -->
  <v-dialog
    :model-value="modelValue"
    max-width="820"
    persistent
    @update:model-value="emit('update:modelValue', $event)" 
  >
    <v-card rounded="lg" class="movie-details-modal">

      <template v-if="movie">

        <!-- Header -->
        <div class="modal-header">
          <h2 class="text-h5 font-weight-regular">
            Movie Details
          </h2>

          <v-btn
            icon="mdi-close"
            variant="text"
            density="comfortable"
            color="grey-darken-1"
            aria-label="Close"
            @click="closeDialog"
          />
        </div>

        <v-divider />

        <!-- Movie Details -->
        <v-card-text class="modal-content">
          <div class="movie-details-layout">

            <!-- Movie Poster -->
            <div class="poster-container">
              <v-img
                v-if="movie.coverImage"
                :src="movie.coverImage"
                aspect-ratio="16/9"
                cover
                rounded="sm"
              />

              <div
                v-else
                class="poster-placeholder"
              >
                No Poster Available
              </div>
            </div>

            <!-- Movie Information -->
            <div class="movie-information">
              <!-- Name -->
              <h1 class="text-h4 font-weight-regular mb-2">
                {{ movie.name }}
              </h1>

              <!-- Year -->
              <p class="text-body-1 text-medium-emphasis mb-5">
                Release year: {{ movie.yearOfRelease }}
              </p>

              <!-- Producer -->
              <div class="detail-item">
                <strong>Producer:</strong>
                {{ movie.producer?.name || 'Unknown' }}
              </div>

              <!-- Genres array to string -->
              <div class="detail-item">
                <strong>Genre:</strong>

                {{
                  movie.genres.map(genre => genre.name).join(', ')
                  || 'None listed'
                }}
              </div>

              <!-- Actors array to string -->
              <div class="detail-item">
                <strong>Cast:</strong>

                {{
                  movie.actors.map(actor => actor.name).join(', ')
                  || 'None listed'
                }}
              </div>

              <!-- Plot para -->
              <div class="plot-section">
                <strong>Plot</strong>

                <p class="mt-1">
                  {{ movie.plot || 'No plot available.' }}
                </p>
              </div>

            </div>
          </div>
        </v-card-text>

        <!-- Footer -->
        <v-divider />

        <v-card-actions class="modal-footer">
          <v-spacer />

          <v-btn
            color="grey-darken-1"
            variant="flat"
            size="large"
            @click="closeDialog"
          >
            Close
          </v-btn>
        </v-card-actions>

      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.movie-details-modal {
  width: 100%;
  background: white;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 18px;
}

.modal-content {
  padding: 16px 18px;
}

.movie-details-layout {
  display: flex;
  align-items: flex-start;
  gap: 28px;
}

.poster-container {
  flex: 0 0 260px;
  width: 260px;
}

.poster-placeholder {
  width: 100%;
  aspect-ratio: 16 / 9;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eeeeee;
  color: #757575;
  border-radius: 4px;
}

.movie-information {
  flex: 1;
  min-width: 0;
  color: #30343a;
}

.movie-information h1 {
  font-size: 26px !important;
}

.detail-item {
  margin-bottom: 14px;
  font-size: 15px;
  line-height: 1.5;
}

.detail-item strong,
.plot-section strong {
  font-weight: 700;
}

.plot-section {
  font-size: 15px;
  line-height: 1.5;
}

.plot-section p {
  margin-bottom: 0;
}

.modal-footer {
  padding: 12px 18px;
  min-height: 68px;
}

@media (max-width: 650px) {
  .movie-details-layout {
    flex-direction: column;
    gap: 22px;
  }

  .poster-container {
    flex: auto;
    width: 100%;
  }

  .movie-information {
    width: 100%;
  }

  .movie-information h1 {
    font-size: 26px !important;
  }
}
</style>