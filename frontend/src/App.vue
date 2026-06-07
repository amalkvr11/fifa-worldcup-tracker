<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useFavoritesStore } from './stores/favorites'
import { useMatchesStore } from './stores/matches'
import AppHeader from './components/AppHeader.vue'
import ChatBot from './components/ChatBot.vue'
import LiveScoreBar from './components/LiveScoreBar.vue'
import ParticleBackground from './components/ParticleBackground.vue'

const favStore = useFavoritesStore()
const matchStore = useMatchesStore()

onMounted(() => {
  favStore.requestNotification()
  matchStore.connectWebSocket()
  matchStore.fetchLiveActive()
})
onUnmounted(() => { matchStore.disconnectWebSocket() })
</script>

<template>
  <div class="min-h-screen bg-[#070b14] text-white antialiased relative pitch-lines">
    <ParticleBackground />
    <div class="relative z-10">
      <AppHeader />
      <LiveScoreBar />
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 relative z-10">
        <router-view v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
      <footer class="border-t border-yellow-500/5 py-8 mt-12 relative z-10">
        <div class="max-w-7xl mx-auto px-4 text-center">
          <div class="flex items-center justify-center gap-2 mb-2">
            <span class="text-xl">🏆</span>
            <span class="text-gradient-gold font-black text-sm">FIFA WORLD CUP 2026</span>
            <span class="text-xl">⚽</span>
          </div>
          <p class="text-surface-500 text-xs">Live Match Tracker · AI Predictions · Real-time Scores · All times in IST</p>
        </div>
      </footer>
    </div>
    <ChatBot />
  </div>
</template>

<style>
.page-enter-active { transition: all 0.3s ease-out; }
.page-leave-active { transition: all 0.2s ease-in; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
