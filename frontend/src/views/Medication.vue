<template>
  <div class="medication-page">
    <h2>💊 用药管理</h2>
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header><span>当前用药方案</span></template>
          <el-table :data="medications" size="default" style="width: 100%; font-size: 14px">
            <el-table-column prop="drug_name" label="药品名称" min-width="120" />
            <el-table-column prop="drug_type" label="类型" width="80" align="center" />
            <el-table-column prop="dosage" label="剂量" width="80" align="center" />
            <el-table-column prop="frequency" label="频次" width="100" align="center" />
            <el-table-column prop="timing" label="服用时间" width="130" align="center" />
            <el-table-column label="操作" width="160" fixed="right" align="center">
              <template #default="{ row }">
                <el-button type="primary" link @click="openEdit(row)">编辑</el-button>
                <el-button type="danger" link @click="confirmDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!medications.length" description="暂无用药记录" />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span>{{ editForm ? '编辑用药' : '添加用药' }}</span></template>
          <el-form :model="form" label-position="top">
            <el-form-item label="药品名称"><el-input v-model="form.drug_name" /></el-form-item>
            <el-form-item label="药品类型">
              <el-select v-model="form.drug_type" style="width: 100%">
                <el-option label="口服药" value="口服药" />
                <el-option label="胰岛素" value="胰岛素" />
              </el-select>
            </el-form-item>
            <el-form-item label="剂量"><el-input v-model="form.dosage" placeholder="如 500mg" /></el-form-item>
            <el-form-item label="频次"><el-input v-model="form.frequency" placeholder="如 每日2次" /></el-form-item>
            <el-form-item label="服用时间"><el-input v-model="form.timing" placeholder="如 餐后" /></el-form-item>
            <el-form-item>
              <div style="display: flex; gap: 8px">
                <el-button type="primary" style="flex: 1" @click="submit" :loading="submitting">
                  {{ editForm ? '保存修改' : '添加' }}
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
import { medicationApi } from '../api/medication'
import type { Medication } from '../types'
import { ElMessage, ElMessageBox } from 'element-plus'

const patientStore = usePatientStore()
const medications = ref<Medication[]>([])
const submitting = ref(false)
const editForm = ref<Medication | null>(null)

const defaultForm = () => ({
  drug_name: '',
  drug_type: '口服药',
  dosage: '',
  frequency: '',
  timing: '',
  start_date: new Date().toISOString().slice(0, 10),
})

const form = reactive(defaultForm())

async function load() {
  if (!patientStore.currentPatient) return
  const { data } = await medicationApi.list(patientStore.currentPatient.id)
  medications.value = data
}

function openEdit(row: Medication) {
  editForm.value = row
  Object.assign(form, {
    drug_name: row.drug_name,
    drug_type: row.drug_type,
    dosage: row.dosage,
    frequency: row.frequency,
    timing: row.timing,
    start_date: row.start_date || new Date().toISOString().slice(0, 10),
  })
}

function resetForm() {
  editForm.value = null
  Object.assign(form, defaultForm())
}

async function confirmDelete(row: Medication) {
  await ElMessageBox.confirm(`确定删除「${row.drug_name}」吗？`, '删除确认', { type: 'warning' })
  await medicationApi.delete(row.id)
  ElMessage.success('删除成功')
  await load()
}

async function submit() {
  if (!patientStore.currentPatient) return
  submitting.value = true
  try {
    if (editForm.value) {
      await medicationApi.update(editForm.value.id, form)
      ElMessage.success('修改成功')
      resetForm()
    } else {
      await medicationApi.create({ ...form, patient_id: patientStore.currentPatient.id })
      ElMessage.success('添加成功')
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
.medication-page h2 {
  margin-bottom: 20px;
}
</style>
