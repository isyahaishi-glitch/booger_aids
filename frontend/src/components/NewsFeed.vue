<template>
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs text-slate-400">{{ articles.length }} articles</span>
      <button @click="$emit('refresh')" class="text-xs text-blue-400 hover:text-blue-300 transition-colors">
        Refresh
      </button>
    </div>

    <div class="mb-2">
      <input
        v-model="keyword"
        type="text"
        placeholder="Filter by keyword..."
        class="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
      />
    </div>

    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="error" class="text-red-400 text-xs p-2 bg-red-900/20 rounded">
      {{ error }}
    </div>

    <div v-else class="flex-1 overflow-y-auto space-y-2 pr-1">
      <a
        v-for="(article, i) in filtered"
        :key="i"
        :href="article.link"
        target="_blank"
        rel="noopener"
        class="block bg-slate-800/50 border border-slate-700/50 rounded-lg p-3 hover:border-blue-500/40 transition-colors no-underline"
      >
        <div class="flex items-start justify-between gap-2 mb-1">
          <h3 class="text-slate-100 text-xs font-semibold leading-snug line-clamp-2">{{ article.title }}</h3>
          <span
            v-if="article.matched_keyword"
            class="shrink-0 text-[10px] bg-amber-500/20 text-amber-400 border border-amber-500/30 px-1.5 py-0.5 rounded"
          >
            {{ article.matched_keyword }}
          </span>
        </div>
        <p class="text-slate-400 text-xs leading-relaxed line-clamp-2 mb-1">{{ article.summary }}</p>
        <div class="flex items-center gap-2 mt-1">
          <span class="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
          <span class="text-slate-500 text-[10px]">{{ formatDate(article.published) }}</span>
        </div>
      </a>

      <div v-if="filtered.length === 0" class="text-slate-500 text-xs text-center py-8">
        No articles found
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { NewsArticle } from '../types'

const props = defineProps<{
  articles: NewsArticle[]
  loading: boolean
  error: string | null
}>()

defineEmits<{ refresh: [] }>()

const keyword = ref('')

const filtered = computed(() => {
  if (!keyword.value.trim()) return props.articles
  const kw = keyword.value.toLowerCase()
  return props.articles.filter(a =>
    a.title.toLowerCase().includes(kw) || a.summary.toLowerCase().includes(kw)
  )
})

function formatDate(date: string): string {
  if (!date) return ''
  try {
    return new Date(date).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch {
    return date
  }
}
</script>
