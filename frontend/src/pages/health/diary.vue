<template>
  <view class="page">
    <!-- Write Area -->
    <view class="write-card">
      <text class="section-title">记录今日健康</text>
      <textarea
        v-model="content"
        placeholder="今天身体感觉如何？有什么想记录的..."
        class="diary-input"
        maxlength="500"
      />

      <!-- Mood Selection -->
      <view class="mood-row">
        <text class="mood-label">心情</text>
        <view class="mood-options">
          <view
            v-for="m in moods"
            :key="m.value"
            :class="['mood-item', selectedMood === m.value ? 'mood-active' : '']"
            @tap="selectedMood = selectedMood === m.value ? '' : m.value"
          >
            <text class="mood-icon">{{ m.icon }}</text>
            <text class="mood-text">{{ m.label }}</text>
          </view>
        </view>
      </view>

      <!-- Tags -->
      <view class="tags-row">
        <text class="mood-label">标签</text>
        <view class="tags-wrap">
          <view
            v-for="tag in availableTags"
            :key="tag"
            :class="['tag-item', selectedTags.includes(tag) ? 'tag-active' : '']"
            @tap="toggleTag(tag)"
          >
            <text>{{ tag }}</text>
          </view>
        </view>
      </view>

      <!-- Metrics -->
      <view class="metrics-row">
        <view class="metric-item">
          <text class="metric-label">体重(kg)</text>
          <input v-model="weight" type="digit" placeholder="--" class="metric-input" />
        </view>
        <view class="metric-item">
          <text class="metric-label">睡眠(h)</text>
          <input v-model="sleep" type="digit" placeholder="--" class="metric-input" />
        </view>
        <view class="metric-item">
          <text class="metric-label">步数</text>
          <input v-model="steps" type="number" placeholder="--" class="metric-input" />
        </view>
      </view>

      <button class="save-btn" :disabled="!content.trim()" @tap="saveDiary">
        保存日记
      </button>
    </view>

    <!-- History -->
    <view class="history-section">
      <text class="section-title">历史记录</text>

      <view v-for="diary in healthStore.diaries" :key="diary.id" class="diary-card">
        <view class="diary-header">
          <view class="diary-date-row">
            <text class="diary-date">{{ formatDate(diary.diary_date) }}</text>
            <text v-if="diary.mood" class="diary-mood">{{ moodMap[diary.mood] }}</text>
          </view>
        </view>
        <text class="diary-content">{{ diary.content }}</text>

        <view v-if="diary.tags && diary.tags.length" class="diary-tags">
          <text v-for="tag in diary.tags" :key="tag" class="diary-tag">{{ tag }}</text>
        </view>

        <view v-if="hasMetrics(diary)" class="diary-metrics">
          <text v-if="diary.metrics?.weight" class="diary-metric">体重 {{ diary.metrics.weight }}kg</text>
          <text v-if="diary.metrics?.sleep" class="diary-metric">睡眠 {{ diary.metrics.sleep }}h</text>
          <text v-if="diary.metrics?.steps" class="diary-metric">步数 {{ diary.metrics.steps }}</text>
        </view>
      </view>

      <view v-if="healthStore.diaries.length === 0" class="empty">
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有日记记录</text>
        <text class="empty-desc">每天花一分钟记录健康状态，养成好习惯</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()
const content = ref('')
const selectedMood = ref('')
const selectedTags = ref<string[]>([])
const weight = ref('')
const sleep = ref('')
const steps = ref('')

const moods = [
  { value: 'great', icon: '😊', label: '很好' },
  { value: 'good', icon: '🙂', label: '不错' },
  { value: 'okay', icon: '😐', label: '一般' },
  { value: 'bad', icon: '😔', label: '较差' },
]

const moodMap: Record<string, string> = {
  great: '😊',
  good: '🙂',
  okay: '😐',
  bad: '😔',
}

const availableTags = ['运动', '饮食清淡', '早睡', '多喝水', '头痛', '疲劳', '感冒', '好心情']

