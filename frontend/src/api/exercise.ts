import api from './index'
import type { Exercise } from '../types'

export const exerciseApi = {
  list: (patientId: number) => api.get<Exercise[]>(`/exercise/patient/${patientId}`),
  create: (data: Record<string, unknown>) => api.post('/exercise/', data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/exercise/${id}`, data),
  delete: (id: number) => api.delete(`/exercise/${id}`),
}
