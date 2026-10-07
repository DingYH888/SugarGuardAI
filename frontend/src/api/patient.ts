import api from './index'
import type { Patient } from '../types'

export const patientApi = {
  list: () => api.get<Patient[]>('/patients/'),
  get: (id: number) => api.get<Patient>(`/patients/${id}`),
  create: (data: Partial<Patient>) => api.post<Patient>('/patients/', data),
  update: (id: number, data: Partial<Patient>) => api.put<Patient>(`/patients/${id}`, data),
  delete: (id: number) => api.delete(`/patients/${id}`),
}
