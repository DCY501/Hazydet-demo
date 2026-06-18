<template>
  <el-card class="result-card" shadow="hover" v-loading="!!loading">
    <template #header>
      <div class="card-header">
        <span>{{ title }}</span>
        <el-tag v-if="modelName" type="primary" size="small">{{ modelName }}</el-tag>
      </div>
    </template>

    <div class="image-wrapper">
      <el-image
        :src="imageUrl"
        fit="contain"
        :preview-src-list="[imageUrl]"
        class="result-image"
      >
        <template #error>
          <div class="image-placeholder">
            <el-icon :size="40"><Picture /></el-icon>
            <span>暂无结果</span>
          </div>
        </template>
      </el-image>
    </div>

    <div class="metrics" v-if="metrics">
      <el-descriptions :column="3" size="small" border>
        <el-descriptions-item label="检出目标">{{ metrics.count ?? 0 }}</el-descriptions-item>
        <el-descriptions-item label="平均置信度">{{ metrics.avg_conf?.toFixed(3) ?? '-' }}</el-descriptions-item>
        <el-descriptions-item label="推理耗时">{{ metrics.inference_ms ? `${metrics.inference_ms}ms` : '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>

    <div class="detections" v-if="detections && detections.length">
      <el-divider content-position="left">检测详情</el-divider>
      <el-table :data="detections" size="small" max-height="200">
        <el-table-column prop="class_name" label="类别" width="120" />
        <el-table-column prop="confidence" label="置信度" width="120">
          <template #default="{ row }">
            <el-progress :percentage="Math.round(row.confidence * 100)" :stroke-width="8" />
          </template>
        </el-table-column>
        <el-table-column prop="bbox" label="边界框" />
      </el-table>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { Picture } from '@element-plus/icons-vue'

interface Detection {
  class_name: string
  confidence: number
  bbox: number[]
}

interface Metrics {
  count?: number
  avg_conf?: number
  inference_ms?: number
}

withDefaults(
  defineProps<{
    title: string
    imageUrl?: string
    modelName?: string
    metrics?: Metrics
    detections?: Detection[]
    loading?: boolean
  }>(),
  {
    imageUrl: '',
    modelName: '',
    loading: false,
  }
)
</script>

<style scoped lang="scss">
.result-card {
  height: 100%;

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;
  }
}

.image-wrapper {
  width: 100%;
  height: 360px;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-image {
  width: 100%;
  height: 100%;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #94a3b8;
  gap: 8px;
}

.metrics {
  margin-top: 16px;
}

.detections {
  margin-top: 16px;
}
</style>
