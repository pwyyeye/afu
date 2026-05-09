export type TrafficLight = 'red' | 'yellow' | 'blue' | 'green'

export interface ReportIndicator {
  id: string
  name: string
  name_en?: string
  value: string
  unit?: string
  reference_range?: string
  light: TrafficLight
  explanation?: string
  trend?: 'rising' | 'falling' | 'stable'
}

export interface MedicalReport {
  id: string
  title: string
  hospital?: string
  report_date: string
  overall_light: TrafficLight
  summary?: string
  indicators: ReportIndicator[]
  action_plan?: ActionPlanItem[]
  status: 'processing' | 'completed' | 'failed'
  created_at: string
}

export interface ActionPlanItem {
  title: string
  description: string
  priority: TrafficLight
  category: 'checkup' | 'diet' | 'exercise' | 'medication' | 'lifestyle'
  checked?: boolean
}

export interface TrendData {
  name: string
  unit?: string
  data: { year: string; value: number }[]
}
