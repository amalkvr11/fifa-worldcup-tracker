<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import TeamFlag from '../components/TeamFlag.vue'

const favStore = useFavoritesStore()
const teams = ref([])
const groups = ref({})
const loading = ref(true)
const searchQuery = ref('')
const selectedGroup = ref('all')
const sortBy = ref('group')
const predictions = ref({})
const hoveredTeam = ref(null)

onMounted(async () => {
  try {
    const [teamsRes, groupsRes] = await Promise.all([fetch('/api/teams'), fetch('/api/groups')])
    teams.value = await teamsRes.json()
    groups.value = await groupsRes.json()
    for (const g of Object.keys(groups.value)) {
      try { const r = await fetch(`/api/predict/group/${g}`); if (r.ok) predictions.value[g] = (await r.json()).predictions } catch {}
    }
  } catch (e) { console.error(e) } finally { loading.value = false }
})

const filteredTeams = computed(() => {
  let r = [...teams.value]
  if (searchQuery.value) { const q = searchQuery.value.toLowerCase(); r = r.filter(t => t.name.toLowerCase().includes(q) || t.code.toLowerCase().includes(q)) }
  if (selectedGroup.value !== 'all') r = r.filter(t => t.group === selectedGroup.value)
  if (sortBy.value === 'name') r.sort((a, b) => a.name.localeCompare(b.name))
  else r.sort((a, b) => a.group.localeCompare(b.group) || a.name.localeCompare(b.name))
  return r
})

const groupedTeams = computed(() => {
  const g = {}
  for (const t of filteredTeams.value) { if (!g[t.group]) g[t.group] = []; g[t.group].push(t) }
  return Object.entries(g).sort(([a], [b]) => a.localeCompare(b))
})

