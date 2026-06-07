<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMatchesStore } from '../stores/matches'
import { useFavoritesStore } from '../stores/favorites'
import CountdownTimer from '../components/CountdownTimer.vue'
import TeamFlag from '../components/TeamFlag.vue'

const route = useRoute()
const router = useRouter()
const store = useMatchesStore()
const favStore = useFavoritesStore()

const match = ref(null)
const prediction = ref(null)
const loading = ref(true)
const error = ref(null)
const showEvents = ref(false)

async function loadPrediction() {
  if (!match.value || match.value.team1_code === 'TBD') return
  try { const r = await fetch(`/api/predict/match/${match.value.id}`); if (r.ok) prediction.value = await r.json() } catch {}
}

async function simulateMatch() {
  if (!match.value) return
  await store.startSimulation(match.value.id)
}

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    const data = await store.fetchMatch(id)
    if (!data || data.error) error.value = 'Match not found'
    else { match.value = data; loadPrediction() }
  } catch (e) { error.value = e.message } finally { loading.value = false }
})

const istInfo = computed(() => {
  if (!match.value) return {}
  const d = new Date(match.value.date_utc)
  return {
    time: d.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: true }),
    date: d.toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }),
    utc: d.toLocaleString('en-US', { timeZone: 'UTC', hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short' }),
  }
})

const events = computed(() => store.liveEvents[match.value?.id] || [])
</script>

