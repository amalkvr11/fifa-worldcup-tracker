<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  code: { type: String, default: '' },
  flag: { type: String, default: '' },
  name: { type: String, default: '' },
  size: { type: String, default: 'md' },
})

const sizeMap = {
  xs: 'w-5 h-3',
  sm: 'w-6 h-4',
  md: 'w-8 h-5',
  lg: 'w-12 h-7',
  xl: 'w-16 h-9',
  '2xl': 'w-24 h-14',
}

const imgError = ref(false)
const validCode = computed(() => {
  const c = (props.code || '').trim().toUpperCase()
  return c && c !== 'TBD' && c !== '❓' && /^[A-Z]+$/.test(c)
})
</script>

<template>
  <span
    class="inline-flex items-center justify-center flex-shrink-0"
    :title="name || code"
    :class="sizeMap[size] || sizeMap.md"
  >
    <img
      v-if="validCode && !imgError"
      :src="`/flags/${code}.svg`"
      :alt="name || code"
      class="w-full h-full object-contain rounded-sm"
      loading="lazy"
      @error="imgError = true"
    />
    <span
      v-else
      class="inline-flex items-center justify-center w-full h-full bg-surface-800/50 rounded-sm border border-surface-700/20 leading-none"
      :style="{
        fontSize: size === 'xs' ? '8px' : size === 'sm' ? '10px' : size === 'md' ? '14px' : size === 'lg' ? '20px' : size === 'xl' ? '28px' : '36px'
      }"
    >
      {{ flag || code }}
    </span>
  </span>
</template>
