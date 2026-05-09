export function getStorage<T>(key: string, defaultValue?: T): T | undefined {
  try {
    const value = uni.getStorageSync(key)
    return value ?? defaultValue
  } catch {
    return defaultValue
  }
}

export function setStorage(key: string, value: any): void {
  try {
    uni.setStorageSync(key, value)
  } catch (e) {
    console.error('Storage write failed:', e)
  }
}

export function removeStorage(key: string): void {
  try {
    uni.removeStorageSync(key)
  } catch (e) {
    console.error('Storage remove failed:', e)
  }
}
