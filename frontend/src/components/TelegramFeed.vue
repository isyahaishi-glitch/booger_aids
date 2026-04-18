<template>
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs text-slate-400">{{ messages.length }} channels</span>
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
        v-for="(msg, i) in messages"
        :key="i"
        class="bg-slate-800/50 border border-slate-700/50 rounded-lg p-3 hover:border-blue-500/40 transition-colors"
      >
        <div class="flex items-center gap-2 mb-2">
          <div class="w-5 h-5 shrink-0">
            <svg viewBox="0 0 24 24" fill="none" class="w-full h-full text-sky-400">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8l-1.7 8c-.12.58-.45.72-.92.44l-2.5-1.84-1.2 1.16c-.13.13-.25.24-.5.24l.18-2.52 4.6-4.16c.2-.18-.04-.28-.31-.1L7.6 14.9l-2.44-.76c-.53-.16-.54-.53.11-.79l9.54-3.68c.44-.16.83.1.83.63z" fill="currentColor"/>
            </svg>
          </div>
          <span class="text-sky-400 text-xs font-semibold truncate">{{ msg.channel }}</span>
          <span class="text-slate-500 text-[10px] ml-auto shrink-0">{{ formatDate(msg.date) }}</span>
        </div>

        <p v-if="msg.text" class="text-slate-200 text-xs leading-relaxed line-clamp-5">{{ msg.text }}</p>
        <p v-else class="text-slate-500 text-xs italic">No text content</p>
      </div>

      <div v-if="messages.length === 0" class="text-slate-500 text-xs text-center py-8">
        No messages loaded yet
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TelegramMessage } from '../types'

defineProps<{
  messages: TelegramMessage[]
  loading: boolean
  error: string | null
}>()

defineEmits<{ refresh: [] }>()

function formatDate(date: string): string {
  if (!date) return ''
  try {
    return new Date(date).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch {
    return date
  }
}
</script>
