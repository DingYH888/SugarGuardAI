<template>
  <el-card shadow="hover" class="diet-card">
    <div class="food-info">
      <span class="food-name">{{ item.name || item.food_name }}</span>
      <el-tag :type="giTagType" size="small">GI: {{ item.gi_value ?? item.gi }}</el-tag>
    </div>
    <div class="nutrition">
      <span>{{ item.calories }} kcal</span>
      <span>碳水 {{ item.carbs }}g</span>
      <span v-if="item.protein != null">蛋白 {{ item.protein }}g</span>
    </div>
    <div class="tip" v-if="item.tip">{{ item.tip }}</div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ item: Record<string, unknown> }>()
const giTagType = computed(() => {
  const gi = Number(props.item.gi_value ?? props.item.gi ?? 0)
  if (gi <= 55) return 'success'
  if (gi <= 70) return 'warning'
  return 'danger'
})
</script>

<style scoped>
.diet-card {
  margin-bottom: 12px;
}
.food-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.food-name {
  font-weight: bold;
  font-size: 16px;
}
.nutrition {
  display: flex;
  gap: 16px;
  color: #666;
  font-size: 13px;
}
.tip {
  margin-top: 8px;
  color: #909399;
  font-size: 12px;
}
</style>
