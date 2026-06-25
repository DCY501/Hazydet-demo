<template>
  <div class="image-compare">
    <div
      v-for="(item, idx) in items"
      :key="idx"
      class="compare-item"
      :style="{ width: columnWidth }"
    >
      <div class="compare-label">{{ item.label }}</div>
      <el-image
        :src="item.url"
        fit="contain"
        :preview-src-list="previewList"
        class="compare-image"
      >
        <template #error>
          <div class="compare-placeholder">暂无图片</div>
        </template>
      </el-image>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface CompareItem {
  label: string
  url?: string
}

const props = defineProps<{
  items: CompareItem[]
}>()

const columnWidth = computed(() => {
  const count = props.items.length || 1
  return `${100 / count}%`
})

const previewList = computed(() => {
  return props.items.map((i) => i.url).filter((url): url is string => !!url)
})
</script>

<style scoped lang="scss">
.image-compare {
  display: flex;
  gap: 12px;
  width: 100%;
  flex-wrap: wrap;
}

.compare-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compare-label {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  text-align: center;
}

.compare-image {
  width: 100%;
  min-height: 160px;
  max-height: 400px;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  :deep(img) {
    max-width: 100%;
    max-height: 400px;
    height: auto;
    object-fit: contain;
    display: block;
  }
}

.compare-placeholder {
  width: 100%;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}
</style>