<template>
  <div class="space-y-6">
    <button @click="router.back()" class="flex items-center gap-2 text-surface-400 hover:text-yellow-400 transition-colors group">
      <span class="group-hover:-translate-x-1 transition-transform text-lg">←</span>
      <span class="text-sm font-bold">Back to Matches</span>
    </button>

    <div v-if="loading" class="glass rounded-3xl p-8 animate-pulse"><div class="flex items-center justify-between gap-8"><div class="flex-1 text-center"><div class="w-20 h-20 rounded-full bg-surface-700 mx-auto"></div></div><div class="text-center"><div class="h-8 w-24 bg-surface-700 rounded"></div></div><div class="flex-1 text-center"><div class="w-20 h-20 rounded-full bg-surface-700 mx-auto"></div></div></div></div>

    <div v-else-if="error" class="text-center py-16 glass rounded-2xl"><span class="text-6xl block mb-4">😕</span><p class="text-red-400 text-lg font-bold">{{ error }}</p></div>

    <template v-else-if="match">
      <div class="glass-gold rounded-3xl p-6 sm:p-10 overflow-hidden relative">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-500 via-green-500 to-yellow-500"></div>

        <div class="absolute top-4 right-4 text-[100px] opacity-[0.03] animate-trophy-shine select-none">🏆</div>

        <div class="text-center mb-8 relative z-10">
          <div class="flex items-center justify-center gap-2 mb-3">
            <span v-if="match.stage === 'Group Stage'" class="px-3 py-1.5 rounded-xl bg-surface-800/80 text-surface-400 text-xs font-bold uppercase tracking-wider border border-surface-700/30">Group {{ match.group }}</span>
            <span v-else class="px-3 py-1.5 rounded-xl bg-gradient-to-r from-yellow-600/30 to-amber-500/30 text-yellow-400 text-xs font-black uppercase tracking-wider border border-yellow-500/20">🏅 {{ match.stage }}</span>
            <span v-if="match.status === 'live'" class="px-2.5 py-1 rounded-xl bg-red-500/20 text-red-400 text-[10px] font-black uppercase tracking-wider flex items-center gap-1.5 border border-red-500/20"><span class="live-dot"></span>LIVE</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-black text-gradient-gold">{{ match.team1 }} vs {{ match.team2 }}</h1>
          <p class="text-surface-400 text-sm mt-2 font-medium">{{ istInfo.date }}</p>
        </div>

        <div class="flex items-center justify-between gap-4 sm:gap-12 py-8 sm:py-10 relative z-10">
          <div class="flex-1 text-center">
            <TeamFlag :code="match.team1_code" :flag="match.team1_flag" :name="match.team1" size="xl" class="mx-auto" />
            <p class="font-black text-lg sm:text-xl">{{ match.team1 }}</p>
            <p class="text-[10px] text-surface-500 uppercase tracking-widest font-bold mt-1">{{ match.team1_code }}</p>
          </div>
          <div class="text-center flex-shrink-0">
            <div v-if="match.score_team1 !== null" class="flex items-center gap-3 sm:gap-5">
              <span class="text-4xl sm:text-6xl font-black tabular-nums" :class="match.status === 'live' ? 'text-yellow-400 score-pop' : 'text-white'">{{ match.score_team1 }}</span>
              <span class="text-3xl sm:text-4xl font-black text-surface-600">:</span>
              <span class="text-4xl sm:text-6xl font-black tabular-nums" :class="match.status === 'live' ? 'text-yellow-400 score-pop' : 'text-white'">{{ match.score_team2 }}</span>
            </div>
            <div v-else class="space-y-4">
              <div class="text-4xl sm:text-5xl font-black text-yellow-400 tabular-nums">{{ istInfo.time }}</div>
              <div class="text-xs text-surface-500 font-bold uppercase tracking-wider">IST (UTC+5:30)</div>
              <CountdownTimer :date-utc="match.date_utc" />
            </div>
          </div>
          <div class="flex-1 text-center">
            <TeamFlag :code="match.team2_code" :flag="match.team2_flag" :name="match.team2" size="xl" class="mx-auto" />
            <p class="font-black text-lg sm:text-xl">{{ match.team2 }}</p>
            <p class="text-[10px] text-surface-500 uppercase tracking-widest font-bold mt-1">{{ match.team2_code }}</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-4 mt-6 pt-6 border-t border-yellow-500/10 relative z-10">
          <div class="flex items-center gap-1.5 text-sm text-surface-400"><span>📍</span><span class="font-medium">{{ match.venue }}</span></div>
          <span class="text-surface-700">·</span>
          <div class="text-sm text-surface-400 font-medium">🕐 UTC: {{ istInfo.utc }}</div>
          <span class="text-surface-700">·</span>
          <button @click="favStore.toggleMatch(match.id)" class="flex items-center gap-1.5 text-sm font-bold transition-all duration-200 px-3 py-1.5 rounded-lg" :class="favStore.isMatchFavorite(match.id) ? 'text-yellow-400 bg-yellow-500/10' : 'text-surface-400 hover:text-yellow-400 hover:bg-surface-800'">
            <span>{{ favStore.isMatchFavorite(match.id) ? '★' : '☆' }}</span>
            <span>{{ favStore.isMatchFavorite(match.id) ? 'Favorited' : 'Favorite' }}</span>
          </button>
        </div>

        <div v-if="match.status !== 'finished' && !match.team1_code.includes('TBD')" class="mt-8 flex justify-center relative z-10">
          <button @click="simulateMatch" class="px-8 py-3.5 rounded-2xl bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-black text-sm hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300 shadow-2xl shadow-yellow-500/20 hover:shadow-yellow-500/40 hover:scale-105 flex items-center gap-2 active:scale-95">
            <span class="text-lg">▶</span> Start Live Simulation
          </button>
        </div>
      </div>

      <div v-if="prediction && match.team1_code !== 'TBD'" class="glass-gold rounded-3xl p-6 sm:p-8">
        <h3 class="text-lg font-black flex items-center gap-2 mb-6"><span class="text-2xl animate-float" style="animation-duration:2.5s">🔮</span><span class="text-gradient-gold">AI Match Prediction</span></h3>
        <div class="grid sm:grid-cols-3 gap-4">
          <div class="p-5 rounded-2xl bg-gradient-to-br from-green-500/15 to-green-600/5 border border-green-500/15 text-center card-hover">
            <p class="text-3xl font-black text-green-400 tabular-nums">{{ prediction.win_probability }}</p>
            <p class="text-xs text-surface-400 mt-2 font-bold">{{ match.team1 }} Win</p>
          </div>
          <div class="p-5 rounded-2xl bg-surface-800/40 border border-surface-700/20 text-center card-hover">
            <p class="text-3xl font-black text-surface-300 tabular-nums">{{ prediction.draw_probability }}</p>
            <p class="text-xs text-surface-400 mt-2 font-bold">Draw</p>
          </div>
          <div class="p-5 rounded-2xl bg-gradient-to-br from-red-500/15 to-red-600/5 border border-red-500/15 text-center card-hover">
            <p class="text-3xl font-black text-red-400 tabular-nums">{{ prediction.lose_probability }}</p>
            <p class="text-xs text-surface-400 mt-2 font-bold">{{ match.team2 }} Win</p>
          </div>
        </div>
        <div class="mt-6 text-center">
          <span class="text-sm text-surface-400 font-medium">AI Confidence: <span class="font-black text-white capitalize px-2 py-0.5 rounded-lg" :class="prediction.confidence === 'high' ? 'bg-green-500/15 text-green-400' : 'bg-yellow-500/15 text-yellow-400'">{{ prediction.confidence }}</span></span>
          <span class="mx-3 text-surface-700">·</span>
          <span class="text-sm text-surface-400 font-medium">Predicted Winner: <span class="font-black text-gradient-gold">{{ prediction.predicted_winner === match.team1_code ? match.team1 : prediction.predicted_winner === match.team2_code ? match.team2 : 'Draw' }}</span></span>
        </div>
      </div>

      <div v-if="events.length > 0" class="glass-gold rounded-3xl p-6 sm:p-8">
        <h3 class="text-lg font-black flex items-center gap-2 mb-6"><span class="text-2xl">⚡</span><span class="text-gradient-gold">Live Events</span><span v-if="match.status === 'live'" class="ml-2"><span class="live-dot"></span></span></h3>
        <div class="space-y-2">
          <div v-for="evt in events" :key="evt.minute + '-' + evt.text" class="flex items-start gap-4 text-sm py-2 px-3 rounded-xl hover:bg-surface-800/30 transition-colors animate-slide-up">
            <span class="font-mono text-yellow-500/60 text-xs mt-0.5 w-12 flex-shrink-0 font-bold">{{ evt.minute }}'</span>
            <span :class="evt.type === 'goal' ? 'text-yellow-400 font-bold text-base' : 'text-surface-300'">{{ evt.text }}</span>
          </div>
        </div>
      </div>

      <div class="glass-gold rounded-3xl p-6 sm:p-8">
        <h3 class="text-lg font-black flex items-center gap-2 mb-4"><span class="text-2xl">🔔</span><span class="text-gradient-gold">Notifications & Reminders</span></h3>
        <p class="text-sm text-surface-400 mb-5 font-medium">Get notified before the match starts and follow live updates.</p>
        <div class="flex flex-wrap gap-3">
          <button @click="favStore.requestNotification()" class="px-5 py-2.5 rounded-xl bg-surface-800/60 text-white text-sm font-bold hover:bg-surface-700 transition-all duration-200 border border-surface-700/30 hover:border-surface-600 flex items-center gap-2">🔔 Enable Notifications</button>
          <button @click="favStore.toggleMatch(match.id)" class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 border flex items-center gap-2" :class="favStore.isMatchFavorite(match.id) ? 'bg-yellow-500/15 border-yellow-500/30 text-yellow-400' : 'bg-surface-800/60 border-surface-700/30 text-surface-400 hover:text-white hover:border-surface-600'">
            {{ favStore.isMatchFavorite(match.id) ? '★ Favorited' : '☆ Add to Favorites' }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>
