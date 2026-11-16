<script setup lang="ts">
interface Props {
  modelValue: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  loading: false,
})

const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
  (event: 'confirm'): void
}>()

function closeDialog() {
  if (emit) {
    emit('update:modelValue', false)
  }
}
</script>

<template>
  <v-dialog
    :model-value="modelValue"
    max-width="450"
    :persistent="loading"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">
      <v-card-title class="text-h6">
        {{ title }}
      </v-card-title>

      <v-card-text>
        {{ message }}
      </v-card-text>

      <v-card-actions>
        <v-spacer />

        <v-btn
          variant="text"
          :disabled="loading"
          @click="closeDialog"
        >
          {{ cancelText }}
        </v-btn>

        <v-btn
          color="error"
          variant="flat"
          :loading="loading"
          :disabled="loading"
          @click="emit('confirm')"
        >
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
