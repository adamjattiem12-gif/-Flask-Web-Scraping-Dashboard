<template>
  <div style="background:#FFFFFF; border:1px solid #E5E2DD; border-radius:8px; padding:16px 20px;">

    <div style="display:flex; flex-wrap:wrap; align-items:flex-end; gap:16px;">
      <div style="display:flex; flex-direction:column; gap:4px;">
        <label style="font-size:12px; color:#5C5A6B;">Market</label>
        <select
          v-model="market"
          @change="emitFilters"
          style="border:1px solid #E5E2DD; border-radius:6px; padding:6px 10px; font-size:14px; color:#2D2A3E; min-width:120px;"
        >
          <option value="">All markets</option>
          <option value="Retail Goods">Retail Goods</option>
          <option value="Digital Assets">Digital Assets</option>
        </select>
      </div>

      <div style="display:flex; flex-direction:column; gap:4px;">
        <label style="font-size:12px; color:#5C5A6B;">Min price</label>
        <input
          type="number"
          v-model.number="minPrice"
          placeholder="0"
          @change="emitFilters"
          style="border:1px solid #E5E2DD; border-radius:6px; padding:6px 10px; font-size:14px; color:#2D2A3E; min-width:120px;"
        />
      </div>

      <div style="display:flex; flex-direction:column; gap:4px;">
        <label style="font-size:12px; color:#5C5A6B;">Max price</label>
        <input
          type="number"
          v-model.number="maxPrice"
          placeholder="Any"
          @change="emitFilters"
          style="border:1px solid #E5E2DD; border-radius:6px; padding:6px 10px; font-size:14px; color:#2D2A3E; min-width:120px;"
        />
      </div>

      <button
        v-if="activeTags.length"
        @click="clearAll"
        style="background:transparent; border:none; color:#C1666B; font-size:13px; cursor:pointer; margin-left:auto;"
      >Clear all</button>
    </div>

    <!-- Removable filter tags -->
    <div v-if="activeTags.length" style="display:flex; flex-wrap:wrap; gap:8px; margin-top:14px;">
      <span
        v-for="tag in activeTags"
        :key="tag.key"
        style="display:inline-flex; align-items:center; gap:6px; background:#F7F5F2; border:1px solid #E5E2DD; border-radius:999px; padding:4px 10px; font-size:12px; color:#2D2A3E;"
      >
        {{ tag.label }}
        <button
          @click="removeTag(tag.key)"
          aria-label="Remove filter"
          style="border:none; background:transparent; color:#9E9BB0; cursor:pointer; font-size:11px;"
          onmouseover="this.style.color='#C1666B'"
          onmouseout="this.style.color='#9E9BB0'"
        >✕</button>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['change'])

// --- All FilterPanel logic lives here, inline ---

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
