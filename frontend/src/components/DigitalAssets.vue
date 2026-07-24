<script> 
  import { computed } from 'vue'
  import { useItemsStore } from '../stores/itemsStore'
  const itemsStore = useItemsStore()
  const cryptoItems = computed(() => itemsStore.getCryptoItems)
</script>
<template>
  <main class="app-shell">
    <h1>Digital Assets</h1>
    <p>Track digital-asset prices and market movements here.</p>
  </main>
</template>
