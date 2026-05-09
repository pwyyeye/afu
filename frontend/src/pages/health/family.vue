<template>
  <view class="page">
    <button class="add-btn" @tap="goToAdd">
      <text class="add-icon">+</text>
      <text>添加家庭成员</text>
    </button>

    <view
      v-for="member in healthStore.familyMembers"
      :key="member.id"
      class="member-card"
      @tap="goToEdit(member.id)"
    >
      <view class="member-avatar" :class="avatarClass(member.relationship)">
        <text>{{ avatarEmoji(member.relationship) }}</text>
      </view>
      <view class="member-info">
        <view class="member-row">
          <text class="member-name">{{ member.name }}</text>
          <text class="member-tag" :class="tagClass(member.relationship)">
            {{ relationshipLabels[member.relationship] || '其他' }}
          </text>
        </view>
        <view class="member-meta">
          <text v-if="member.gender" class="meta-item">{{ member.gender }}</text>
          <text v-if="member.birth_date" class="meta-item">{{ calcAge(member.birth_date) }}岁</text>
          <text v-if="member.phone" class="meta-item">{{ member.phone }}</text>
        </view>
      </view>
      <text class="member-arrow">›</text>
    </view>

    <view v-if="healthStore.familyMembers.length === 0" class="empty">
      <text class="empty-icon">👨‍👩‍👧‍👦</text>
      <text class="empty-text">暂无家庭成员</text>
      <text class="empty-desc">添加家人，一起守护健康</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onShow } from '@dcloudio/uni-app'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()

const relationshipLabels: Record<string, string> = {
  spouse: '配偶',
  parent: '父母',
  child: '子女',
  other: '其他',
}

onShow(() => {
  healthStore.fetchFamily()
})

function avatarEmoji(relation: string): string {
  const map: Record<string, string> = {
    spouse: '💑',
    parent: '👴',
    child: '👦',
    other: '👤',
  }
  return map[relation] || '👤'
}

function avatarClass(relation: string): string {
  return `avatar-${relation}`
}

function tagClass(relation: string): string {
  return `tag-${relation}`
}

function calcAge(birthDate: string): string {
  if (!birthDate) return ''
  const birth = new Date(birthDate)
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  const m = now.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && now.getDate() < birth.getDate())) {
    age--
  }
  return String(age)
}

function goToAdd() {
  uni.navigateTo({ url: '/pages/health/member-edit' })
}

function goToEdit(id: string) {
  uni.navigateTo({ url: `/pages/health/member-edit?id=${id}` })
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
  background: linear-gradient(135deg, #4a90d9, #357abd);
  color: #fff;
  font-size: 30rpx;
  font-weight: 500;
  border-radius: 16rpx;
  border: none;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(74, 144, 217, 0.3);
}

.add-icon {
  font-size: 36rpx;
  font-weight: bold;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 28rpx 24rpx;
  background: #fff;
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.member-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  flex-shrink: 0;
}

.avatar-spouse { background: #fff0f6; }
.avatar-parent { background: #fff7e6; }
.avatar-child { background: #e6f7ff; }
.avatar-other { background: #f0f0f0; }

.member-info {
  flex: 1;
  min-width: 0;
}

.member-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.member-name {
  font-size: 32rpx;
  color: #333;
  font-weight: 600;
}

.member-tag {
  font-size: 20rpx;
  padding: 2rpx 12rpx;
  border-radius: 999rpx;
}

.tag-spouse { background: #fff0f6; color: #eb2f96; }
.tag-parent { background: #fff7e6; color: #fa8c16; }
.tag-child { background: #e6f7ff; color: #1890ff; }
.tag-other { background: #f0f0f0; color: #999; }

.member-meta {
  display: flex;
  gap: 16rpx;
  margin-top: 8rpx;
}

.meta-item {
  font-size: 24rpx;
  color: #999;
}

.member-arrow {
  font-size: 36rpx;
  color: #ccc;
  flex-shrink: 0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #999;
  margin-bottom: 12rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #ccc;
}
</style>
