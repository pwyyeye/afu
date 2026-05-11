<template>
  <view v-if="visible" class="modal-overlay" @tap="onOverlayTap">
    <view class="modal-content" :class="[`modal-${size}`]" @tap.stop>
      <view v-if="title" class="modal-header">
        <text class="modal-title">{{ title }}</text>
        <text class="modal-close" @tap="close">×</text>
      </view>
      <view class="modal-body">
        <slot />
      </view>
      <view v-if="$slots.footer" class="modal-footer">
        <slot name="footer" />
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  title?: string
  size?: 'small' | 'medium' | 'large'
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

function onOverlayTap() {
  emit('close')
}

function close() {
  emit('close')
}
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background: #fff;
  border-radius: 28rpx;
  width: 80%;
  max-height: 80vh;
  overflow: hidden;
}

.modal-small { width: 60%; }
.modal-large { width: 90%; }

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 32rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2C2C2E;
}

.modal-close {
  font-size: 40rpx;
  color: #A0A0A5;
  padding: 8rpx;
}

.modal-body {
  padding: 32rpx;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  gap: 16rpx;
  padding: 24rpx 32rpx;
  border-top: 1rpx solid #f0f0f0;
}
</style>
