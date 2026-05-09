<template>
  <view class="login-page">
    <view class="logo-area">
      <text class="logo-text">🏥</text>
      <text class="app-name">阿福健康</text>
      <text class="app-desc">您的AI健康助手</text>
    </view>

    <view class="form-area">
      <view class="input-group">
        <text class="label">手机号</text>
        <input
          v-model="phone"
          type="number"
          maxlength="11"
          placeholder="请输入手机号"
          class="input"
        />
      </view>

      <view class="input-group">
        <text class="label">验证码</text>
        <view class="code-row">
          <input
            v-model="code"
            type="number"
            maxlength="6"
            placeholder="请输入验证码"
            class="input code-input"
          />
          <button
            class="send-btn"
            :disabled="countdown > 0 || !phoneValid"
            @tap="sendCode"
          >
            {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
          </button>
        </view>
      </view>

      <button class="login-btn" :disabled="!canLogin" @tap="handleLogin">
        登录 / 注册
      </button>
    </view>

    <view class="footer">
      <text class="footer-text">
        登录即表示同意《用户协议》和《隐私政策》
      </text>
      <text class="dev-hint">开发环境验证码：123456</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { request } from '@/api/request'

const userStore = useUserStore()

const phone = ref('')
const code = ref('')
const countdown = ref(0)

const phoneValid = computed(() => /^1[3-9]\d{9}$/.test(phone.value))
const canLogin = computed(() => phoneValid.value && code.value.length >= 4)

let timer: ReturnType<typeof setInterval> | null = null

async function sendCode() {
  if (!phoneValid.value || countdown.value > 0) return

  try {
    await request.post('/api/v1/auth/sms-code', { phone: phone.value })
    countdown.value = 60
    timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0 && timer) {
        clearInterval(timer)
        timer = null
      }
    }, 1000)
    uni.showToast({ title: '验证码已发送', icon: 'none' })
  } catch {
    uni.showToast({ title: '发送失败，请重试', icon: 'none' })
  }
}

async function handleLogin() {
  if (!canLogin.value) return

  try {
    uni.showLoading({ title: '登录中...' })
    await userStore.login({ phone: phone.value, code: code.value })
    uni.hideLoading()
    uni.switchTab({ url: '/pages/index/index' })
  } catch (e) {
    uni.hideLoading()
    uni.showToast({ title: '登录失败', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 0 48rpx;
  background: linear-gradient(180deg, #e8f0fe 0%, #f5f7fa 40%);
}

.logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 180rpx;
  margin-bottom: 80rpx;
}

.logo-text {
  font-size: 96rpx;
  margin-bottom: 16rpx;
}

.app-name {
  font-size: 44rpx;
  font-weight: bold;
  color: #333;
}

.app-desc {
  font-size: 28rpx;
  color: #999;
  margin-top: 8rpx;
}

.form-area {
  flex: 1;
}

.input-group {
  margin-bottom: 32rpx;
}

.label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 12rpx;
  display: block;
}

.input {
  width: 100%;
  height: 88rpx;
  background: #fff;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 30rpx;
  border: 2rpx solid #e8e8e8;
}

.code-row {
  display: flex;
  gap: 16rpx;
}

.code-input {
  flex: 1;
}

.send-btn {
  width: 220rpx;
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  background: #4a90d9;
  color: #fff;
  font-size: 26rpx;
  border-radius: 12rpx;
  border: none;
  padding: 0;

  &[disabled] {
    background: #ccc;
    color: #999;
  }
}

.login-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: #4a90d9;
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
  margin-top: 48rpx;

  &[disabled] {
    background: #a0c4e8;
  }
}

.footer {
  padding: 40rpx 0;
  text-align: center;
}

.footer-text {
  font-size: 24rpx;
  color: #999;
}

.dev-hint {
  display: block;
  font-size: 22rpx;
  color: #4a90d9;
  margin-top: 12rpx;
  opacity: 0.6;
}
</style>
