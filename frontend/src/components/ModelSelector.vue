<template>
  <el-select
    :model-value="modelValue"
    placeholder="请选择检测模型"
    @change="handleChange"
    :disabled="disabled"
    style="width: 100%"
  >
    <el-option
      v-for="m in store.availableModels"
      :key="m.key"
      :label="m.name"
      :value="m.key"
    >
      <div class="model-option">
        <span>{{ m.name }}</span>
        <el-tag size="small" type="info" v-if="m.description">
          {{ m.description.slice(0, 20) }}...
        </el-tag>
      </div>
    </el-option>
  </el-select>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'

defineProps<{
  modelValue: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const store = useAppStore()

function handleChange(val: string) {
  emit('update:modelValue', val)
}
</script>

<style scoped lang="scss">
.model-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
