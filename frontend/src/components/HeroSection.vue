<script setup>
import { ref, onMounted } from 'vue'
import TeamFlag from './TeamFlag.vue'

const visible = ref(false)
const trophyScale = ref(0)
const stats = ref({ matches: 0, teams: 0, goals: 0 })
const playerCelebrating = ref(false)

const teamData = [
  { code: 'ARG', flag: '🇦🇷', name: 'Argentina', rating: 92 },
  { code: 'BRA', flag: '🇧🇷', name: 'Brazil', rating: 91 },
  { code: 'FRA', flag: '🇫🇷', name: 'France', rating: 91 },
  { code: 'ESP', flag: '🇪🇸', name: 'Spain', rating: 90 },
  { code: 'ENG', flag: '🏴󠁧󠁢󠁥󠁮󠁧󠁿', name: 'England', rating: 89 },
]

function triggerCelebration() {
  playerCelebrating.value = true
  setTimeout(() => { playerCelebrating.value = false }, 1200)
}

onMounted(() => {
  visible.value = true
  setTimeout(() => { trophyScale.value = 1 }, 200)

      const targetMatches = 72
  const targetTeams = 48
  const targetGoals = 156
  let frame = 0
  const totalFrames = 60
  const animateStats = () => {
    frame++
    const progress = Math.min(frame / totalFrames, 1)
    const ease = 1 - Math.pow(1 - progress, 3)
    stats.value = {
      matches: Math.round(targetMatches * ease),
      teams: Math.round(targetTeams * ease),
      goals: Math.round(targetGoals * ease),
    }
    if (frame < totalFrames) requestAnimationFrame(animateStats)
  }
  setTimeout(animateStats, 500)
})
</script>

<template>
  <div class="relative overflow-hidden rounded-3xl mb-8 hero-pattern" :class="{ 'opacity-100': visible, 'opacity-0': !visible }" style="transition: opacity 0.8s ease">
    <div class="absolute inset-0">
      <img src="/images/download.jpg" alt="FIFA 2026 Background" class="w-full h-full object-cover opacity-20 mix-blend-overlay" />
      <div class="absolute inset-0 bg-gradient-to-br from-[#0a0e17]/90 via-[#0a0e17]/70 to-[#0a0e17]/90"></div>
    </div>
    <div class="absolute top-4 right-8 text-[120px] opacity-[0.04] animate-trophy-shine select-none" style="filter: drop-shadow(0 0 20px rgba(250,204,21,0.3))">🏆</div>

    <div class="relative px-6 sm:px-10 py-10 sm:py-14">
      <div class="flex flex-col xl:flex-row items-center gap-8">
        <div class="flex-1 text-center sm:text-left">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs font-semibold mb-4 animate-slide-up">
            <span class="w-2 h-2 rounded-full bg-yellow-400 animate-pulse"></span>
            FIFA WORLD CUP 2026
          </div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black leading-tight mb-3" style="animation: slide-up 0.6s ease-out">
            <span class="text-gradient-gold">Track Every</span><br>
            <span class="text-white">Moment Live</span>
          </h1>
          <p class="text-surface-400 text-sm sm:text-base max-w-md mb-6" style="animation: slide-up 0.8s ease-out">
             48 teams. 12 groups. 72 matches. All in IST with AI predictions, live scores, and real-time match tracking.
          </p>

          <div class="flex flex-wrap justify-center sm:justify-start gap-6" style="animation: slide-up 1s ease-out">
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-black text-gradient-gold">{{ stats.matches }}+</div>
              <div class="text-[10px] text-surface-500 uppercase tracking-widest mt-1 font-bold">Matches</div>
            </div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-black text-gradient">{{ stats.teams }}</div>
              <div class="text-[10px] text-surface-500 uppercase tracking-widest mt-1 font-bold">Teams</div>
            </div>
            <div class="text-center">
              <div class="text-3xl sm:text-4xl font-black text-white">{{ stats.goals }}+</div>
              <div class="text-[10px] text-surface-500 uppercase tracking-widest mt-1 font-bold">Expected Goals</div>
            </div>
          </div>
        </div>

        <div class="flex-shrink-0" :style="{ transform: `scale(${trophyScale})`, transition: 'transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)' }">
          <div class="relative w-40 h-40 sm:w-52 sm:h-52 flex items-center justify-center">
            <div class="absolute inset-0 rounded-full bg-gradient-to-br from-yellow-500/15 to-green-500/10 animate-spin-slow"></div>
            <div class="absolute inset-3 rounded-full bg-gradient-to-br from-yellow-500/10 to-transparent"></div>
            <div class="absolute inset-6 rounded-full bg-surface-900/60 border border-yellow-500/10 animate-3d-rotate"></div>
            <span
              class="text-7xl sm:text-8xl relative z-10 animate-float"
              style="filter: drop-shadow(0 0 30px rgba(250,204,21,0.3)); cursor: pointer;"
              @click="triggerCelebration"
              title="Click the trophy to celebrate!"
            >🏆</span>
          </div>
        </div>
      </div>

      <div class="mt-10 mb-6">
        <div class="flex items-center gap-3 mb-4">
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-green-500/10 to-transparent"></div>
          <span class="text-[10px] text-surface-500 uppercase tracking-widest font-bold px-3">Star Players</span>
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-green-500/10 to-transparent"></div>
        </div>
        <div class="flex justify-center gap-4 sm:gap-6 flex-wrap">
          <button
            v-for="(player, idx) in teamData"
            :key="player.code"
            @click="triggerCelebration"
            class="group relative flex flex-col items-center p-3 sm:p-4 rounded-2xl bg-surface-900/60 border border-surface-700/20 transition-all duration-300 hover:border-yellow-500/30 hover:shadow-lg hover:shadow-yellow-500/10 hover:scale-105 active:scale-95"
            :style="{ animationDelay: idx * 0.1 + 's' }"
          >
            <TeamFlag :code="player.code" :flag="player.flag" :name="player.name" size="lg" />
            <div class="text-xs sm:text-sm font-black text-white group-hover:text-yellow-400 transition-colors">{{ player.name }}</div>
            <div class="text-[10px] text-surface-500 font-bold mt-0.5">OVR: <span class="text-yellow-400">{{ player.rating }}</span></div>
            <div class="absolute top-1 right-1 w-2 h-2 rounded-full bg-yellow-400 opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
          </button>
          <div class="hidden lg:flex items-center justify-center">
            <img
              src="/images/player-sprite.png"
              alt="Star Player"
              class="h-32 w-auto object-contain drop-shadow-2xl animate-float-slow"
              style="filter: drop-shadow(0 0 30px rgba(250,204,21,0.3));"
            />
          </div>
        </div>
      </div>

      <div class="mt-6 flex justify-center sm:justify-start">
        <div class="stadium-wave">
          <span v-for="i in 24" :key="i" :style="{ animationDelay: (i * 0.08) + 's', height: (12 + Math.sin(i * 0.7) * 8) + 'px' }"></span>
        </div>
      </div>
    </div>

    <div class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-yellow-500/20 to-transparent"></div>
  </div>
</template>
