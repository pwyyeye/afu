import { defineStore } from 'pinia'
import { ref } from 'vue'
import type {
  HealthProfile,
  FamilyMember,
  HealthDiary,
  HealthGoal,
  Reminder,
  TimelineItem,
} from '@/types/health'
import { request } from '@/api/request'

export const useHealthStore = defineStore('health', () => {
  const profile = ref<HealthProfile | null>(null)
  const familyMembers = ref<FamilyMember[]>([])
  const diaries = ref<HealthDiary[]>([])
  const goals = ref<HealthGoal[]>([])
  const reminders = ref<Reminder[]>([])
  const timeline = ref<TimelineItem[]>([])

  // Profile
  async function fetchProfile() {
    profile.value = await request.get<HealthProfile>('/api/v1/health/profile')
  }

  async function updateProfile(data: Partial<HealthProfile>) {
    profile.value = await request.put<HealthProfile>('/api/v1/health/profile', data)
  }

  // Family
  async function fetchFamily() {
    familyMembers.value = await request.get<FamilyMember[]>('/api/v1/health/family')
  }

  async function addMember(data: Partial<FamilyMember>) {
    const member = await request.post<FamilyMember>('/api/v1/health/family', data)
    familyMembers.value.push(member)
    return member
  }

  async function updateMember(id: string, data: Partial<FamilyMember>) {
    const member = await request.put<FamilyMember>(`/api/v1/health/family/${id}`, data)
    const idx = familyMembers.value.findIndex((m) => m.id === id)
    if (idx >= 0) familyMembers.value[idx] = member
    return member
  }

  async function deleteMember(id: string) {
    await request.delete(`/api/v1/health/family/${id}`)
    familyMembers.value = familyMembers.value.filter((m) => m.id !== id)
  }

  // Diary
  async function fetchDiaries(page = 1) {
    const res = await request.get<HealthDiary[]>('/api/v1/health/diary', { page })
    if (page === 1) diaries.value = res
    else diaries.value.push(...res)
    return res
  }

  async function createDiary(data: Partial<HealthDiary>) {
    const diary = await request.post<HealthDiary>('/api/v1/health/diary', data)
    diaries.value.unshift(diary)
    return diary
  }

  // Goals
  async function fetchGoals() {
    goals.value = await request.get<HealthGoal[]>('/api/v1/health/goals')
  }

  async function createGoal(data: Partial<HealthGoal>) {
    const goal = await request.post<HealthGoal>('/api/v1/health/goals', data)
    goals.value.push(goal)
    return goal
  }

  async function updateGoal(id: string, data: Partial<HealthGoal>) {
    const goal = await request.put<HealthGoal>(`/api/v1/health/goals/${id}`, data)
    const idx = goals.value.findIndex((g) => g.id === id)
    if (idx >= 0) goals.value[idx] = goal
    return goal
  }

  async function deleteGoal(id: string) {
    await request.delete(`/api/v1/health/goals/${id}`)
    goals.value = goals.value.filter((g) => g.id !== id)
  }

  async function updateGoalProgress(id: string, progress: Record<string, any>) {
    return updateGoal(id, { progress } as any)
  }

  // Timeline
  async function fetchTimeline() {
    timeline.value = await request.get<TimelineItem[]>('/api/v1/health/timeline')
  }

  // Reminders
  async function fetchReminders() {
    reminders.value = await request.get<Reminder[]>('/api/v1/health/reminders')
  }

  async function createReminder(data: Partial<Reminder>) {
    const reminder = await request.post<Reminder>('/api/v1/health/reminders', data)
    reminders.value.push(reminder)
    return reminder
  }

  return {
    profile,
    familyMembers,
    diaries,
    goals,
    reminders,
    timeline,
    fetchProfile,
    updateProfile,
    fetchFamily,
    addMember,
    updateMember,
    deleteMember,
    fetchDiaries,
    createDiary,
    fetchGoals,
    createGoal,
    updateGoal,
    deleteGoal,
    updateGoalProgress,
    fetchTimeline,
    fetchReminders,
    createReminder,
  }
})
