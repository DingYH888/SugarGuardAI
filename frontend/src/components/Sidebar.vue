<template>
  <el-aside width="240px" class="sidebar">
    <div class="logo">
      <el-icon :size="28" color="#409EFF"><Monitor /></el-icon>
      <span class="logo-title">糖尿病AI健康助手</span>
    </div>
    <el-menu
      :default-active="route.path"
      router
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <el-menu-item index="/"><el-icon><Odometer /></el-icon><span>仪表盘</span></el-menu-item>
      <el-menu-item index="/patients"><el-icon><User /></el-icon><span>患者管理</span></el-menu-item>
      <el-menu-item index="/blood-sugar"><el-icon><TrendCharts /></el-icon><span>血糖管理</span></el-menu-item>
      <el-menu-item index="/diet"><el-icon><Food /></el-icon><span>饮食管理</span></el-menu-item>
      <el-menu-item index="/medication"><el-icon><FirstAidKit /></el-icon><span>用药管理</span></el-menu-item>
      <el-menu-item index="/exercise"><el-icon><Bicycle /></el-icon><span>运动管理</span></el-menu-item>
      <el-menu-item index="/reports"><el-icon><Document /></el-icon><span>健康报告</span></el-menu-item>
      <el-menu-item index="/chat"><el-icon><ChatDotRound /></el-icon><span>AI健康助手</span></el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import {
  Monitor,
  Odometer,
  User,
  TrendCharts,
  Food,
  FirstAidKit,
  Bicycle,
  Document,
  ChatDotRound,
} from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped>
.sidebar {
  background: #304156;
  height: 100vh;
}
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 60px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}
.logo-title {
  flex: 1;
  min-width: 0;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  line-height: 1.35;
}
.el-menu {
  border-right: none;
}
</style>
