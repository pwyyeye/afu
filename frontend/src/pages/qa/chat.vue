<template>
  <view class="chat-page">
    <!-- Header -->
    <view class="chat-header">
      <text class="back-btn" @tap="goBack">←</text>
      <text class="header-title">健康咨询</text>
      <view class="header-right" />
    </view>

    <!-- Messages -->
    <scroll-view
      class="chat-messages"
      scroll-y
      :scroll-into-view="scrollTarget"
      :scroll-with-animation="true"
      @scrolltoupper="loadMore"
    >
      <view class="messages-wrapper">
        <ChatBubble
          v-for="(msg, index) in chatStore.messages"
          :key="msg.id"
          :id="'msg-' + msg.id"
          :message="msg"
          :is-streaming="chatStore.isStreaming"
          :is-last="index === chatStore.messages.length - 1"
        />

        <view id="chat-bottom" />
      </view>
    </scroll-view>

    <!-- Input -->
    <ChatInput
      @send="onSendText"
      @voice="onSendVoice"
      @image="onSendImage"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useChatStore } from '@/stores/chat'
import ChatBubble from '@/components/chat/ChatBubble.vue'
import ChatInput from '@/components/chat/ChatInput.vue'

const chatStore = useChatStore()
const scrollTarget = ref('')
let sessionId = ''

onLoad(async (options) => {
  if (options?.sessionId) {
    sessionId = options.sessionId
    await chatStore.fetchMessages(sessionId)
  } else {
    const session = await chatStore.createSession()
    sessionId = session.id
  }
  scrollToBottom()
})

watch(
  () => chatStore.messages.length,
  () => nextTick(scrollToBottom)
)

// Also watch streaming content for auto-scroll
watch(
  () => chatStore.streamingContent,
  () => nextTick(scrollToBottom)
)

function scrollToBottom() {
  scrollTarget.value = ''
  setTimeout(() => {
    scrollTarget.value = 'chat-bottom'
  }, 50)
}

function goBack() {
  uni.navigateBack()
}

async function onSendText(content: string) {
  if (!sessionId) return
  await chatStore.sendMessage(sessionId, content, 'text')
  scrollToBottom()
}

async function onSendVoice(filePath: string) {
  if (!sessionId) return
  await chatStore.sendVoiceMessage(sessionId, filePath)
  scrollToBottom()
}

async function onSendImage(filePath: string) {
  if (!sessionId) return
  await chatStore.sendImageMessage(sessionId, filePath)
  scrollToBottom()
}

function loadMore() {
  // TODO: Load older messages
}
</script>

<style scoped lang="scss">
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background: #f5f7fa;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12rpx 24rpx;
  padding-top: calc(var(--status-bar-height, 44px) + 8px);
  background: #fff;
  border-bottom: 1rpx solid #e8e8e8;
  flex-shrink: 0;
}

.back-btn {
  font-size: 36rpx;
  color: #333;
  padding: 8rpx 16rpx;
}

.header-title {
  font-size: 32rpx;
  font-weight: 500;
  color: #333;
}

.header-right {
  width: 60rpx;
}

.chat-messages {
  flex: 1;
  overflow: hidden;
}

.messages-wrapper {
  padding: 24rpx;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
</style>
