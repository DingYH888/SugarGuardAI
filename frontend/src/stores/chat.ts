import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatMessage } from '../types'
import { chatApi } from '../api/chat'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const loading = ref(false)

  async function sendMessage(patientId: number, content: string) {
    messages.value.push({
      id: Date.now(),
      role: 'user',
      content,
      created_at: new Date().toISOString(),
    })
    loading.value = true
    try {
      const { data } = await chatApi.send(patientId, content)
      messages.value.push({
        id: data.id,
        role: 'assistant',
        content: data.ai_response,
        created_at: data.created_at,
      })
    } finally {
      loading.value = false
    }
  }

  async function fetchHistory(patientId: number) {
    const { data } = await chatApi.history(patientId)
    messages.value = [...data].reverse()
  }

  return { messages, loading, sendMessage, fetchHistory }
})
