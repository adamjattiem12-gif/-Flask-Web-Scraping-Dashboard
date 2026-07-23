<template>
  <div class="stat-card">
    <div class="stat-icon">{{ icon }}</div>
    <div class="stat-content">
      <div class="stat-label">{{ label }}</div>
      <div class="stat-value">{{ value }}</div>
      <div class="stat-sub">{{ sub }}</div>
    </div>
  </div>
</template>

<script setup>

defineProps({
  icon: String,
  label: String,
  value: [String, Number],
  sub: String
})
</script>

<style scoped>
.stat-card {
  background: white;
  border: 1px solid #E5E2DD;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 28px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #5C5A6B;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2D2A3E;
}

.stat-sub {
  font-size: 12px;
  color: #9E9BB0;
}
</style>
