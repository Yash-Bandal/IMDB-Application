<template>
  <v-app>
    <AppNavbar />

    <v-main>
      <v-container fluid class="pa-4 pa-md-0">
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppNavbar from './components/layout/AppNavbar.vue'
</script>
