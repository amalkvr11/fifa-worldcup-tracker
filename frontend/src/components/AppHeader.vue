<script setup>
import { ref } from 'vue'
import { useFavoritesStore } from '../stores/favorites'

const favStore = useFavoritesStore()
const showFavs = ref(false)
</script>

<template>
  <header class="sticky top-0 z-50 glass-strong">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="flex items-center gap-3 group">
          <span class="text-2xl group-hover:animate-kick transition-transform">🏆</span>
          <div>
            <h1 class="text-lg font-black tracking-tight">
              <span class="text-gradient-gold">FIFA</span>
              <span class="text-white ml-1">2026</span>
            </h1>
            <p class="text-[9px] text-surface-500 font-bold uppercase tracking-[0.25em] -mt-0.5">World Cup Tracker</p>
          </div>
        </router-link>

        <nav class="flex items-center gap-1">
          <router-link to="/" class="px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200" :class="$route.path === '/' ? 'bg-yellow-500/15 text-yellow-400 shadow-lg shadow-yellow-500/5' : 'text-surface-400 hover:text-white hover:bg-surface-800/50'">
            <span class="hidden sm:inline">⚽ Matches</span>
            <span class="sm:hidden">⚽</span>
          </router-link>
          <router-link to="/teams" class="px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200" :class="$route.path === '/teams' ? 'bg-yellow-500/15 text-yellow-400 shadow-lg shadow-yellow-500/5' : 'text-surface-400 hover:text-white hover:bg-surface-800/50'">
            <span class="hidden sm:inline">👥 Teams</span>
            <span class="sm:hidden">👥</span>
          </router-link>
          <router-link to="/gallery" class="px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200" :class="$route.path === '/gallery' ? 'bg-yellow-500/15 text-yellow-400 shadow-lg shadow-yellow-500/5' : 'text-surface-400 hover:text-white hover:bg-surface-800/50'">
            <span class="hidden sm:inline">📸 Gallery</span>
            <span class="sm:hidden">📸</span>
          </router-link>

          <div class="relative ml-2" @mouseenter="showFavs = true" @mouseleave="showFavs = false">
            <button class="p-2 rounded-xl text-surface-400 hover:text-yellow-400 hover:bg-surface-800/50 transition-all duration-200 relative">
              <span class="text-lg">🔔</span>
              <span v-if="favStore.favoriteTeamsCount > 0" class="absolute -top-0.5 -right-0.5 w-4 h-4 bg-yellow-500 rounded-full text-[9px] font-black flex items-center justify-center text-black animate-bounce-in">
                {{ favStore.favoriteTeamsCount }}
              </span>
            </button>
            <div v-show="showFavs" class="absolute right-0 top-full mt-2 w-72 glass-gold rounded-2xl p-4 shadow-2xl animate-slide-up" style="animation-duration: 0.2s">
              <p v-if="favStore.favoriteTeamsCount === 0" class="text-sm text-surface-400">No favorite teams yet. Go to Teams to add some!</p>
              <div v-else>
                <p class="text-xs text-yellow-400 uppercase tracking-wider mb-2 font-bold">⭐ Favorite Teams</p>
                <p class="text-sm text-white font-medium">{{ favStore.favoriteTeamsCount }} team{{ favStore.favoriteTeamsCount > 1 ? 's' : '' }} selected</p>
              </div>
            </div>
          </div>
        </nav>
      </div>
    </div>
  </header>
</template>
