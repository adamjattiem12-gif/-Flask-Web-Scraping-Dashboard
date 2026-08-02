<template>
  <div class="filter-panel">
    <div class="filter-controls">
      <div class="filter-field">
        <label for="source-select">Source</label>
        <select id="source-select" v-model="source" @change="emitFilters">
          <option value="">All sources</option>
          <option value="WebScraper.io E-Commerce">Retail (WebScraper.io)</option>
          <option value="CoinPaprika API">Crypto (CoinPaprika)</option>
        </select>
      </div>

      <div class="filter-field">
        <label for="min-price">Min price</label>
        <input
          id="min-price"
          type="number"
          v-model.number="minPrice"
          placeholder="0"
          min="0"
          @change="emitFilters"
        />
      </div>

      <div class="filter-field">
        <label for="max-price">Max price</label>
        <input
          id="max-price"
          type="number"
          v-model.number="maxPrice"
          placeholder="Any"
          min="0"
          @change="emitFilters"
        />
      </div>
    </div>

    <!-- Active filter tags -->
    <div v-if="activeTags.length" class="filter-tags">
      <span v-for="tag in activeTags" :key="tag.key" class="filter-tag">
        {{ tag.label }}
        <button type="button" class="tag-remove" @click="removeTag(tag.key)" aria-label="Remove filter">✕</button>
      </span>
      <button type="button" class="clear-all" @click="clearAll">Clear all</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['filter'])

const source = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)

const SOURCE_LABELS = {
  'WebScraper.io E-Commerce': 'Retail (WebScraper.io)',
  'CoinPaprika API': 'Crypto (CoinPaprika)'
}

const activeTags = computed(() => {
  const tags = []
  if (source.value) {
    tags.push({ key: 'source', label: `Source: ${SOURCE_LABELS[source.value] || source.value}` })
  }
  if (minPrice.value !== null && minPrice.value !== '') {
    tags.push({ key: 'minPrice', label: `Min: ${minPrice.value}` })
  }
  if (maxPrice.value !== null && maxPrice.value !== '') {
    tags.push({ key: 'maxPrice', label: `Max: ${maxPrice.value}` })
  }
  return tags
})

const emitFilters = () => {
  emit('filter', {
    source: source.value || null,
    minPrice: minPrice.value !== '' ? minPrice.value : null,
    maxPrice: maxPrice.value !== '' ? maxPrice.value : null,
  })
}

const removeTag = (key) => {
  if (key === 'source') source.value = ''
  if (key === 'minPrice') minPrice.value = null
  if (key === 'maxPrice') maxPrice.value = null
  emitFilters()
}

const clearAll = () => {
  source.value = ''
  minPrice.value = null
  maxPrice.value = null
  emitFilters()
}
</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.filter-controls {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-field label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.filter-field select,
.filter-field input {
  padding: 8px 10px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 14px;
  color: var(--color-text);
  background: var(--color-surface);
  min-width: 110px;
}

.filter-field select:focus,
.filter-field input:focus {
  outline: none;
  border-color: var(--color-success);
}

.filter-tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 8px;
  border-top: 1px solid var(--color-border-subtle);
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background: var(--color-success-bg);
  color: var(--color-success-strong);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
}

.tag-remove {
  border: none;
  background: transparent;
  cursor: pointer;
  color: var(--color-success-strong);
  font-size: 11px;
  padding: 0;
  line-height: 1;
}

.tag-remove:hover {
  color: var(--color-danger);
}

.clear-all {
  border: none;
  background: transparent;
  cursor: pointer;
  color: var(--color-info);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 6px;
}

.clear-all:hover {
  text-decoration: underline;
}
</style>
