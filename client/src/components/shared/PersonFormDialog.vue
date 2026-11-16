
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAppStore } from '../../stores/store'
import type { PersonRequest } from '../../types/person'

interface Props {
  modelValue: boolean
  type: 'actor' | 'producer'
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
  (event: 'saved', personId: number): void
}>()

const store = useAppStore()

const name = ref('')
const bio = ref('')
const dob = ref('')
const gender = ref('')

const loading = ref(false)
const error = ref('')

const dialogTitle = ref('')

watch(
  () => props.type,
  (type) => {
    dialogTitle.value = type === 'actor' ? 'Add Actor' : 'Add Producer'
  },
  { immediate: true }
)

watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      name.value = ''
      bio.value = ''
      dob.value = ''
      gender.value = ''
      error.value = ''
    }
  }
)

function closeDialog() {
  if (loading.value) return

  emit('update:modelValue', false)
}

async function handleSave() {
  error.value = ''

  if (!name.value.trim()) {
    error.value = 'Name is required.'
    return
  }

  if (!bio.value.trim()) {
    error.value = 'Biography is required.'
    return
  }

  if (!dob.value) {
    error.value = 'Date of birth is required.'
    return
  }

  if (!gender.value) {
    error.value = 'Please select a gender.'
    return
  }

  const request: PersonRequest = {
    name: name.value.trim(),
    bio: bio.value.trim(),
    dob: dob.value,
    gender: gender.value,
  }

  loading.value = true

  try {
    let personId: number

    if (props.type === 'actor') {
      const response = await store.addActor(request)
      personId = response.id
    } else {
      const response = await store.addProducer(request)
      personId = response.id
    }

    emit('saved', personId)
    emit('update:modelValue', false)
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to save person.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-dialog
    :model-value="modelValue"
    max-width="500"
    :persistent="loading"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">
      <v-card-title>{{ dialogTitle }}</v-card-title>

      <v-card-text>
        <v-text-field
          v-model="name"
          label="Name"
          placeholder="Enter name"
          variant="outlined"
          :error-messages="error === 'Name is required.' ? error : []"
          autofocus
        />

        <v-textarea
          v-model="bio"
          label="Biography"
          placeholder="Enter biography"
          variant="outlined"
          rows="3"
        />

        <v-text-field
          v-model="dob"
          label="Date of Birth"
          type="date"
          variant="outlined"
        />

        <v-select
          v-model="gender"
          label="Gender"
          :items="['Male', 'Female', 'Other']"
          variant="outlined"
        />

        <v-alert
          v-if="error && error !== 'Name is required.'"
          type="error"
          variant="tonal"
          class="mt-2"
        >
          {{ error }}
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-spacer />

        <v-btn
          variant="text"
          :disabled="loading"
          @click="closeDialog"
        >
          Cancel
        </v-btn>

        <v-btn
          color="primary"
          variant="flat"
          :loading="loading"
          :disabled="loading"
          @click="handleSave"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
