<template>
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs text-slate-400">{{ aircraft.length }} aircraft</span>
      <div class="flex items-center gap-2">
        <label class="flex items-center gap-1 text-xs text-slate-400 cursor-pointer">
          <input v-model="showMilOnly" type="checkbox" class="accent-red-500" />
          Mil only
        </label>
        <button @click="$emit('refresh')" class="text-xs text-blue-400 hover:text-blue-300 transition-colors">
          Refresh
        </button>
      </div>
    </div>

    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="error" class="text-red-400 text-xs p-2 bg-red-900/20 rounded">
      {{ error }}
    </div>

    <div v-else class="flex-1 overflow-y-auto space-y-1.5 pr-1">
      <div
        v-for="(ac, i) in filtered"
        :key="i"
        class="bg-slate-800/50 border rounded-lg p-2.5 hover:border-blue-500/40 transition-colors text-xs"
        :class="ac.is_military ? 'border-red-500/30' : 'border-slate-700/50'"
      >
        <div class="flex items-center gap-2 mb-1">
          <span class="text-lg leading-none">
            <svg viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5" :class="ac.is_military ? 'text-red-400' : 'text-blue-400'">
              <path d="M21 16v-2l-8-5V3.5A1.5 1.5 0 0 0 11.5 2 1.5 1.5 0 0 0 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/>
            </svg>
          </span>
          <span class="font-semibold" :class="ac.is_military ? 'text-red-300' : 'text-slate-100'">
            {{ ac.callsign || '(no callsign)' }}
          </span>
          <span class="ml-auto font-mono text-slate-400">{{ ac.hex }}</span>
          <span
            v-if="ac.is_military"
            class="text-[9px] bg-red-500/20 text-red-400 border border-red-500/30 px-1 py-0.5 rounded uppercase"
          >
            MIL
          </span>
        </div>
        <div class="grid grid-cols-3 gap-x-2 text-slate-400 text-[10px]">
          <span>Type: <b class="text-slate-300">{{ ac.type || '?' }}</b></span>
          <span>Alt: <b class="text-slate-300">{{ ac.altitude ?? '?' }}</b></span>
          <span>Spd: <b class="text-slate-300">{{ ac.speed ?? '?' }}</b></span>
        </div>
        <div class="text-slate-500 text-[10px] mt-1 truncate">{{ ac.tile }}</div>
      </div>

      <div v-if="filtered.length === 0" class="text-slate-500 text-xs text-center py-8">
        No aircraft data
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Aircraft } from '../types'

const props = defineProps<{
  aircraft: Aircraft[]
  loading: boolean
  error: string | null
}>()

defineEmits<{ refresh: [] }>()

const showMilOnly = ref(false)

const filtered = computed(() =>
  showMilOnly.value ? props.aircraft.filter(a => a.is_military) : props.aircraft
)
</script>
