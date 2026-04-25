<template>
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs text-slate-400">{{ tweets.length }} sources</span>
      <button @click="$emit('refresh')" class="text-xs text-blue-400 hover:text-blue-300 transition-colors">
        Refresh
      </button>
    </div>

    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="error" class="text-red-400 text-xs p-2 bg-red-900/20 rounded">
      {{ error }}
    </div>

    <div v-else class="flex-1 overflow-y-auto space-y-2 pr-1">
      <div
        v-for="(tweet, i) in tweets"
        :key="i"
        class="bg-slate-800/50 border border-slate-700/50 rounded-lg p-3 hover:border-blue-500/40 transition-colors"
      >
        <div class="flex items-center gap-2 mb-2">
          <div class="w-6 h-6 rounded-full bg-blue-500/20 border border-blue-500/40 flex items-center justify-center text-xs font-bold text-blue-400">
            {{ tweet.source[0].toUpperCase() }}
          </div>
          <span class="text-blue-400 text-xs font-semibold">@{{ tweet.source }}</span>
          <span v-if="tweet.created_at" class="text-slate-500 text-xs ml-auto">{{ formatDate(tweet.created_at) }}</span>
        </div>

        <p class="text-slate-200 text-xs leading-relaxed line-clamp-4">{{ cleanText(tweet.text) }}</p>

        <img
          v-if="tweet.image_url"
          :src="tweet.image_url"
          class="mt-2 w-full rounded object-cover max-h-32"
          loading="lazy"
        />
      </div>

      <div v-if="tweets.length === 0" class="text-slate-500 text-xs text-center py-8">
        No tweets loaded yet
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Tweet } from '../types'

defineProps<{
  tweets: Tweet[]
  loading: boolean
  error: string | null
}>()

defineEmits<{ refresh: [] }>()

function cleanText(text: string): string {
  return text.replace(/\n{3,}/g, '\n\n').trim()
}

function formatDate(date: string): string {
  if (!date) return ''
  try {
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}
</script>
