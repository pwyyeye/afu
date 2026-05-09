export interface ChatSession {
  id: string
  title: string
  last_message: string
  family_member_id?: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: string
  session_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  content_type: 'text' | 'image' | 'voice'
  media_url?: string
  created_at: string
}

export interface SendMessageParams {
  session_id: string
  content: string
  content_type?: 'text' | 'image' | 'voice'
}
