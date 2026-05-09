export interface HealthProfile {
  id: string
  blood_type?: string
  height_cm?: number
  weight_kg?: number
  allergies?: string[]
  chronic_conditions?: string[]
  medications?: string[]
  surgical_history?: string[]
  family_history?: string[]
  smoking?: 'never' | 'former' | 'current'
  drinking?: 'never' | 'occasional' | 'regular'
  exercise_freq?: 'rare' | 'weekly' | 'daily'
  notes?: string
}

export interface FamilyMember {
  id: string
  name: string
  relationship: 'self' | 'spouse' | 'parent' | 'child' | 'other'
  gender?: string
  birth_date?: string
  phone?: string
  avatar_url?: string
  health_profile?: Partial<HealthProfile>
  created_at: string
}

export interface HealthDiary {
  id: string
  content: string
  mood?: 'great' | 'good' | 'okay' | 'bad'
  tags?: string[]
  metrics?: Record<string, number>
  diary_date: string
  created_at: string
}

export interface HealthGoal {
  id: string
  title: string
  category: 'exercise' | 'diet' | 'habit' | 'checkup'
  target?: Record<string, any>
  target_value?: number
  current_value?: number
  unit?: string
  progress?: Record<string, any>
  start_date?: string
  end_date?: string
  status: 'active' | 'completed' | 'paused'
  created_at: string
}

export interface Reminder {
  id: string
  title: string
  type: 'medication' | 'checkup' | 'exercise' | 'custom'
  schedule?: Record<string, any>
  next_trigger?: string
  enabled: boolean
}

export interface TimelineItem {
  id: string
  type: 'report' | 'diary' | 'goal' | 'reminder'
  title: string
  description?: string
  date: string
  data?: any
}
