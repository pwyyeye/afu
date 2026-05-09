<template>
  <view class="page">
    <text class="page-title">趋势对比</text>
    <text class="page-desc">查看关键指标的变化趋势</text>

    <view class="filter-section">
      <text class="filter-label">选择指标</text>
      <view class="filter-chips">
        <view
          v-for="name in availableIndicators"
          :key="name"
          :class="['chip', selectedIndicators.includes(name) ? 'chip-active' : '']"
          @tap="toggleIndicator(name)"
        >
          <text class="chip-text">{{ name }}</text>
        </view>
      </view>
    </view>

    <view v-if="trendData.length > 0" class="chart-section">
      <view v-for="trend in trendData" :key="trend.name" class="chart-card">
        <text class="chart-title">{{ trend.name }} {{ trend.unit ? `(${trend.unit})` : '' }}</text>
        <view class="chart-area">
          <view
            v-for="(point, idx) in trend.data"
            :key="idx"
            class="chart-bar-wrapper"
          >
            <view
              class="chart-bar"
              :style="{ height: `${getBarHeight(point.value, trend.data)}%` }"
            />
            <text class="chart-value">{{ point.value }}</text>
            <text class="chart-year">{{ point.year }}</text>
          </view>
        </view>
      </view>
    </view>

    <view v-else-if="selectedIndicators.length > 0" class="empty">
      <text class="empty-text">暂无对比数据</text>
    </view>

    <view v-else class="empty">
      <text class="empty-text">请选择要对比的指标</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useReportStore } from '@/stores/report'
import type { TrendData as TrendDataType } from '@/types/report'

const reportStore = useReportStore()
const availableIndicators = ref<string[]>(['空腹血糖', '总胆固醇', '甘油三酯', '血红蛋白', '尿酸'])
const selectedIndicators = ref<string[]>([])
const trendData = ref<TrendDataType[]>([])

function toggleIndicator(name: string) {
  const idx = selectedIndicators.value.indexOf(name)
  if (idx >= 0) {
    selectedIndicators.value.splice(idx, 1)
  } else {
    selectedIndicators.value.push(name)
  }
}

watch(selectedIndicators, async (names) => {
  if (names.length === 0) {
    trendData.value = []
    return
  }
  try {
    const years = ['2022', '2023', '2024', '2025']
    trendData.value = await reportStore.fetchComparison(names, years)
  } catch {
    trendData.value = []
  }
}, { immediate: true })

function getBarHeight(value: number, data: { value: number }[]) {
  const max = Math.max(...data.map((d) => d.value))
  return max > 0 ? (value / max) * 80 : 0
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
}

.page-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
}

.page-desc {
  font-size: 26rpx;
  color: #999;
  margin-top: 8rpx;
  display: block;
  margin-bottom: 32rpx;
}

.filter-section {
  margin-bottom: 32rpx;
}

.filter-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.chip {
  padding: 12rpx 24rpx;
  background: #fff;
  border-radius: 999rpx;
  border: 2rpx solid #e8e8e8;
}

.chip-active {
  background: #e8f0fe;
  border-color: #4a90d9;
}

.chip-text {
  font-size: 26rpx;
  color: #666;
}

.chip-active .chip-text {
  color: #4a90d9;
}

.chart-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.chart-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.chart-area {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 300rpx;
  gap: 16rpx;
}

.chart-bar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
  justify-content: flex-end;
}

.chart-bar {
  width: 48rpx;
  background: linear-gradient(180deg, #4a90d9 0%, #6ba3e0 100%);
  border-radius: 8rpx 8rpx 0 0;
  min-height: 10rpx;
}

.chart-value {
  font-size: 22rpx;
  color: #4a90d9;
  margin-top: 8rpx;
}

.chart-year {
  font-size: 22rpx;
  color: #999;
  margin-top: 4rpx;
}

.empty {
  padding: 80rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}
</style>
