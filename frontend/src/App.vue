<template>
  <div class="flex flex-col h-screen bg-slate-900 text-slate-200 select-none overflow-hidden">
    <!-- Header -->
    <header class="flex items-center gap-4 px-4 py-2.5 bg-slate-900 border-b border-slate-700/60 shrink-0 z-10">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        <span class="font-mono font-bold text-sm tracking-widest text-slate-100">OSINT DASHBOARD</span>
      </div>
      <div class="flex items-center gap-3 ml-4">
        <span class="text-xs font-mono text-slate-400">{{ timestamp }}</span>
        <span class="flex items-center gap-1 text-xs text-green-400">
          <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
          LIVE
        </span>
      </div>
      <div class="ml-auto flex items-center gap-4 text-xs text-slate-400 font-mono">
        <span>Planes: <b class="text-blue-400">{{ planeData.length }}</b></span>
        <span>Tweets: <b class="text-blue-400">{{ tweets.length }}</b></span>
        <span>News: <b class="text-blue-400">{{ news.length }}</b></span>
        <span>TG: <b class="text-blue-400">{{ telegram.length }}</b></span>
        <span class="text-slate-500">Refresh in {{ countdown }}s</span>
      </div>
    </header>

    <!-- Body -->
    <div class="flex flex-1 min-h-0">
      <!-- Sidebar -->
      <aside class="w-72 shrink-0 flex flex-col bg-slate-900 border-r border-slate-700/60">
        <!-- Tab nav -->
        <nav class="flex border-b border-slate-700/60 shrink-0">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="flex-1 py-2 text-xs font-mono font-semibold transition-colors relative"
            :class="activeTab === tab.id
              ? 'text-blue-400 bg-slate-800/60'
              : 'text-slate-500 hover:text-slate-300'"
          >
            {{ tab.label }}
            <span
              v-if="tab.badge"
              class="ml-0.5 text-[9px] bg-blue-500/20 text-blue-400 px-1 rounded"
            >{{ tab.badge }}</span>
            <div
              v-if="activeTab === tab.id"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500"
            />
          </button>
        </nav>

        <!-- Tab content -->
        <div class="flex-1 min-h-0 overflow-hidden p-3">
          <TweetFeed
            v-show="activeTab === 'tweets'"
            :tweets="tweets"
            :loading="loadingTweets"
            :error="errorTweets"
            @refresh="loadTweets"
          />
          <NewsFeed
            v-show="activeTab === 'news'"
            :articles="news"
            :loading="loadingNews"
            :error="errorNews"
            @refresh="loadNews"
          />
          <TelegramFeed
            v-show="activeTab === 'telegram'"
            :messages="telegram"
            :loading="loadingTelegram"
            :error="errorTelegram"
            @refresh="loadTelegram"
          />
          <PlaneTracker
            v-show="activeTab === 'planes'"
            :aircraft="planeData"
            :loading="loadingPlanes"
            :error="errorPlanes"
            @refresh="loadPlanes"
          />
        </div>
      </aside>

      <!-- Map area -->
      <main class="flex-1 min-w-0 relative">
        <MapView :aircraft="planeData" />

        <!-- Map overlay stats -->
        <div class="absolute top-3 right-3 z-[1000] bg-slate-900/90 border border-slate-700/60 rounded-lg p-2.5 text-xs font-mono space-y-1 backdrop-blur-sm">
          <div class="text-slate-400 text-[10px] uppercase tracking-wider mb-1.5">Active Aircraft</div>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-500" />
            <span class="text-slate-300">Civil: <b>{{ civilCount }}</b></span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-red-500" />
            <span class="text-slate-300">Military: <b>{{ milCount }}</b></span>
          </div>
          <div class="border-t border-slate-700/50 pt-1 mt-1 text-slate-400">
            Total: <b class="text-white">{{ planeData.length }}</b>
          </div>
        </div>

        <!-- Last updated overlay -->
        <div class="absolute bottom-3 left-3 z-[1000] bg-slate-900/80 border border-slate-700/60 rounded px-2 py-1 text-[10px] font-mono text-slate-400 backdrop-blur-sm">
          Last sync: {{ planeTimestamp || 'awaiting data' }}
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import MapView from './components/MapView.vue'
import TweetFeed from './components/TweetFeed.vue'
import NewsFeed from './components/NewsFeed.vue'
import TelegramFeed from './components/TelegramFeed.vue'
import PlaneTracker from './components/PlaneTracker.vue'
import { fetchTweets, fetchNews, fetchTelegram, fetchPlanes } from './api'
import type { Tweet, NewsArticle, TelegramMessage, Aircraft } from './types'

