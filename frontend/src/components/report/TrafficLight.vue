<template>
  <view :class="['traffic-light', `light-${level}`]">
    <view class="light-circle">
      <text class="light-icon">{{ icons[level] }}</text>
    </view>
    <text v-if="label" class="light-label">{{ label }}</text>
    <text v-if="description" class="light-desc">{{ description }}</text>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  level: 'red' | 'yellow' | 'blue' | 'green'
  label?: string
  description?: string
}>()

const icons: Record<string, string> = {
  red: '!',
  yellow: '!',
  blue: 'i',
  green: '✓',
}
</script>

<style scoped lang="scss">
.traffic-light {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.light-circle {
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.light-red .light-circle { background: #E07070; }
.light-yellow .light-circle { background: #E8B84A; }
.light-blue .light-circle { background: #5A9BB8; }
.light-green .light-circle { background: #5CB87A; }

.light-icon {
  font-size: 20rpx;
  color: #fff;
  font-weight: bold;
}

.light-label {
  font-size: 24rpx;
  font-weight: 500;
}

.light-red .light-label { color: #E07070; }
.light-yellow .light-label { color: #E8B84A; }
.light-blue .light-label { color: #5A9BB8; }
.light-green .light-label { color: #5CB87A; }

.light-desc {
  font-size: 22rpx;
  color: #A0A0A5;
}
</style>
