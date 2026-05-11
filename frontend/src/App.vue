<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style>
page {
  background-color: #F8F6F3;
  font-family: 'Plus Jakarta Sans', 'Source Sans 3', 'PingFang SC', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 28rpx;
  color: #2C2C2E;
  box-sizing: border-box;
}

view, text {
  box-sizing: border-box;
}

.elder-mode page {
  font-size: 36rpx;
}
</style>
