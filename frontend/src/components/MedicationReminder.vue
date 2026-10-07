<template>
  <el-card shadow="hover" class="med-card">
    <div class="med-header">
      <el-icon :size="20" color="#409EFF"><FirstAidKit /></el-icon>
      <span class="drug-name">{{ med.drug_name }}</span>
      <el-tag :type="med.is_active ? 'success' : 'info'" size="small">
        {{ med.is_active ? '用药中' : '已停用' }}
      </el-tag>
    </div>
    <div class="med-detail">
      <p><strong>剂量：</strong>{{ med.dosage }}</p>
      <p><strong>频次：</strong>{{ med.frequency }}</p>
      <p><strong>时间：</strong>{{ med.timing }}</p>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { FirstAidKit } from '@element-plus/icons-vue'
import type { Medication } from '../types'

defineProps<{ med: Medication }>()
</script>

<style scoped>
.med-card {
  margin-bottom: 12px;
}
.med-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.drug-name {
  font-weight: bold;
  font-size: 16px;
  flex: 1;
}
.med-detail p {
  margin: 4px 0;
  color: #666;
  font-size: 14px;
}
</style>
