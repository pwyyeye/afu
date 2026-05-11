<template>
  <view class="page">
    <!-- Toggle -->
    <view class="toggle-card">
      <view class="toggle-info">
        <text class="toggle-title">长辈模式</text>
        <text class="toggle-desc">更大的字体、更清晰的界面、语音优先</text>
      </view>
      <switch :checked="settingsStore.elderMode" @change="toggleElderMode" color="#3B82A0" />
    </view>

    <!-- Preview -->
    <view class="preview-section">
      <text class="section-title">效果预览</text>
      <view class="preview-card" :class="{ 'elder-preview': settingsStore.elderMode }">
        <view class="preview-header">
          <text class="preview-label">{{ settingsStore.elderMode ? '长辈模式' : '普通模式' }}</text>
        </view>
        <view class="preview-content">
          <text class="preview-big">血压 120/80 mmHg</text>
          <text class="preview-normal">您的血压处于正常范围，继续保持良好生活习惯。</text>
          <view class="preview-btn">
            <text>查看详情</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Features -->
    <view class="features-section">
      <text class="section-title">功能特点</text>
      <view class="features-grid">
        <view class="feature-card">
          <text class="feature-icon">🔤</text>
          <text class="feature-name">大字体</text>
          <text class="feature-desc">文字放大，阅读更轻松</text>
        </view>
        <view class="feature-card">
          <text class="feature-icon">🎤</text>
          <text class="feature-name">语音优先</text>
          <text class="feature-desc">说话就能问，操作更简单</text>
        </view>
        <view class="feature-card">
          <text class="feature-icon">🔊</text>
          <text class="feature-name">自动朗读</text>
          <text class="feature-desc">AI回复自动播报</text>
        </view>
        <view class="feature-card">
          <text class="feature-icon">👆</text>
          <text class="feature-name">大按钮</text>
          <text class="feature-desc">点击区域更大，操作更方便</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()

function toggleElderMode() {
  settingsStore.toggleElderMode()
  uni.showToast({
    title: settingsStore.elderMode ? '已开启长辈模式' : '已关闭长辈模式',
    icon: 'none',
  })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.toggle-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx 24rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.toggle-info {
  flex: 1;
}

.toggle-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2C2C2E;
  display: block;
}

.toggle-desc {
  font-size: 24rpx;
  color: #A0A0A5;
  margin-top: 6rpx;
  display: block;
}

.section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 16rpx;
  display: block;
}

.preview-section {
  margin-bottom: 32rpx;
}

.preview-card {
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
}

.preview-header {
  padding: 16rpx 24rpx;
  background: #f8f9fa;
  border-bottom: 1rpx solid #f0f0f0;
}

.preview-label {
  font-size: 24rpx;
  color: #A0A0A5;
}

.preview-content {
  padding: 28rpx 24rpx;
}

.preview-big {
  font-size: 36rpx;
  font-weight: bold;
  color: #2C2C2E;
  display: block;
  margin-bottom: 16rpx;
}

.elder-preview .preview-big {
  font-size: 48rpx;
}

.preview-normal {
  font-size: 26rpx;
  color: #6B6B70;
  line-height: 1.6;
  display: block;
  margin-bottom: 20rpx;
}

.elder-preview .preview-normal {
  font-size: 34rpx;
}

.preview-btn {
  display: inline-block;
  padding: 16rpx 40rpx;
  background: #3B82A0;
  color: #fff;
  border-radius: 12rpx;
  font-size: 28rpx;
}

.elder-preview .preview-btn {
  padding: 24rpx 56rpx;
  font-size: 34rpx;
  border-radius: 20rpx;
}

.features-section {
  margin-bottom: 32rpx;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16rpx;
}

.feature-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.feature-icon {
  font-size: 48rpx;
  margin-bottom: 4rpx;
}

.feature-name {
  font-size: 28rpx;
  font-weight: 500;
  color: #2C2C2E;
}

.feature-desc {
  font-size: 22rpx;
  color: #A0A0A5;
  text-align: center;
}
</style>
