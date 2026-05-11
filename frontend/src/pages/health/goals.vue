<template>
  <view class="page">
    <!-- Add Goal -->
    <button class="add-btn" @tap="showAdd = !showAdd">
      <text class="add-icon">{{ showAdd ? '−' : '+' }}</text>
      <text>{{ showAdd ? '收起' : '新建目标' }}</text>
    </button>

    <view v-if="showAdd" class="add-form">
      <view class="form-item">
        <text class="form-label">目标名称</text>
        <input v-model="newGoal.title" placeholder="如：每天走8000步" class="form-input" />
      </view>
      <view class="form-item">
        <text class="form-label">分类</text>
        <view class="category-options">
          <view
            v-for="(cat, idx) in categories"
            :key="cat.value"
            :class="['cat-item', categoryIndex === idx ? 'cat-active' : '']"
            @tap="selectCategory(idx)"
          >
            <text class="cat-icon">{{ cat.icon }}</text>
            <text class="cat-label">{{ cat.label }}</text>
          </view>
        </view>
      </view>
      <view class="form-item">
        <text class="form-label">目标值</text>
        <input v-model="newGoal.target_value" placeholder="如：30（天）" type="number" class="form-input" />
      </view>
      <view class="form-item">
        <text class="form-label">单位</text>
        <input v-model="newGoal.unit" placeholder="如：天、次、公里" class="form-input" />
      </view>
      <button class="save-btn" :disabled="!newGoal.title" @tap="createGoal">创建目标</button>
    </view>

    <!-- Active Goals -->
    <view v-if="activeGoals.length" class="section">
      <text class="section-title">进行中</text>
      <view v-for="goal in activeGoals" :key="goal.id" class="goal-card" @tap="showGoalActions(goal)">
        <view class="goal-header">
          <view class="goal-left">
            <text class="goal-icon">{{ categoryIcon(goal.category) }}</text>
            <view class="goal-info">
              <text class="goal-title">{{ goal.title }}</text>
              <text class="goal-category">{{ categoryLabel(goal.category) }}</text>
            </view>
          </view>
          <view class="goal-status status-active">
            <text>进行中</text>
          </view>
        </view>
        <view v-if="goal.target_value" class="goal-progress">
          <view class="progress-bar">
            <view class="progress-fill" :style="{ width: progressPercent(goal) + '%' }" />
          </view>
          <text class="progress-text">{{ goal.current_value || 0 }} / {{ goal.target_value }} {{ goal.unit || '' }}</text>
        </view>
      </view>
    </view>

    <!-- Completed Goals -->
    <view v-if="completedGoals.length" class="section">
      <text class="section-title">已完成</text>
      <view v-for="goal in completedGoals" :key="goal.id" class="goal-card completed-card">
        <view class="goal-header">
          <view class="goal-left">
            <text class="goal-icon">{{ categoryIcon(goal.category) }}</text>
            <view class="goal-info">
              <text class="goal-title">{{ goal.title }}</text>
              <text class="goal-category">{{ categoryLabel(goal.category) }}</text>
            </view>
          </view>
          <view class="goal-status status-completed">
            <text>已完成</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Empty -->
    <view v-if="healthStore.goals.length === 0 && !showAdd" class="empty">
      <text class="empty-icon">🎯</text>
      <text class="empty-text">暂无健康目标</text>
      <text class="empty-desc">设定一个小目标，让健康习惯坚持下去</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()
const showAdd = ref(false)
const newGoal = ref({
  title: '',
  category: 'exercise',
  target_value: '',
  unit: '',
})

const categories = [
  { value: 'exercise', label: '运动', icon: '🏃' },
  { value: 'diet', label: '饮食', icon: '🥗' },
  { value: 'habit', label: '习惯', icon: '✅' },
  { value: 'checkup', label: '体检', icon: '🏥' },
]
const categoryIndex = ref(0)

const activeGoals = computed(() => healthStore.goals.filter((g) => g.status === 'active'))
const completedGoals = computed(() => healthStore.goals.filter((g) => g.status === 'completed'))

onMounted(() => {
  healthStore.fetchGoals()
})

function selectCategory(idx: number) {
  categoryIndex.value = idx
  newGoal.value.category = categories[idx].value
}

function categoryIcon(cat?: string): string {
  const found = categories.find((c) => c.value === cat)
  return found?.icon || '📌'
}

function categoryLabel(cat?: string): string {
  const found = categories.find((c) => c.value === cat)
  return found?.label || '其他'
}

function progressPercent(goal: any): number {
  if (!goal.target_value) return 0
  const current = Number(goal.current_value || 0)
  const target = Number(goal.target_value)
  return Math.min(100, Math.round((current / target) * 100))
}

