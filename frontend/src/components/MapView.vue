<template>
  <div ref="mapEl" class="w-full h-full" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import type { Aircraft } from '../types'

const props = defineProps<{ aircraft: Aircraft[] }>()

const mapEl = ref<HTMLDivElement | null>(null)
let map: L.Map | null = null
const markers = new Map<string, L.Marker>()

const planeIconSvg = (isMilitary: boolean) => {
  const color = isMilitary ? '#ef4444' : '#3b82f6'
  return L.divIcon({
    className: '',
    html: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="${color}" style="filter:drop-shadow(0 0 3px ${color})">
      <path d="M21 16v-2l-8-5V3.5A1.5 1.5 0 0 0 11.5 2 1.5 1.5 0 0 0 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/>
    </svg>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  })
}

function buildPopup(ac: Aircraft): string {
  const callsign = ac.callsign || '(no callsign)'
  const alt = ac.altitude ?? '?'
  const spd = ac.speed ?? '?'
  const type = ac.type || '?'
  const squawk = ac.squawk || '?'
  const milBadge = ac.is_military
    ? `<span style="background:#ef4444;color:#fff;padding:2px 6px;border-radius:4px;font-size:11px">MILITARY</span>`
    : `<span style="background:#3b82f6;color:#fff;padding:2px 6px;border-radius:4px;font-size:11px">CIVIL</span>`
  return `
    <div style="font-family:monospace;font-size:12px;min-width:180px;color:#e2e8f0">
      <div style="font-size:14px;font-weight:700;margin-bottom:6px">${callsign} ${milBadge}</div>
      <div>Hex: <b>${ac.hex}</b></div>
      <div>Type: <b>${type}</b></div>
      <div>Alt: <b>${alt} ft</b></div>
      <div>Speed: <b>${spd} kts</b></div>
      <div>Squawk: <b>${squawk}</b></div>
      <div style="margin-top:6px;color:#94a3b8;font-size:11px">${ac.tile}</div>
    </div>
  `
}

onMounted(() => {
  if (!mapEl.value) return
  map = L.map(mapEl.value, {
    center: [5, 115],
    zoom: 4,
    zoomControl: true,
    attributionControl: false,
  })

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 18,
  }).addTo(map)

  updateMarkers(props.aircraft)
})

onUnmounted(() => {
  map?.remove()
})

function updateMarkers(aircraft: Aircraft[]) {
  if (!map) return
  const seen = new Set<string>()

  for (const ac of aircraft) {
    if (ac.lat == null || ac.lon == null) continue
    seen.add(ac.hex)

    if (markers.has(ac.hex)) {
      markers.get(ac.hex)!.setLatLng([ac.lat, ac.lon])
    } else {
      const m = L.marker([ac.lat, ac.lon], { icon: planeIconSvg(ac.is_military) })
        .bindPopup(buildPopup(ac), { className: 'dark-popup' })
        .addTo(map!)
      markers.set(ac.hex, m)
    }
  }

  for (const [hex, marker] of markers) {
    if (!seen.has(hex)) {
      marker.remove()
      markers.delete(hex)
    }
  }
}

watch(() => props.aircraft, updateMarkers)
</script>
