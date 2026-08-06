<template>
  <div class="market-card" :style="{ borderTopColor: accentColor }">
    <h3 class="market-title">{{ title }}</h3>
    
    <div class="market-price-row">
      <div class="price-block">
        <span class="price-label">AVG PRICE</span>
        <span class="price-value">${{ avgPrice.toFixed(2) }}</span>
      </div>
      <div class="price-block">
        <span class="price-label">ITEMS</span>
        <span class="price-value">{{ itemsCount }}</span>
      </div>
    </div>

    <div class="market-activity">
      <p class="activity-label">RECENT ACTIVITY</p>
      <div v-if="recentItems && recentItems.length > 0">
        <div v-for="item in recentItems" :key="item.name" class="activity-item">
          <span class="activity-name">{{ item.name }}</span>
          <!-- ✅ Show percentage for Digital Assets -->
          <span v-if="item.change !== null && item.change !== undefined" class="activity-change" :class="item.change >= 0 ? 'positive' : 'negative'">
            {{ item.change >= 0 ? '+' : '' }}{{ Number(item.change).toFixed(1) }}%
          </span>
          <!-- ✅ Show price for Retail Goods -->
          <span v-else-if="item.price !== null && item.price !== undefined" class="activity-price">
            ${{ Number(item.price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
          </span>
        </div>
      </div>
      <div v-else class="activity-empty">
        <span>No recent activity</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  accentColor: { type: String, default: '#D4914A' },
  avgPrice: { type: Number, required: true },
  itemsCount: { type: Number, default: 0 },
  recentItems: { type: Array, default: () => [] }
})
</script>

<style scoped>
.market-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  border-top: 4px solid var(--color-warning);
}

.market-title {
  color: var(--color-text);
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}

.market-price-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border-subtle);
}

.price-block {
  display: flex;
  flex-direction: column;
}

.price-label {
  color: var(--color-text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.price-value {
  color: var(--color-text);
  font-size: 22px;
  font-weight: 700;
  margin-top: 2px;
}

.activity-label {
  color: var(--color-text-muted);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin-bottom: 12px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid var(--color-bg);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-name {
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.activity-change {
  font-size: 14px;
  font-weight: 600;
}

.activity-change.positive {
  color: var(--color-success);
}

.activity-change.negative {
  color: var(--color-danger);
}

.activity-price {
  color: var(--color-text);
  font-size: 14px;
  font-weight: 600;
}

.activity-empty {
  color: var(--color-text-muted);
  font-size: 14px;
  padding: 6px 0;
}

@media (max-width: 768px) {
  .market-card {
    padding: 16px;
  }
}
</style>