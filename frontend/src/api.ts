import axios from 'axios'
import type { Tweet, NewsArticle, TelegramMessage, PlaneResponse } from './types'

const tweet = axios.create({ baseURL: 'http://localhost:5000' })
const rss   = axios.create({ baseURL: 'http://localhost:5001' })
const tg    = axios.create({ baseURL: 'http://localhost:5002' })
const plane = axios.create({ baseURL: 'http://localhost:5003' })

export const fetchTweets    = (): Promise<Tweet[]>           => tweet.get('/tweets').then(r => r.data)
export const fetchNews      = (): Promise<NewsArticle[]>     => rss.get('/antara').then(r => r.data)
export const fetchTelegram  = (): Promise<TelegramMessage[]> => tg.get('/telegram').then(r => r.data)
export const fetchPlanes    = (): Promise<PlaneResponse>     => plane.get('/plane').then(r => r.data)
