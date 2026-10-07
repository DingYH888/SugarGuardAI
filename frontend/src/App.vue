<template>
  <el-container class="app-container" direction="horizontal">
    <Sidebar />
    <el-container direction="vertical">
      <Navbar />
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f7fa;
}
.app-container {
  height: 100vh;
}
.el-main {
  padding: 20px;
  background: #f5f7fa;
}
</style>
