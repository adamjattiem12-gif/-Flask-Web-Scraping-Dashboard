<template>
  <div class="filter-panel">
    <div class="filter-panel__controls">
      <div class="filter-field">
        <label>Market</label>
        <select v-model="market" @change="emitFilters">
          <option value="">All markets</option>
          <option value="Retail Goods">Retail Goods</option>
          <option value="Digital Assets">Digital Assets</option>
        </select>
      </div>

      <div class="filter-field">
        <label>Min price</label>
        <input type="number" v-model.number="minPrice" placeholder="0" @change="emitFilters" />
      </div>

      <div class="filter-field">
        <label>Max price</label>
        <input type="number" v-model.number="maxPrice" placeholder="Any" @change="emitFilters" />
      </div>

      <button class="filter-panel__clear-all" v-if="activeTags.length" @click="clearAll">
        Clear all
      </button>
    </div>

    <!-- Removable filter tags -->
    <div class="filter-tags" v-if="activeTags.length">
      <span class="filter-tag" v-for="tag in activeTags" :key="tag.key">
        {{ tag.label }}
        <button @click="removeTag(tag.key)" aria-label="Remove filter">✕</button>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['change'])

const market = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)

const activeTags = computed(() => {
  const tags = []
  if (market.value) tags.push({ key: 'market', label: `Market: ${market.value}` })
  if (minPrice.value !== null && minPrice.value !== '') tags.push({ key: 'minPrice', label: `Min: $${minPrice.value}` })
  if (maxPrice.value !== null && maxPrice.value !== '') tags.push({ key: 'maxPrice', label: `Max: $${maxPrice.value}` })
  return tags
})

function emitFilters() {
  emit('change', {
    market: market.value || null,
    minPrice: minPrice.value === '' ? null : minPrice.value,
    maxPrice: maxPrice.value === '' ? null : maxPrice.value,
  })
}

function removeTag(key) {
  if (key === 'market') market.value = ''
  if (key === 'minPrice') minPrice.value = null
  if (key === 'maxPrice') maxPrice.value = null
  emitFilters()
}

function clearAll() {
  market.value = ''
  minPrice.value = null
  maxPrice.value = null
  emitFilters()
}
</script>

<style scoped>
.filter-panel {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 16px 20px;
}

.filter-panel__controls {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 16px;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-field label {
  font-size: 12px;
  color: #5C5A6B;
}

.filter-field select,
.filter-field input {
  border: 1px solid #E5E2DD;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 14px;
  color: #2D2A3E;
  min-width: 120px;
}

.filter-panel__clear-all {
  background: transparent;
  border: none;
  color: #C1666B;
  font-size: 13px;
  cursor: pointer;
  margin-left: auto;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #F7F5F2;
  border: 1px solid #E5E2DD;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  color: #2D2A3E;
}

.filter-tag button {
  border: none;
  background: transparent;
  color: #9E9BB0;
  cursor: pointer;
  font-size: 11px;
}

.filter-tag button:hover {
  color: #C1666B;
}
</style>
