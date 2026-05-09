<template>
  <view class="page">
    <view class="upload-section">
      <view class="upload-options">
        <view class="option-card" @tap="chooseImage">
          <text class="option-icon">📷</text>
          <text class="option-title">拍照上传</text>
          <text class="option-desc">拍摄体检报告</text>
        </view>
        <view class="option-card" @tap="chooseFile">
          <text class="option-icon">📄</text>
          <text class="option-title">选择文件</text>
          <text class="option-desc">支持PDF/图片</text>
        </view>
      </view>

      <view v-if="selectedFiles.length > 0" class="preview-section">
        <text class="preview-title">已选择 {{ selectedFiles.length }} 个文件</text>
        <view class="preview-list">
          <view v-for="(file, index) in selectedFiles" :key="index" class="preview-item">
            <image :src="file" mode="aspectFill" class="preview-image" />
            <text class="remove-btn" @tap="removeFile(index)">×</text>
          </view>
        </view>
      </view>

      <view class="form-section">
        <view class="form-item">
          <text class="form-label">报告标题</text>
          <input v-model="title" placeholder="如：2025年度体检报告" class="form-input" />
        </view>
        <view class="form-item">
          <text class="form-label">体检医院</text>
          <input v-model="hospital" placeholder="如：北京协和医院" class="form-input" />
        </view>
      </view>

      <button class="submit-btn" :disabled="selectedFiles.length === 0" @tap="submitReport">
        开始分析
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useReportStore } from '@/stores/report'

const reportStore = useReportStore()
const selectedFiles = ref<string[]>([])
const title = ref('')
const hospital = ref('')

function chooseImage() {
  uni.chooseImage({
    count: 5,
    sizeType: ['compressed'],
    sourceType: ['camera', 'album'],
    success: (res) => {
      selectedFiles.value.push(...res.tempFilePaths)
    },
  })
}

function chooseFile() {
  // For H5
  uni.chooseImage({
    count: 5,
    sourceType: ['album'],
    success: (res) => {
      selectedFiles.value.push(...res.tempFilePaths)
    },
  })
}

function removeFile(index: number) {
  selectedFiles.value.splice(index, 1)
}

async function submitReport() {
  if (selectedFiles.value.length === 0) return

  try {
    uni.showLoading({ title: '上传分析中...' })
    const res = await reportStore.uploadReport(selectedFiles.value)
    uni.hideLoading()
    uni.showToast({ title: '上传成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateTo({ url: `/pages/report/detail?id=${res.report_id}` })
    }, 1500)
  } catch {
    uni.hideLoading()
    uni.showToast({ title: '上传失败', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
}

.upload-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
  margin-bottom: 32rpx;
}

.option-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 24rpx;
  background: #fff;
  border-radius: 16rpx;
  border: 2rpx dashed #4a90d9;
}

.option-icon {
  font-size: 56rpx;
  margin-bottom: 12rpx;
}

.option-title {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

.option-desc {
  font-size: 22rpx;
  color: #999;
  margin-top: 4rpx;
}

.preview-section {
  margin-bottom: 32rpx;
}

.preview-title {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}

.preview-list {
  display: flex;
  gap: 16rpx;
  flex-wrap: wrap;
}

.preview-item {
  position: relative;
  width: 160rpx;
  height: 160rpx;
}

.preview-image {
  width: 100%;
  height: 100%;
  border-radius: 8rpx;
}

.remove-btn {
  position: absolute;
  top: -12rpx;
  right: -12rpx;
  width: 40rpx;
  height: 40rpx;
  line-height: 40rpx;
  text-align: center;
  background: #e74c3c;
  color: #fff;
  border-radius: 50%;
  font-size: 28rpx;
}

.form-section {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 32rpx;
}

.form-item {
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

.form-label {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 8rpx;
  display: block;
}

.form-input {
  width: 100%;
  height: 72rpx;
  font-size: 28rpx;
}

.submit-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: #4a90d9;
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;

  &[disabled] {
    background: #a0c4e8;
  }
}
</style>
