<script> 
  import { computed } from 'vue'
  import { useWatchlistStore } from '../stores/watchlistStore'
  import { useItemsStore } from '../stores/itemsStore'
  const watchlistStore = useWatchlistStore()
  const itemsStore = useItemsStore()
  const watchedItems = computed(() => watchlistStore.getWatchedItems(itemsStore))
</script>
<template>
  <main class="app-shell">
    <h1>Watchlist</h1>
    <p>Save the products and assets you want to monitor here.</p>
  </main>
</template>
