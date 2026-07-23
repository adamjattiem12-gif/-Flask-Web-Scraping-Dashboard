<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ background: iconBg || '#5B8C5A' }">
      {{ icon }}
    </div>
    <div class="stat-content">
      <p class="stat-label">{{ label }}</p>
      <p class="stat-value">{{ value }}</p>
      <p v-if="subtitle" class="stat-subtitle">{{ subtitle }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, required: true },
  iconBg: { type: String, default: '#5B8C5A' },
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  subtitle: { type: String, default: '' }
})
</script>

<style scoped>
.stat-card {
  background: #FFFFFF;
  border: 1px solid #E5E2DD;
  border-radius: 12px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: box-shadow 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  color: #5C5A6B;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.stat-value {
  color: #2D2A3E;
  font-size: 26px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-subtitle {
  color: #9E9BB0;
  font-size: 13px;
  margin-top: 2px;
}

@media (max-width: 768px) {
  .stat-card {
    padding: 16px;
  }
  .stat-value {
    font-size: 20px;
  }
}
</style>
