<template>
  <view class="page">
    <!-- Basic Info -->
    <view class="section-card">
      <text class="section-title">基本信息</text>
      <view class="form-item">
        <text class="form-label">血型</text>
        <picker :value="bloodTypeIndex" :range="bloodTypes" @change="onBloodTypeChange">
          <view class="picker-value">
            <text>{{ profile.blood_type || '请选择' }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">身高 (cm)</text>
        <input v-model="profile.height_cm" type="digit" placeholder="请输入" class="form-input" />
      </view>
      <view class="form-item">
        <text class="form-label">体重 (kg)</text>
        <input v-model="profile.weight_kg" type="digit" placeholder="请输入" class="form-input" />
      </view>
      <view v-if="profile.height_cm && profile.weight_kg" class="bmi-info">
        <text class="bmi-label">BMI:</text>
        <text class="bmi-value" :class="bmiClass">{{ bmi }}</text>
        <text class="bmi-desc">{{ bmiDesc }}</text>
      </view>
    </view>

    <!-- Health History -->
    <view class="section-card">
      <text class="section-title">健康史</text>
      <view class="form-item column">
        <text class="form-label">过敏史</text>
        <textarea
          v-model="allergiesText"
          placeholder="如：花粉、海鲜、青霉素（多个用逗号分隔）"
          class="form-textarea"
        />
      </view>
      <view class="form-item column">
        <text class="form-label">慢性病</text>
        <textarea
          v-model="conditionsText"
          placeholder="如：高血压、糖尿病（多个用逗号分隔）"
          class="form-textarea"
        />
      </view>
      <view class="form-item column">
        <text class="form-label">当前用药</text>
        <textarea
          v-model="medicationsText"
          placeholder="正在服用的药物"
          class="form-textarea"
        />
      </view>
      <view class="form-item column">
        <text class="form-label">手术史</text>
        <textarea
          v-model="surgeryText"
          placeholder="过往手术记录"
          class="form-textarea"
        />
      </view>
    </view>

    <!-- Lifestyle -->
    <view class="section-card">
      <text class="section-title">生活习惯</text>
      <view class="form-item">
        <text class="form-label">吸烟</text>
        <picker :value="smokingIndex" :range="smokingOptions" @change="onSmokingChange">
          <view class="picker-value">
            <text>{{ smokingOptions[smokingIndex] }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">饮酒</text>
        <picker :value="drinkingIndex" :range="drinkingOptions" @change="onDrinkingChange">
          <view class="picker-value">
            <text>{{ drinkingOptions[drinkingIndex] }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">运动频率</text>
        <picker :value="exerciseIndex" :range="exerciseOptions" @change="onExerciseChange">
          <view class="picker-value">
            <text>{{ exerciseOptions[exerciseIndex] }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
    </view>

    <!-- Notes -->
    <view class="section-card">
      <text class="section-title">备注</text>
      <textarea
        v-model="profile.notes"
        placeholder="其他需要医生了解的健康信息"
        class="form-textarea"
      />
    </view>

    <button class="save-btn" @tap="saveProfile">保存档案</button>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()

const bloodTypes = ['A', 'B', 'AB', 'O', '未知']
const bloodTypeIndex = ref(4)

const smokingOptions = ['从不', '已戒', '吸烟']
const smokingValues = ['never', 'former', 'current']
const smokingIndex = ref(0)

const drinkingOptions = ['从不', '偶尔', '经常']
const drinkingValues = ['never', 'occasional', 'regular']
const drinkingIndex = ref(0)

const exerciseOptions = ['很少', '每周', '每天']
const exerciseValues = ['rare', 'weekly', 'daily']
const exerciseIndex = ref(0)

const profile = ref({
  blood_type: '',
  height_cm: '',
  weight_kg: '',
  notes: '',
})

const allergiesText = ref('')
const conditionsText = ref('')
const medicationsText = ref('')
const surgeryText = ref('')

const bmi = computed(() => {
  const h = Number(profile.value.height_cm) / 100
  const w = Number(profile.value.weight_kg)
  if (h > 0 && w > 0) {
    return (w / (h * h)).toFixed(1)
  }
  return '--'
})

const bmiClass = computed(() => {
  const val = Number(bmi.value)
  if (isNaN(val)) return ''
  if (val < 18.5) return 'bmi-under'
  if (val < 24) return 'bmi-normal'
  if (val < 28) return 'bmi-over'
  return 'bmi-obese'
})

const bmiDesc = computed(() => {
  const val = Number(bmi.value)
  if (isNaN(val)) return ''
  if (val < 18.5) return '偏瘦'
  if (val < 24) return '正常'
  if (val < 28) return '偏胖'
  return '肥胖'
})

onMounted(async () => {
  await healthStore.fetchProfile()
  if (healthStore.profile) {
    const p = healthStore.profile
    profile.value.blood_type = p.blood_type || ''
    profile.value.height_cm = String(p.height_cm || '')
    profile.value.weight_kg = String(p.weight_kg || '')
    profile.value.notes = p.notes || ''
    allergiesText.value = (p.allergies || []).join('、')
    conditionsText.value = (p.chronic_conditions || []).join('、')
    medicationsText.value = (p.medications || []).join('、')
    surgeryText.value = (p.surgical_history || []).join('、')

    bloodTypeIndex.value = bloodTypes.indexOf(p.blood_type || '未知')
    if (bloodTypeIndex.value < 0) bloodTypeIndex.value = 4

    smokingIndex.value = smokingValues.indexOf(p.smoking || 'never')
    drinkingIndex.value = drinkingValues.indexOf(p.drinking || 'never')
    exerciseIndex.value = exerciseValues.indexOf(p.exercise_freq || 'rare')
  }
})

function onBloodTypeChange(e: any) {
  bloodTypeIndex.value = e.detail.value
  profile.value.blood_type = bloodTypes[bloodTypeIndex.value]
}

function onSmokingChange(e: any) {
  smokingIndex.value = e.detail.value
}

function onDrinkingChange(e: any) {
  drinkingIndex.value = e.detail.value
}

function onExerciseChange(e: any) {
  exerciseIndex.value = e.detail.value
}

async function saveProfile() {
  try {
    uni.showLoading({ title: '保存中...' })
    await healthStore.updateProfile({
      blood_type: profile.value.blood_type,
      height_cm: Number(profile.value.height_cm) || undefined,
      weight_kg: Number(profile.value.weight_kg) || undefined,
      allergies: allergiesText.value.split(/[、,，]/).filter(Boolean),
      chronic_conditions: conditionsText.value.split(/[、,，]/).filter(Boolean),
      medications: medicationsText.value.split(/[、,，]/).filter(Boolean),
      surgical_history: surgeryText.value.split(/[、,，]/).filter(Boolean),
      smoking: smokingValues[smokingIndex.value],
      drinking: drinkingValues[drinkingIndex.value],
      exercise_freq: exerciseValues[exerciseIndex.value],
      notes: profile.value.notes,
    })
    uni.hideLoading()
    uni.showToast({ title: '保存成功', icon: 'success' })
  } catch {
    uni.hideLoading()
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

.section-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2C2C2E;
  margin-bottom: 20rpx;
  display: block;
}

.form-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  &.column {
    flex-direction: column;
    align-items: flex-start;
    gap: 12rpx;
  }
}

.form-label {
  font-size: 28rpx;
  color: #2C2C2E;
  min-width: 140rpx;
}

.form-input {
  flex: 1;
  text-align: right;
  font-size: 28rpx;
  height: 48rpx;
}

.form-textarea {
  width: 100%;
  min-height: 120rpx;
  font-size: 28rpx;
  color: #2C2C2E;
  line-height: 1.6;
  padding: 12rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
}

.picker-value {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.picker-value text {
  font-size: 28rpx;
  color: #2C2C2E;
}

.arrow {
  color: #C5C5C8;
  font-size: 32rpx;
}

.bmi-info {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 16rpx;
  background: #f8f9fa;
  border-radius: 12rpx;
  margin-top: 16rpx;
}

.bmi-label {
  font-size: 26rpx;
  color: #6B6B70;
}

.bmi-value {
  font-size: 32rpx;
  font-weight: bold;
}

.bmi-under { color: #5A9BB8; }
.bmi-normal { color: #5CB87A; }
.bmi-over { color: #E8B84A; }
.bmi-obese { color: #E07070; }

.bmi-desc {
  font-size: 24rpx;
  color: #A0A0A5;
}

.save-btn {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  margin: 24rpx 32rpx;
  margin-bottom: calc(24rpx + env(safe-area-inset-bottom));
  height: 96rpx;
  line-height: 96rpx;
  background: #3B82A0;
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 12rpx;
  border: none;
}
</style>
