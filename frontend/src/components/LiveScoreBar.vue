<script setup>
import { onMounted } from 'vue'
import { useMatchesStore } from '../stores/matches'

const store = useMatchesStore()
onMounted(() => { store.fetchLiveActive() })
</script>

<template>
  <div v-if="store.liveMatches.length > 0" class="bg-gradient-to-r from-red-900/30 via-red-800/20 to-red-900/30 border-b border-red-700/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
      <div class="flex items-center gap-4 overflow-x-auto" style="scrollbar-width:none">
        <div class="flex items-center gap-2 flex-shrink-0">
          <span class="live-dot"></span>
          <span class="text-xs font-black text-red-400 uppercase tracking-wider">LIVE</span>
        </div>
        <div v-for="lm in store.liveMatches" :key="lm.match_id" class="flex items-center gap-3 flex-shrink-0 bg-surface-900/50 rounded-xl px-4 py-2 border border-red-500/10">
          <span class="text-sm font-bold text-white">{{ lm.team1 }}</span>
          <span class="text-lg font-black text-yellow-400 tabular-nums">{{ lm.score_team1 }}</span>
          <span class="text-surface-600 text-xs">:</span>
          <span class="text-lg font-black text-yellow-400 tabular-nums">{{ lm.score_team2 }}</span>
          <span class="text-sm font-bold text-white">{{ lm.team2 }}</span>
          <span class="bg-red-500/20 text-red-400 text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider animate-pulse">● LIVE</span>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="bg-gradient-to-r from-surface-900/30 via-surface-800/10 to-surface-900/30 border-b border-surface-800/20">
    <div class="max-w-7xl mx-auto px-4 py-2 text-center">
      <p class="text-[11px] text-surface-600 font-medium">⚡ Click "Start Live Simulation" on any match to see real-time score updates!</p>
    </div>
  </div>
</template>
