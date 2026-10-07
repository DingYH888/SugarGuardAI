<template>
  <div class="dashboard">
    <h2>📊 健康仪表盘</h2>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header><span>血糖趋势（近7天）</span></template>
          <BloodSugarChart v-if="bloodStore.records.length" :records="bloodStore.records" />
          <el-empty v-else description="暂无血糖数据" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>健康评分</span></template>
          <HealthScore :score="healthScore" />
          <div class="score-tip">{{ scoreTip }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>血糖统计</span></template>
          <div v-if="bloodStore.stats" class="stat-item">
            <p>平均血糖：<strong>{{ bloodStore.stats.avg }}</strong> mmol/L</p>
            <p>达标率：<strong>{{ bloodStore.stats.time_in_range }}%</strong></p>
            <p>趋势：<el-tag size="small">{{ bloodStore.stats.trend }}</el-tag></p>
            <p>
              风险：<el-tag :type="riskTag" size="small">{{ bloodStore.stats.risk_level }}</el-tag>
            </p>
          </div>
          <el-empty v-else description="暂无统计" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>今日用药</span></template>
          <MedicationReminder v-for="med in medications" :key="med.id" :med="med" />
          <el-empty v-if="!medications.length" description="无用药记录" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>今日营养</span></template>
          <div v-if="dietStore.dailyNutrition" class="stat-item">
            <p>热量：<strong>{{ dietStore.dailyNutrition.total_calories }}</strong> kcal</p>
            <p>碳水：<strong>{{ dietStore.dailyNutrition.total_carbs }}</strong> g</p>
            <p>蛋白质：<strong>{{ dietStore.dailyNutrition.total_protein }}</strong> g</p>
            <p>平均GI：<strong>{{ dietStore.dailyNutrition.avg_gi }}</strong></p>
          </div>
          <el-empty v-else description="暂无饮食记录" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { usePatientStore } from '../stores/patient'
import { useBloodSugarStore } from '../stores/bloodSugar'
import { useDietStore } from '../stores/diet'
import { medicationApi } from '../api/medication'
import BloodSugarChart from '../components/BloodSugarChart.vue'
import HealthScore from '../components/HealthScore.vue'
import MedicationReminder from '../components/MedicationReminder.vue'
import type { Medication } from '../types'

const patientStore = usePatientStore()
const bloodStore = useBloodSugarStore()
const dietStore = useDietStore()
const medications = ref<Medication[]>([])

const healthScore = computed(() => {
  if (!bloodStore.stats) return 0
  const tir = bloodStore.stats.time_in_range
  if (tir >= 90) return 90
  if (tir >= 70) return 75
  if (tir >= 50) return 60
  return 40
})

const scoreTip = computed(() => {
  const s = healthScore.value
  if (s >= 80) return '血糖控制良好，继续保持！'
  if (s >= 60) return '血糖控制一般，注意饮食和用药。'
  return '血糖控制不理想，建议咨询医生。'
})

const riskTag = computed(() => {
  const r = bloodStore.stats?.risk_level
  if (r === '高风险') return 'danger'
  if (r === '中风险') return 'warning'
  return 'success'
})

async function loadAll() {
  const p = patientStore.currentPatient
  if (!p) return
  const pid = p.id
  await Promise.all([
    bloodStore.fetchRecords(pid),
    bloodStore.fetchStats(pid),
    dietStore.fetchDaily(pid),
    medicationApi.list(pid).then(({ data }) => {
      medications.value = data
    }),
  ])
}

onMounted(loadAll)
watch(
  () => patientStore.currentPatient?.id,
  () => {
    loadAll()
  },
)
</script>

<style scoped>
.dashboard h2 {
  margin-bottom: 20px;
  color: #303133;
}
.stat-item p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}
.score-tip {
  text-align: center;
  color: #909399;
  font-size: 13px;
  margin-top: 8px;
}
</style>
