<template>
  <view class="page">
    <view class="new-chat" @tap="startNewChat">
      <text class="new-chat-icon">+</text>
      <text class="new-chat-text">开始新的健康咨询</text>
    </view>

    <view class="session-list">
      <view
        v-for="session in chatStore.sessions"
        :key="session.id"
        class="session-item"
        @tap="goToChat(session.id)"
      >
        <view class="session-info">
          <text class="session-title">{{ session.title }}</text>
          <text class="session-preview">{{ session.last_message }}</text>
        </view>
        <text class="session-time">{{ formatRelativeTime(session.updated_at) }}</text>
      </view>

      <view v-if="chatStore.sessions.length === 0" class="empty">
        <text class="empty-text">暂无咨询记录</text>
        <text class="empty-desc">点击上方按钮开始健康咨询</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onShow } from '@dcloudio/uni-app'
import { useChatStore } from '@/stores/chat'
import { formatRelativeTime } from '@/utils/format'

const chatStore = useChatStore()

onShow(() => {
  chatStore.fetchSessions()
})

function startNewChat() {
  uni.navigateTo({ url: '/pages/qa/chat' })
}

function goToChat(sessionId: string) {
  uni.navigateTo({ url: `/pages/qa/chat?sessionId=${sessionId}` })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  background: #F8F6F3;
}

.new-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  height: 96rpx;
  background: #3B82A0;
  border-radius: 20rpx;
  margin-bottom: 32rpx;
}

.new-chat-icon {
  font-size: 40rpx;
  color: #fff;
  font-weight: bold;
}

.new-chat-text {
  font-size: 30rpx;
  color: #fff;
}

.session-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 24rpx;
  background: #fff;
  border-radius: 20rpx;
}

.session-info {
  flex: 1;
  overflow: hidden;
}

.session-title {
  font-size: 30rpx;
  color: #2C2C2E;
  font-weight: 500;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.session-preview {
  font-size: 24rpx;
  color: #A0A0A5;
  margin-top: 8rpx;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.session-time {
  font-size: 22rpx;
  color: #C5C5C8;
  margin-left: 16rpx;
  flex-shrink: 0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 120rpx 0;
}

.empty-text {
  font-size: 30rpx;
  color: #A0A0A5;
}

.empty-desc {
  font-size: 24rpx;
  color: #C5C5C8;
  margin-top: 12rpx;
}
</style>
