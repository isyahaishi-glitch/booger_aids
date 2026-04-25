export interface Tweet {
  source: string
  text: string
  created_at: string
  image_url: string | null
}

export interface NewsArticle {
  title: string
  link: string
  published: string
  summary: string
  matched_keyword?: string
}

export interface TelegramMessage {
  channel: string
  text: string | null
  date: string
  id: number
}

export interface Aircraft {
  callsign: string | null
  hex: string
  lat: number | null
  lon: number | null
  altitude: number | string | null
  speed: number | null
  type: string | null
  squawk: string | null
  tile: string
  reasons: string[]
  is_military: boolean
}

export interface PlaneResponse {
  timestamp: string
  count: number
  data: Aircraft[]
}
