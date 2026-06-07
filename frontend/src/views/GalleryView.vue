<script setup>
import WorldCupGallery from '../components/WorldCupGallery.vue'
</script>

<template>
  <div class="space-y-6">
    <div class="glass-gold rounded-3xl p-6 sm:p-8 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-500 via-green-500 to-yellow-500"></div>
      <div class="flex items-center gap-4">
        <div class="relative">
          <div class="text-5xl sm:text-6xl animate-float" style="animation-duration: 3s">📸</div>
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-gradient-gold">FIFA World Cup Gallery</h1>
          <p class="text-surface-400 text-sm mt-1">Relive the magic from every tournament through history</p>
        </div>
      </div>
    </div>

    <WorldCupGallery />

    <div class="glass rounded-2xl p-6 sm:p-8 text-center">
      <div class="max-w-2xl mx-auto">
        <h3 class="text-lg font-black text-white mb-3">🏆 The Greatest Show on Earth</h3>
        <p class="text-surface-400 text-sm leading-relaxed mb-6">
          From the inaugural tournament in 1930 to the expanded 48-team format in 2026,
          the FIFA World Cup has brought nations together in celebration of the beautiful game.
          Each tournament has its own story, its own heroes, and its own unforgettable moments.
        </p>
        <div class="grid grid-cols-3 gap-4">
          <div class="p-3 rounded-xl bg-surface-800/40 border border-surface-700/20">
            <div class="text-2xl font-black text-gradient-gold">22</div>
            <div class="text-[10px] text-surface-500 uppercase tracking-wider font-bold">Tournaments</div>
          </div>
          <div class="p-3 rounded-xl bg-surface-800/40 border border-surface-700/20">
            <div class="text-2xl font-black text-white">79</div>
            <div class="text-[10px] text-surface-500 uppercase tracking-wider font-bold">Years</div>
          </div>
          <div class="p-3 rounded-xl bg-surface-800/40 border border-surface-700/20">
            <div class="text-2xl font-black text-green-400">8</div>
            <div class="text-[10px] text-surface-500 uppercase tracking-wider font-bold">Nations Won</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
