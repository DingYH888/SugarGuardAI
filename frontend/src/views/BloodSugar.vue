<template>
  <div class="blood-sugar-page">
    <h2>📊 血糖管理</h2>

    <el-card shadow="hover" style="margin-bottom: 20px">
      <template #header><span>{{ editId ? '编辑血糖记录' : '记录血糖' }}</span></template>
      <el-form :model="form" inline>
        <el-form-item label="血糖值">
          <el-input-number v-model="form.value" :min="1" :max="33.3" :step="0.1" />
        </el-form-item>
        <el-form-item label="测量类型">
          <el-select v-model="form.measure_type" style="width: 120px">
            <el-option label="空腹" value="空腹" />
            <el-option label="餐后2h" value="餐后2h" />
            <el-option label="睡前" value="睡前" />
            <el-option label="随机" value="随机" />
          </el-select>
        </el-form-item>
        <el-form-item label="测量时间">
          <el-date-picker v-model="form.measured_at" type="datetime" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.note" placeholder="可选" style="width: 150px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitRecord" :loading="submitting">
            {{ editId ? '保存修改' : '提交' }}
          </el-button>
          <el-button v-if="editId" @click="cancelEdit">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="hover" style="margin-bottom: 20px">
      <template #header><span>历史记录</span></template>
      <el-table :data="bloodStore.records" stripe size="default" style="font-size: 14px">
        <el-table-column prop="value" label="血糖值" width="110">
          <template #default="{ row }">
            <span :style="{ color: getColor(row.value) }">{{ row.value }} mmol/L</span>
          </template>
        </el-table-column>
        <el-table-column prop="measure_type" label="类型" width="90" />
        <el-table-column prop="measured_at" label="时间" width="180">
          <template #default="{ row }">{{ formatDateTime(row.measured_at) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.value)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editRecord(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="removeRecord(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>血糖趋势</span>
          <el-radio-group v-model="days" size="small" @change="loadData">
            <el-radio-button :value="7">7天</el-radio-button>
            <el-radio-button :value="14">14天</el-radio-button>
            <el-radio-button :value="30">30天</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <BloodSugarChart v-if="bloodStore.records.length" :records="bloodStore.records" />
      <el-empty v-else description="暂无数据" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { usePatientStore } from '../stores/patient'
import { useBloodSugarStore } from '../stores/bloodSugar'
import { bloodSugarApi } from '../api/bloodSugar'
import BloodSugarChart from '../components/BloodSugarChart.vue'
import { formatDateTime } from '../utils/date'
import { ElMessage } from 'element-plus'
import type { BloodSugar } from '../types'

const patientStore = usePatientStore()
const bloodStore = useBloodSugarStore()
const days = ref(7)
const editId = ref<number | null>(null)
const submitting = ref(false)

const form = reactive({
  value: 5.6,
  measure_type: '空腹',
  measured_at: new Date() as Date,
  note: '',
})

function getColor(v: number) {
  if (v < 3.9) return '#E6A23C'
  if (v <= 7.0) return '#67C23A'
  if (v <= 10.0) return '#E6A23C'
  return '#F56C6C'
}

function statusTag(v: number) {
  if (v < 3.9) return 'warning'
  if (v <= 7.0) return 'success'
  if (v <= 10.0) return 'warning'
  return 'danger'
}

async function loadData() {
  if (!patientStore.currentPatient) return
  await bloodStore.fetchRecords(patientStore.currentPatient.id, days.value)
}

async function submitRecord() {
  if (!patientStore.currentPatient) return
  submitting.value = true
  try {
    const at = form.measured_at instanceof Date ? form.measured_at : new Date(form.measured_at as string)
    const payload = {
      value: form.value,
      measure_type: form.measure_type,
      measured_at: at.toISOString(),
      note: form.note || undefined,
    }
    if (editId.value) {
      await bloodSugarApi.update(editId.value, payload)
      ElMessage.success('修改成功')
    } else {
      await bloodSugarApi.create({ patient_id: patientStore.currentPatient.id, ...payload })
      ElMessage.success('血糖记录成功')
    }
    cancelEdit()
    await loadData()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

function editRecord(row: BloodSugar) {
  editId.value = row.id
  form.value = row.value
  form.measure_type = row.measure_type
  form.measured_at = new Date(row.measured_at)
  form.note = row.note || ''
}

function cancelEdit() {
  editId.value = null
  form.value = 5.6
  form.measure_type = '空腹'
  form.measured_at = new Date()
  form.note = ''
}

async function removeRecord(id: number) {
  try {
    await bloodSugarApi.remove(id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || '删除失败')
  }
}

onMounted(loadData)
watch(
  () => patientStore.currentPatient?.id,
  () => loadData(),
)
</script>

<style scoped>
.blood-sugar-page h2 {
  margin-bottom: 20px;
}
</style>
