<template>
  <div :class="['message', msg.role]">
    <el-avatar :size="36" :class="msg.role">
      {{ msg.role === 'user' ? '患' : 'AI' }}
    </el-avatar>
    <div class="bubble">
      <div class="content" v-html="formattedContent"></div>
      <div class="time">{{ formatTime(msg.created_at) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ChatMessage } from '../types'
import { formatTime as fmtTime } from '../utils/date'

const props = defineProps<{ msg: ChatMessage }>()
const formattedContent = computed(() => props.msg.content.replace(/\n/g, '<br>'))
const formatTime = fmtTime
</script>

<style scoped>
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
.message.user {
  flex-direction: row-reverse;
}
.bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
}
.message.user .bubble {
  background: #409eff;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.message.assistant .bubble {
  background: #f4f4f5;
  color: #333;
  border-bottom-left-radius: 4px;
}
.time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  text-align: right;
}
.message.user .time {
  color: rgba(255, 255, 255, 0.7);
}
</style>
