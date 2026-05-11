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

      <!-- User text: plain -->
      <view v-else-if="isUser" class="bubble-content">
        <text class="bubble-text user-text">{{ message.content }}</text>
      </view>

      <!-- AI text: typewriter during streaming, markdown after -->
      <view v-else class="ai-content">
        <!-- Typewriter mode: raw text + cursor -->
        <view v-if="showTypewriter" class="bubble-content">
          <text class="bubble-text ai-text typing-text">{{ displayContent }}</text>
          <text v-if="showCursor" class="cursor">|</text>
        </view>

        <!-- Markdown mode: rendered blocks -->
        <view v-else>
          <template v-for="(block, bi) in mdBlocks" :key="bi">
            <!-- Heading -->
            <view v-if="block.type === 'heading'" class="md-heading" :class="'md-h' + block.level">
              <text v-for="(t, ti) in block.tokens" :key="ti" :class="['md-inline', 'md-' + t.type]">{{ t.content }}</text>
            </view>

            <!-- Paragraph -->
            <view v-else-if="block.type === 'paragraph'" class="md-paragraph">
              <text v-for="(t, ti) in block.tokens" :key="ti" :class="['md-inline', 'md-' + t.type]">{{ t.content }}</text>
            </view>

            <!-- Unordered list -->
            <view v-else-if="block.type === 'list' && !block.ordered" class="md-list">
              <view v-for="(item, ii) in block.items" :key="ii" class="md-list-item">
                <text class="md-bullet">•</text>
                <view class="md-list-text">
                  <text v-for="(t, ti) in item" :key="ti" :class="['md-inline', 'md-' + t.type]">{{ t.content }}</text>
                </view>
              </view>
            </view>

            <!-- Ordered list -->
            <view v-else-if="block.type === 'list' && block.ordered" class="md-list">
              <view v-for="(item, ii) in block.items" :key="ii" class="md-list-item">
                <text class="md-bullet">{{ ii + 1 }}.</text>
                <view class="md-list-text">
                  <text v-for="(t, ti) in item" :key="ti" :class="['md-inline', 'md-' + t.type]">{{ t.content }}</text>
                </view>
              </view>
            </view>

            <!-- Blockquote -->
            <view v-else-if="block.type === 'blockquote'" class="md-blockquote">
              <text class="md-quote-text">{{ block.content }}</text>
            </view>

            <!-- Code block -->
            <view v-else-if="block.type === 'codeblock'" class="md-codeblock">
              <text v-if="block.lang" class="md-code-lang">{{ block.lang }}</text>
              <text class="md-code-content">{{ block.content }}</text>
            </view>

            <!-- HR -->
            <view v-else-if="block.type === 'hr'" class="md-hr" />
          </template>
        </view>
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
import { ref, computed, watch, onUnmounted } from 'vue'
import type { ChatMessage } from '@/types/chat'
import { parseMarkdown } from '@/utils/markdown'

const props = defineProps<{
  message: ChatMessage
  isStreaming?: boolean
  isLast?: boolean
}>()

const isUser = computed(() => props.message.role === 'user')

// --- Typewriter state ---
const displayedLength = ref(0)
let typeTimer: ReturnType<typeof setInterval> | null = null
const isTyping = ref(false)

const showTypewriter = computed(() => {
  return props.isLast && (isTyping.value || (props.isStreaming && !props.message.content))
})

const displayContent = computed(() => {
  if (!props.message.content && props.isStreaming && props.isLast) {
    return '思考中'
  }
  if (isTyping.value && props.isLast && displayedLength.value < props.message.content.length) {
    return props.message.content.slice(0, displayedLength.value)
  }
  return props.message.content
})

const showCursor = computed(() => {
  if (!props.isLast) return false
  if (isTyping.value) return true
  if (props.isStreaming && !props.message.content) return true
  return false
})

// --- Markdown blocks (computed from full content) ---
const mdBlocks = computed(() => {
  if (!props.message.content) return []
  return parseMarkdown(props.message.content)
})

