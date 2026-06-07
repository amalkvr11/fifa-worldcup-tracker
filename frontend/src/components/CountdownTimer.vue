<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({ dateUtc: { type: String, required: true }, small: { type: Boolean, default: false } })

const now = ref(Date.now())
let interval = null

const target = computed(() => new Date(props.dateUtc).getTime())
const diff = computed(() => target.value - now.value)
const isLive = computed(() => diff.value <= 0 && diff.value > -7200000)
const isFinished = computed(() => diff.value <= -7200000)
const isUpcoming = computed(() => diff.value > 0)

const timeLeft = computed(() => {
  if (diff.value <= 0) return { d: 0, h: 0, m: 0, s: 0 }
  const t = Math.floor(diff.value / 1000)
  return { d: Math.floor(t / 86400), h: Math.floor((t % 86400) / 3600), m: Math.floor((t % 3600) / 60), s: t % 60 }
})

onMounted(() => { interval = setInterval(() => { now.value = Date.now() }, 1000) })
onUnmounted(() => { if (interval) clearInterval(interval) })
</script>

<template>
  <div v-if="isUpcoming" :class="['font-mono', small ? 'text-xs text-surface-400' : 'text-sm']">
    <div v-if="small" class="flex items-center gap-1.5">
      <span class="text-yellow-500/60">⏳</span>
      <span v-if="timeLeft.d > 0" class="text-surface-300">{{ timeLeft.d }}d</span>
      <span class="tabular-nums text-surface-400">{{ String(timeLeft.h).padStart(2,'0') }}:{{ String(timeLeft.m).padStart(2,'0') }}:{{ String(timeLeft.s).padStart(2,'0') }}</span>
    </div>
    <div v-else class="flex items-center gap-2 sm:gap-3">
      <div v-if="timeLeft.d > 0" class="text-center">
        <div class="text-2xl sm:text-3xl font-black text-white tabular-nums">{{ timeLeft.d }}</div>
        <div class="text-[9px] text-surface-500 uppercase tracking-widest font-bold">Days</div>
      </div>
      <div class="text-center">
        <div class="text-2xl sm:text-3xl font-black text-white tabular-nums">{{ String(timeLeft.h).padStart(2,'0') }}</div>
        <div class="text-[9px] text-surface-500 uppercase tracking-widest font-bold">Hours</div>
      </div>
      <span class="text-xl text-yellow-500/40 mt-[-8px] animate-pulse">:</span>
      <div class="text-center">
        <div class="text-2xl sm:text-3xl font-black text-white tabular-nums">{{ String(timeLeft.m).padStart(2,'0') }}</div>
        <div class="text-[9px] text-surface-500 uppercase tracking-widest font-bold">Mins</div>
      </div>
      <span class="text-xl text-yellow-500/40 mt-[-8px] animate-pulse">:</span>
      <div class="text-center">
        <div class="text-2xl sm:text-3xl font-black text-yellow-400 tabular-nums">{{ String(timeLeft.s).padStart(2,'0') }}</div>
        <div class="text-[9px] text-surface-500 uppercase tracking-widest font-bold">Secs</div>
      </div>
    </div>
  </div>
  <div v-else-if="isLive" class="flex items-center gap-2">
    <span class="live-dot"></span>
    <span class="text-red-400 font-black text-sm uppercase tracking-wider">LIVE</span>
  </div>
  <div v-else class="text-surface-500 text-sm font-medium">✅ Finished</div>
</template>
