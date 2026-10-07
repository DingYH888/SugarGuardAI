<template>
  <div class="diet-page">
    <h2>🍽️ 饮食管理</h2>
    <el-row :gutter="16">
      <el-col :span="14">
        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header><span>{{ editId ? '编辑饮食记录' : '记录饮食' }}</span></template>
          <el-form :model="form" label-position="top" ref="formRef">
            <el-form-item label="食物名称" required>
              <el-input v-model="form.food_name" placeholder="例如：米饭、苹果" />
            </el-form-item>
            <el-form-item label="餐别" required>
              <el-select v-model="form.meal_type" style="width: 100%" placeholder="请选择">
                <el-option label="早餐" value="早餐" />
                <el-option label="午餐" value="午餐" />
                <el-option label="晚餐" value="晚餐" />
                <el-option label="加餐" value="加餐" />
              </el-select>
            </el-form-item>
            <el-form-item label="摄入时间" required>
              <el-date-picker
                v-model="form.eaten_at"
                type="datetime"
                placeholder="选择日期时间"
                style="width: 100%"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
              />
            </el-form-item>
            <el-row :gutter="8">
              <el-col :span="8">
                <el-form-item label="热量(kcal)">
                  <el-input-number v-model="form.calories" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="碳水(g)">
                  <el-input-number v-model="form.carbs" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="蛋白质(g)">
                  <el-input-number v-model="form.protein" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="8">
              <el-col :span="8">
                <el-form-item label="脂肪(g)">
                  <el-input-number v-model="form.fat" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="GI值">
                  <el-input-number v-model="form.gi_value" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="份量">
                  <el-input-number v-model="form.portion" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item>
              <div style="display: flex; gap: 8px">
                <el-button type="primary" style="flex: 1" @click="submit" :loading="submitting">
                  {{ editId ? '保存修改' : '保存记录' }}
                </el-button>
                <el-button v-if="editId" style="flex: 1" @click="cancelEdit">
                  取消编辑
                </el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="hover">
          <template #header><span>饮食记录</span></template>
          <el-table :data="dietStore.records" size="default" style="font-size: 14px">
            <el-table-column prop="food_name" label="食物" min-width="100" show-overflow-tooltip />
            <el-table-column prop="meal_type" label="餐别" width="60" align="center" />
            <el-table-column prop="calories" label="kcal" width="70" align="center" />
            <el-table-column prop="carbs" label="碳(g)" width="70" align="center" />
            <el-table-column prop="protein" label="蛋(g)" width="70" align="center" />
            <el-table-column prop="fat" label="脂(g)" width="70" align="center" />
            <el-table-column prop="gi_value" label="GI" width="60" align="center" />
            <el-table-column label="操作" min-width="130" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="primary" @click="editRecord(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="removeRecord(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 8px; text-align: right">
            <el-button size="small" @click="loadRecords">刷新</el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="10">
        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center">
              <span>今日推荐食谱</span>
              <el-radio-group v-model="mealType" size="small" @change="loadRecommend">
                <el-radio-button value="早餐">早餐</el-radio-button>
                <el-radio-button value="午餐">午餐</el-radio-button>
                <el-radio-button value="晚餐">晚餐</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <DietCard v-for="item in dietStore.recommendations" :key="String(item.name || item.food_name)" :item="item" />
        </el-card>

        <el-card shadow="hover">
          <template #header>
            <span>今日营养摄入</span>
            <el-tag size="small" style="margin-left: 8px">{{ dietStore.dailyNutrition?.meal_count || 0 }}餐</el-tag>
          </template>
          <div v-if="dietStore.dailyNutrition">
            <el-row :gutter="12" class="nutrition-summary">
              <el-col :span="12">
                <div class="stat-item">
                  <span class="stat-label">热量</span>
                  <span class="stat-value">{{ dietStore.dailyNutrition.total_calories }} kcal</span>
                  <span class="stat-status">{{ dietStore.dailyNutrition.calorie_status }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="stat-item">
                  <span class="stat-label">碳水</span>
                  <span class="stat-value">{{ dietStore.dailyNutrition.total_carbs }}g</span>
                  <span class="stat-status">{{ dietStore.dailyNutrition.carb_status }}</span>
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="12" class="nutrition-summary">
              <el-col :span="8">
                <div class="stat-item small">
                  <span class="stat-label">蛋白质</span>
                  <span class="stat-value">{{ dietStore.dailyNutrition.total_protein }}g</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item small">
                  <span class="stat-label">脂肪</span>
                  <span class="stat-value">{{ dietStore.dailyNutrition.total_fat }}g</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item small">
                  <span class="stat-label">平均GI</span>
                  <span class="stat-value">{{ dietStore.dailyNutrition.avg_gi }}</span>
                </div>
              </el-col>
            </el-row>

            <el-divider v-if="dietStore.dailyNutrition.records?.length" />
            
            <div v-if="dietStore.dailyNutrition.records?.length" class="record-list">
              <div class="record-list-title">今日食物记录</div>
              <div v-for="(record, index) in dietStore.dailyNutrition.records" :key="index" class="record-item">
                <div class="record-info">
                  <el-tag size="small" type="info">{{ record.meal }}</el-tag>
                  <span class="record-name">{{ record.name }}</span>
                </div>
                <span class="record-calories">{{ record.calories }} kcal</span>
              </div>
            </div>
            <el-empty v-else description="今日暂无饮食记录" :image-size="60" />
          </div>
          <el-skeleton v-else animated />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { usePatientStore } from '../stores/patient'
import { useDietStore } from '../stores/diet'
import { dietApi } from '../api/diet'
import DietCard from '../components/DietCard.vue'
import { ElMessage, FormInstance } from 'element-plus'
import { formatDateTime } from '../utils/date'
import type { DietRecord } from '../types'

const patientStore = usePatientStore()
const dietStore = useDietStore()
const mealType = ref('早餐')
const formRef = ref<FormInstance>()
const editId = ref<number | null>(null)
const submitting = ref(false)

const form = ref({
  food_name: '',
  meal_type: '早餐',
  eaten_at: '',
  calories: null as number | null,
  portion: null as number | null,
  carbs: null as number | null,
  protein: null as number | null,
  fat: null as number | null,
  gi_value: null as number | null,
})

async function loadPage() {
  if (!patientStore.currentPatient) return
  const pid = patientStore.currentPatient.id
  await Promise.all([dietStore.fetchDaily(pid), dietStore.fetchRecords(pid), dietStore.fetchRecommend(mealType.value, pid)])
}

async function loadRecommend() {
  if (!patientStore.currentPatient) return
  await dietStore.fetchRecommend(mealType.value, patientStore.currentPatient.id)
}

async function loadRecords() {
  if (!patientStore.currentPatient) return
  await dietStore.fetchRecords(patientStore.currentPatient.id)
}

function editRecord(row: DietRecord) {
  editId.value = row.id
  form.value = {
    food_name: row.food_name,
    meal_type: row.meal_type || '早餐',
    eaten_at: row.eaten_at,
    calories: row.calories,
    portion: row.portion,
    carbs: row.carbs,
    protein: row.protein,
    fat: row.fat,
    gi_value: row.gi_value,
  }
}

function cancelEdit() {
  editId.value = null
  form.value = {
    food_name: '',
    meal_type: '早餐',
    eaten_at: '',
    calories: null,
    portion: null,
    carbs: null,
    protein: null,
    fat: null,
    gi_value: null,
  }
}

async function submit() {
  if (!patientStore.currentPatient) {
    ElMessage.warning('请先选择患者')
    return
  }
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  submitting.value = true
  try {
    const payload = {
      food_name: form.value.food_name,
      meal_type: form.value.meal_type,
      eaten_at: form.value.eaten_at,
      calories: form.value.calories,
      portion: form.value.portion,
      carbs: form.value.carbs,
      protein: form.value.protein,
      fat: form.value.fat,
      gi_value: form.value.gi_value,
      note: null,
    }
    if (editId.value) {
      await dietApi.update(editId.value, payload)
      ElMessage.success('饮食记录已更新')
    } else {
      await dietApi.create({ patient_id: patientStore.currentPatient.id, ...payload })
      ElMessage.success('饮食记录已保存')
    }
    cancelEdit()
    await loadPage()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '保存失败')
  } finally {
    submitting.value = false
  }
}

async function removeRecord(id: number) {
  try {
    await dietApi.remove(id)
    ElMessage.success('删除成功')
    await loadPage()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '删除失败')
  }
}

onMounted(loadPage)
watch(
  () => patientStore.currentPatient?.id,
  () => loadPage(),
)
</script>

<style scoped>
.diet-page h2 {
  margin-bottom: 20px;
}
.nutrition-summary {
  margin-bottom: 12px;
}
.stat-item {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}
.stat-item.small {
  padding: 8px;
}
.stat-label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}
.stat-value {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}
.stat-item.small .stat-value {
  font-size: 14px;
}
.stat-status {
  display: block;
  font-size: 11px;
  color: #67c23a;
  margin-top: 2px;
}
.record-list {
  margin-top: 12px;
}
.record-list-title {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}
.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #f0f0f0;
}
.record-item:last-child {
  border-bottom: none;
}
.record-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
.record-name {
  font-size: 13px;
  color: #303133;
}
.record-calories {
  font-size: 12px;
  color: #909399;
}
</style>