// --- Typewriter watchers ---
watch(
  () => props.message.content,
  (newVal, oldVal) => {
    if (!props.isStreaming || !props.isLast) {
      displayedLength.value = newVal?.length || 0
      return
    }
    if (!oldVal && newVal && !isTyping.value) {
      displayedLength.value = 0
      startTyping()
    }
  }
)

watch(
  () => props.isStreaming,
  (streaming) => {
    if (!streaming && !isTyping.value) {
      displayedLength.value = props.message.content?.length || 0
    }
  }
)

watch(isTyping, (typing) => {
  if (!typing) {
    displayedLength.value = props.message.content?.length || 0
  }
})

function startTyping() {
  if (typeTimer) return
  isTyping.value = true
  typeTimer = setInterval(() => {
    const total = props.message.content?.length || 0
    if (displayedLength.value >= total) {
      stopTyping()
      return
    }
    const remaining = total - displayedLength.value
    const charsPerTick = remaining > 40 ? 6 : remaining > 15 ? 4 : 2
    displayedLength.value = Math.min(displayedLength.value + charsPerTick, total)
  }, 60)
}

function stopTyping() {
  if (typeTimer) {
    clearInterval(typeTimer)
    typeTimer = null
  }
  isTyping.value = false
}

onUnmounted(() => {
  stopTyping()
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
  background: #E8F4F8;
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
  max-width: 80%;
  padding: 20rpx 24rpx;
  border-radius: 20rpx;
  position: relative;
}

.user-bubble {
  background: #3B82A0;
  border-bottom-right-radius: 4rpx;
  max-width: 70%;
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

.user-text {
  color: #ffffff;
}

.ai-text {
  color: #2C2C2E;
}

.typing-text {
  color: #A0A0A5;
}

.cursor {
  font-size: 28rpx;
  color: #3B82A0;
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
  color: #6B6B70;
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

/* --- Markdown styles --- */

.ai-content {
  min-width: 0;
}

// Headings
.md-heading {
  margin-bottom: 12rpx;
}
.md-h1 {
  font-size: 36rpx;
  font-weight: 700;
  margin-top: 8rpx;
  margin-bottom: 16rpx;
}
.md-h2 {
  font-size: 32rpx;
  font-weight: 600;
  margin-top: 8rpx;
}
.md-h3 {
  font-size: 28rpx;
  font-weight: 600;
}

// Paragraph
.md-paragraph {
  margin-bottom: 16rpx;
  line-height: 1.7;
}

// Inline tokens
.md-inline {
  font-size: 28rpx;
  line-height: 1.7;
  color: #2C2C2E;
}
.md-bold {
  font-weight: 600;
}
.md-italic {
  font-style: italic;
}
.md-code {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 24rpx;
  background: #F0EDE8;
  color: #3B82A0;
  padding: 2rpx 8rpx;
  border-radius: 6rpx;
}
.md-link {
  color: #3B82A0;
  text-decoration: underline;
}

// Lists
.md-list {
  margin-bottom: 16rpx;
  padding-left: 8rpx;
}
.md-list-item {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin-bottom: 8rpx;
}
.md-bullet {
  font-size: 28rpx;
  color: #3B82A0;
  margin-right: 12rpx;
  line-height: 1.7;
  flex-shrink: 0;
  width: 36rpx;
}
.md-list-text {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
}

// Blockquote
.md-blockquote {
  border-left: 6rpx solid #3B82A0;
  padding: 12rpx 16rpx;
  margin-bottom: 16rpx;
  background: #F8F6F3;
  border-radius: 0 8rpx 8rpx 0;
}
.md-quote-text {
  font-size: 26rpx;
  color: #6B6B70;
  line-height: 1.6;
  font-style: italic;
}

// Code block
.md-codeblock {
  background: #2C2C2E;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
  margin-bottom: 16rpx;
}
.md-code-lang {
  font-size: 20rpx;
  color: #A0A0A5;
  margin-bottom: 8rpx;
  display: block;
}
.md-code-content {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 24rpx;
  color: #E8F4F8;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}

// HR
.md-hr {
  height: 2rpx;
  background: #E8E5E0;
  margin: 16rpx 0;
}
</style>
