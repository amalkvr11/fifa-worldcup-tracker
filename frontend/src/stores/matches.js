import { defineStore } from 'pinia'
import { ref, computed, onUnmounted } from 'vue'

const API_BASE = '/api'
let ws = null
let wsReconnectTimer = null

export const useMatchesStore = defineStore('matches', () => {
  const matches = ref([])
  const dates = ref([])
  const loading = ref(false)
  const error = ref(null)
  const selectedDate = ref(null)
  const liveMatches = ref([])
  const liveEvents = ref({})
  const wsConnected = ref(false)

  function connectWebSocket() {
    if (ws && ws.readyState === WebSocket.OPEN) return
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:'
    try {
      ws = new WebSocket(`${proto}//${location.host}/ws`)
      ws.onopen = () => { wsConnected.value = true }
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'score_update') {
            const m = matches.value.find(x => x.id === data.match_id)
            if (m) {
              m.score_team1 = data.score_team1
              m.score_team2 = data.score_team2
              m.status = data.status
            }
            if (data.events && data.events.length > 0) {
              liveEvents.value[data.match_id] = data.events
            }
            const lm = liveMatches.value.find(x => x.match_id === data.match_id)
            if (lm) {
              lm.score_team1 = data.score_team1
              lm.score_team2 = data.score_team2
              lm.status = data.status
            } else if (data.status === 'live') {
              liveMatches.value.push({
                match_id: data.match_id,
                team1: data.team1,
                team2: data.team2,
                score_team1: data.score_team1,
                score_team2: data.score_team2,
                status: data.status,
              })
            }
          }
        } catch {}
      }
      ws.onclose = () => {
        wsConnected.value = false
        wsReconnectTimer = setTimeout(connectWebSocket, 5000)
      }
      ws.onerror = () => { ws.close() }
    } catch {}
  }

  function disconnectWebSocket() {
    if (wsReconnectTimer) { clearTimeout(wsReconnectTimer); wsReconnectTimer = null }
    if (ws) { ws.close(); ws = null }
    wsConnected.value = false
  }

  async function fetchMatches(params = {}) {
    loading.value = true; error.value = null
    try {
      const q = new URLSearchParams(params).toString()
      const res = await fetch(`${API_BASE}/matches${q ? '?' + q : ''}`)
      if (!res.ok) throw new Error('Failed to fetch matches')
      const data = await res.json()
      matches.value = data.matches
    } catch (e) { error.value = e.message }
    finally { loading.value = false }
  }

  async function fetchDates() {
    try {
      const res = await fetch(`${API_BASE}/dates`)
      const data = await res.json()
      dates.value = data.dates
    } catch {}
  }

  async function fetchMatch(id) {
    try {
      const res = await fetch(`${API_BASE}/matches/${id}`)
      if (!res.ok) throw new Error('Match not found')
      return await res.json()
    } catch (e) { error.value = e.message; return null }
  }

  async function fetchToday() {
    loading.value = true
    try {
      const res = await fetch(`${API_BASE}/today`)
      const data = await res.json()
      matches.value = data.matches
      selectedDate.value = 'today'
    } catch (e) { error.value = e.message }
    finally { loading.value = false }
  }

  async function fetchLiveActive() {
    try {
      const res = await fetch(`${API_BASE}/live/active`)
      const data = await res.json()
      liveMatches.value = data.active || []
    } catch {}
  }

  async function startSimulation(matchId) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'start_simulation', match_id: matchId }))
    } else {
      await fetch(`${API_BASE}/live/start/${matchId}`, { method: 'POST' })
    }
    connectWebSocket()
  }

  const matchesByDate = computed(() => {
    const grouped = {}
    for (const m of matches.value) {
      const date = m.date_utc.slice(0, 10)
      if (!grouped[date]) grouped[date] = []
      grouped[date].push(m)
    }
    return Object.entries(grouped).sort(([a], [b]) => a.localeCompare(b))
  })

  return {
    matches, dates, loading, error, selectedDate,
    liveMatches, liveEvents, wsConnected,
    matchesByDate,
    fetchMatches, fetchDates, fetchMatch, fetchToday,
    fetchLiveActive, startSimulation,
    connectWebSocket, disconnectWebSocket,
  }
})
