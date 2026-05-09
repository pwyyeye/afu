<template>
  <view class="report-card" @tap="$emit('tap')">
    <view class="card-header">
      <text class="card-title">{{ report.title }}</text>
      <view :class="['light-badge', `light-${report.overall_light}`]">
        {{ lightLabels[report.overall_light] }}
      </view>
    </view>

    <view v-if="report.hospital" class="card-meta">
      <text class="meta-icon">🏥</text>
      <text class="meta-text">{{ report.hospital }}</text>
    </view>

    <view class="card-footer">
      <text class="footer-date">{{ report.report_date || '未知日期' }}</text>
      <view class="status-tag" :class="`status-${report.status}`">
        {{ statusLabels[report.status] }}
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { MedicalReport } from '@/types/report'

defineProps<{
  report: MedicalReport
}>()

defineEmits<{
  (e: 'tap'): void
}>()

const lightLabels: Record<string, string> = {
  red: '紧急',
  yellow: '关注',
  blue: '随访',
  green: '正常',
}

const statusLabels: Record<string, string> = {
  processing: '分析中',
  completed: '已完成',
  failed: '分析失败',
}
</script>

<style scoped lang="scss">
.report-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.card-title {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.light-badge {
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 999rpx;
  color: #fff;
  flex-shrink: 0;
  margin-left: 12rpx;
}

.light-red { background: #e74c3c; }
.light-yellow { background: #f39c12; }
.light-blue { background: #3498db; }
.light-green { background: #27ae60; }

.card-meta {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 12rpx;
}

.meta-icon {
  font-size: 24rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #666;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-date {
  font-size: 22rpx;
  color: #999;
}

.status-tag {
  font-size: 20rpx;
  padding: 2rpx 10rpx;
  border-radius: 4rpx;
}

.status-processing { background: #fff3e0; color: #f39c12; }
.status-completed { background: #e8f5e9; color: #27ae60; }
.status-failed { background: #fdecea; color: #e74c3c; }
</style>
