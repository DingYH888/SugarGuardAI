import api from './index'
import type { ChatMessage } from '../types'

export interface ChatSendResponse {
  id: number
  patient_id: number
  user_message: string
  ai_response: string
  created_at: string
}

export const chatApi = {
  send: (patientId: number, message: string) =>
    api.post<ChatSendResponse>('/chat/message', { patient_id: patientId, message }),
  history: (patientId: number) => api.get<ChatMessage[]>(`/chat/history/${patientId}`),
}
