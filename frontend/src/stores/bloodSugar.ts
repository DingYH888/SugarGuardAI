import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { BloodSugar, BloodSugarStats } from '../types'
import { bloodSugarApi } from '../api/bloodSugar'

export const useBloodSugarStore = defineStore('bloodSugar', () => {
  const records = ref<BloodSugar[]>([])
  const stats = ref<BloodSugarStats | null>(null)
  const loading = ref(false)

  async function fetchRecords(patientId: number, days = 7) {
    loading.value = true
    try {
      const { data } = await bloodSugarApi.list(patientId, days)
      records.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchStats(patientId: number, days = 7) {
    const { data } = await bloodSugarApi.stats(patientId, days)
    stats.value = data
  }

  async function addRecord(
    patientId: number,
    value: number,
    type: string,
    time: string,
    note?: string,
  ) {
    await bloodSugarApi.create({
      patient_id: patientId,
      value,
      measure_type: type,
      measured_at: time,
      note,
    })
    await fetchRecords(patientId)
    await fetchStats(patientId)
  }

  return { records, stats, loading, fetchRecords, fetchStats, addRecord }
})
