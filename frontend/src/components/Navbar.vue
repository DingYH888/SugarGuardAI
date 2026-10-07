<template>
  <el-header class="navbar">
    <div class="navbar-right">
      <el-select
        v-model="selectedPatient"
        placeholder="选择患者"
        size="small"
        style="width: 160px"
        @change="onPatientChange"
      >
        <el-option v-for="p in patientStore.patients" :key="p.id" :label="p.name" :value="p.id" />
      </el-select>
      <el-avatar :size="36" style="margin-left: 16px">
        <el-icon><User /></el-icon>
      </el-avatar>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { User } from '@element-plus/icons-vue'
import { usePatientStore } from '../stores/patient'

const patientStore = usePatientStore()
const selectedPatient = ref<number | undefined>()

onMounted(async () => {
  await patientStore.fetchPatients()
  if (patientStore.currentPatient) {
    selectedPatient.value = patientStore.currentPatient.id
  }
})

function onPatientChange(id: number) {
  const patient = patientStore.patients.find((p) => p.id === id)
  if (patient) patientStore.selectPatient(patient)
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 24px;
  height: 60px;
}
.navbar-right {
  display: flex;
  align-items: center;
}
</style>