onMounted(() => {
  healthStore.fetchDiaries()
})

function toggleTag(tag: string) {
  const idx = selectedTags.value.indexOf(tag)
  if (idx >= 0) {
    selectedTags.value.splice(idx, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

function hasMetrics(diary: any): boolean {
  const m = diary.metrics
  return m && (m.weight || m.sleep || m.steps)
}

function formatDate(dateStr?: string): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const month = d.getMonth() + 1
  const day = d.getDate()
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  return `${month}月${day}日 周${weekdays[d.getDay()]}`
}

async function saveDiary() {
  if (!content.value.trim()) return
  try {
    const metrics: Record<string, any> = {}
    if (weight.value) metrics.weight = Number(weight.value)
    if (sleep.value) metrics.sleep = Number(sleep.value)
    if (steps.value) metrics.steps = Number(steps.value)

    await healthStore.createDiary({
      content: content.value,
      mood: selectedMood.value as any,
      tags: selectedTags.value,
      metrics: Object.keys(metrics).length ? metrics : undefined,
      diary_date: new Date().toISOString().split('T')[0],
    })

    content.value = ''
    selectedMood.value = ''
    selectedTags.value = []
    weight.value = ''
    sleep.value = ''
    steps.value = ''
    uni.showToast({ title: '保存成功', icon: 'success' })
  } catch {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.write-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 28rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.diary-input {
  width: 100%;
  height: 180rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
  background: #f8f9fa;
  border-radius: 12rpx;
  padding: 16rpx;
}

.mood-row {
  margin-top: 24rpx;
}

.mood-label {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 12rpx;
  display: block;
}

.mood-options {
  display: flex;
  gap: 16rpx;
}

.mood-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  padding: 12rpx 16rpx;
  border-radius: 12rpx;
  background: #f8f9fa;
  opacity: 0.6;
  transition: all 0.2s;

  &.mood-active {
    opacity: 1;
    background: #e8f5e9;
    transform: scale(1.05);
  }
}

.mood-icon {
  font-size: 40rpx;
}

.mood-text {
  font-size: 20rpx;
  color: #666;
}

.tags-row {
  margin-top: 24rpx;
}

.tags-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.tag-item {
  padding: 8rpx 24rpx;
  border-radius: 999rpx;
  background: #f0f0f0;
  font-size: 24rpx;
  color: #666;

  &.tag-active {
    background: #4a90d9;
    color: #fff;
  }
}

.metrics-row {
  display: flex;
  gap: 16rpx;
  margin-top: 24rpx;
}

.metric-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.metric-label {
  font-size: 24rpx;
  color: #666;
}

.metric-input {
  height: 72rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
  text-align: center;
  font-size: 28rpx;
}

.save-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background: linear-gradient(135deg, #4a90d9, #357abd);
  color: #fff;
  font-size: 30rpx;
  font-weight: 500;
  border-radius: 12rpx;
  border: none;
  margin-top: 24rpx;

  &[disabled] {
    background: #a0c4e8;
  }
}

.history-section {
  margin-top: 16rpx;
}

.diary-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.diary-header {
  margin-bottom: 12rpx;
}

.diary-date-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.diary-date {
  font-size: 24rpx;
  color: #999;
}

.diary-mood {
  font-size: 28rpx;
}

.diary-content {
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
}

.diary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-top: 12rpx;
}

.diary-tag {
  font-size: 20rpx;
  padding: 4rpx 16rpx;
  border-radius: 999rpx;
  background: #f0f0f0;
  color: #666;
}

.diary-metrics {
  display: flex;
  gap: 24rpx;
  margin-top: 12rpx;
  padding-top: 12rpx;
  border-top: 1rpx solid #f5f5f5;
}

.diary-metric {
  font-size: 22rpx;
  color: #4a90d9;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 48rpx;
}

.empty-icon {
  font-size: 64rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 30rpx;
  color: #999;
  margin-bottom: 8rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #ccc;
  text-align: center;
}
</style>
