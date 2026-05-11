<template>
  <view class="page">
    <view class="upload-area" @tap="goToUpload">
      <text class="upload-icon">📷</text>
      <text class="upload-text">拍照或上传体检报告</text>
      <text class="upload-desc">支持图片和PDF格式</text>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-title">我的报告</text>
        <text class="section-action" @tap="goToCompare">趋势对比</text>
      </view>

      <ReportCard
        v-for="report in reportStore.reports"
        :key="report.id"
        :report="report"
        @tap="goToDetail(report.id)"
      />

      <view v-if="reportStore.reports.length === 0" class="empty">
        <text class="empty-icon">📋</text>
        <text class="empty-text">暂无报告</text>
        <text class="empty-desc">上传您的第一份体检报告</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onShow } from '@dcloudio/uni-app'
import { useReportStore } from '@/stores/report'
import ReportCard from '@/components/report/ReportCard.vue'

const reportStore = useReportStore()

onShow(() => {
  reportStore.fetchReports()
})

function goToUpload() {
  uni.navigateTo({ url: '/pages/report/upload' })
}

function goToDetail(id: string) {
  uni.navigateTo({ url: `/pages/report/detail?id=${id}` })
}

function goToCompare() {
  uni.navigateTo({ url: '/pages/report/compare' })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48rpx;
  background: linear-gradient(135deg, #3B82A0 0%, #5A9BB8 100%);
  border-radius: 20rpx;
  margin-bottom: 32rpx;
}

.upload-icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
}

.upload-text {
  font-size: 32rpx;
  color: #fff;
  font-weight: 500;
}

.upload-desc {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 8rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2C2C2E;
}

.section-action {
  font-size: 26rpx;
  color: #3B82A0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 0;
}

.empty-icon {
  font-size: 64rpx;
  margin-bottom: 16rpx;
}

.empty-text {
  font-size: 30rpx;
  color: #A0A0A5;
}

.empty-desc {
  font-size: 24rpx;
  color: #C5C5C8;
  margin-top: 12rpx;
}
</style>
