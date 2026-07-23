<template>
  <div class="app-container">
    <Sidebar :class="{ open: isMenuOpen }" />
    <button
      v-if="isMenuOpen"
      class="menu-overlay"
      aria-label="Close navigation menu"
      @click="isMenuOpen = false"
    ></button>
    <button
      class="menu-toggle"
      type="button"
      :aria-expanded="isMenuOpen"
      aria-label="Toggle navigation menu"
      @click="isMenuOpen = !isMenuOpen"
    >
      <span></span><span></span><span></span>
    </button>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

const isMenuOpen = ref(false)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #F7F5F2;
  color: #2D2A3E;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  background: #F7F5F2;
  margin-left: 240px;
  min-height: 100vh;
}

.menu-toggle,
.menu-overlay {
  display: none;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .menu-toggle {
    display: grid;
    position: fixed;
    z-index: 110;
    top: 14px;
    left: 20px;
    width: 38px;
    height: 38px;
    place-content: center;
    gap: 5px;
    padding: 0;
    border: 1px solid #E5E2DD;
    border-radius: 8px;
    background: #FFFFFF;
    cursor: pointer;
  }

  .menu-toggle span {
    display: block;
    width: 18px;
    height: 2px;
    border-radius: 99px;
    background: #2D2A3E;
  }

  .menu-overlay {
    display: block;
    position: fixed;
    z-index: 90;
    inset: 0;
    border: 0;
    background: rgb(0 0 0 / 40%);
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 0;
  }
}
</style>