function showGoalActions(goal: any) {
  uni.showActionSheet({
    itemList: ['更新进度', '标记完成', '暂停', '删除'],
    success: async (res) => {
      switch (res.tapIndex) {
        case 0:
          updateGoalProgress(goal)
          break
        case 1:
          await healthStore.updateGoal(goal.id, { status: 'completed' })
          uni.showToast({ title: '已标记完成', icon: 'success' })
          break
        case 2:
          await healthStore.updateGoal(goal.id, { status: 'paused' })
          uni.showToast({ title: '已暂停', icon: 'success' })
          break
        case 3:
          uni.showModal({
            title: '确认删除',
            content: '确定删除该目标？',
            confirmColor: '#E07070',
            success: async (r) => {
              if (r.confirm) {
                await healthStore.deleteGoal(goal.id)
                uni.showToast({ title: '已删除', icon: 'success' })
              }
            },
          })
          break
      }
    },
  })
}

function updateGoalProgress(goal: any) {
  uni.showModal({
    title: '更新进度',
    editable: true,
    placeholderText: `当前进度（目标: ${goal.target_value} ${goal.unit || ''}）`,
    success: async (res) => {
      if (res.confirm && res.content) {
        const value = Number(res.content)
        if (isNaN(value)) {
          uni.showToast({ title: '请输入数字', icon: 'none' })
          return
        }
        const newStatus = value >= Number(goal.target_value) ? 'completed' : 'active'
        await healthStore.updateGoal(goal.id, {
          current_value: value,
          status: newStatus,
        })
        uni.showToast({ title: '进度已更新', icon: 'success' })
      }
    },
  })
}

async function createGoal() {
  if (!newGoal.value.title) return
  try {
    await healthStore.createGoal({
      title: newGoal.value.title,
      category: newGoal.value.category,
      target_value: newGoal.value.target_value ? Number(newGoal.value.target_value) : undefined,
      unit: newGoal.value.unit || undefined,
    })
    newGoal.value = { title: '', category: 'exercise', target_value: '', unit: '' }
    showAdd.value = false
    uni.showToast({ title: '创建成功', icon: 'success' })
  } catch {
    uni.showToast({ title: '创建失败', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.add-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: linear-gradient(135deg, #5CB87A, #4A9E66);
  color: #fff;
  font-size: 30rpx;
  font-weight: 500;
  border-radius: 20rpx;
  border: none;
  margin-bottom: 24rpx;
  box-shadow: 0 8rpx 24rpx rgba(39, 174, 96, 0.3);
}

.add-icon {
  font-size: 36rpx;
  font-weight: bold;
}

.add-form {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.form-item {
  margin-bottom: 20rpx;
}

.form-label {
  font-size: 26rpx;
  color: #6B6B70;
  margin-bottom: 12rpx;
  display: block;
}

.form-input {
  width: 100%;
  height: 80rpx;
  font-size: 28rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  padding: 0 16rpx;
}

.category-options {
  display: flex;
  gap: 16rpx;
}

.cat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  padding: 16rpx 0;
  border-radius: 12rpx;
  background: #f8f9fa;

  &.cat-active {
    background: #E8F8EF;
    box-shadow: 0 0 0 2rpx #5CB87A;
  }
}

.cat-icon {
  font-size: 36rpx;
}

.cat-label {
  font-size: 24rpx;
  color: #2C2C2E;
}

.save-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background: #5CB87A;
  color: #fff;
  font-size: 30rpx;
  font-weight: 500;
  border-radius: 12rpx;
  border: none;
  margin-top: 8rpx;

  &[disabled] {
    background: #a0d8b0;
  }
}

.section {
  margin-bottom: 32rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 16rpx;
  display: block;
}

.goal-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.completed-card {
  opacity: 0.7;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.goal-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.goal-icon {
  font-size: 36rpx;
}

.goal-info {
  display: flex;
  flex-direction: column;
}

.goal-title {
  font-size: 30rpx;
  color: #2C2C2E;
  font-weight: 500;
}

.goal-category {
  font-size: 22rpx;
  color: #A0A0A5;
  margin-top: 4rpx;
}

.goal-status {
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 999rpx;
}

.status-active {
  background: #E8F8EF;
  color: #5CB87A;
}

.status-completed {
  background: #E8F4F8;
  color: #5A9BB8;
}

.goal-progress {
  margin-top: 16rpx;
}

.progress-bar {
  height: 12rpx;
  background: #f0f0f0;
  border-radius: 6rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #5CB87A, #70D494);
  border-radius: 6rpx;
  transition: width 0.3s;
}

.progress-text {
  font-size: 22rpx;
  color: #A0A0A5;
  margin-top: 8rpx;
  display: block;
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
}
</style>
