<template>
  <view v-if="visible" class="recorder-overlay" @touchstart.stop @touchmove.stop>
    <view class="recorder-panel">
      <view class="waveform">
        <view
          v-for="i in 20"
          :key="i"
          class="wave-bar"
          :style="{ height: `${randomHeight()}rpx`, animationDelay: `${i * 0.05}s` }"
        />
      </view>
      <text class="recorder-time">{{ formatTime(recordingTime) }}</text>
      <text class="recorder-hint">松开发送，上滑取消</text>
      <view class="recorder-actions">
        <button class="cancel-btn" @touchend="cancel">取消</button>
        <button class="send-btn" @touchend="stop">发送</button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'recorded', filePath: string): void
  (e: 'cancel'): void
}>()

const recordingTime = ref(0)
let recorderManager: any = null
let timer: ReturnType<typeof setInterval> | null = null

function randomHeight() {
  return Math.floor(Math.random() * 40) + 10
}

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

watch(() => props.visible, (val) => {
  if (val) {
    startRecording()
  } else {
    stopRecording()
  }
})

function startRecording() {
  recordingTime.value = 0
  timer = setInterval(() => {
    recordingTime.value++
    if (recordingTime.value >= 60) {
      stop()
    }
  }, 1000)

  recorderManager = uni.getRecorderManager()
  recorderManager.onStop((res: any) => {
    if (timer) clearInterval(timer)
    if (res.tempFilePath) {
      emit('recorded', res.tempFilePath)
    }
  })
  recorderManager.onError(() => {
    if (timer) clearInterval(timer)
    uni.showToast({ title: '录音失败', icon: 'none' })
  })

  recorderManager.start({
    format: 'mp3',
    sampleRate: 16000,
    numberOfChannels: 1,
  })
}

function stopRecording() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  try {
    recorderManager?.stop()
  } catch {}
}

function stop() {
  stopRecording()
}

function cancel() {
  stopRecording()
  emit('cancel')
}
</script>

<style scoped lang="scss">
.recorder-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.recorder-panel {
  width: 500rpx;
  background: #fff;
  border-radius: 28rpx;
  padding: 48rpx 32rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.waveform {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  height: 80rpx;
  margin-bottom: 24rpx;
}

.wave-bar {
  width: 6rpx;
  background: #3B82A0;
  border-radius: 3rpx;
  animation: wave 0.8s ease-in-out infinite alternate;
}

@keyframes wave {
  from { height: 10rpx; }
  to { height: 60rpx; }
}

.recorder-time {
  font-size: 48rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 12rpx;
}

.recorder-hint {
  font-size: 24rpx;
  color: #A0A0A5;
  margin-bottom: 32rpx;
}

.recorder-actions {
  display: flex;
  gap: 32rpx;
}

.cancel-btn, .send-btn {
  width: 180rpx;
  height: 72rpx;
  line-height: 72rpx;
  text-align: center;
  border-radius: 36rpx;
  font-size: 28rpx;
  border: none;
  padding: 0;
}

.cancel-btn {
  background: #f0f0f0;
  color: #6B6B70;
}

.send-btn {
  background: #3B82A0;
  color: #fff;
}
</style>
