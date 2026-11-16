<template>
  <v-app>
    <!-- Authentication in progress -->
    <v-main v-if="authStatus.isLoading">
      <v-container class="fill-height d-flex align-center justify-center">
        <div class="text-center">
          <LoadingSpinner/>
          <p class="mt-4">Authenticating...</p>
        </div>
      </v-container>
    </v-main>

    <!-- Authentication failed -->
    <v-main v-else-if="authStatus.error">
      <v-container class="fill-height d-flex align-center justify-center">
        <v-card max-width="450" width="100%" class="pa-6">
          <v-icon color="error" size="40">
            mdi-alert-circle-outline
          </v-icon>

          <h2 class="mt-3">Authentication Failed</h2>

          <p class="mt-2 text-medium-emphasis">
            {{ authStatus.error }}
          </p>

          <v-btn
            color="primary"
            class="mt-5"
            block
            :loading="authStatus.isLoading"
            @click="initializeAuth"
          >
            Retry
          </v-btn>
        </v-card>
      </v-container>
    </v-main>

    <!-- Application content -->
    <template v-else>
      <AppNavbar />

      <v-main>
        <v-container fluid class="pa-4 pa-md-0">
          <RouterView />
        </v-container>
      </v-main>
    </template>
  </v-app>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppNavbar from './components/layout/AppNavbar.vue'
import LoadingSpinner from './components/shared/LoadingSpinner.vue';

import {authStatus, initializeAuth,} from './services/modules/authService'
</script>