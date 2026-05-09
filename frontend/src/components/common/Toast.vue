<template>
  <view v-if="visible" class="toast" :class="`toast-${type}`">
    <text class="toast-icon">{{ icons[type] }}</text>
    <text class="toast-text">{{ message }}</text>
  </view>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  message: string
  type?: 'success' | 'error' | 'info'
  duration?: number
}>()

const visible = ref(false)

const icons: Record<string, string> = {
  success: '✓',
  error: '✗',
  info: 'i',
}

watch(() => props.message, (msg) => {
  if (msg) {
    visible.value = true
    setTimeout(() => {
      visible.value = false
    }, props.duration || 2000)
  }
})
</script>

<style scoped lang="scss">
.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 24rpx 32rpx;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 12rpx;
  z-index: 1000;
}

.toast-success { background: rgba(39, 174, 96, 0.9); }
.toast-error { background: rgba(231, 76, 60, 0.9); }
.toast-info { background: rgba(52, 152, 219, 0.9); }

.toast-icon {
  font-size: 32rpx;
  color: #fff;
}

.toast-text {
  font-size: 28rpx;
  color: #fff;
}
</style>
