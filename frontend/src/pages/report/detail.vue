<template>
  <view class="page">
    <view v-if="report" class="report-detail">
      <!-- Summary -->
      <view class="summary-card">
        <view class="summary-header">
          <text class="summary-title">{{ report.title }}</text>
          <TrafficLight
            :level="report.overall_light"
            :label="lightLabels[report.overall_light]"
          />
        </view>
        <text v-if="report.summary" class="summary-text">{{ report.summary }}</text>
      </view>

      <!-- Indicators -->
      <view class="section">
        <text class="section-title">指标详情</text>
        <IndicatorRow
          v-for="indicator in report.indicators"
          :key="indicator.id"
          :indicator="indicator"
        />
      </view>

      <!-- Action Plan -->
      <ActionPlan
        v-if="report.action_plan?.length"
        :actions="report.action_plan"
      />

      <!-- Actions -->
      <view class="bottom-actions">
        <button class="action-btn" @tap="saveToArchive">存入健康档案</button>
        <button class="action-btn secondary" @tap="goToCompare">查看趋势</button>
      </view>
    </view>

    <view v-else class="loading">
      <text class="loading-text">加载中...</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useReportStore } from '@/stores/report'
import TrafficLight from '@/components/report/TrafficLight.vue'
import IndicatorRow from '@/components/report/IndicatorRow.vue'
import ActionPlan from '@/components/report/ActionPlan.vue'
import type { MedicalReport } from '@/types/report'

const reportStore = useReportStore()
const report = ref<MedicalReport | null>(null)

const lightLabels: Record<string, string> = {
  red: '紧急关注',
  yellow: '需要关注',
  blue: '定期随访',
  green: '基本正常',
}

onLoad(async (options) => {
  if (options?.id) {
    report.value = await reportStore.fetchReportDetail(options.id)
  }
})

function saveToArchive() {
  uni.showToast({ title: '已存入健康档案', icon: 'success' })
}

function goToCompare() {
  uni.navigateTo({ url: '/pages/report/compare' })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 180rpx;
}

.summary-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.summary-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2C2C2E;
}

.summary-text {
  font-size: 26rpx;
  color: #6B6B70;
  line-height: 1.6;
}

.section {
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 16rpx;
  display: block;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 16rpx;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  background: #fff;
  border-top: 1rpx solid #E8E5E0;
}

.action-btn {
  flex: 1;
  height: 88rpx;
  line-height: 88rpx;
  background: #3B82A0;
  color: #fff;
  font-size: 28rpx;
  border-radius: 12rpx;
  border: none;
}

.action-btn.secondary {
  background: #fff;
  color: #3B82A0;
  border: 2rpx solid #3B82A0;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 120rpx 0;
}

.loading-text {
  font-size: 28rpx;
  color: #A0A0A5;
}
</style>
