<template>
  <div class="exercise-page">
    <h2>🏃 运动管理</h2>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="hover" body-style="padding: 0">
          <template #header><span>运动记录</span></template>
          <el-table :data="records" stripe size="default" style="width: 100%; font-size: 14px">
            <el-table-column prop="exercise_type" label="运动类型" min-width="80" />
            <el-table-column prop="duration_min" label="时长(分钟)" min-width="90" align="center" />
            <el-table-column prop="intensity" label="强度" min-width="70" align="center" />
            <el-table-column prop="calories_burned" label="消耗(kcal)" min-width="90" align="center" />
            <el-table-column label="血糖变化" min-width="130" align="center">
              <template #default="{ row }">
                <span v-if="row.blood_sugar_before != null" style="font-size: 12px">
                  {{ row.blood_sugar_before }}→{{ row.blood_sugar_after }}
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column label="时间" min-width="150" align="center">
              <template #default="{ row }">{{ formatShortDateTime(row.performed_at) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="110" fixed="right" align="center">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="openEdit(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click="confirmDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!records.length" description="暂无运动记录" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>{{ editForm ? '编辑运动' : '记录运动' }}</span></template>
          <el-form :model="form" label-position="top">
            <el-form-item label="运动类型">
              <el-select v-model="form.exercise_type" style="width: 100%">
                <el-option label="快走" value="快走" />
                <el-option label="慢跑" value="慢跑" />
                <el-option label="游泳" value="游泳" />
                <el-option label="骑自行车" value="骑自行车" />
                <el-option label="瑜伽" value="瑜伽" />
                <el-option label="太极拳" value="太极拳" />
              </el-select>
            </el-form-item>
            <el-form-item label="时长(分钟)">
              <el-input-number v-model="form.duration_min" :min="5" :max="180" style="width: 100%" />
            </el-form-item>
            <el-form-item label="强度">
              <el-select v-model="form.intensity" style="width: 100%">
                <el-option label="低" value="低" />
                <el-option label="中等" value="中等" />
                <el-option label="高" value="高" />
              </el-select>
            </el-form-item>
            <el-form-item label="运动时间">
              <el-date-picker v-model="form.performed_at" type="datetime" style="width: 100%" />
            </el-form-item>
            <el-form-item label="消耗(kcal)">
              <el-input-number v-model="form.calories_burned" :min="0" :step="10" style="width: 100%" />
            </el-form-item>
            <el-form-item label="运动前血糖">
              <el-input-number v-model="form.blood_sugar_before" :min="1" :max="33" :step="0.1" style="width: 100%" />
            </el-form-item>
            <el-form-item label="运动后血糖">
              <el-input-number v-model="form.blood_sugar_after" :min="1" :max="33" :step="0.1" style="width: 100%" />
            </el-form-item>
            <el-form-item label="备注">
              <el-input v-model="form.note" type="textarea" />
            </el-form-item>
            <el-form-item>
              <div style="display: flex; gap: 8px">
                <el-button type="primary" style="flex: 1" @click="submit" :loading="submitting">
                  {{ editForm ? '保存修改' : '记录' }}
                </el-button>
                <el-button v-if="editForm" style="flex: 1" @click="resetForm">取消编辑</el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { usePatientStore } from '../stores/patient'
import { exerciseApi } from '../api/exercise'
import { formatShortDateTime } from '../utils/date'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Exercise } from '../types'

const patientStore = usePatientStore()
const records = ref<Exercise[]>([])
const submitting = ref(false)
const editForm = ref<Exercise | null>(null)

const defaultForm = () => ({
  exercise_type: '快走',
  duration_min: 30,
  intensity: '中等',
  calories_burned: undefined as number | undefined,
  performed_at: new Date() as Date,
  blood_sugar_before: undefined as number | undefined,
  blood_sugar_after: undefined as number | undefined,
  note: undefined as string | undefined,
})

const form = reactive(defaultForm())

async function load() {
  if (!patientStore.currentPatient) return
  const { data } = await exerciseApi.list(patientStore.currentPatient.id)
  records.value = data
}

function openEdit(row: Exercise) {
  editForm.value = row
  Object.assign(form, {
    exercise_type: row.exercise_type,
    duration_min: row.duration_min,
    intensity: row.intensity,
    calories_burned: row.calories_burned,
    performed_at: row.performed_at ? new Date(row.performed_at) : new Date(),
    blood_sugar_before: row.blood_sugar_before,
    blood_sugar_after: row.blood_sugar_after,
    note: row.note,
  })
}

function resetForm() {
  editForm.value = null
  Object.assign(form, defaultForm())
}

async function confirmDelete(row: Exercise) {
  await ElMessageBox.confirm(`确定删除「${row.exercise_type}」记录吗？`, '删除确认', { type: 'warning' })
  await exerciseApi.delete(row.id)
  ElMessage.success('删除成功')
  await load()
}

async function submit() {
  if (!patientStore.currentPatient) return
  submitting.value = true
  try {
    const payload: Record<string, unknown> = {
      patient_id: patientStore.currentPatient.id,
      ...form,
      performed_at: (form.performed_at instanceof Date ? form.performed_at : new Date()).toISOString(),
    }
    if (editForm.value) {
      await exerciseApi.update(editForm.value.id, payload)
      ElMessage.success('修改成功')
      resetForm()
    } else {
      await exerciseApi.create(payload)
      ElMessage.success('记录成功')
    }
    await load()
  } finally {
    submitting.value = false
  }
}

onMounted(load)
watch(
  () => patientStore.currentPatient?.id,
  () => load(),
)
</script>

<style scoped>
.exercise-page h2 {
  margin-bottom: 20px;
}
</style>
