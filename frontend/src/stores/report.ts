import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { MedicalReport, TrendData } from '@/types/report'
import { request } from '@/api/request'

export const useReportStore = defineStore('report', () => {
  const reports = ref<MedicalReport[]>([])
  const currentReport = ref<MedicalReport | null>(null)
  const isUploading = ref(false)
  const uploadProgress = ref(0)

  async function fetchReports() {
    const res = await request.get<MedicalReport[]>('/api/v1/reports')
    reports.value = res
  }

  async function fetchReportDetail(id: string) {
    const res = await request.get<MedicalReport>(`/api/v1/reports/${id}`)
    currentReport.value = res
    return res
  }

  async function uploadReport(files: string[], familyMemberId?: string) {
    isUploading.value = true
    uploadProgress.value = 0
    try {
      const res = await request.upload<{ report_id: string }>(
        '/api/v1/reports/upload',
        files,
        { family_member_id: familyMemberId || '' }
      )
      return res
    } finally {
      isUploading.value = false
    }
  }

  async function fetchComparison(indicatorNames: string[], years: string[]) {
    const res = await request.get<TrendData[]>('/api/v1/reports/compare', {
      indicator_names: indicatorNames.join(','),
      years: years.join(','),
    })
    return res
  }

  return {
    reports,
    currentReport,
    isUploading,
    uploadProgress,
    fetchReports,
    fetchReportDetail,
    uploadReport,
    fetchComparison,
  }
})
