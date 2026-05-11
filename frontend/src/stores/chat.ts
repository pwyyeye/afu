import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatSession, ChatMessage } from '@/types/chat'
import { request } from '@/api/request'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'

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
    // Use the proxied reference from the reactive array — the plain aiMsg object
    // won't trigger Vue reactivity when its properties change.
    const aiMsgRef = messages.value[messages.value.length - 1]

    // Try SSE streaming first
    isStreaming.value = true
    streamingContent.value = ''

    try {
      const token = uni.getStorageSync('token')
      const response = await new Promise<string>((resolve, reject) => {
        let fullContent = ''
        let realTimeChunks = false
        let sseBuffer = ''
        const decoder = new TextDecoder()

        // Parse SSE events, updating content in real-time
        function processSSEText(text: string) {
          sseBuffer += text
          const parts = sseBuffer.split('\n\n')
          sseBuffer = parts.pop() || ''
          for (const part of parts) {
            for (const line of part.split('\n')) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.type === 'chunk') {
                    fullContent += data.content
                    aiMsgRef.content = fullContent
                    streamingContent.value = fullContent
                  } else if (data.type === 'done') {
                    aiMsgRef.id = data.message_id || aiMsgRef.id
                  }
                } catch {}
              }
            }
          }
        }

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
            if (realTimeChunks) {
              resolve(fullContent)
              return
            }
            // H5 fallback: complete response arrived at once — parse SSE
            const text = typeof res.data === 'string' ? res.data : ''
            // Extract all chunk contents from the complete SSE response
            const chunks: string[] = []
            const lines = text.split('\n')
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.type === 'chunk') chunks.push(data.content)
                  else if (data.type === 'done') aiMsgRef.id = data.message_id || aiMsgRef.id
                } catch {}
              }
            }
            if (chunks.length) {
              // Simulate streaming: feed chunks progressively
              fullContent = ''
              let i = 0
              const feedTimer = setInterval(() => {
                if (i >= chunks.length) {
                  clearInterval(feedTimer)
                  resolve(fullContent)
                  return
                }
                fullContent += chunks[i]
                aiMsgRef.content = fullContent
                streamingContent.value = fullContent
                i++
              }, 50)
            } else if (text) {
              // No SSE framing — use raw text as-is
              fullContent = text
              aiMsgRef.content = fullContent
              streamingContent.value = fullContent
              resolve(fullContent)
            } else {
              resolve('')
            }
          },
          fail: (err) => reject(err),
        })

        // Listen for chunked data (real-time streaming, works on mini-programs)
        if (requestTask && typeof requestTask.onChunkReceived === 'function') {
          requestTask.onChunkReceived((res) => {
            realTimeChunks = true
            let text = ''
            try {
              if (typeof res.data === 'string') {
                text = res.data
              } else {
                text = decoder.decode(new Uint8Array(res.data))
              }
            } catch {
              text = typeof res.data === 'string' ? res.data : ''
            }
            if (text) processSSEText(text)
          })
        }
      })

      aiMsgRef.content = response || aiMsgRef.content
    } catch {
      // Fallback to non-streaming endpoint
      try {
        const res = await request.post<{ content: string; message_id: string }>(
          '/api/v1/chat/messages',
          { session_id: sessionId, content, content_type: contentType }
        )
        aiMsgRef.content = res.content
        aiMsgRef.id = res.message_id || aiMsgRef.id
      } catch {
        aiMsgRef.content = '抱歉，服务暂时不可用，请稍后重试。'
      }
    }

    // Keep isStreaming true for ChatBubble typewriter animation
    const finalLen = aiMsgRef.content?.length || 0
    const typewriterDelay = Math.min(Math.max(finalLen * 30, 300), 2000)
    setTimeout(() => {
      isStreaming.value = false
      streamingContent.value = ''
    }, typewriterDelay)
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
    const aiMsgRef = messages.value[messages.value.length - 1]

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

      aiMsgRef.content = uploadRes.content || '图片已收到，正在分析...'
    } catch {
      aiMsgRef.content = '图片分析失败，请重试。'
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
