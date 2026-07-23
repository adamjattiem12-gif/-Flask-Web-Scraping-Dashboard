<template>
  <div class="market-card">
    <h3>{{ title }}</h3>
    <div class="market-stats">
      <p>{{ itemCount }} items</p>
      <p>Avg Price: ${{ avgPrice.toFixed(2) }}</p>
      <p class="last-updated">Last: 2 min ago</p>
    </div>
    <div class="market-sources">
      <span class="source-badge" :class="market">
        {{ market === 'retail' ? '🟧' : '🟦' }} {{ source }} - {{ sourceItems }} items
      </span>
    </div>
  </div>
</template>

<script setup>
/**
 * MarketOverviewCard - Displays market summary for Retail or Digital Assets
 * 
 * Props:
 *   - title: '🛒 Retail Goods' or '₿ Digital Assets'
 *   - itemCount: number of items in this market
 *   - avgPrice: average price in this market
 *   - source: website name (e.g., 'WebScraper.io')
 *   - sourceItems: number of items from this source
 *   - market: 'retail' or 'crypto' (determines badge color)
 * 
 * Used by: Dashboard.vue
 */
defineProps({
  title: String,
  itemCount: Number,
  avgPrice: Number,
  source: String,
  sourceItems: String,
  market: String // 'retail' or 'crypto'
})
</script>

<style scoped>
.market-card {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 24px;
}

.market-card h3 {
  color: #2D2A3E;
  margin-top: 0;
  margin-bottom: 12px;
}

.market-stats p {
  color: #5C5A6B;
  margin: 4px 0;
}

.last-updated {
  color: #9E9BB0;
  font-size: 13px;
}

.market-sources {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #F7F5F2;
}

.source-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
}

.source-badge.retail {
  background: #FFF0E6;
  color: #D4914A;
}

.source-badge.crypto {
  background: #E6F4F4;
  color: #4A8C8C;
}
</style>
