<template>
  <view class="indicator-row" @tap="expanded = !expanded">
    <view class="indicator-header">
      <view :class="['light-dot', `dot-${indicator.light}`]" />
      <text class="indicator-name">{{ indicator.name }}</text>
      <text class="indicator-value" :class="{ 'value-abnormal': indicator.light !== 'green' }">
        {{ indicator.value }}
        <text v-if="indicator.unit" class="indicator-unit">{{ indicator.unit }}</text>
      </text>
    </view>

    <view v-if="indicator.reference_range" class="indicator-meta">
      <text class="meta-label">参考范围:</text>
      <text class="meta-value">{{ indicator.reference_range }}</text>
      <text v-if="indicator.trend" :class="['trend-tag', `trend-${indicator.trend}`]">
        {{ trendLabels[indicator.trend] }}
      </text>
    </view>

    <view v-if="expanded && indicator.explanation" class="indicator-explanation">
      <text class="explanation-text">{{ indicator.explanation }}</text>
    </view>

    <text class="expand-hint">{{ expanded ? '收起' : '查看详情' }}</text>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ReportIndicator } from '@/types/report'

defineProps<{
  indicator: ReportIndicator
}>()

const expanded = ref(false)

const trendLabels: Record<string, string> = {
  rising: '↑ 上升',
  falling: '↓ 下降',
  stable: '→ 稳定',
}
</script>

<style scoped lang="scss">
.indicator-row {
  background: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 12rpx;
}

.indicator-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.light-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-red { background: #e74c3c; }
.dot-yellow { background: #f39c12; }
.dot-blue { background: #3498db; }
.dot-green { background: #27ae60; }

.indicator-name {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.indicator-value {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.value-abnormal {
  color: #e74c3c;
}

.indicator-unit {
  font-size: 22rpx;
  color: #999;
  font-weight: normal;
}

.indicator-meta {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-top: 12rpx;
  padding-top: 12rpx;
  border-top: 1rpx solid #f5f5f5;
}

.meta-label {
  font-size: 22rpx;
  color: #999;
}

.meta-value {
  font-size: 22rpx;
  color: #666;
}

.trend-tag {
  font-size: 20rpx;
  padding: 2rpx 8rpx;
  border-radius: 4rpx;
  margin-left: auto;
}

.trend-rising { background: #fdecea; color: #e74c3c; }
.trend-falling { background: #e8f5e9; color: #27ae60; }
.trend-stable { background: #e3f2fd; color: #3498db; }

.indicator-explanation {
  margin-top: 12rpx;
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
}

.explanation-text {
  font-size: 24rpx;
  color: #666;
  line-height: 1.6;
}

.expand-hint {
  display: block;
  text-align: center;
  font-size: 22rpx;
  color: #4a90d9;
  margin-top: 8rpx;
}
</style>
