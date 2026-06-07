<script setup>
import { ref, nextTick } from 'vue'

const open = ref(false)
const messages = ref([{ role: 'bot', text: '🏆 Welcome to the FIFA 2026 AI Assistant! Ask me about teams, matches, rules, predictions, history, or anything World Cup!' }])
const input = ref('')
const loading = ref(false)
const chatBody = ref(null)

function scrollToBottom() { nextTick(() => { if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight }) }

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return
  input.value = ''
  messages.value.push({ role: 'user', text })
  loading.value = true
  scrollToBottom()
  try {
    const res = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }) })
    const data = await res.json()
    messages.value.push({ role: 'bot', text: data.reply })
  } catch { messages.value.push({ role: 'bot', text: '⚠️ Connection error. Please try again.' }) }
  finally { loading.value = false; scrollToBottom() }
}

function handleKey(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }
</script>

<template>
  <div class="fixed bottom-6 right-6 z-[999]">
    <button @click="open = !open" class="w-14 h-14 rounded-full bg-gradient-to-br from-yellow-500 to-yellow-600 text-black shadow-2xl shadow-yellow-500/30 hover:shadow-yellow-500/50 hover:scale-110 transition-all duration-300 flex items-center justify-center text-2xl font-black" :class="open ? 'rotate-90' : ''" style="transition: transform 0.3s ease, box-shadow 0.3s ease">
      {{ open ? '✕' : '💬' }}
    </button>

    <Transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 scale-90 translate-y-4" enter-to-class="opacity-100 scale-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-90 translate-y-4">
      <div v-if="open" class="absolute bottom-16 right-0 w-[350px] sm:w-[400px] h-[500px] glass-gold rounded-2xl shadow-2xl shadow-yellow-500/5 flex flex-col overflow-hidden">
        <div class="flex items-center gap-3 p-4 border-b border-yellow-500/10 bg-gradient-to-r from-yellow-500/10 via-transparent to-green-500/5">
          <span class="text-2xl animate-float" style="animation-duration: 2s">🤖</span>
          <div class="flex-1">
            <p class="font-bold text-sm text-white">FIFA 2026 AI</p>
            <p class="text-[10px] text-yellow-400 font-medium">● Online • Ask me anything!</p>
          </div>
          <div class="flex gap-1">
            <span class="w-2 h-2 rounded-full bg-green-400"></span>
            <span class="w-2 h-2 rounded-full bg-yellow-400"></span>
            <span class="w-2 h-2 rounded-full bg-red-400"></span>
          </div>
        </div>

        <div ref="chatBody" class="flex-1 overflow-y-auto p-4 space-y-3">
          <div v-for="(msg, i) in messages" :key="i" :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
            <div :class="['max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed', msg.role === 'user' ? 'bg-yellow-500/15 text-yellow-100 border border-yellow-500/20 rounded-br-md' : 'bg-surface-800/60 text-surface-200 border border-surface-700/20 rounded-bl-md']">
              {{ msg.text }}
            </div>
          </div>
          <div v-if="loading" class="flex justify-start">
            <div class="bg-surface-800/60 rounded-2xl rounded-bl-md px-4 py-3 border border-surface-700/20">
              <div class="flex gap-1.5 items-center">
                <span class="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style="animation-delay:0ms"></span>
                <span class="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style="animation-delay:150ms"></span>
                <span class="w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style="animation-delay:300ms"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="p-3 border-t border-yellow-500/10 bg-surface-900/30">
          <div class="flex gap-2">
            <textarea v-model="input" @keydown="handleKey" placeholder="Ask about FIFA 2026..." rows="1" class="flex-1 bg-surface-800/50 border border-surface-700/30 rounded-xl px-3 py-2.5 text-sm text-white placeholder-surface-500 resize-none focus:outline-none focus:border-yellow-500/40 focus:ring-1 focus:ring-yellow-500/20 transition-all"></textarea>
            <button @click="send" :disabled="loading || !input.trim()" class="px-4 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl text-black font-bold transition-all text-sm shadow-lg shadow-yellow-500/20">
              ⚡
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
