<template>
  <div class="loading-container">
    <div class="loading-content">
      <p class="loading-text">
        Loading Movies
      </p>

      <div class="loading-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  background-color: white;
  transition: background-color 300ms;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
}

.loading-text {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: 0.1em;
  color: #475569;
  margin: 0;
}

.loading-dots {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #64748b;
  animation: calmPulse 1.5s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.25s;
}

.dot:nth-child(3) {
  animation-delay: 0.5s;
}

@keyframes calmPulse {
  0%, 80%, 100% {
    transform: scale(0.75);
    opacity: 0.35;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Dark mode */
:global(.v-theme--dark) .loading-container {
  background-color: #020617;
}

:global(.v-theme--dark) .loading-text {
  color: #cbd5e1;
}

:global(.v-theme--dark) .dot {
  background-color: #94a3b8;
}

/* Smaller screens */
@media (max-width: 600px) {
  .loading-text {
    font-size: 20px;
  }
}
</style>
