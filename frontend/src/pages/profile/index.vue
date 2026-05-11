<template>
  <view class="page">
    <!-- User Card -->
    <view class="user-card">
      <view class="avatar-wrap">
        <text class="user-avatar">👤</text>
      </view>
      <view class="user-info">
        <text class="user-name">{{ userStore.user?.nickname || '未登录' }}</text>
        <text class="user-phone">{{ userStore.user?.phone || '点击登录' }}</text>
      </view>
      <text class="card-arrow">›</text>
    </view>

    <!-- Menu Groups -->
    <view class="menu-group">
      <view class="menu-item" @tap="goTo('/pages/health/profile')">
        <text class="menu-icon">📋</text>
        <text class="menu-text">个人档案</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/family')">
        <text class="menu-icon">👨‍👩‍👧‍👦</text>
        <text class="menu-text">家庭成员</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/health/timeline')">
        <text class="menu-icon">📊</text>
        <text class="menu-text">健康时间线</text>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <view class="menu-group">
      <view class="menu-item" @tap="goTo('/pages/profile/settings')">
        <text class="menu-icon">⚙️</text>
        <text class="menu-text">设置</text>
        <text class="menu-arrow">›</text>
      </view>
      <view class="menu-item" @tap="goTo('/pages/profile/elder-mode')">
        <text class="menu-icon">👴</text>
        <text class="menu-text">长辈模式</text>
        <text class="menu-value">{{ settingsStore.elderMode ? '已开启' : '未开启' }}</text>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <view class="menu-group">
      <view class="menu-item" @tap="showAbout">
        <text class="menu-icon">ℹ️</text>
        <text class="menu-text">关于</text>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <!-- Logout / Login -->
    <button v-if="userStore.isLoggedIn" class="logout-btn" @tap="handleLogout">
      退出登录
    </button>
    <button v-else class="login-btn" @tap="goTo('/pages/login/index')">
      登录 / 注册
    </button>

    <text class="version">阿福健康 v1.0.0</text>
  </view>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useSettingsStore } from '@/stores/settings'

const userStore = useUserStore()
const settingsStore = useSettingsStore()

function goTo(url: string) {
  uni.navigateTo({ url })
}

function handleLogout() {
  uni.showModal({
    title: '提示',
    content: '确定退出登录？',
    success: async (res) => {
      if (res.confirm) {
        await userStore.logout()
        uni.reLaunch({ url: '/pages/login/index' })
      }
    },
  })
}

function showAbout() {
  uni.showModal({
    title: '关于阿福健康',
    content: '阿福健康是您的AI健康助手，提供健康问答、体检报告解读、健康档案管理等功能。\n\n版本：v1.0.0',
    showCancel: false,
  })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 36rpx 28rpx;
  background: linear-gradient(135deg, #3B82A0 0%, #5A9BB8 100%);
  border-radius: 20rpx;
  margin-bottom: 32rpx;
}

.avatar-wrap {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar {
  font-size: 56rpx;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
  display: block;
}

.user-phone {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 6rpx;
  display: block;
}

.card-arrow {
  font-size: 36rpx;
  color: rgba(255, 255, 255, 0.6);
}

.menu-group {
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 24rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
}

.menu-icon {
  font-size: 36rpx;
  margin-right: 16rpx;
}

.menu-text {
  flex: 1;
  font-size: 28rpx;
  color: #2C2C2E;
}

.menu-value {
  font-size: 26rpx;
  color: #A0A0A5;
  margin-right: 8rpx;
}

.menu-arrow {
  font-size: 32rpx;
  color: #C5C5C8;
}

.logout-btn, .login-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 20rpx;
  border: none;
  font-size: 30rpx;
  margin-top: 16rpx;
}

.logout-btn {
  background: #fff;
  color: #E07070;
  border: 2rpx solid #E07070;
}

.login-btn {
  background: linear-gradient(135deg, #3B82A0, #2D6A82);
  color: #fff;
}

.version {
  display: block;
  text-align: center;
  font-size: 22rpx;
  color: #C5C5C8;
  margin-top: 48rpx;
}
</style>
