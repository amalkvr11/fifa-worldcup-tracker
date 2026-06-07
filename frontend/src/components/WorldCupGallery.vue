<script setup>
import { ref } from 'vue'

const worldCups = [
  { year: '2026', host: 'USA · Canada · Mexico', logo: '🏆', color: 'from-yellow-500 to-green-500', matches: 104, teams: 48, tagline: 'Expanded to 48 Teams' },
  { year: '2022', host: 'Qatar', logo: '⚽', color: 'from-purple-600 to-red-500', matches: 64, teams: 32, tagline: 'First Arab World Cup' },
  { year: '2018', host: 'Russia', logo: '🥇', color: 'from-blue-700 to-red-600', matches: 64, teams: 32, tagline: 'France Wins Again' },
  { year: '2014', host: 'Brazil', logo: '🌟', color: 'from-green-600 to-yellow-500', matches: 64, teams: 32, tagline: 'Germany Triumphs' },
  { year: '2010', host: 'South Africa', logo: '🌍', color: 'from-yellow-500 to-black', matches: 64, teams: 32, tagline: 'First in Africa' },
  { year: '2006', host: 'Germany', logo: '🇩🇪', color: 'from-yellow-400 to-red-600', matches: 64, teams: 32, tagline: 'Italy Wins on Penalties' },
  { year: '2002', host: 'Korea · Japan', logo: '🇰🇷', color: 'from-red-600 to-blue-700', matches: 64, teams: 32, tagline: 'Brazil 5th Title' },
  { year: '1998', host: 'France', logo: '🇫🇷', color: 'from-blue-700 to-red-500', matches: 64, teams: 32, tagline: 'Zidane\'s Masterclass' },
  { year: '1994', host: 'United States', logo: '🇺🇸', color: 'from-blue-600 to-red-600', matches: 52, teams: 24, tagline: 'Bravo\'s Golden Save' },
  { year: '1990', host: 'Italy', logo: '🇮🇹', color: 'from-green-600 to-white', matches: 52, teams: 24, tagline: 'Germany\'s 3rd Title' },
  { year: '1986', host: 'Mexico', logo: '🇲🇽', color: 'from-green-600 to-red-600', matches: 52, teams: 24, tagline: 'Maradona\'s Hand of God' },
  { year: '1982', host: 'Spain', logo: '🇪🇸', color: 'from-red-600 to-yellow-500', matches: 52, teams: 24, tagline: 'First 24-Team Format' },
]

const selectedCup = ref(null)

function selectCup(cup) {
  selectedCup.value = cup
}

function closeModal() {
  selectedCup.value = null
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center gap-3">
      <h2 class="text-xl sm:text-2xl font-black flex items-center gap-2">
        <span class="text-2xl">📸</span>
        <span class="text-gradient-gold">FIFA World Cup Gallery</span>
      </h2>
      <p class="text-surface-400 text-sm hidden sm:block">Relive the magic from every tournament</p>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
      <button
        v-for="(cup, idx) in worldCups"
        :key="cup.year"
        @click="selectCup(cup)"
        class="group relative overflow-hidden rounded-2xl aspect-[3/4] card-hover animate-slide-up"
        :style="{ animationDelay: idx * 0.03 + 's' }"
      >
        <div class="absolute inset-0 bg-gradient-to-br" :class="cup.color"></div>
        <div class="absolute inset-0 bg-[#0a0e17]/50 group-hover:bg-[#0a0e17]/30 transition-all duration-500"></div>

        <div class="relative z-10 h-full flex flex-col items-center justify-center p-3 text-center">
          <div class="text-4xl sm:text-5xl mb-2 filter drop-shadow-lg group-hover:scale-110 transition-transform duration-300">
            {{ cup.logo }}
          </div>
          <div class="text-lg sm:text-xl font-black text-white mb-1">{{ cup.year }}</div>
          <div class="text-[10px] text-white/80 font-bold uppercase tracking-wider">{{ cup.host }}</div>
          <div class="mt-2 text-[9px] text-white/60 font-medium max-w-[120px] line-clamp-2">{{ cup.tagline }}</div>
        </div>

        <div class="absolute top-2 right-2 w-6 h-6 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
          <span class="text-xs text-white">↗</span>
        </div>
      </button>
    </div>

    <Transition name="modal">
      <div v-if="selectedCup" class="fixed inset-0 z-[999] flex items-center justify-center p-4" @click.self="closeModal">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="closeModal"></div>
        <div class="relative glass-gold rounded-3xl p-6 sm:p-8 max-w-lg w-full animate-bounce-in shadow-2xl shadow-yellow-500/10">
          <button @click="closeModal" class="absolute top-4 right-4 w-10 h-10 rounded-full bg-surface-800/80 text-white hover:bg-surface-700 transition-colors flex items-center justify-center text-lg">✕</button>

          <div class="text-center">
            <div class="text-6xl sm:text-7xl mb-4">{{ selectedCup.logo }}</div>
            <h3 class="text-3xl sm:text-4xl font-black text-gradient-gold mb-2">{{ selectedCup.year }}</h3>
            <p class="text-surface-300 font-medium mb-6">{{ selectedCup.host }}</p>
            <p class="text-sm text-surface-400 italic mb-8">"{{ selectedCup.tagline }}"</p>

            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="p-4 rounded-2xl bg-surface-800/40 border border-surface-700/20">
                <div class="text-2xl font-black text-white">{{ selectedCup.teams }}</div>
                <div class="text-[10px] text-surface-500 uppercase tracking-wider font-bold">Teams</div>
              </div>
              <div class="p-4 rounded-2xl bg-surface-800/40 border border-surface-700/20">
                <div class="text-2xl font-black text-white">{{ selectedCup.matches }}</div>
                <div class="text-[10px] text-surface-500 uppercase tracking-wider font-bold">Matches</div>
              </div>
            </div>

            <div class="h-px bg-gradient-to-r from-transparent via-yellow-500/20 to-transparent mb-6"></div>

            <div class="flex flex-wrap justify-center gap-2">
              <span class="px-3 py-1.5 rounded-xl bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs font-bold">🏅 Historic</span>
              <span class="px-3 py-1.5 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-bold">⚽ Iconic</span>
              <span class="px-3 py-1.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold">✨ Legendary</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.modal-enter-active { transition: all 0.3s ease-out; }
.modal-leave-active { transition: all 0.2s ease-in; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
