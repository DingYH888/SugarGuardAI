import { defineStore } from 'pinia'
import { ref } from 'vue'
import { dietApi } from '../api/diet'
import type { DietRecord } from '../types'

export const useDietStore = defineStore('diet', () => {
  const dailyNutrition = ref<Record<string, unknown> | null>(null)
  const recommendations = ref<Record<string, unknown>[]>([])
  const records = ref<DietRecord[]>([])

  async function fetchDaily(patientId: number) {
    const { data } = await dietApi.daily(patientId)
    dailyNutrition.value = data as Record<string, unknown>
  }

  async function fetchRecommend(mealType: string, patientId?: number, bg?: number) {
    const { data } = await dietApi.recommend(mealType, patientId, bg)
    recommendations.value = data as Record<string, unknown>[]
  }

  async function fetchRecords(patientId: number) {
    const { data } = await dietApi.records(patientId)
    records.value = data as DietRecord[]
  }

  async function addRecord(patientId: number, record: Record<string, unknown>) {
    await dietApi.create({ patient_id: patientId, ...record })
    await fetchRecords(patientId)
    await fetchDaily(patientId)
  }

  return { dailyNutrition, recommendations, records, fetchDaily, fetchRecommend, fetchRecords, addRecord }
})
