<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  playerName: { type: String, default: '' },
  teamCode: { type: String, default: '' },
  eventType: { type: String, default: 'goal' },
})

const emit = defineEmits(['closed'])

const particles = ref([])
let particlesCount = 0

watch(() => props.show, (newVal) => {
  if (newVal) {
    particles.value = []
    particlesCount = 0
    generateParticles()
  }
})

function generateParticles() {
  const colors = ['#facc15', '#22c55e', '#ef4444', '#f59e0b', '#fff', '#fde047']
  for (let i = 0; i < 60; i++) {
    const angle = Math.random() * Math.PI * 2
    const distance = 150 + Math.random() * 250
    const tx = Math.cos(angle) * distance
    const ty = Math.sin(angle) * distance
    const size = 6 + Math.random() * 8
    const rotation = Math.random() * 720
    particles.value.push({
      id: i,
      color: colors[Math.floor(Math.random() * colors.length)],
      tx,
      ty,
      size,
      rotation,
      delay: Math.random() * 0.3,
      shape: ['circle', 'rect', 'triangle'][Math.floor(Math.random() * 3)],
    })
  }
  particlesCount = particles.value.length
}
</script>

<template>
  <Teleport to="body">
    <Transition name="celebration">
      <div v-if="show" class="fixed inset-0 z-50 pointer-events-none">
        <div class="absolute inset-0 scoreboard-gradient"></div>
        <div class="absolute inset-0 flex items-center justify-center overflow-hidden">
          <div class="text-center animate-bounce-in relative z-10">
            <div class="text-8xl mb-8" style="animation: playerCelebrate 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)">⚽</div>
            <h2 class="text-5xl sm:text-7xl font-black mb-4" style="background: linear-gradient(135deg, #fde047, #facc15, #f59e0b, #facc15, #fde047); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: goldShimmer 1.5s ease infinite; text-shadow: 0 0 80px rgba(250,204,21,0.8);">
              GOAL!
            </h2>
            <p class="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-white via-yellow-100 to-white bg-clip-text text-transparent">
              {{ playerName }} scores!
            </p>
          </div>
          <div
            v-for="p in particles"
            :key="p.id"
            class="absolute"
            :style="{
              left: '50%',
              top: '50%',
              width: `${p.size}px`,
              height: p.shape === 'circle' ? `${p.size}px` : `${p.size * 1.5}px`,
              background: p.color,
              borderRadius: p.shape === 'circle' ? '50%' : p.shape === 'rect' ? '2px' : '0',
              transform: `translate(-50%, -50%) rotate(0deg)`,
              animation: `confettiBurst 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${p.delay}s forwards`,
              '--tx': `${p.tx}px`,
              '--ty': `${p.ty}px`,
              '--rot': `${p.rotation}deg`,
            }"
          ></div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.scoreboard-gradient {
  background: radial-gradient(ellipse at center, rgba(250,204,21,0.35) 0%, rgba(34,197,94,0.1) 30%, transparent 60%);
  animation: pulse-glow-bg 1s ease-in-out 2;
}

@keyframes pulse-glow-bg {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

@keyframes confettiBurst {
  0% {
    transform: translate(-50%, -50%) scale(1) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) rotate(var(--rot)) scale(0);
    opacity: 0;
  }
}

.celebration-enter-active { transition: opacity 0.3s ease-out; }
.celebration-leave-active { transition: opacity 0.5s ease-in 0.8s; }
.celebration-enter-from,
.celebration-leave-to { opacity: 0; }
</style>
