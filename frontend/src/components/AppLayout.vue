<template>
  <el-container class="app-layout">
    <el-aside :width="store.sidebarCollapsed ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <el-icon :size="24"><Monitor /></el-icon>
        <span v-show="!store.sidebarCollapsed" class="logo-text">Hazydet</span>
      </div>
      <el-menu
        :default-active="route.path"
        :collapse="store.sidebarCollapsed"
        :collapse-transition="false"
        router
        class="nav-menu"
        background-color="#1e293b"
        text-color="#cbd5e1"
        active-text-color="#38bdf8"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/detect">
          <el-icon><Picture /></el-icon>
          <template #title>单图检测</template>
        </el-menu-item>
        <el-menu-item index="/compare">
          <el-icon><Grid /></el-icon>
          <template #title>三模型对比</template>
        </el-menu-item>
        <el-menu-item index="/robustness">
          <el-icon><Histogram /></el-icon>
          <template #title>浓度鲁棒性</template>
        </el-menu-item>
        <el-menu-item index="/intermediate">
          <el-icon><Share /></el-icon>
          <template #title>中间结果</template>
        </el-menu-item>
        <el-menu-item index="/video">
          <el-icon><VideoCamera /></el-icon>
          <template #title>视频检测</template>
        </el-menu-item>
        <el-menu-item index="/about">
          <el-icon><InfoFilled /></el-icon>
          <template #title>关于</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button text @click="store.toggleSidebar">
            <el-icon :size="20"><Fold v-if="!store.sidebarCollapsed" /><Expand v-else /></el-icon>
          </el-button>
          <h2 class="page-title">{{ route.meta.title || 'Hazydet Demo' }}</h2>
        </div>
        <div class="header-right">
          <el-tag type="info" effect="plain" size="small">
            可用模型: {{ store.availableModels.length }}
          </el-tag>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  Monitor,
  HomeFilled,
  Picture,
  Grid,
  Histogram,
  Share,
  VideoCamera,
  InfoFilled,
  Fold,
  Expand,
} from '@element-plus/icons-vue'

const route = useRoute()
const store = useAppStore()

onMounted(() => {
  store.fetchModels()
})
</script>

<style scoped lang="scss">
.app-layout {
  min-height: 100vh;
}

.sidebar {
  background: #1e293b;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #38bdf8;
  border-bottom: 1px solid #334155;

  .logo-text {
    margin-left: 10px;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 1px;
  }
}

.nav-menu {
  border-right: none;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.main-content {
  background: #f8fafc;
  padding: 20px;
}
</style>
