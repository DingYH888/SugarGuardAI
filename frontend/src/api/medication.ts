import api from './index'
import type { Medication } from '../types'

export const medicationApi = {
  list: (patientId: number) => api.get<Medication[]>(`/medication/patient/${patientId}`),
  create: (data: Record<string, unknown>) => api.post('/medication/', data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/medication/${id}`, data),
  delete: (id: number) => api.delete(`/medication/${id}`),
}
