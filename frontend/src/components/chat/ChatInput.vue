<template>
  <view class="chat-input-container">
    <view class="input-row">
      <!-- Voice button -->
      <view
        class="icon-btn voice-btn"
        :class="{ active: inputMode === 'voice' }"
        @tap="toggleMode"
      >
        <text class="icon">{{ inputMode === 'voice' ? '⌨️' : '🎤' }}</text>
      </view>

      <!-- Text input -->
      <input
        v-if="inputMode === 'text'"
        v-model="text"
        class="text-input"
        placeholder="描述您的健康问题..."
        confirm-type="send"
        :adjust-position="true"
        @confirm="sendText"
      />

      <!-- Voice press button -->
      <view
        v-else
        class="voice-press-btn"
        @touchstart="startVoice"
        @touchend="endVoice"
        @touchcancel="cancelVoice"
      >
        <text class="voice-press-text">按住说话</text>
      </view>

      <!-- Image button -->
      <view class="icon-btn" @tap="chooseImage">
        <text class="icon">📷</text>
      </view>

      <!-- Send button -->
      <button
        v-if="inputMode === 'text'"
        class="send-btn"
        :disabled="!text.trim()"
        @tap="sendText"
      >
        发送
      </button>
    </view>

    <!-- Voice recorder overlay -->
    <VoiceRecorder
      :visible="showRecorder"
      @recorded="onVoiceRecorded"
      @cancel="showRecorder = false"
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import VoiceRecorder from './VoiceRecorder.vue'

const emit = defineEmits<{
  (e: 'send', content: string, type: 'text'): void
  (e: 'voice', filePath: string): void
  (e: 'image', filePath: string): void
}>()

const text = ref('')
const inputMode = ref<'text' | 'voice'>('text')
const showRecorder = ref(false)

function toggleMode() {
  inputMode.value = inputMode.value === 'text' ? 'voice' : 'text'
}

function sendText() {
  const content = text.value.trim()
  if (!content) return
  emit('send', content, 'text')
  text.value = ''
}

function startVoice() {
  showRecorder.value = true
}

function endVoice() {
  // Handled by VoiceRecorder component
}

function cancelVoice() {
  showRecorder.value = false
}

function onVoiceRecorded(filePath: string) {
  showRecorder.value = false
  emit('voice', filePath)
}

function chooseImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ['compressed'],
    sourceType: ['camera', 'album'],
    success: (res) => {
      emit('image', res.tempFilePaths[0])
    },
  })
}
</script>

<style scoped lang="scss">
.chat-input-container {
  background: #ffffff;
  border-top: 1rpx solid #E8E5E0;
  padding: 16rpx 24rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
}

.input-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.icon-btn {
  width: 64rpx;
  height: 64rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-btn.active {
  background: #E8F4F8;
  border-radius: 50%;
}

.icon {
  font-size: 36rpx;
}

.text-input {
  flex: 1;
  height: 72rpx;
  background: #F8F6F3;
  border-radius: 36rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
}

.voice-press-btn {
  flex: 1;
  height: 72rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F8F6F3;
  border-radius: 36rpx;
}

.voice-press-text {
  font-size: 28rpx;
  color: #6B6B70;
}

.voice-press-btn:active {
  background: #E8F4F8;
}

.send-btn {
  width: 120rpx;
  height: 72rpx;
  line-height: 72rpx;
  text-align: center;
  background: #3B82A0;
  color: #fff;
  font-size: 28rpx;
  border-radius: 36rpx;
  border: none;
  padding: 0;
  flex-shrink: 0;

  &[disabled] {
    background: #8FBFDB;
  }
}
</style>
