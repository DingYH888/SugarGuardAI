<template>
  <div class="report-page">
    <h2>📝 健康报告</h2>
    <div style="margin-bottom: 20px">
      <el-button type="primary" @click="generate('周报')">生成周报</el-button>
      <el-button @click="generate('月报')">生成月报</el-button>
    </div>
    <el-card v-for="report in reports" :key="report.id" shadow="hover" style="margin-bottom: 16px">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>{{ report.report_type }} - {{ report.period_start }} ~ {{ report.period_end }}</span>
          <el-tag :type="riskTag(report.risk_level)">{{ report.risk_level || '未知' }}</el-tag>
        </div>
      </template>
      <div class="report-stats">
        <p>平均血糖：<strong>{{ report.avg_blood_sugar }} mmol/L</strong></p>
        <p>达标率：<strong>{{ report.time_in_range }}%</strong></p>
      </div>
      <el-divider />
      <div class="report-summary"><strong>摘要：</strong>{{ report.summary }}</div>
      <div v-if="report.recommendations" class="report-reco">
        <strong>建议：</strong>{{ report.recommendations }}
      </div>
    </el-card>
    <el-empty v-if="!reports.length" description="暂无健康报告" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePatientStore } from '../stores/patient'
import { reportApi } from '../api/reports'
import type { HealthReport } from '../types'
import { ElMessage } from 'element-plus'

const patientStore = usePatientStore()
const reports = ref<HealthReport[]>([])

function riskTag(level: string | null) {
  if (!level) return 'info'
  if (level.includes('高')) return 'danger'
  if (level.includes('中')) return 'warning'
  return 'success'
}

async function load() {
  if (!patientStore.currentPatient) return
  const { data } = await reportApi.list(patientStore.currentPatient.id)
  reports.value = data
}

async function generate(type: string) {
  if (!patientStore.currentPatient) return
  await reportApi.generate(patientStore.currentPatient.id, type)
  ElMessage.success('报告生成成功！')
  await load()
}

onMounted(load)
watch(
  () => patientStore.currentPatient?.id,
  () => load(),
)
</script>

<style scoped>
.report-page h2 {
  margin-bottom: 20px;
}
.report-stats p {
  margin: 4px 0;
}
.report-summary,
.report-reco {
  margin: 8px 0;
  line-height: 1.8;
}
</style>
