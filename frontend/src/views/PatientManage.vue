<template>
  <div class="patient-page">
    <h2>👤 患者管理</h2>
    <el-row :gutter="20">
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center">
              <span>患者列表</span>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索患者姓名或电话"
                style="width: 200px"
                clearable
              >
                <template #prefix><el-icon><Search /></el-icon></template>
              </el-input>
            </div>
          </template>
          <el-table :data="filteredPatients" @row-click="selectPatient" highlight-current-row>
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="age" label="年龄" width="70" />
            <el-table-column prop="gender" label="性别" width="70" />
            <el-table-column prop="diabetes_type" label="糖尿病类型" />
            <el-table-column label="BMI" width="120">
              <template #default="{ row }">
                <span v-if="row.bmi">
                  {{ row.bmi.toFixed(1) }} - {{ row.bmi_status }}
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button size="small" type="primary" @click.stop="editPatient(row)">编辑</el-button>
                <el-button size="small" type="danger" @click.stop="deletePatient(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header><span>{{ isEditing ? '编辑患者' : '添加患者' }}</span></template>
          <el-form :model="form" label-position="top" :rules="rules" ref="formRef">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" placeholder="请输入患者姓名" />
            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="1" :max="120" style="width: 100%" />
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="糖尿病类型" prop="diabetes_type">
              <el-select v-model="form.diabetes_type" style="width: 100%">
                <el-option label="1型糖尿病" value="1型糖尿病" />
                <el-option label="2型糖尿病" value="2型糖尿病" />
                <el-option label="妊娠糖尿病" value="妊娠糖尿病" />
                <el-option label="其他类型" value="其他类型" />
              </el-select>
            </el-form-item>
            <el-form-item label="确诊日期">
              <el-date-picker
                v-model="form.diagnosis_date"
                type="date"
                placeholder="选择确诊日期"
                style="width: 100%"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
            <el-form-item label="身高 (cm)">
              <el-input-number v-model="form.height" :min="50" :max="250" style="width: 100%" />
            </el-form-item>
            <el-form-item label="体重 (kg)">
              <el-input-number v-model="form.weight" :min="20" :max="300" style="width: 100%" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="form.phone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" style="width: 100%" @click="submit">
                {{ isEditing ? '保存修改' : '添加患者' }}
              </el-button>
              <el-button v-if="isEditing" style="width: 100%; margin-top: 10px" @click="cancelEdit">
                取消编辑
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { patientApi } from '../api/patient'
import { usePatientStore } from '../stores/patient'
import type { Patient } from '../types'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const patientStore = usePatientStore()
const patients = ref<Patient[]>([])
const searchKeyword = ref('')
const isEditing = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  age: 30,
  gender: '男',
  diabetes_type: '2型糖尿病',
  diagnosis_date: null as string | null,
  height: null as number | null,
  weight: null as number | null,
  phone: null as string | null,
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  diabetes_type: [{ required: true, message: '请选择糖尿病类型', trigger: 'change' }],
}

const filteredPatients = computed(() => {
  if (!searchKeyword.value) return patients.value
  const kw = searchKeyword.value.toLowerCase()
  return patients.value.filter(
    p =>
      p.name.toLowerCase().includes(kw) ||
      (p.phone && p.phone.includes(kw))
  )
})

async function loadPatients() {
  try {
    const { data } = await patientApi.list()
    patients.value = data
    if (data.length > 0 && !patientStore.currentPatient) {
      patientStore.selectPatient(data[0])
    }
  } catch (error) {
    ElMessage.error('加载患者列表失败')
  }
}

function selectPatient(row: Patient) {
  patientStore.selectPatient(row)
  ElMessage.success(`已选择患者: ${row.name}`)
}

function resetForm() {
  form.name = ''
  form.age = 30
  form.gender = '男'
  form.diabetes_type = '2型糖尿病'
  form.diagnosis_date = null
  form.height = null
  form.weight = null
  form.phone = null
  editingId.value = null
  isEditing.value = false
}

function editPatient(patient: Patient) {
  isEditing.value = true
  editingId.value = patient.id
  form.name = patient.name
  form.age = patient.age
  form.gender = patient.gender
  form.diabetes_type = patient.diabetes_type
  form.diagnosis_date = patient.diagnosis_date
  form.height = patient.height
  form.weight = patient.weight
  form.phone = patient.phone
}

function cancelEdit() {
  resetForm()
}

async function submit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    
    if (isEditing.value && editingId.value) {
      await patientApi.update(editingId.value, form)
      ElMessage.success('患者信息已更新')
    } else {
      await patientApi.create(form)
      ElMessage.success('患者添加成功')
    }
    
    resetForm()
    await loadPatients()
  } catch (error: any) {
    if (error?.message) {
      ElMessage.error(error.message)
    }
  }
}

async function deletePatient(id: number) {
  try {
    await patientApi.delete(id)
    ElMessage.success('患者已删除')
    if (patientStore.currentPatient?.id === id) {
      patientStore.selectPatient(patients.value.find(p => p.id !== id) || null)
    }
    await loadPatients()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(loadPatients)
</script>

<style scoped>
.patient-page h2 {
  margin-bottom: 20px;
}

:deep(.el-table__row) {
  cursor: pointer;
}

:deep(.el-table__row.current-row) {
  background-color: #ecf5ff;
}
</style>
