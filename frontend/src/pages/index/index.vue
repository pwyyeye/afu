<template>
  <view class="page">
    <!-- Header -->
    <view class="header">
      <view class="header-left">
        <text class="title">阿福健康</text>
        <text class="subtitle">您的AI健康助手</text>
      </view>
      <view class="header-right" @tap="goTo('/pages/profile/index')">
        <text class="avatar-icon">👤</text>
      </view>
    </view>

    <!-- Quick Actions -->
    <view class="quick-actions">
      <view class="action-item" @tap="goTo('/pages/qa/chat')">
        <view class="action-icon-wrap action-blue">
          <text class="action-icon">💬</text>
        </view>
        <text class="action-text">健康问答</text>
      </view>
      <view class="action-item" @tap="goTo('/pages/report/upload')">
        <view class="action-icon-wrap action-green">
          <text class="action-icon">📋</text>
        </view>
        <text class="action-text">报告解读</text>
      </view>
      <view class="action-item" @tap="goTo('/pages/health/diary')">
        <view class="action-icon-wrap action-orange">
          <text class="action-icon">📝</text>
        </view>
        <text class="action-text">健康日记</text>
      </view>
      <view class="action-item" @tap="goTo('/pages/health/goals')">
        <view class="action-icon-wrap action-purple">
          <text class="action-icon">🎯</text>
        </view>
        <text class="action-text">健康目标</text>
      </view>
    </view>

    <!-- Health Overview -->
    <view class="section">
      <text class="section-title">健康概览</text>
      <view class="overview-card">
        <view class="overview-item">
          <text class="overview-value" :class="bmiClass">{{ bmi }}</text>
          <text class="overview-label">BMI</text>
        </view>
        <view class="overview-divider" />
        <view class="overview-item">
          <text class="overview-value">{{ profile?.height_cm || '--' }}</text>
          <text class="overview-label">身高cm</text>
        </view>
        <view class="overview-divider" />
        <view class="overview-item">
          <text class="overview-value">{{ profile?.weight_kg || '--' }}</text>
          <text class="overview-label">体重kg</text>
        </view>
      </view>
    </view>

    <!-- Health Tips -->
    <view class="section">
      <text class="section-title">健康小贴士</text>
      <view class="tip-card">
        <text class="tip-icon">💡</text>
        <text class="tip-text">{{ currentTip }}</text>
      </view>
    </view>

    <!-- Recent Entries -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">最近动态</text>
        <text class="section-more" @tap="goTo('/pages/health/timeline')">查看全部 ›</text>
      </view>
      <view v-for="item in recentTimeline" :key="item.id" class="recent-item" @tap="goTo('/pages/health/timeline')">
        <text class="recent-icon">{{ timelineIcon(item.type) }}</text>
        <view class="recent-info">
          <text class="recent-title">{{ item.title }}</text>
          <text class="recent-date">{{ item.date }}</text>
        </view>
      </view>
      <view v-if="recentTimeline.length === 0" class="recent-empty">
        <text class="recent-empty-text">暂无记录，快去体验吧</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()
const profile = computed(() => healthStore.profile)

const tips = [
  '每天保持8杯水的饮水习惯，有助于新陈代谢和身体健康。',
  '饭后百步走，活到九十九。适量运动是最好的养生方式。',
  '保持规律作息，每晚7-8小时睡眠，让身体充分恢复。',
  '多吃蔬菜水果，每天至少5份，补充维生素和膳食纤维。',
  '定期体检是预防疾病的关键，建议每年至少一次。',
  '保持心情愉悦，笑一笑十年少，愁一愁白了头。',
]
const currentTip = ref(tips[0])

const bmi = computed(() => {
  const h = Number(profile.value?.height_cm) / 100
  const w = Number(profile.value?.weight_kg)
  if (h > 0 && w > 0) return (w / (h * h)).toFixed(1)
  return '--'
})

const bmiClass = computed(() => {
  const val = Number(bmi.value)
  if (isNaN(val)) return ''
  if (val < 18.5) return 'bmi-under'
  if (val < 24) return 'bmi-normal'
  if (val < 28) return 'bmi-over'
  return 'bmi-obese'
})

const recentTimeline = computed(() => healthStore.timeline.slice(0, 3))

function timelineIcon(type?: string): string {
  const icons: Record<string, string> = { report: '📊', diary: '📝', goal: '🎯', reminder: '⏰' }
  return icons[type || ''] || '📌'
}

onMounted(async () => {
  currentTip.value = tips[Math.floor(Math.random() * tips.length)]
  try {
    await healthStore.fetchProfile()
    await healthStore.fetchTimeline()
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
  padding-top: 16rpx;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
}

.subtitle {
  font-size: 26rpx;
  color: #999;
  margin-top: 4rpx;
}

.header-right {
  padding: 8rpx;
}

.avatar-icon {
  font-size: 48rpx;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
  margin-bottom: 32rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.action-icon-wrap {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-blue { background: #e3f2fd; }
.action-green { background: #e8f5e9; }
.action-orange { background: #fff3e0; }
.action-purple { background: #f3e5f5; }

.action-icon {
  font-size: 40rpx;
}

.action-text {
  font-size: 24rpx;
  color: #666;
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
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.section-more {
  font-size: 24rpx;
  color: #4a90d9;
  margin-bottom: 16rpx;
}

.overview-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 16rpx;
  padding: 28rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.overview-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.overview-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
}

.bmi-under { color: #3498db; }
.bmi-normal { color: #27ae60; }
.bmi-over { color: #f39c12; }
.bmi-obese { color: #e74c3c; }

.overview-label {
  font-size: 22rpx;
  color: #999;
}

.overview-divider {
  width: 1rpx;
  height: 60rpx;
  background: #f0f0f0;
}

.tip-card {
  display: flex;
  align-items: flex-start;
  gap: 16rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 28rpx;
  border-left: 6rpx solid #4a90d9;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.tip-icon {
  font-size: 32rpx;
  flex-shrink: 0;
}

.tip-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: #fff;
  border-radius: 12rpx;
  margin-bottom: 8rpx;
}

.recent-icon {
  font-size: 32rpx;
}

.recent-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-title {
  font-size: 26rpx;
  color: #333;
}

.recent-date {
  font-size: 22rpx;
  color: #999;
}

.recent-empty {
  padding: 32rpx;
  text-align: center;
  background: #fff;
  border-radius: 12rpx;
}

.recent-empty-text {
  font-size: 24rpx;
  color: #ccc;
}
</style>