const groupKeys = computed(() => Object.keys(groups.value).sort())
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h2 class="text-xl sm:text-2xl font-black flex items-center gap-2"><span class="text-2xl">👥</span><span class="text-gradient-gold">Teams</span></h2>
        <p class="text-surface-400 text-sm mt-1">{{ teams.length }} teams · {{ groupKeys.length }} groups · AI-powered group predictions</p>
      </div>
      <button
        @click="$refs.playerAnimation.showDemo()"
        class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-yellow-500/20 to-green-500/15 border border-yellow-500/20 text-yellow-400 text-sm font-black hover:from-yellow-500/30 hover:to-green-500/20 transition-all duration-300 shadow-lg shadow-yellow-500/5 hover:shadow-yellow-500/15 flex items-center gap-2 hover:scale-105 active:scale-95"
      >
        <span>🎮</span> Player Animation
      </button>
    </div>

    <div class="flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-surface-500">🔍</span>
        <input v-model="searchQuery" type="text" placeholder="Search teams..." class="w-full pl-10 pr-4 py-3 rounded-xl bg-surface-800/50 border border-surface-700/30 text-white placeholder-surface-500 text-sm font-medium focus:outline-none focus:border-yellow-500/40 focus:ring-1 focus:ring-yellow-500/20 transition-all">
      </div>
      <select v-model="selectedGroup" class="px-4 py-3 rounded-xl bg-surface-800/50 border border-surface-700/30 text-white text-sm font-bold focus:outline-none focus:border-yellow-500/40 appearance-none cursor-pointer">
        <option value="all">All Groups</option>
        <option v-for="g in groupKeys" :key="g" :value="g">Group {{ g }}</option>
      </select>
      <select v-model="sortBy" class="px-4 py-3 rounded-xl bg-surface-800/50 border border-surface-700/30 text-white text-sm font-bold focus:outline-none focus:border-yellow-500/40 appearance-none cursor-pointer">
        <option value="group">By Group</option>
        <option value="name">By Name</option>
      </select>
    </div>

    <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
      <div v-for="i in 16" :key="i" class="glass rounded-2xl p-5 text-center animate-pulse"><div class="w-12 h-12 rounded-full bg-surface-700 mx-auto"></div><div class="h-4 w-20 bg-surface-700 rounded mx-auto mt-3"></div></div>
    </div>

    <div v-else-if="filteredTeams.length === 0" class="text-center py-16 glass rounded-2xl"><p class="text-surface-400 text-lg">No teams found</p></div>

    <div v-else-if="sortBy === 'group'" class="space-y-10">
      <div v-for="([group, groupTeams], gIdx) in groupedTeams" :key="group" class="animate-slide-up" :style="{ animationDelay: gIdx * 0.05 + 's' }">
        <div class="flex items-center gap-3 mb-4">
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-yellow-500/10 to-transparent"></div>
          <span class="text-lg font-black px-5 py-2 rounded-full bg-gradient-to-r from-yellow-500/10 to-green-500/5 border border-yellow-500/15 text-gradient-gold">Group {{ group }}</span>
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-yellow-500/10 to-transparent"></div>
        </div>

        <div v-if="predictions[group]" class="mb-5 p-4 rounded-2xl bg-gradient-to-r from-surface-800/50 to-surface-800/30 border border-surface-700/20">
          <p class="text-[10px] text-yellow-500 uppercase tracking-widest font-bold mb-3 flex items-center gap-1.5"><span>🔮</span> AI Group Prediction</p>
          <div class="flex gap-2 flex-wrap">
               <span v-for="p in predictions[group]" :key="p.code" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all duration-300" :class="p.qualify ? 'bg-yellow-500/15 text-yellow-400 border border-yellow-500/20 shadow-lg shadow-yellow-500/5' : 'bg-surface-800/60 text-surface-500 border border-surface-700/20'">
               <TeamFlag :code="p.code" :flag="p.flag" :name="p.code" size="xs" /> {{ p.code }} <span v-if="p.qualify" class="text-green-400">✓</span><span v-else class="text-red-400/50">✗</span>
               <span class="text-[9px] opacity-60">#{{ p.predicted_position }}</span>
             </span>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          <router-link
            v-for="(team, tIdx) in groupTeams"
            :key="team.code"
            :to="`/country/${team.code}`"
            class="glass-gold rounded-2xl p-5 text-center card-hover relative overflow-hidden group block"
            @mouseenter="hoveredTeam = team.code"
            @mouseleave="hoveredTeam = null"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <button @click.stop="favStore.toggleTeam(team.code)" class="absolute top-2 right-2 text-sm transition-all duration-200 z-10" :class="favStore.isTeamFavorite(team.code) ? 'text-yellow-400 scale-110' : 'text-surface-600 hover:text-yellow-500'">
              {{ favStore.isTeamFavorite(team.code) ? '★' : '☆' }}
            </button>
            <TeamFlag :code="team.code" :flag="team.flag" :name="team.name" size="lg" />
            <p class="font-bold text-sm truncate relative z-10">{{ team.name }}</p>
            <p class="text-[10px] text-surface-500 uppercase tracking-widest mt-1 font-medium relative z-10">{{ team.code }}</p>
            <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-yellow-500/0 to-transparent group-hover:via-yellow-500/40 transition-all duration-300"></div>
          </router-link>
        </div>
      </div>
    </div>

    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
      <router-link
        v-for="(team, tIdx) in filteredTeams"
        :key="team.code"
        :to="`/country/${team.code}`"
        class="glass-gold rounded-2xl p-5 text-center card-hover relative overflow-hidden group block animate-slide-up"
        :style="{ animationDelay: tIdx * 0.02 + 's' }"
        @mouseenter="hoveredTeam = team.code"
        @mouseleave="hoveredTeam = null"
      >
        <div class="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <button @click.stop="favStore.toggleTeam(team.code)" class="absolute top-2 right-2 text-sm transition-all duration-200 z-10" :class="favStore.isTeamFavorite(team.code) ? 'text-yellow-400 scale-110' : 'text-surface-600 hover:text-yellow-500'">
          {{ favStore.isTeamFavorite(team.code) ? '★' : '☆' }}
        </button>
        <TeamFlag :code="team.code" :flag="team.flag" :name="team.name" size="lg" />
        <p class="font-bold text-sm truncate relative z-10">{{ team.name }}</p>
        <p class="text-[10px] text-surface-500 uppercase tracking-widest mt-1 font-medium relative z-10">{{ team.code }}</p>
        <span class="inline-block mt-2 px-2 py-0.5 rounded-lg bg-surface-800/60 text-surface-500 text-[10px] font-mono border border-surface-700/20 relative z-10">Grp {{ team.group }}</span>
        <div class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-yellow-500/0 to-transparent group-hover:via-yellow-500/40 transition-all duration-300"></div>
      </router-link>
    </div>
  </div>
</template>
