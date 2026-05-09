<template>
  <view class="page">
    <!-- Basic Info -->
    <view class="section-card">
      <text class="section-title">基本信息</text>
      <view class="form-item">
        <text class="form-label">姓名</text>
        <input v-model="form.name" placeholder="请输入姓名" class="form-input" />
      </view>
      <view class="form-item">
        <text class="form-label">关系</text>
        <picker :value="relationIndex" :range="relationOptions" @change="onRelationChange">
          <view class="picker-value">
            <text>{{ relationOptions[relationIndex] || '请选择' }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">性别</text>
        <picker :value="genderIndex" :range="genderOptions" @change="onGenderChange">
          <view class="picker-value">
            <text>{{ genderOptions[genderIndex] || '请选择' }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">出生日期</text>
        <picker mode="date" :value="form.birth_date" @change="onDateChange">
          <view class="picker-value">
            <text>{{ form.birth_date || '请选择' }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item">
        <text class="form-label">手机号</text>
        <input v-model="form.phone" type="number" placeholder="可选" class="form-input" />
      </view>
    </view>

    <!-- Health Info -->
    <view class="section-card">
      <text class="section-title">健康信息</text>
      <view class="form-item">
        <text class="form-label">血型</text>
        <picker :value="bloodTypeIndex" :range="bloodTypes" @change="onBloodTypeChange">
          <view class="picker-value">
            <text>{{ bloodTypes[bloodTypeIndex] || '请选择' }}</text>
            <text class="arrow">›</text>
          </view>
        </picker>
      </view>
      <view class="form-item column">
        <text class="form-label">过敏史</text>
        <textarea
          v-model="allergiesText"
          placeholder="如：花粉、海鲜（多个用逗号分隔）"
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
    </view>

    <!-- Actions -->
    <button class="save-btn" @tap="saveMember">保存</button>
    <button v-if="isEdit" class="delete-btn" @tap="deleteMember">删除该成员</button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useHealthStore } from '@/stores/health'

const healthStore = useHealthStore()
const isEdit = ref(false)
const editId = ref('')

const relationOptions = ['配偶', '父母', '子女', '其他']
const relationValues = ['spouse', 'parent', 'child', 'other']
const relationIndex = ref(0)

const genderOptions = ['男', '女']
const genderIndex = ref(0)

const bloodTypes = ['A', 'B', 'AB', 'O', '未知']
const bloodTypeIndex = ref(4)

const form = ref({
  name: '',
  birth_date: '',
  phone: '',
})

const allergiesText = ref('')
const conditionsText = ref('')
const medicationsText = ref('')

onLoad((options) => {
  if (options?.id) {
    isEdit.value = true
    editId.value = options.id
    const member = healthStore.familyMembers.find((m) => m.id === options.id)
    if (member) {
      form.value.name = member.name
      form.value.birth_date = member.birth_date || ''
      form.value.phone = member.phone || ''
      relationIndex.value = relationValues.indexOf(member.relationship)
      genderIndex.value = member.gender === '女' ? 1 : 0

      const hp = member.health_profile || {} as any
      bloodTypeIndex.value = bloodTypes.indexOf(hp.blood_type || '未知')
      if (bloodTypeIndex.value < 0) bloodTypeIndex.value = 4
      allergiesText.value = (hp.allergies || []).join('、')
      conditionsText.value = (hp.chronic_conditions || []).join('、')
      medicationsText.value = (hp.medications || []).join('、')
    }
  }
})

function onRelationChange(e: any) {
  relationIndex.value = e.detail.value
}

function onGenderChange(e: any) {
  genderIndex.value = e.detail.value
}

function onDateChange(e: any) {
  form.value.birth_date = e.detail.value
}

function onBloodTypeChange(e: any) {
  bloodTypeIndex.value = e.detail.value
}

async function saveMember() {
  if (!form.value.name) {
    uni.showToast({ title: '请输入姓名', icon: 'none' })
    return
  }

  const data = {
    name: form.value.name,
    relationship: relationValues[relationIndex.value],
    gender: genderOptions[genderIndex.value],
    birth_date: form.value.birth_date,
    phone: form.value.phone,
    health_profile: {
      blood_type: bloodTypes[bloodTypeIndex.value],
      allergies: allergiesText.value.split(/[、,，]/).filter(Boolean),
      chronic_conditions: conditionsText.value.split(/[、,，]/).filter(Boolean),
      medications: medicationsText.value.split(/[、,，]/).filter(Boolean),
    },
  }

  try {
    uni.showLoading({ title: '保存中...' })
    if (isEdit.value) {
      await healthStore.updateMember(editId.value, data)
    } else {
      await healthStore.addMember(data)
    }
    uni.hideLoading()
    uni.showToast({ title: '保存成功', icon: 'success' })
    setTimeout(() => uni.navigateBack(), 1500)
  } catch {
    uni.hideLoading()
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}

function deleteMember() {
  uni.showModal({
    title: '确认删除',
    content: '删除后不可恢复，确定删除该家庭成员？',
    confirmColor: '#e74c3c',
    success: async (res) => {
      if (res.confirm) {
        try {
          uni.showLoading({ title: '删除中...' })
          await healthStore.deleteMember(editId.value)
          uni.hideLoading()
          uni.showToast({ title: '已删除', icon: 'success' })
          setTimeout(() => uni.navigateBack(), 1500)
        } catch {
          uni.hideLoading()
          uni.showToast({ title: '删除失败', icon: 'none' })
        }
      }
    },
  })
}
</script>

<style scoped lang="scss">
.page {
  padding: 24rpx 32rpx;
  min-height: 100vh;
  padding-bottom: 48rpx;
}

.section-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
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
  color: #333;
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
  min-height: 100rpx;
  font-size: 28rpx;
  color: #333;
  line-height: 1.6;
  padding: 12rpx;
  background: #f8f9fa;
  border-radius: 8rpx;
}

.picker-value {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.picker-value text {
  font-size: 28rpx;
  color: #333;
}

.arrow {
  color: #ccc;
  font-size: 32rpx;
}

.save-btn {
  width: 100%;
  height: 96rpx;
  line-height: 96rpx;
  background: linear-gradient(135deg, #4a90d9, #357abd);
  color: #fff;
  font-size: 32rpx;
  font-weight: bold;
  border-radius: 16rpx;
  border: none;
  margin-bottom: 16rpx;
}

.delete-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background: #fff;
  color: #e74c3c;
  font-size: 28rpx;
  border-radius: 16rpx;
  border: 2rpx solid #e74c3c;
}
</style>
