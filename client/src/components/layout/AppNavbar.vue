<template>
  <v-app-bar
    color="white"
    height="64"
    elevation="0"
    class="navbar"
  >
   <v-container fluid class="navbar-container d-flex align-center h-100">
   
    <RouterLink to="/movies" class="logo-link">
      <img
        src="@/assets/images/logoi.png"
        alt="IMDB Movies"
        class="navbar-logo"
      />
    </RouterLink>

      <v-spacer />

      <!-- Navigation Links -->
      <nav class="d-flex align-center ga-6">
      <nav class="d-flex align-center ga-6">
        <RouterLink to="/movies" class="nav-link">
          Movies
        </RouterLink>

        <!-- <RouterLink to="/movies/create" class="nav-link">
          Add Movie
        </RouterLink> -->
      </nav>

      </nav>
    </v-container>
  </v-app-bar>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.navbar {
  border-bottom: 2px solid #eeeeee;
}
.navbar-container {
  /* max-width: 1180px; */
  max-width: 1600px;
  margin: 0 auto;
  padding-left: 32px;
  padding-right: 32px;
  width: 100%;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.navbar-logo {
  width: 40px;
  object-fit: contain;
}

.nav-link {
  color: #333333;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0;
  text-transform: none;
  min-width: auto;
  border-radius: 0;
}

.nav-link.router-link-active {
  border-bottom: 2px solid #333333;
}

.nav-link {
  color: #333333;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  padding: 2px 0;
}

.nav-link.router-link-exact-active {
  border-bottom: 2px solid #333333;
}


/* Mobile */
@media (max-width: 600px) {
  .navbar-container {
    padding-left: 8px;
    padding-right: 8px;
  }
}
</style>
