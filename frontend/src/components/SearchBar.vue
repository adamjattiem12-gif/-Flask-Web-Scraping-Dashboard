<template>
  <div class="search-bar">
    <span class="search-icon">🔍</span>
    <input
      type="text"
      class="search-input"
      v-model="query"
      placeholder="Search by name..."
      @input="onInput"
    />
    <button
      v-if="query"
      class="clear-btn"
      type="button"
      @click="clearSearch"
      aria-label="Clear search"
    >
      ✕
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])

const query = ref('')
let debounceTimer = null
const DEBOUNCE_MS = 300

const onInput = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('search', query.value.trim())
  }, DEBOUNCE_MS)
}

const clearSearch = () => {
  clearTimeout(debounceTimer)
  query.value = ''
  emit('search', '')
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  max-width: 400px;
  padding: 10px 14px;
  background: white;
  border: 1px solid #E0DEEB;
  border-radius: 6px;
  transition: border-color 0.2s ease;
}

.search-bar:focus-within {
  border-color: #5B8C5A;
}

.search-icon {
  font-size: 14px;
  opacity: 0.6;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #333;
  background: transparent;
}

.search-input::placeholder {
  color: #9E9BB0;
}

.clear-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  color: #9E9BB0;
  font-size: 13px;
  padding: 2px 4px;
  line-height: 1;
}

.clear-btn:hover {
  color: #C1666B;
}
</style>
