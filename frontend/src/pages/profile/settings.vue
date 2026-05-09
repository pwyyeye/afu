<template>
  <view class="page">
    <!-- General -->
    <view class="menu-group">
      <text class="group-title">通用</text>
      <view class="settings-item">
        <text class="settings-label">消息通知</text>
        <switch :checked="settingsStore.notifications" @change="toggleNotifications" color="#4a90d9" />
      </view>
      <view class="settings-item">
        <text class="settings-label">语音自动播放</text>
        <switch :checked="settingsStore.voiceAutoPlay" @change="toggleVoice" color="#4a90d9" />
      </view>
    </view>

    <!-- Display -->
    <view class="menu-group">
      <text class="group-title">显示</text>
      <view class="settings-item" @tap="goTo('/pages/profile/elder-mode')">
        <text class="settings-label">长辈模式</text>
        <text class="settings-value">{{ settingsStore.elderMode ? '已开启' : '未开启' }}</text>
        <text class="settings-arrow">›</text>
      </view>
      <view class="settings-item">
        <text class="settings-label">字体大小</text>
        <view class="font-size-options">
          <view
            v-for="size in fontSizes"
            :key="size.value"
            :class="['size-btn', settingsStore.fontSize === size.value ? 'size-active' : '']"
            @tap="setFontSize(size.value)"
          >
            <text>{{ size.label }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Data -->
    <view class="menu-group">
      <text class="group-title">数据</text>
      <view class="settings-item" @tap="clearCache">
        <text class="settings-label">清除缓存</text>
        <text class="settings-value">{{ cacheSize }}</text>
        <text class="settings-arrow">›</text>
      </view>
    </view>

    <!-- About -->
    <view class="menu-group">
      <text class="group-title">关于</text>
      <view class="settings-item">
        <text class="settings-label">版本</text>
        <text class="settings-value">v1.0.0</text>
      </view>
      <view class="settings-item" @tap="showPrivacy">
        <text class="settings-label">隐私政策</text>
        <text class="settings-arrow">›</text>
      </view>
      <view class="settings-item" @tap="showTerms">
        <text class="settings-label">用户协议</text>
        <text class="settings-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const cacheSize = ref('12.5 MB')

const fontSizes = [
  { label: '小', value: 'small' },
  { label: '标准', value: 'normal' },
  { label: '大', value: 'large' },
]

function toggleNotifications() {
  settingsStore.notifications = !settingsStore.notifications
}

function toggleVoice() {
  settingsStore.voiceAutoPlay = !settingsStore.voiceAutoPlay
}

function setFontSize(size: string) {
  settingsStore.fontSize = size
}

function clearCache() {
  uni.showModal({
    title: '清除缓存',
    content: '确定清除本地缓存？不会影响您的账号数据。',
    success: (res) => {
      if (res.confirm) {
        uni.clearStorageSync()
        cacheSize.value = '0 MB'
        uni.showToast({ title: '已清除', icon: 'success' })
      }
    },
  })
}

function showPrivacy() {
  uni.showModal({
    title: '隐私政策',
    content: '阿福健康重视您的隐私。我们收集的数据仅用于提供健康服务，不会泄露给第三方。',
    showCancel: false,
  })
}

function showTerms() {
  uni.showModal({
    title: '用户协议',
    content: '使用阿福健康即表示您同意我们的服务条款。本应用提供的健康建议仅供参考，不构成医疗诊断。',
    showCancel: false,
  })
}

function goTo(url: string) {
  uni.navigateTo({ url })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.menu-group {
  margin-bottom: 32rpx;
}

.group-title {
  font-size: 24rpx;
  color: #999;
  margin-bottom: 12rpx;
  margin-left: 8rpx;
  display: block;
}

.settings-item {
  display: flex;
  align-items: center;
  padding: 28rpx 24rpx;
  background: #fff;
  border-bottom: 1rpx solid #f5f5f5;

  &:first-of-type {
    border-radius: 16rpx 16rpx 0 0;
  }

  &:last-child {
    border-bottom: none;
    border-radius: 0 0 16rpx 16rpx;
  }

  &:only-of-type {
    border-radius: 16rpx;
  }
}

.settings-label {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.settings-value {
  font-size: 26rpx;
  color: #999;
  margin-right: 8rpx;
}

.settings-arrow {
  font-size: 32rpx;
  color: #ccc;
}

.font-size-options {
  display: flex;
  gap: 12rpx;
}

.size-btn {
  padding: 8rpx 24rpx;
  border-radius: 999rpx;
  background: #f0f0f0;
  font-size: 24rpx;
  color: #666;

  &.size-active {
    background: #4a90d9;
    color: #fff;
  }
}
</style>
