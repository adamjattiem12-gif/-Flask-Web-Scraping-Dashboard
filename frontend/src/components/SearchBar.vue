<template>
  <div class="search-bar">
    <span class="search-bar__icon"></span>
    <input
      class="search-bar__input"
      type="text"
      v-model="query"
      :placeholder="placeholder"
      @input="onInput"
    />
    <button v-if="query" class="search-bar__clear" @click="clear" aria-label="Clear search">✕</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  placeholder: { type: String, default: 'Search items…' },
  debounceMs: { type: Number, default: 300 },
})

const emit = defineEmits(['search'])

const query = ref('')
let debounceTimer = null

function onInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('search', query.value.trim())
  }, props.debounceMs)
}

function clear() {
  query.value = ''
  clearTimeout(debounceTimer)
  emit('search', '')
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 10px 14px;
}

.search-bar__icon {
  font-size: 14px;
  opacity: 0.6;
}

.search-bar__input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #2D2A3E;
  background: transparent;
}

.search-bar__input::placeholder {
  color: #9E9BB0;
}

.search-bar__clear {
  border: none;
  background: transparent;
  color: #9E9BB0;
  cursor: pointer;
  font-size: 13px;
}

.search-bar__clear:hover {
  color: #C1666B;
}
</style>