const INTERVAL = 60

const activeTab = ref<'tweets' | 'news' | 'telegram' | 'planes'>('planes')
const countdown  = ref(INTERVAL)
const timestamp  = ref('')
const planeTimestamp = ref('')

const tweets   = ref<Tweet[]>([])
const news     = ref<NewsArticle[]>([])
const telegram = ref<TelegramMessage[]>([])
const planeData = ref<Aircraft[]>([])

const loadingTweets   = ref(false)
const loadingNews     = ref(false)
const loadingTelegram = ref(false)
const loadingPlanes   = ref(false)

const errorTweets   = ref<string | null>(null)
const errorNews     = ref<string | null>(null)
const errorTelegram = ref<string | null>(null)
const errorPlanes   = ref<string | null>(null)

const tabs = computed(() => [
  { id: 'tweets' as const,   label: 'Tweets',   badge: tweets.value.length || null },
  { id: 'news' as const,     label: 'News',     badge: news.value.length || null },
  { id: 'telegram' as const, label: 'Telegram', badge: telegram.value.length || null },
  { id: 'planes' as const,   label: 'Planes',   badge: planeData.value.length || null },
])

const milCount   = computed(() => planeData.value.filter(a => a.is_military).length)
const civilCount = computed(() => planeData.value.filter(a => !a.is_military).length)

async function loadTweets() {
  loadingTweets.value = true
  errorTweets.value = null
  try { tweets.value = await fetchTweets() }
  catch { errorTweets.value = 'Cannot reach :5000' }
  finally { loadingTweets.value = false }
}

async function loadNews() {
  loadingNews.value = true
  errorNews.value = null
  try { news.value = await fetchNews() }
  catch { errorNews.value = 'Cannot reach :5001' }
  finally { loadingNews.value = false }
}

async function loadTelegram() {
  loadingTelegram.value = true
  errorTelegram.value = null
  try { telegram.value = await fetchTelegram() }
  catch { errorTelegram.value = 'Cannot reach :5002' }
  finally { loadingTelegram.value = false }
}

async function loadPlanes() {
  loadingPlanes.value = true
  errorPlanes.value = null
  try {
    const res = await fetchPlanes()
    planeData.value = res.data
    planeTimestamp.value = res.timestamp
  } catch { errorPlanes.value = 'Cannot reach :5003' }
  finally { loadingPlanes.value = false }
}

function loadAll() {
  loadTweets()
  loadNews()
  loadTelegram()
  loadPlanes()
}

function updateClock() {
  timestamp.value = new Date().toLocaleTimeString()
}

let refreshTimer: ReturnType<typeof setInterval>
let countdownTimer: ReturnType<typeof setInterval>
let clockTimer: ReturnType<typeof setInterval>

onMounted(() => {
  loadAll()
  updateClock()

  clockTimer = setInterval(updateClock, 1000)

  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      countdown.value = INTERVAL
    }
  }, 1000)

  refreshTimer = setInterval(loadAll, INTERVAL * 1000)
})

onUnmounted(() => {
  clearInterval(refreshTimer)
  clearInterval(countdownTimer)
  clearInterval(clockTimer)
})
</script>
