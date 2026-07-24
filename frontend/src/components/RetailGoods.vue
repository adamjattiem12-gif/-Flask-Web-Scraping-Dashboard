<script>
  import { computed } from 'vue'
import { useItemsStore } from '../stores/itemsStore'
const itemsStore = useItemsStore()
const retailItems = computed(() => itemsStore.getRetailItems)
</script>

<template>
  <main class="app-shell">
    <h1>Retail Goods</h1>
    <p>Track prices, availability, and changes for your retail sources here.</p>
  </main>
</template>
