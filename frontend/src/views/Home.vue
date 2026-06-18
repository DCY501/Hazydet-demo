<template>
  <div class="home-page">
    <el-row :gutter="20" justify="center">
      <el-col :xs="24" :md="18" :lg="16">
        <el-card class="welcome-card" shadow="never">
          <div class="welcome-content">
            <el-icon :size="64" class="welcome-icon"><Monitor /></el-icon>
            <h1>Hazydet Demo</h1>
            <p class="subtitle">雾天场景下的目标检测 Web 演示系统</p>
            <p class="description">
              基于 YOLOv8 与去雾辅助多任务学习，支持单图检测、三模型对比、浓度鲁棒性分析、
              中间结果可视化与视频检测。
            </p>
            <div class="actions">
              <el-button type="primary" size="large" @click="$router.push('/detect')">
                开始检测
              </el-button>
              <el-button size="large" @click="$router.push('/compare')">三模型对比</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="feature-row" justify="center">
      <el-col :xs="24" :sm="12" :md="8" v-for="feature in features" :key="feature.title">
        <el-card class="feature-card" shadow="hover" @click="$router.push(feature.route)">
          <el-icon :size="36" class="feature-icon"><component :is="feature.icon" /></el-icon>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="status-row" justify="center">
      <el-col :xs="24" :md="18" :lg="16">
        <el-card shadow="never">
          <template #header>
            <span>模型状态</span>
          </template>
          <el-skeleton :rows="2" animated v-if="loading" />
          <div v-else-if="store.availableModels.length" class="model-tags">
            <el-tag
              v-for="m in store.availableModels"
              :key="m.key"
              size="large"
              :type="m.available ? 'success' : 'info'"
              class="model-tag"
            >
              {{ m.name }}
            </el-tag>
          </div>
          <el-empty description="未加载到模型，请检查 backend/weights/ 目录" v-else />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import {
  Monitor,
  Picture,
  Grid,
  Histogram,
  Share,
  VideoCamera,
} from '@element-plus/icons-vue'

const store = useAppStore()
const loading = computed(() => store.availableModels.length === 0)

const features = [
  { title: '单图检测', desc: '选择模型上传图片，查看检测结果与指标', route: '/detect', icon: Picture },
  { title: '三模型对比', desc: '同一张图同时跑 baseline / phase1 / phase2', route: '/compare', icon: Grid },
  { title: '浓度鲁棒性', desc: '模拟不同雾浓度，观察模型性能变化', route: '/robustness', icon: Histogram },
  { title: '中间结果', desc: '可视化去雾图、透射率、重构图等', route: '/intermediate', icon: Share },
  { title: '视频检测', desc: '上传视频并查看逐帧检测结果', route: '/video', icon: VideoCamera },
]

onMounted(() => {
  store.fetchModels()
})
</script>

<style scoped lang="scss">
.home-page {
  padding: 20px 0;
}

.welcome-card {
  text-align: center;
  padding: 30px 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: none;
}

.welcome-icon {
  color: #38bdf8;
  margin-bottom: 16px;
}

h1 {
  font-size: 36px;
  color: #0f172a;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 18px;
  color: #475569;
  margin-bottom: 16px;
}

.description {
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
  max-width: 640px;
  margin: 0 auto 24px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.feature-row {
  margin-top: 24px;
}

.feature-card {
  margin-bottom: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
  }

  .feature-icon {
    color: #38bdf8;
    margin-bottom: 12px;
  }

  h3 {
    margin-bottom: 8px;
    color: #1e293b;
  }

  p {
    font-size: 13px;
    color: #64748b;
    line-height: 1.6;
  }
}

.status-row {
  margin-top: 24px;
}

.model-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.model-tag {
  font-size: 14px;
}
</style>
