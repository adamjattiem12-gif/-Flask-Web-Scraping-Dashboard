<template>
  <div class="page-layout">
    <header v-if="title" class="page-header">
      <h1>{{ title }}</h1>
      <div class="header-actions">
        <slot name="header-actions"></slot>
      </div>
    </header>
    <div class="page-content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.page-layout {
  min-height: 100vh;
  background: #F7F5F2;
}

.page-header {
  min-height: 82px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;
  padding: 20px 40px;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E2DD;
  gap: 16px;
}

.page-content {
  width: 100%;
  padding: 32px 40px 32px 0;
}

.page-header h1 {
  margin: 0;
  color: #2D2A3E;
  font-size: 28px;
  font-weight: 600;
}

.header-actions {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    min-height: 66px;
    padding: 14px 20px;
    flex-wrap: nowrap;
  }

  .page-content {
    padding: 24px 20px;
  }

  .page-header h1 {
    font-size: 24px;
  }
  
  .header-actions {
    flex-wrap: wrap;
  }
}

@media (max-width: 375px) {
  .page-header h1 {
    font-size: 20px;
  }
}
</style>
