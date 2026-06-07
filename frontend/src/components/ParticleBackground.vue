<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const particles = ref([])
const symbols = ['⚽', '🏆', '⭐', '🌟', '✨', '🎯']
let interval = null

function createParticle() {
  const id = Date.now() + Math.random()
  const particle = {
    id,
    symbol: symbols[Math.floor(Math.random() * symbols.length)],
    left: Math.random() * 100,
    size: 12 + Math.random() * 18,
    duration: 12 + Math.random() * 18,
    delay: Math.random() * 5,
    opacity: 0.08 + Math.random() * 0.12,
  }
  particles.value.push(particle)
  setTimeout(() => {
    particles.value = particles.value.filter(p => p.id !== id)
  }, (particle.duration + particle.delay) * 1000)
}

onMounted(() => {
  for (let i = 0; i < 8; i++) createParticle()
  interval = setInterval(createParticle, 3000)
})

onUnmounted(() => { if (interval) clearInterval(interval) })
</script>

<template>
  <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
    <div
      v-for="p in particles"
      :key="p.id"
      class="particle"
      :style="{
        left: p.left + '%',
        fontSize: p.size + 'px',
        animationDuration: p.duration + 's',
        animationDelay: p.delay + 's',
        opacity: p.opacity,
      }"
    >
      {{ p.symbol }}
    </div>
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-b from-yellow-500/5 to-transparent blur-3xl"></div>
    <div class="absolute bottom-0 right-0 w-[400px] h-[400px] rounded-full bg-gradient-to-t from-green-500/5 to-transparent blur-3xl"></div>
  </div>
</template>
