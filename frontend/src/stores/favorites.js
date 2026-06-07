import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

function loadFromStorage(key, fallback) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : fallback
  } catch { return fallback }
}

function saveToStorage(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)) } catch {}
}

export const useFavoritesStore = defineStore('favorites', () => {
  const favoriteTeams = ref(loadFromStorage('fifa-fav-teams', []))
  const favoriteMatches = ref(loadFromStorage('fifa-fav-matches', []))

  function persist() {
    saveToStorage('fifa-fav-teams', favoriteTeams.value)
    saveToStorage('fifa-fav-matches', favoriteMatches.value)
  }

  const isTeamFavorite = computed(() => (code) => favoriteTeams.value.includes(code))
  const isMatchFavorite = computed(() => (id) => favoriteMatches.value.includes(id))
  const favoriteTeamsCount = computed(() => favoriteTeams.value.length)

  function toggleTeam(code) {
    const idx = favoriteTeams.value.indexOf(code)
    if (idx === -1) favoriteTeams.value = [...favoriteTeams.value, code]
    else favoriteTeams.value = favoriteTeams.value.filter(c => c !== code)
    persist()
  }

  function toggleMatch(id) {
    const idx = favoriteMatches.value.indexOf(id)
    if (idx === -1) favoriteMatches.value = [...favoriteMatches.value, id]
    else favoriteMatches.value = favoriteMatches.value.filter(m => m !== id)
    persist()
  }

  function requestNotification() {
    if ('Notification' in window && Notification.permission === 'default')
      Notification.requestPermission()
  }

  function notifyMatch(match) {
    if (!('Notification' in window) || Notification.permission !== 'granted') return
    const d = new Date(match.date_utc)
    const time = d.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit' })
    new Notification('⚽ Match Starting Soon!', {
      body: `${match.team1_flag} ${match.team1} vs ${match.team2_flag} ${match.team2} at ${time} IST`,
    })
  }

  return {
    favoriteTeams, favoriteMatches, isTeamFavorite, isMatchFavorite,
    favoriteTeamsCount, toggleTeam, toggleMatch, requestNotification, notifyMatch,
  }
})
