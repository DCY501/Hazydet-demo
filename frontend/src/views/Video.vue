<template>
  <div class="video-page">
    <el-row :gutter="20">
      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="control-card">
          <template #header>
            <span>视频检测配置</span>
          </template>

          <el-form label-position="top">
            <el-form-item label="上传视频">
              <el-upload
                class="video-upload"
                drag
                action="#"
                :auto-upload="false"
                :show-file-list="false"
                :on-change="handleChange"
                accept="video/mp4,video/avi,video/mov"
              >
                <el-icon class="upload-icon"><VideoCamera /></el-icon>
                <div class="upload-text">
                  <span>点击或拖拽视频到此处</span>
                  <p>支持 MP4 / AVI / MOV</p>
                </div>
              </el-upload>
              <div class="file-name" v-if="file">已选择: {{ file.name }}</div>
            </el-form-item>

            <el-form-item label="选择模型">
              <ModelSelector v-model="model" />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                :disabled="!file || !model"
                @click="handleVideoDetect"
                style="width: 100%"
              >
                开始视频检测
              </el-button>
            </el-form-item>
          </el-form>

          <el-alert
            v-if="loading"
            title="视频处理中，请耐心等待..."
            type="info"
            :closable="false"
            show-icon
          />
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="16">
        <el-card shadow="never" v-loading="loading">
          <template #header>
            <span>处理结果</span>
          </template>

          <el-empty description="请先上传视频并提交" v-if="!result" />

          <div v-else class="video-result">
            <video :src="result.video_url" controls class="result-video"></video>
            <el-descriptions :column="2" border class="video-metrics">
              <el-descriptions-item label="输出文件">{{ result.filename }}</el-descriptions-item>
              <el-descriptions-item label="总帧数">{{ result.total_frames }}</el-descriptions-item>
              <el-descriptions-item label="FPS">{{ result.fps }}</el-descriptions-item>
              <el-descriptions-item label="处理耗时">{{ result.process_time?.toFixed(2) }}s</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VideoCamera } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'
import ModelSelector from '@/components/ModelSelector.vue'
import { detectVideo } from '@/api/detect'

const file = ref<File | null>(null)
const model = ref('baseline')
const loading = ref(false)
const result = ref<any>(null)

function handleChange(uploadFile: UploadFile) {
  const raw = uploadFile.raw
  if (raw) {
    file.value = raw
    result.value = null
  }
}

async function handleVideoDetect() {
  if (!file.value || !model.value) return

  const formData = new FormData()
  formData.append('file', file.value)
  formData.append('model', model.value)

  loading.value = true
  try {
    const res: any = await detectVideo(formData)
    result.value = res
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.video-page {
  .control-card {
    margin-bottom: 20px;
  }

  .video-upload {
    width: 100%;

    :deep(.el-upload-dragger) {
      padding: 30px 20px;
      background: #f1f5f9;
      border: 2px dashed #cbd5e1;
      border-radius: 12px;
    }
  }

  .upload-icon {
    font-size: 40px;
    color: #64748b;
    margin-bottom: 8px;
  }

  .upload-text {
    span {
      font-size: 15px;
      color: #1e293b;
    }

    p {
      margin-top: 6px;
      font-size: 12px;
      color: #94a3b8;
    }
  }

  .file-name {
    margin-top: 10px;
    font-size: 13px;
    color: #64748b;
  }

  .video-result {
    .result-video {
      width: 100%;
      max-height: 480px;
      border-radius: 8px;
      background: #000;
    }

    .video-metrics {
      margin-top: 16px;
    }
  }
}
</style>
