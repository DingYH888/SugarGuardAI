import api from './index'
import type { BloodSugar, BloodSugarStats } from '../types'

export const bloodSugarApi = {
  create: (data: {
    patient_id: number
    value: number
    measure_type: string
    measured_at: string
    note?: string
  }) => api.post<BloodSugar>('/blood-sugar/', data),
  list: (patientId: number, days = 7) =>
    api.get<BloodSugar[]>(`/blood-sugar/patient/${patientId}?days=${days}`),
  stats: (patientId: number, days = 7) =>
    api.get<BloodSugarStats>(`/blood-sugar/patient/${patientId}/stats?days=${days}`),
  update: (recordId: number, data: Record<string, unknown>) =>
    api.put<BloodSugar>(`/blood-sugar/${recordId}`, data),
  remove: (recordId: number) => api.delete(`/blood-sugar/${recordId}`),
}
