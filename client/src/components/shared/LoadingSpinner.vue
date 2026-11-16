<template>
  <div class="loading-spinner">
    <div class="spinner"></div>
  </div>
</template>

<style scoped>
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border-bottom: 3px solid #2563eb;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>