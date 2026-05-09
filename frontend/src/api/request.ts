import Request from 'luch-request'

const BASE_URL = 'http://localhost:8002'

const http = new Request({
  baseURL: BASE_URL,
  timeout: 30000,
})

// Request interceptor: inject JWT token
http.interceptors.request.use(
  (config) => {
    const token = uni.getStorageSync('token')
    if (token) {
      config.header = {
        ...config.header,
        Authorization: `Bearer ${token}`,
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor: handle errors and token refresh
http.interceptors.response.use(
  (response) => {
    const data = response.data as any
    if (data.code && data.code !== 0) {
      uni.showToast({ title: data.message || '请求失败', icon: 'none' })
      return Promise.reject(new Error(data.message))
    }
    return data?.data ?? data
  },
  async (error) => {
    const statusCode = error.statusCode
    if (statusCode === 401) {
      // Try to refresh token
      const refreshToken = uni.getStorageSync('refresh_token')
      if (refreshToken) {
        try {
          const res = await http.post('/api/v1/auth/refresh', {
            refresh_token: refreshToken,
          })
          const data = res.data as any
          uni.setStorageSync('token', data.access_token)
          uni.setStorageSync('refresh_token', data.refresh_token)
          // Retry original request
          error.config.header.Authorization = `Bearer ${data.access_token}`
          return http.request(error.config)
        } catch {
          // Refresh failed, redirect to login
          uni.removeStorageSync('token')
          uni.removeStorageSync('refresh_token')
          uni.reLaunch({ url: '/pages/login/index' })
        }
      } else {
        uni.reLaunch({ url: '/pages/login/index' })
      }
    }
    uni.showToast({ title: error.errMsg || '网络错误', icon: 'none' })
    return Promise.reject(error)
  }
)

export const request = {
  get<T = any>(url: string, params?: Record<string, any>): Promise<T> {
    return http.get(url, { params }).then((res: any) => res)
  },

  post<T = any>(url: string, data?: any): Promise<T> {
    return http.post(url, data).then((res: any) => res)
  },

  put<T = any>(url: string, data?: any): Promise<T> {
    return http.put(url, data).then((res: any) => res)
  },

  delete<T = any>(url: string): Promise<T> {
    return http.delete(url).then((res: any) => res)
  },

  upload<T = any>(url: string, filePaths: string[], formData?: Record<string, any>): Promise<T> {
    return new Promise((resolve, reject) => {
      const token = uni.getStorageSync('token')
      uni.uploadFile({
        url: `${BASE_URL}${url}`,
        filePath: filePaths[0],
        name: 'file',
        formData,
        header: {
          Authorization: `Bearer ${token}`,
        },
        success: (res) => {
          try {
            const data = JSON.parse(res.data)
            resolve(data.data ?? data)
          } catch {
            reject(new Error('Upload failed'))
          }
        },
        fail: reject,
      })
    })
  },
}
