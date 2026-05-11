<template>
  <view class="action-plan">
    <text class="plan-title">健康行动建议</text>
    <view
      v-for="(action, index) in actions"
      :key="index"
      class="action-item"
    >
      <view :class="['priority-bar', `priority-${action.priority}`]" />
      <view class="action-content">
        <view class="action-header">
          <text class="action-category">{{ categoryLabels[action.category] || action.category }}</text>
          <text class="action-title">{{ action.title }}</text>
        </view>
        <text class="action-desc">{{ action.description }}</text>
      </view>
      <view :class="['check-circle', action.checked ? 'checked' : '']" @tap="toggleCheck(index)">
        <text v-if="action.checked" class="check-icon">✓</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ActionPlanItem } from '@/types/report'

const props = defineProps<{
  actions: ActionPlanItem[]
}>()

const categoryLabels: Record<string, string> = {
  checkup: '复查',
  diet: '饮食',
  exercise: '运动',
  medication: '用药',
  lifestyle: '生活方式',
}

const checkedStates = ref<boolean[]>(props.actions.map(() => false))

function toggleCheck(index: number) {
  checkedStates.value[index] = !checkedStates.value[index]
}
</script>

<style scoped lang="scss">
.action-plan {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
}

.plan-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 20rpx;
  display: block;
}

.action-item {
  display: flex;
  gap: 16rpx;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
}

.priority-bar {
  width: 6rpx;
  border-radius: 3rpx;
  flex-shrink: 0;
}

.priority-red { background: #E07070; }
.priority-yellow { background: #E8B84A; }
.priority-blue { background: #5A9BB8; }
.priority-green { background: #5CB87A; }

.action-content {
  flex: 1;
}

.action-header {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 8rpx;
}

.action-category {
  font-size: 20rpx;
  color: #3B82A0;
  background: #E8F4F8;
  padding: 2rpx 8rpx;
  border-radius: 4rpx;
}

.action-title {
  font-size: 28rpx;
  color: #2C2C2E;
  font-weight: 500;
}

.action-desc {
  font-size: 24rpx;
  color: #6B6B70;
  line-height: 1.5;
}

.check-circle {
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  border: 2rpx solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 4rpx;
}

.check-circle.checked {
  background: #5CB87A;
  border-color: #5CB87A;
}

.check-icon {
  font-size: 24rpx;
  color: #fff;
}
</style>
