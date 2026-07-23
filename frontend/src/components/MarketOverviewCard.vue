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
      <div v-for="item in recentItems" :key="item.name" class="activity-item">
        <span class="activity-name">{{ item.name }}</span>
        <span class="activity-change" :class="item.change >= 0 ? 'positive' : 'negative'">
          {{ item.change >= 0 ? '+' : '' }}{{ item.change }}%
        </span>
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
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 24px;
  border-top: 4px solid #D4914A;
}

.market-title {
  color: #2D2A3E;
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
  border-bottom: 1px solid #F0EDEA;
}

.price-block {
  display: flex;
  flex-direction: column;
}

.price-label {
  color: #9E9BB0;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.price-value {
  color: #2D2A3E;
  font-size: 22px;
  font-weight: 700;
  margin-top: 2px;
}

.activity-label {
  color: #9E9BB0;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin-bottom: 12px;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid #F7F5F2;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-name {
  color: #5C5A6B;
  font-size: 14px;
  font-weight: 500;
}

.activity-change {
  font-size: 14px;
  font-weight: 600;
}

.activity-change.positive {
  color: #5B8C5A;
}

.activity-change.negative {
  color: #C1666B;
}

@media (max-width: 768px) {
  .market-card {
    padding: 16px;
  }
}
</style>
