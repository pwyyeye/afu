<template>
  <view class="page">
    <!-- Filter tabs -->
    <view class="filter-bar">
      <view
        v-for="tab in tabs"
        :key="tab.value"
        class="filter-tab"
        :class="{ active: activeTab === tab.value }"
        @tap="activeTab = tab.value"
      >
        <text>{{ tab.label }}</text>
      </view>
    </view>

    <!-- Timeline -->
    <view v-if="filteredTimeline.length > 0" class="timeline">
      <view v-for="(group, date) in groupedTimeline" :key="date" class="timeline-group">
        <text class="group-date">{{ date }}</text>
        <view
          v-for="item in group"
          :key="item.id"
          class="timeline-item"
        >
          <view class="timeline-dot" :class="dotClass(item.type)" />
          <view class="timeline-content">
            <view class="timeline-header">
              <text class="timeline-icon">{{ typeIcon(item.type) }}</text>
              <text class="timeline-title">{{ item.title }}</text>
            </view>
            <text v-if="item.description" class="timeline-desc">{{ item.description }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Empty -->
    <view v-else class="empty">
      <text class="empty-icon">📋</text>
      <text class="empty-text">暂无健康记录</text>
      <text class="empty-desc">完成体检、建立健康档案后，记录会自动出现在这里</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()
const activeTab = ref('all')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '体检', value: 'report' },
  { label: '日记', value: 'diary' },
  { label: '目标', value: 'goal' },
]

onMounted(() => {
  healthStore.fetchTimeline()
})

const filteredTimeline = computed(() => {
  if (activeTab.value === 'all') return healthStore.timeline
  return healthStore.timeline.filter((t) => t.type === activeTab.value)
})

const groupedTimeline = computed(() => {
  const groups: Record<string, typeof filteredTimeline.value> = {}
  for (const item of filteredTimeline.value) {
    const date = item.date?.slice(0, 10) || '未知日期'
    if (!groups[date]) groups[date] = []
    groups[date].push(item)
  }
  return groups
})

function typeIcon(type?: string): string {
  const icons: Record<string, string> = {
    report: '📊',
    diary: '📝',
    goal: '🎯',
    reminder: '⏰',
  }
  return icons[type || ''] || '📌'
}

function dotClass(type?: string): string {
  return `dot-${type || 'default'}`
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.filter-bar {
  display: flex;
  gap: 16rpx;
  margin-bottom: 32rpx;
  overflow-x: auto;
}

.filter-tab {
  padding: 12rpx 32rpx;
  border-radius: 999rpx;
  background: #f0f0f0;
  font-size: 26rpx;
  color: #6B6B70;
  white-space: nowrap;

  &.active {
    background: #3B82A0;
    color: #fff;
  }
}

.timeline-group {
  margin-bottom: 32rpx;
}

.group-date {
  font-size: 24rpx;
  color: #A0A0A5;
  font-weight: 500;
  margin-bottom: 16rpx;
  display: block;
  padding-left: 36rpx;
}

.timeline-item {
  display: flex;
  gap: 20rpx;
  padding-bottom: 24rpx;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 14rpx;
    top: 28rpx;
    bottom: 0;
    width: 2rpx;
    background: #E8E5E0;
  }

  &:last-child::before {
    display: none;
  }
}

.timeline-dot {
  width: 28rpx;
  height: 28rpx;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4rpx;
}

.dot-report { background: #3B82A0; }
.dot-diary { background: #5CB87A; }
.dot-goal { background: #E8B84A; }
.dot-reminder { background: #E07070; }
.dot-default { background: #A0A0A5; }

.timeline-content {
  flex: 1;
  background: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.timeline-icon {
  font-size: 28rpx;
}

.timeline-title {
  font-size: 28rpx;
  color: #2C2C2E;
  font-weight: 500;
}

.timeline-desc {
  font-size: 24rpx;
  color: #6B6B70;
  margin-top: 8rpx;
  display: block;
  line-height: 1.5;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 48rpx;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #A0A0A5;
  margin-bottom: 12rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #C5C5C8;
  text-align: center;
  line-height: 1.5;
}
</style>
