export interface User {
  id: string
  phone: string
  nickname: string
  avatar_url: string
  elder_mode: boolean
  created_at: string
}

export interface LoginParams {
  phone: string
  code: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  user: User
}
