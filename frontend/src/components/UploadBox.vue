<template>
  <el-upload
    class="upload-box"
    drag
    action="#"
    :auto-upload="false"
    :show-file-list="false"
    :on-change="handleChange"
    accept="image/*,video/*"
  >
    <el-icon class="upload-icon"><Upload /></el-icon>
    <div class="upload-text">
      <span class="primary">点击或拖拽文件到此处上传</span>
      <p class="secondary">支持图片（JPG / PNG）或视频（MP4）</p>
    </div>
    <template #tip>
      <div class="upload-tip">
        当前文件: <strong>{{ currentFile?.name || '未选择' }}</strong>
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'

const props = defineProps<{
  modelValue?: File | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', file: File | null): void
  (e: 'change', file: File | null): void
}>()

const currentFile = computed({
  get: () => props.modelValue || null,
  set: (val: File | null) => emit('update:modelValue', val),
})

function handleChange(uploadFile: UploadFile) {
  const raw = uploadFile.raw
  if (raw) {
    currentFile.value = raw
    emit('change', raw)
  }
}
</script>

<style scoped lang="scss">
.upload-box {
  width: 100%;

  :deep(.el-upload-dragger) {
    padding: 40px 20px;
    background: #f1f5f9;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    transition: all 0.3s;

    &:hover {
      border-color: #38bdf8;
      background: #e0f2fe;
    }
  }
}

.upload-icon {
  font-size: 48px;
  color: #64748b;
  margin-bottom: 12px;
}

.upload-text {
  .primary {
    font-size: 16px;
    color: #1e293b;
    font-weight: 500;
  }

  .secondary {
    margin: 8px 0 0;
    font-size: 13px;
    color: #94a3b8;
  }
}

.upload-tip {
  margin-top: 10px;
  font-size: 13px;
  color: #64748b;
}
</style>
