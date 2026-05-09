<template>
  <view :class="['bubble-row', isUser ? 'user-row' : 'ai-row']">
    <view v-if="!isUser" class="avatar ai-avatar">
      <text class="avatar-text">🏥</text>
    </view>

    <view :class="['bubble', isUser ? 'user-bubble' : 'ai-bubble']">
      <!-- Image message -->
      <image
        v-if="message.content_type === 'image' && message.media_url"
        :src="message.media_url"
        mode="widthFix"
        class="bubble-image"
        @tap="previewImage"
      />

      <!-- Voice message -->
      <view
        v-else-if="message.content_type === 'voice'"
        class="voice-message"
        @tap="playVoice"
      >
        <text class="voice-icon">🎤</text>
        <text class="voice-text">{{ message.content || '语音消息' }}</text>
      </view>

      <!-- Text message -->
      <view v-else class="bubble-content">
        <text
          class="bubble-text"
          :class="{ 'typing-text': isStreaming && isLast }"
        >{{ displayContent }}</text>
        <text v-if="isStreaming && isLast" class="cursor">|</text>
      </view>

      <!-- AI disclaimer -->
      <text v-if="!isUser && !isStreaming" class="disclaimer">
        以上内容仅供参考，不构成医疗建议
      </text>
    </view>

    <view v-if="isUser" class="avatar user-avatar">
      <text class="avatar-text">👤</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ChatMessage } from '@/types/chat'

const props = defineProps<{
  message: ChatMessage
  isStreaming?: boolean
  isLast?: boolean
}>()

const isUser = computed(() => props.message.role === 'user')

const displayContent = computed(() => {
  if (!props.message.content && props.isStreaming && props.isLast) {
    return '思考中'
  }
  return props.message.content
})

function previewImage() {
  if (props.message.media_url) {
    uni.previewImage({ urls: [props.message.media_url] })
  }
}

function playVoice() {
  if (props.message.media_url) {
    const audio = uni.createInnerAudioContext()
    audio.src = props.message.media_url
    audio.play()
  }
}
</script>

<style scoped lang="scss">
.bubble-row {
  display: flex;
  margin-bottom: 24rpx;
  align-items: flex-start;
}

.user-row {
  justify-content: flex-end;
}

.ai-row {
  justify-content: flex-start;
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ai-avatar {
  background: #e8f0fe;
  margin-right: 16rpx;
}

.user-avatar {
  background: #f0f0f0;
  margin-left: 16rpx;
}

.avatar-text {
  font-size: 36rpx;
}

.bubble {
  max-width: 70%;
  padding: 20rpx 24rpx;
  border-radius: 20rpx;
  position: relative;
}

.user-bubble {
  background: #4a90d9;
  border-bottom-right-radius: 4rpx;
}

.ai-bubble {
  background: #ffffff;
  border-bottom-left-radius: 4rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
}

.bubble-content {
  display: flex;
  flex-wrap: wrap;
}

.bubble-text {
  font-size: 28rpx;
  line-height: 1.6;
  word-break: break-all;
  white-space: pre-wrap;
}

.user-bubble .bubble-text {
  color: #ffffff;
}

.ai-bubble .bubble-text {
  color: #333333;
}

.typing-text {
  color: #999;
}

.cursor {
  font-size: 28rpx;
  color: #4a90d9;
  animation: blink 0.8s infinite;
  margin-left: 2rpx;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.bubble-image {
  width: 400rpx;
  border-radius: 12rpx;
  margin-bottom: 8rpx;
}

.voice-message {
  display: flex;
  align-items: center;
  gap: 12rpx;
  min-width: 160rpx;
}

.voice-icon {
  font-size: 32rpx;
}

.voice-text {
  font-size: 26rpx;
  color: #666;
}

.disclaimer {
  display: block;
  font-size: 20rpx;
  color: #bbbbbb;
  margin-top: 12rpx;
  padding-top: 12rpx;
  border-top: 1rpx solid #f0f0f0;
  line-height: 1.4;
}
</style>
