import api from './index'
import type { HealthReport } from '../types'

export const reportApi = {
  list: (patientId: number) => api.get<HealthReport[]>(`/reports/patient/${patientId}`),
  generate: (patientId: number, type = '周报') =>
    api.post<HealthReport>(`/reports/generate/${patientId}?report_type=${encodeURIComponent(type)}`),
}
