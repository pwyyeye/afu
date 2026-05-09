import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatSession, ChatMessage } from '@/types/chat'
import { request } from '@/api/request'

const BASE_URL = 'http://localhost:8002'

export const useChatStore = defineStore('chat', () => {
  const sessions = ref<ChatSession[]>([])
  const currentSession = ref<ChatSession | null>(null)
  const messages = ref<ChatMessage[]>([])
  const isStreaming = ref(false)
  const streamingContent = ref('')

  async function fetchSessions() {
    const res = await request.get<ChatSession[]>('/api/v1/chat/sessions')
    sessions.value = res
  }

  async function createSession(familyMemberId?: string) {
    const res = await request.post<ChatSession>('/api/v1/chat/sessions', {
      family_member_id: familyMemberId,
    })
    sessions.value.unshift(res)
    currentSession.value = res
    return res
  }

  async function deleteSession(id: string) {
    await request.delete(`/api/v1/chat/sessions/${id}`)
    sessions.value = sessions.value.filter((s) => s.id !== id)
    if (currentSession.value?.id === id) {
      currentSession.value = null
      messages.value = []
    }
  }

  async function fetchMessages(sessionId: string) {
    const res = await request.get<ChatMessage[]>(
      `/api/v1/chat/sessions/${sessionId}/messages`
    )
    messages.value = res
  }

  async function sendMessage(sessionId: string, content: string, contentType: string = 'text') {
    // Add user message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      session_id: sessionId,
      role: 'user',
      content,
      content_type: contentType as any,
      created_at: new Date().toISOString(),
    }
    messages.value.push(userMsg)

    // Add AI placeholder
    const aiMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      session_id: sessionId,
      role: 'assistant',
      content: '',
      content_type: 'text',
      created_at: new Date().toISOString(),
    }
    messages.value.push(aiMsg)

    // Try SSE streaming first
    isStreaming.value = true
    streamingContent.value = ''

    try {
      const token = uni.getStorageSync('token')
      const response = await new Promise<string>((resolve, reject) => {
        let fullContent = ''

        // Use uni.request with chunked transfer for SSE-like behavior
        const requestTask = uni.request({
          url: `${BASE_URL}/api/v1/chat/messages/stream`,
          method: 'POST',
          header: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          data: {
            session_id: sessionId,
            content,
            content_type: contentType,
          },
          enableChunked: true,
          success: (res) => {
            // Parse the complete response as SSE
            const text = typeof res.data === 'string' ? res.data : ''
            const lines = text.split('\n')
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.type === 'chunk') {
                    fullContent += data.content
                  } else if (data.type === 'done') {
                    aiMsg.id = data.message_id || aiMsg.id
                  }
                } catch {}
              }
            }
            resolve(fullContent)
          },
          fail: (err) => reject(err),
        })

        // Listen for chunked data
        if (requestTask && typeof requestTask.onChunkReceived === 'function') {
          requestTask.onChunkReceived((res) => {
            const text = new TextDecoder().decode(res.data)
            const lines = text.split('\n')
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.type === 'chunk') {
                    fullContent += data.content
                    aiMsg.content = fullContent
                    streamingContent.value = fullContent
                  } else if (data.type === 'done') {
                    aiMsg.id = data.message_id || aiMsg.id
                  }
                } catch {}
              }
            }
          })
        }
      })

      aiMsg.content = response || aiMsg.content
    } catch {
      // Fallback to non-streaming
      try {
        const res = await request.post<{ content: string; message_id: string }>(
          '/api/v1/chat/messages',
          { session_id: sessionId, content, content_type: contentType }
        )
        aiMsg.content = res.content
        aiMsg.id = res.message_id || aiMsg.id
      } catch {
        aiMsg.content = '抱歉，服务暂时不可用，请稍后重试。'
      }
    } finally {
      isStreaming.value = false
      streamingContent.value = ''
    }
  }

  async function sendVoiceMessage(sessionId: string, filePath: string) {
    // Upload voice file, then send as text
    const token = uni.getStorageSync('token')
    isStreaming.value = true

    try {
      const uploadRes: any = await new Promise((resolve, reject) => {
        uni.uploadFile({
          url: `${BASE_URL}/api/v1/chat/messages/voice`,
          filePath,
          name: 'file',
          formData: { session_id: sessionId },
          header: { Authorization: `Bearer ${token}` },
          success: (res) => {
            try { resolve(JSON.parse(res.data)) } catch { reject(res) }
          },
          fail: reject,
        })
      })

      if (uploadRes.content) {
        await sendMessage(sessionId, uploadRes.content, 'voice')
      }
    } catch {
      uni.showToast({ title: '语音发送失败', icon: 'none' })
    } finally {
      isStreaming.value = false
    }
  }

  async function sendImageMessage(sessionId: string, filePath: string) {
    const token = uni.getStorageSync('token')
    isStreaming.value = true

    // Add user image message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      session_id: sessionId,
      role: 'user',
      content: '',
      content_type: 'image',
      media_url: filePath,
      created_at: new Date().toISOString(),
    }
    messages.value.push(userMsg)

    // Add AI placeholder
    const aiMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      session_id: sessionId,
      role: 'assistant',
      content: '',
      content_type: 'text',
      created_at: new Date().toISOString(),
    }
    messages.value.push(aiMsg)

    try {
      const uploadRes: any = await new Promise((resolve, reject) => {
        uni.uploadFile({
          url: `${BASE_URL}/api/v1/chat/messages/image`,
          filePath,
          name: 'file',
          formData: { session_id: sessionId },
          header: { Authorization: `Bearer ${token}` },
          success: (res) => {
            try { resolve(JSON.parse(res.data)) } catch { reject(res) }
          },
          fail: reject,
        })
      })

      aiMsg.content = uploadRes.content || '图片已收到，正在分析...'
    } catch {
      aiMsg.content = '图片分析失败，请重试。'
    } finally {
      isStreaming.value = false
    }
  }

  return {
    sessions,
    currentSession,
    messages,
    isStreaming,
    streamingContent,
    fetchSessions,
    createSession,
    deleteSession,
    fetchMessages,
    sendMessage,
    sendVoiceMessage,
    sendImageMessage,
  }
})
