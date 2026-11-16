<template>
  <v-dialog
    :model-value="modelValue"
    max-width="500"
    persistent
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">
      <v-card-title>{{ dialogTitle }}</v-card-title>

      <!-- Wrap all input fields inside v-form -->
      <v-form ref="personForm" @submit.prevent="handleSave">
      <v-card-text class="pa-6">
        <div class="d-flex flex-column ga-4">

          <v-text-field
            v-model="form.name"
            label="Name"
            placeholder="Enter name"
            variant="outlined"
            :rules="[requiredRule]"
            autofocus
            hide-details="auto"
          />

          <v-textarea
            v-model="form.bio"
            label="Biography"
            placeholder="Enter biography"
            variant="outlined"
            rows="3"
            :rules="[requiredRule]"
            hide-details="auto"
          />

          <v-text-field
            v-model="form.dob"
            label="Date of Birth"
            type="date"
            variant="outlined"
            :rules="[dateRule]"
            hide-details="auto"
          />

          <v-select
            v-model="form.gender"
            label="Gender"
            :items="['Male', 'Female', 'Other']"
            variant="outlined"
            :rules="[requiredRule]"
            hide-details="auto"
          />
        </div>

          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mt-4"
          >
            {{ error }}
          </v-alert>
        </v-card-text>

        <v-card-actions class="px-6 pb-5 pt-2">
          <v-spacer />

          <v-btn
            variant="text"
            :disabled="saving"
            @click="closeDialog"
          >
            Cancel
          </v-btn>

          <v-btn
            color="primary"
            variant="flat"
            :loading="saving"
            :disabled="saving"
            type="submit"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import {
  useActorStore,
  useProducerStore,
} from '../../stores'
import type { PersonRequest } from '../../types'

// Props and emits
interface Props {
  modelValue: boolean
  type: 'actor' | 'producer'
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
  (event: 'saved', personId: number): void
}>()

// Stores
const actorStore = useActorStore()
const producerStore = useProducerStore()

// Form state
const form = ref<PersonRequest>({
  name: '',
  bio: '',
  dob: '',
  gender: '',
})

// UI state
const saving = ref(false)
const error = ref('')
const dialogTitle = ref('')
const personForm = ref()

// Validation rules
const requiredRule = (value: string) =>
  !!value?.trim() || 'This field is required.'

const dateRule = (value: string) =>
  !!value || 'Date of birth is required.'

// Reset form
function resetForm() {
  form.value = {
    name: '',
    bio: '',
    dob: '',
    gender: '',
  }

  error.value = ''
}

// Watchers
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
      resetForm()
    }
  }
)

// Dialog actions
function closeDialog() {
  if (saving.value) return

  emit('update:modelValue', false)
}

// Submit form
async function handleSave() {
  error.value = ''

  const { valid } = await personForm.value.validate()
  if (!valid) return

  const request: PersonRequest = {
    ...form.value,
    name: form.value.name.trim(),
    bio: form.value.bio.trim(),
  }

  saving.value = true

  try {
    let personId: number

    if (props.type === 'actor') {
      const response = await actorStore.addActor(request)
      personId = response.id
    } else {
      const response = await producerStore.addProducer(request)
      personId = response.id
    }

    emit('saved', personId)
    emit('update:modelValue', false)
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Failed to save person.'
  } finally {
    saving.value = false
  }
}
</script>
