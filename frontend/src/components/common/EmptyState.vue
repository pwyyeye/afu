<template>
  <view class="empty-state">
    <text class="empty-icon">{{ icon }}</text>
    <text class="empty-title">{{ title }}</text>
    <text v-if="description" class="empty-desc">{{ description }}</text>
    <button v-if="actionText" class="empty-action" @tap="$emit('action')">
      {{ actionText }}
    </button>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  icon?: string
  title: string
  description?: string
  actionText?: string
}>()

defineEmits<{
  (e: 'action'): void
}>()
</script>

<style scoped lang="scss">
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 48rpx;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 24rpx;
}

.empty-title {
  font-size: 30rpx;
  color: #999;
  margin-bottom: 12rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #ccc;
  text-align: center;
  line-height: 1.5;
}

.empty-action {
  margin-top: 32rpx;
  padding: 16rpx 48rpx;
  background: #4a90d9;
  color: #fff;
  font-size: 28rpx;
  border-radius: 999rpx;
  border: none;
}
</style>
