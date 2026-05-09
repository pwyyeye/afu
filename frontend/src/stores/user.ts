import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginParams, TokenResponse } from '@/types/user'
import { request } from '@/api/request'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const refreshToken = ref<string>('')
  const user = ref<User | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(params: LoginParams) {
    const res = await request.post<TokenResponse>('/api/v1/auth/login', params)
    token.value = res.access_token
    refreshToken.value = res.refresh_token
    user.value = res.user
    uni.setStorageSync('token', res.access_token)
    uni.setStorageSync('refresh_token', res.refresh_token)
  }

  async function logout() {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    uni.removeStorageSync('token')
    uni.removeStorageSync('refresh_token')
  }

  async function fetchProfile() {
    const res = await request.get<User>('/api/v1/users/me')
    user.value = res
  }

  function restoreToken() {
    token.value = uni.getStorageSync('token') || ''
    refreshToken.value = uni.getStorageSync('refresh_token') || ''
  }

  return {
    token,
    refreshToken,
    user,
    isLoggedIn,
    login,
    logout,
    fetchProfile,
    restoreToken,
  }
})
