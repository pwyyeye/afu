import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const elderMode = ref(false)
  const fontSize = ref<'normal' | 'large' | 'xlarge'>('normal')
  const notifications = ref(true)
  const voiceAutoPlay = ref(false)

  function toggleElderMode() {
    elderMode.value = !elderMode.value
    if (elderMode.value) {
      fontSize.value = 'large'
      voiceAutoPlay.value = true
    } else {
      fontSize.value = 'normal'
      voiceAutoPlay.value = false
    }
    uni.setStorageSync('settings', {
      elderMode: elderMode.value,
      fontSize: fontSize.value,
      notifications: notifications.value,
      voiceAutoPlay: voiceAutoPlay.value,
    })
  }

  function restoreSettings() {
    const saved = uni.getStorageSync('settings')
    if (saved) {
      elderMode.value = saved.elderMode ?? false
      fontSize.value = saved.fontSize ?? 'normal'
      notifications.value = saved.notifications ?? true
      voiceAutoPlay.value = saved.voiceAutoPlay ?? false
    }
  }

  return {
    elderMode,
    fontSize,
    notifications,
    voiceAutoPlay,
    toggleElderMode,
    restoreSettings,
  }
})
