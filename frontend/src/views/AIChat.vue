<template>
  <div class="chat-page">
    <h2>🤖 AI 健康助手</h2>
    <el-card shadow="hover" class="chat-card">
      <div ref="chatBox" class="chat-messages">
        <ChatMessage v-for="msg in chatStore.messages" :key="msg.id" :msg="msg" />
        <div v-if="chatStore.loading" class="loading">
          <el-icon class="is-loading"><Loading /></el-icon> AI 正在思考...
        </div>
      </div>
      <el-divider style="margin: 12px 0" />
      <div class="chat-input">
        <el-input
          v-model="input"
          placeholder="输入健康问题，如：我今天血糖偏高怎么办？"
          :disabled="chatStore.loading"
          @keyup.enter="send"
        >
          <template #append>
            <el-button :disabled="!input.trim()" @click="send">
              <el-icon><Promotion /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import { usePatientStore } from '../stores/patient'
import { useChatStore } from '../stores/chat'
import ChatMessage from '../components/ChatMessage.vue'
import { Loading, Promotion } from '@element-plus/icons-vue'

const patientStore = usePatientStore()
const chatStore = useChatStore()
const input = ref('')
const chatBox = ref<HTMLElement | null>(null)

async function send() {
  if (!input.value.trim() || !patientStore.currentPatient) return
  const msg = input.value
  input.value = ''
  await chatStore.sendMessage(patientStore.currentPatient.id, msg)
  await nextTick()
  chatBox.value?.scrollTo({ top: chatBox.value.scrollHeight, behavior: 'smooth' })
}

async function loadHistory() {
  if (patientStore.currentPatient) {
    await chatStore.fetchHistory(patientStore.currentPatient.id)
  }
}

onMounted(loadHistory)
watch(
  () => patientStore.currentPatient?.id,
  () => loadHistory(),
)
</script>

<style scoped>
.chat-page h2 {
  margin-bottom: 20px;
}
.chat-card {
  height: calc(100vh - 180px);
  display: flex;
  flex-direction: column;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.chat-input {
  padding: 0 16px 8px;
}
.loading {
  text-align: center;
  color: #909399;
  padding: 16px;
}
</style>
