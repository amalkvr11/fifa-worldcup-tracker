<script setup>
import { computed, ref, onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import CountdownTimer from './CountdownTimer.vue'
import TeamFlag from './TeamFlag.vue'

const props = defineProps({ match: { type: Object, required: true } })

const favStore = useFavoritesStore()
const prediction = ref(null)
const hovered = ref(false)
const isFav = computed(() => favStore.isMatchFavorite(props.match.id))
const isKnockout = computed(() => props.match.stage !== 'Group Stage')
const isTbd = computed(() => props.match.team1_code === 'TBD')

const istTime = computed(() => new Date(props.match.date_utc).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: true }))
const istDate = computed(() => new Date(props.match.date_utc).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', weekday: 'short', day: 'numeric', month: 'short' }))

async function loadPrediction() {
  if (isTbd.value) return
  try { const r = await fetch(`/api/predict/match/${props.match.id}`); if (r.ok) prediction.value = await r.json() } catch {}
}
onMounted(loadPrediction)
</script>

<template>
  <router-link :to="`/match/${match.id}`" class="block glass-holographic rounded-2xl p-4 sm:p-5 card-hover cursor-pointer relative overflow-hidden group match-border-glow holographic-sweep" @mouseenter="hovered = true" @mouseleave="hovered = false">
    <div class="scan-line"></div>

    <div class="flex items-center justify-between mb-3 relative z-10">
      <div class="flex items-center gap-2">
        <span v-if="isKnockout" class="px-2.5 py-1 rounded-lg bg-gradient-to-r from-yellow-600/30 to-amber-500/30 text-yellow-400 text-[10px] font-black uppercase tracking-wider border border-yellow-500/20">
          🏅 {{ match.stage }}
        </span>
        <span v-else class="px-2.5 py-1 rounded-lg bg-surface-800/80 text-surface-400 text-[10px] font-bold uppercase tracking-wider border border-surface-700/30">
          Group {{ match.group }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <CountdownTimer :date-utc="match.date_utc" small />
        <button @click.prevent.stop="favStore.toggleMatch(match.id)" class="p-1.5 rounded-lg transition-all duration-200" :class="isFav ? 'text-yellow-400 bg-yellow-500/10' : 'text-surface-600 hover:text-yellow-500 hover:bg-surface-800'">
          <span class="text-sm">{{ isFav ? '★' : '☆' }}</span>
        </button>
      </div>
    </div>

    <div class="flex items-center justify-between gap-3 relative z-10">
      <div class="flex items-center gap-3 flex-1 min-w-0">
        <TeamFlag :code="match.team1_code" :flag="match.team1_flag" :name="match.team1" size="lg" />
        <span class="font-bold text-sm sm:text-base truncate" :class="isTbd ? 'text-surface-500 italic' : 'text-white'">{{ match.team1 }}</span>
      </div>

      <div class="flex items-center gap-3 flex-shrink-0">
        <div v-if="match.score_team1 !== null" class="flex items-center gap-2 font-black text-xl sm:text-2xl score-pop">
          <span class="text-white tabular-nums w-7 text-right">{{ match.score_team1 }}</span>
          <span class="text-surface-600">:</span>
          <span class="text-white tabular-nums w-7">{{ match.score_team2 }}</span>
        </div>
        <div v-else class="text-center min-w-[70px]">
          <div class="text-xs font-bold text-yellow-400">{{ istTime }}</div>
          <div class="text-[10px] text-surface-500">{{ istDate }}</div>
        </div>
      </div>

      <div class="flex items-center gap-3 flex-1 min-w-0 justify-end">
        <span class="font-bold text-sm sm:text-base truncate" :class="isTbd ? 'text-surface-500 italic' : 'text-white'">{{ match.team2 }}</span>
        <TeamFlag :code="match.team2_code" :flag="match.team2_flag" :name="match.team2" size="lg" />
      </div>
    </div>

    <div class="mt-3 flex items-center justify-between text-[11px] relative z-10">
      <div class="flex items-center gap-1.5 text-surface-500 truncate"><span>📍</span><span class="truncate">{{ match.venue }}</span></div>
      <div v-if="prediction && !isTbd" class="flex items-center gap-1.5 flex-shrink-0">
        <span class="text-[9px] text-yellow-500/60 font-bold">AI</span>
        <span class="px-2 py-0.5 rounded-lg bg-yellow-500/10 text-yellow-400 text-[10px] font-bold border border-yellow-500/10">
          {{ prediction.predicted_winner === match.team1_code ? match.team1 : match.team2 }} {{ prediction.win_probability }}
        </span>
      </div>
    </div>

    <div v-if="match.status === 'live'" class="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-red-500 to-red-600"></div>
  </router-link>
</template>
