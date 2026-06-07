<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({ dates: { type: Array, default: () => [] }, selected: { type: String, default: null } })
const emit = defineEmits(['select', 'today'])
const scrollRef = ref(null)

const dateLabels = computed(() => props.dates.map(d => {
  const dt = new Date(d + 'T00:00:00Z')
  const today = new Date(); today.setHours(0,0,0,0)
  const diff = Math.round((dt - today) / 86400000)
  let label
  if (diff === 0) label = '📅 Today'
  else if (diff === 1) label = 'Tomorrow'
  else label = dt.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' })
  return { date: d, label }
}))
</script>

<template>
  <div class="flex items-center gap-3">
    <button @click="emit('today')" class="flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 border" :class="selected === 'today' ? 'bg-yellow-500/15 border-yellow-500/30 text-yellow-400 shadow-lg shadow-yellow-500/10' : 'bg-surface-800/30 border-surface-700/30 text-surface-400 hover:text-white hover:border-surface-600 hover:bg-surface-800/50'">
      🏟️ Today
    </button>
    <div ref="scrollRef" class="flex gap-2 overflow-x-auto pb-2 flex-1" style="scrollbar-width:none">
      <button v-for="(dl, idx) in dateLabels" :key="dl.date" @click="emit('select', dl.date)" class="flex-shrink-0 px-3 py-2.5 rounded-xl text-xs font-bold transition-all duration-300 whitespace-nowrap border" :class="selected === dl.date ? 'bg-yellow-500/15 border-yellow-500/30 text-yellow-400 shadow-lg shadow-yellow-500/10' : 'bg-surface-800/30 border-surface-700/30 text-surface-400 hover:text-white hover:border-surface-600'" :style="{ animationDelay: idx * 0.02 + 's' }">
        {{ dl.label }}
      </button>
    </div>
  </div>
</template>
