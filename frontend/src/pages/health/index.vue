<template>
  <view class="page">
    <!-- Menu Grid -->
    <view class="menu-grid">
      <view class="menu-item" @tap="goTo('/pages/health/profile')">
        <view class="menu-icon-wrap bg-blue">
          <text class="menu-icon">👤</text>
        </view>
        <text class="menu-text">个人档案</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/family')">
        <view class="menu-icon-wrap bg-green">
          <text class="menu-icon">👨‍👩‍👧‍👦</text>
        </view>
        <text class="menu-text">家庭成员</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/diary')">
        <view class="menu-icon-wrap bg-orange">
          <text class="menu-icon">📝</text>
        </view>
        <text class="menu-text">健康日记</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/goals')">
        <view class="menu-icon-wrap bg-purple">
          <text class="menu-icon">🎯</text>
        </view>
        <text class="menu-text">健康目标</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/timeline')">
        <view class="menu-icon-wrap bg-teal">
          <text class="menu-icon">📅</text>
        </view>
        <text class="menu-text">时间线</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/qa/chat')">
        <view class="menu-icon-wrap bg-red">
          <text class="menu-icon">💬</text>
        </view>
        <text class="menu-text">问医生</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/report/upload')">
        <view class="menu-icon-wrap bg-cyan">
          <text class="menu-icon">📋</text>
        </view>
        <text class="menu-text">查报告</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/profile/settings')">
        <view class="menu-icon-wrap bg-gray">
          <text class="menu-icon">⚙️</text>
        </view>
        <text class="menu-text">设置</text>
      </view>
    </view>

    <!-- Health Summary -->
    <view class="section">
      <text class="section-title">健康概况</text>
      <view class="summary-card">
        <view class="summary-row">
          <view class="summary-item">
            <text class="summary-value">{{ familyCount }}</text>
            <text class="summary-label">家庭成员</text>
          </view>
          <view class="summary-divider" />
          <view class="summary-item">
            <text class="summary-value">{{ diaryCount }}</text>
            <text class="summary-label">日记记录</text>
          </view>
          <view class="summary-divider" />
          <view class="summary-item">
            <text class="summary-value">{{ goalCount }}</text>
            <text class="summary-label">进行中目标</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Recent Timeline -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">最近动态</text>
        <text class="section-more" @tap="goTo('/pages/health/timeline')">查看全部 ›</text>
      </view>
      <view v-for="item in recentItems" :key="item.id" class="timeline-item" @tap="goTo('/pages/health/timeline')">
        <text class="tl-icon">{{ typeIcon(item.type) }}</text>
        <view class="tl-info">
          <text class="tl-title">{{ item.title }}</text>
          <text v-if="item.description" class="tl-desc">{{ item.description }}</text>
        </view>
        <text class="tl-date">{{ item.date?.slice(5) }}</text>
      </view>
      <view v-if="recentItems.length === 0" class="empty">
        <text class="empty-text">暂无健康记录</text>
        <text class="empty-desc">建立健康档案、记录日记后会出现在这里</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()

const familyCount = computed(() => healthStore.familyMembers.length)
const diaryCount = computed(() => healthStore.diaries.length)
const goalCount = computed(() => healthStore.goals.filter((g) => g.status === 'active').length)
const recentItems = computed(() => healthStore.timeline.slice(0, 5))

function typeIcon(type?: string): string {
  const icons: Record<string, string> = { report: '📊', diary: '📝', goal: '🎯', reminder: '⏰' }
  return icons[type || ''] || '📌'
}

onMounted(async () => {
  try {
    await Promise.all([
      healthStore.fetchFamily(),
      healthStore.fetchDiaries(),
      healthStore.fetchGoals(),
      healthStore.fetchTimeline(),
    ])
  } catch {}
})

function goTo(url: string) {
  uni.navigateTo({ url })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24rpx;
  margin-bottom: 32rpx;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.menu-icon-wrap {
  width: 96rpx;
  height: 96rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-blue { background: #E8F4F8; }
.bg-green { background: #E8F8EF; }
.bg-orange { background: #FFF3E6; }
.bg-purple { background: #f3e5f5; }
.bg-teal { background: #e0f2f1; }
.bg-red { background: #ffebee; }
.bg-cyan { background: #e0f7fa; }
.bg-gray { background: #f5f5f5; }

.menu-icon {
  font-size: 40rpx;
}

.menu-text {
  font-size: 24rpx;
  color: #6B6B70;
}

.section {
  margin-bottom: 32rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 16rpx;
  display: block;
}

.section-more {
  font-size: 24rpx;
  color: #3B82A0;
  margin-bottom: 16rpx;
}

.summary-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.summary-row {
  display: flex;
  align-items: center;
}

.summary-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.summary-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #3B82A0;
}

.summary-label {
  font-size: 22rpx;
  color: #A0A0A5;
}

.summary-divider {
  width: 1rpx;
  height: 60rpx;
  background: #f0f0f0;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: #fff;
  border-radius: 12rpx;
  margin-bottom: 8rpx;
}

.tl-icon {
  font-size: 28rpx;
  flex-shrink: 0;
}

.tl-info {
  flex: 1;
  min-width: 0;
}

.tl-title {
  font-size: 26rpx;
  color: #2C2C2E;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tl-desc {
  font-size: 22rpx;
  color: #A0A0A5;
  display: block;
  margin-top: 4rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tl-date {
  font-size: 22rpx;
  color: #C5C5C8;
  flex-shrink: 0;
}

.empty {
  padding: 48rpx;
  text-align: center;
  background: #fff;
  border-radius: 12rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #A0A0A5;
  display: block;
}

.empty-desc {
  font-size: 22rpx;
  color: #C5C5C8;
  margin-top: 8rpx;
  display: block;
}
</style>
