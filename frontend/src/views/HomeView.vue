<script setup>
import { onMounted, computed, ref } from 'vue'
import { useMatchesStore } from '../stores/matches'
import MatchCard from '../components/MatchCard.vue'
import DateNavigator from '../components/DateNavigator.vue'
import HeroSection from '../components/HeroSection.vue'

const store = useMatchesStore()
const tournamentPrediction = ref(null)
const showPredictions = ref(false)

const displayGroups = computed(() => {
  if (store.selectedDate === 'today' && store.matchesByDate.length > 0) return store.matchesByDate
  if (store.selectedDate && store.selectedDate !== 'today') return [[store.selectedDate, store.matches]]
  return store.matchesByDate
})

function onDateSelect(date) { store.selectedDate = date; store.fetchMatches({ date }) }
function onToday() { store.selectedDate = 'today'; store.fetchToday() }

async function loadTournamentPrediction() {
  try { const r = await fetch('/api/predict/tournament'); if (r.ok) tournamentPrediction.value = await r.json() } catch {}
}

onMounted(() => { store.fetchDates(); store.fetchToday(); loadTournamentPrediction() })
</script>

<template>
  <div class="space-y-6">
    <HeroSection />

    <div class="flex items-center gap-3">
      <h2 class="text-xl sm:text-2xl font-black flex items-center gap-2">
        <span class="text-2xl">⚽</span>
        <span class="text-gradient-gold">Match Schedule</span>
      </h2>
      <span v-if="store.wsConnected" class="px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 text-[10px] font-bold border border-green-500/20 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>LIVE</span>
      <span v-if="store.matches.length > 0" class="px-2 py-0.5 rounded-full bg-surface-800/50 text-surface-500 text-[10px] font-bold border border-surface-700/30">{{ store.matches.length }} matches</span>
    </div>

    <DateNavigator :dates="store.dates" :selected="store.selectedDate" @select="onDateSelect" @today="onToday" />

    <div v-if="store.loading" class="grid gap-4">
      <div v-for="i in 4" :key="i" class="glass rounded-2xl p-5 animate-pulse">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4"><div class="w-10 h-10 rounded-full bg-surface-700"></div><div class="h-4 w-24 bg-surface-700 rounded"></div></div>
          <div class="h-6 w-16 bg-surface-700 rounded"></div>
          <div class="flex items-center gap-4"><div class="h-4 w-24 bg-surface-700 rounded"></div><div class="w-10 h-10 rounded-full bg-surface-700"></div></div>
        </div>
      </div>
    </div>

    <div v-else-if="store.error" class="text-center py-12 glass rounded-2xl"><p class="text-red-400 text-lg">⚠️ {{ store.error }}</p></div>

    <div v-else-if="store.matches.length === 0" class="text-center py-16 glass rounded-2xl">
      <span class="text-6xl block mb-4 animate-float">🏖️</span>
      <p class="text-surface-400 text-lg font-medium">No matches on this day</p>
      <p class="text-surface-600 text-sm mt-1">Select another date from the calendar above</p>
    </div>

    <div v-else class="space-y-8">
      <div v-for="([date, matches], gIdx) in displayGroups" :key="date" class="animate-slide-up" :style="{ animationDelay: gIdx * 0.05 + 's' }">
        <div class="flex items-center gap-3 mb-4">
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-yellow-500/10 to-transparent"></div>
          <span class="text-surface-400 text-sm font-bold px-4 py-1.5 rounded-full bg-surface-800/50 border border-surface-700/20 flex items-center gap-2">
            <span class="text-yellow-500/60">📅</span>
            {{ new Date(date + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) }}
          </span>
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-yellow-500/10 to-transparent"></div>
        </div>
        <div class="grid gap-3">
          <MatchCard v-for="(m, i) in matches" :key="m.id" :match="m" :style="{ animationDelay: (i * 0.05) + 's' }" class="animate-slide-up" />
        </div>
      </div>
    </div>

    <div v-if="tournamentPrediction" class="mt-10 glass-gold rounded-3xl overflow-hidden border-t-2 border-yellow-500/20">
      <button @click="showPredictions = !showPredictions" class="flex items-center justify-between w-full p-6 sm:p-8 group">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 flex items-center justify-center text-3xl animate-float group-hover:animate-kick transition-all">🔮</div>
          <div class="text-left">
            <h3 class="font-black text-lg text-gradient-gold">AI Tournament Prediction</h3>
            <p class="text-sm text-surface-400">Who will lift the trophy? Our AI analyzes team strength metrics</p>
          </div>
        </div>
        <span class="text-surface-500 text-xl transition-transform duration-300" :class="showPredictions ? 'rotate-180' : ''">▼</span>
      </button>

      <div v-show="showPredictions" class="px-6 sm:px-8 pb-6 sm:pb-8">
        <div class="flex items-center gap-4 p-4 rounded-2xl bg-gradient-to-r from-yellow-500/10 via-yellow-500/5 to-transparent border border-yellow-500/15 mb-6">
          <span class="text-4xl animate-trophy-shine">🏆</span>
          <div>
            <p class="text-xs text-surface-500 uppercase tracking-wider font-bold">Predicted Champion</p>
            <p class="font-black text-xl text-gradient-gold">{{ tournamentPrediction.favorite_name }}</p>
          </div>
        </div>

        <div class="space-y-3">
          <div v-for="(prob, code, idx) in tournamentPrediction.predictions" :key="code" class="flex items-center gap-3 p-2 rounded-xl hover:bg-surface-800/30 transition-colors" :style="{ animationDelay: idx * 0.05 + 's' }">
            <span class="text-sm font-bold w-10 text-surface-300 tabular-nums">#{{ idx + 1 }}</span>
            <span class="text-xl">{{ ['🇦🇷','🇧🇷','🇫🇷','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🇪🇸','🇩🇪','🇳🇱','🇵🇹'][idx] || '' }}</span>
            <span class="text-sm font-bold w-20 truncate text-white">{{ code }}</span>
            <div class="flex-1 h-4 rounded-full bg-surface-800/80 overflow-hidden">
              <div class="h-full rounded-full bg-gradient-to-r from-yellow-500 via-yellow-400 to-green-500 transition-all duration-1000 ease-out" :style="{ width: prob + '%', transitionDelay: idx * 0.1 + 's' }"></div>
            </div>
            <span class="text-xs font-black text-yellow-400 w-14 text-right tabular-nums">{{ prob }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
