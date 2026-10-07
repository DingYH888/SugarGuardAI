import api from './index'
import type { DietRecord } from '../types'

export const dietApi = {
  create: (data: Record<string, unknown>) => api.post('/diet/', data),
  daily: (patientId: number) => api.get(`/diet/patient/${patientId}/daily`),
  recommend: (mealType: string, patientId?: number, bg?: number) =>
    api.get(`/diet/recommend/${encodeURIComponent(mealType)}`, {
      params: { patient_id: patientId, recent_bg: bg }
    }),
  records: (patientId: number) => api.get<DietRecord[]>(`/diet/patient/${patientId}/records`),
  update: (recordId: number, data: Record<string, unknown>) =>
    api.put(`/diet/${recordId}`, data),
  remove: (recordId: number) => api.delete(`/diet/${recordId}`),
}
