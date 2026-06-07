<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import TeamFlag from '../components/TeamFlag.vue'

const route = useRoute()

const allPlayers = {
  ARG: [
    { name: 'Lionel Messi', number: 10, position: 'Forward', rating: 93, photo: '⚽' },
    { name: 'Emiliano Martínez', number: 23, position: 'Goalkeeper', rating: 89, photo: '🧤' },
    { name: 'Julián Alvarez', number: 9, position: 'Forward', rating: 88, photo: '⚽' },
    { name: 'Enzo Fernández', number: 24, position: 'Midfielder', rating: 87, photo: '👟' },
    { name: 'Alexis Mac Allister', number: 20, position: 'Midfielder', rating: 86, photo: '👟' },
    { name: 'Nicolás Otamendi', number: 19, position: 'Defender', rating: 84, photo: '🛡️' },
  ],
  BRA: [
    { name: 'Vinícius Jr', number: 7, position: 'Forward', rating: 91, photo: '⚡' },
    { name: 'Rodrygo', number: 9, position: 'Forward', rating: 87, photo: '⚡' },
    { name: 'Alisson', number: 1, position: 'Goalkeeper', rating: 89, photo: '🧤' },
    { name: 'Casemiro', number: 5, position: 'Midfielder', rating: 86, photo: '👟' },
    { name: 'Marquinhos', number: 4, position: 'Defender', rating: 87, photo: '🛡️' },
    { name: 'Danilo', number: 2, position: 'Defender', rating: 83, photo: '🛡️' },
  ],
  FRA: [
    { name: 'Kylian Mbappé', number: 10, position: 'Forward', rating: 92, photo: '⚡' },
    { name: 'Antoine Griezmann', number: 7, position: 'Midfielder', rating: 87, photo: '👟' },
    { name: 'Hugo Lloris', number: 1, position: 'Goalkeeper', rating: 87, photo: '🧤' },
    { name: 'Randal Kolo Muani', number: 12, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Jules Koundé', number: 5, position: 'Defender', rating: 85, photo: '🛡️' },
    { name: 'Aurélien Tchouaméni', number: 8, position: 'Midfielder', rating: 86, photo: '👟' },
  ],
  ESP: [
    { name: 'Pedri', number: 16, position: 'Midfielder', rating: 88, photo: '👟' },
    { name: 'Gavi', number: 6, position: 'Midfielder', rating: 85, photo: '👟' },
    { name: 'Unai Simón', number: 1, position: 'Goalkeeper', rating: 87, photo: '🧤' },
    { name: 'Dani Olmo', number: 10, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Aymeric Laporte', number: 3, position: 'Defender', rating: 85, photo: '🛡️' },
    { name: 'Ferra Garcia', number: 11, position: 'Forward', rating: 83, photo: '⚡' },
  ],
  ENG: [
    { name: 'Harry Kane', number: 9, position: 'Forward', rating: 89, photo: '⚡' },
    { name: 'Jude Bellingham', number: 22, position: 'Midfielder', rating: 88, photo: '👟' },
    { name: 'Jordan Pickford', number: 1, position: 'Goalkeeper', rating: 84, photo: '🧤' },
    { name: 'Bukayo Saka', number: 17, position: 'Forward', rating: 86, photo: '⚡' },
    { name: 'John Stones', number: 5, position: 'Defender', rating: 84, photo: '🛡️' },
    { name: 'Declan Rice', number: 4, position: 'Midfielder', rating: 85, photo: '👟' },
  ],
  GER: [
    { name: 'Joshua Kimmich', number: 6, position: 'Midfielder', rating: 87, photo: '👟' },
    { name: 'Manuel Neuer', number: 1, position: 'Goalkeeper', rating: 86, photo: '🧤' },
    { name: 'Kai Havertz', number: 10, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Antonio Rüdiger', number: 2, position: 'Defender', rating: 84, photo: '🛡️' },
    { name: 'İlkay Gündoğan', number: 8, position: 'Midfielder', rating: 84, photo: '👟' },
    { name: 'Timo Werner', number: 9, position: 'Forward', rating: 82, photo: '⚡' },
  ],
  NED: [
    { name: 'Virgil van Dijk', number: 4, position: 'Defender', rating: 89, photo: '🛡️' },
    { name: 'Memphis Depay', number: 10, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Bart Verbruggen', number: 1, position: 'Goalkeeper', rating: 81, photo: '🧤' },
    { name: 'Frenkie de Jong', number: 21, position: 'Midfielder', rating: 86, photo: '👟' },
    { name: 'Denzel Dumfries', number: 22, position: 'Defender', rating: 82, photo: '🛡️' },
  ],
  POR: [
    { name: 'Cristiano Ronaldo', number: 7, position: 'Forward', rating: 87, photo: '⚡' },
    { name: 'Bruno Fernandes', number: 23, position: 'Midfielder', rating: 87, photo: '👟' },
    { name: 'Diogo Costa', number: 22, position: 'Goalkeeper', rating: 84, photo: '🧤' },
    { name: 'Rúben Dias', number: 4, position: 'Defender', rating: 86, photo: '🛡️' },
    { name: 'Bernardo Silva', number: 10, position: 'Midfielder', rating: 86, photo: '👟' },
  ],
  BEL: [
    { name: 'Romelu Lukaku', number: 9, position: 'Forward', rating: 83, photo: '⚡' },
    { name: 'Kevin De Bruyne', number: 7, position: 'Midfielder', rating: 90, photo: '👟' },
    { name: 'Thibaut Courtois', number: 1, position: 'Goalkeeper', rating: 89, photo: '🧤' },
    { name: 'Jan Vertonghen', number: 5, position: 'Defender', rating: 81, photo: '🛡️' },
  ],
  ITA: [
    { name: 'Gianluigi Donnarumma', number: 1, position: 'Goalkeeper', rating: 87, photo: '🧤' },
    { name: 'Federico Chiesa', number: 14, position: 'Forward', rating: 85, photo: '⚡' },
    { name: 'Nicolò Barella', number: 18, position: 'Midfielder', rating: 85, photo: '👟' },
    { name: 'Leonardo Bonucci', number: 3, position: 'Defender', rating: 82, photo: '🛡️' },
  ],
  CRO: [
    { name: 'Luka Modrić', number: 10, position: 'Midfielder', rating: 86, photo: '👟' },
    { name: 'Dominik Livaković', number: 1, position: 'Goalkeeper', rating: 83, photo: '🧤' },
    { name: 'Andrej Kramarić', number: 9, position: 'Forward', rating: 82, photo: '⚡' },
  ],
  URU: [
    { name: 'Luis Suárez', number: 9, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Darwin Núñez', number: 19, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Fernando Muslera', number: 1, position: 'Goalkeeper', rating: 82, photo: '🧤' },
  ],
  SUI: [
    { name: 'Yann Sommer', number: 1, position: 'Goalkeeper', rating: 84, photo: '🧤' },
    { name: 'Granit Xhaka', number: 10, position: 'Midfielder', rating: 82, photo: '👟' },
    { name: 'Haris Seferović', number: 9, position: 'Forward', rating: 78, photo: '⚡' },
  ],
  DEN: [
    { name: 'Christian Eriksen', number: 10, position: 'Midfielder', rating: 83, photo: '👟' },
    { name: 'Kasper Schmeichel', number: 1, position: 'Goalkeeper', rating: 83, photo: '🧤' },
    { name: 'Yussuf Poulsen', number: 9, position: 'Forward', rating: 80, photo: '⚡' },
  ],
  SRB: [
    { name: 'Aleksandar Mitrović', number: 9, position: 'Forward', rating: 82, photo: '⚡' },
    { name: 'Sergej Milinković-Savić', number: 20, position: 'Midfielder', rating: 83, photo: '👟' },
    { name: 'Vanja Milinković-Savić', number: 1, position: 'Goalkeeper', rating: 80, photo: '🧤' },
  ],
  JPN: [
    { name: 'Takumi Minamino', number: 8, position: 'Forward', rating: 81, photo: '⚡' },
    { name: 'Wataru Endō', number: 6, position: 'Midfielder', rating: 81, photo: '👟' },
    { name: 'Eiji Kawashima', number: 1, position: 'Goalkeeper', rating: 78, photo: '🧤' },
  ],
  KOR: [
    { name: 'Son Heung-min', number: 7, position: 'Forward', rating: 87, photo: '⚡' },
    { name: 'Kim Min-jae', number: 4, position: 'Defender', rating: 84, photo: '🛡️' },
    { name: 'Jo Hyeon-woo', number: 1, position: 'Goalkeeper', rating: 79, photo: '🧤' },
  ],
  AUS: [
    { name: 'Mathew Ryan', number: 1, position: 'Goalkeeper', rating: 80, photo: '🧤' },
    { name: 'Aaron Mooy', number: 13, position: 'Midfielder', rating: 79, photo: '👟' },
    { name: 'Awer Mabil', number: 11, position: 'Forward', rating: 76, photo: '⚡' },
  ],
  KSA: [
    { name: 'Salman Al-Faraj', number: 7, position: 'Midfielder', rating: 78, photo: '👟' },
    { name: 'Mohammed Al-Owais', number: 1, position: 'Goalkeeper', rating: 78, photo: '🧤' },
    { name: 'Fahad Al-Muwallad', number: 9, position: 'Forward', rating: 76, photo: '⚡' },
  ],
  IRN: [
    { name: 'Sardar Azmoun', number: 9, position: 'Forward', rating: 79, photo: '⚡' },
    { name: 'Mehdi Taremi', number: 10, position: 'Forward', rating: 79, photo: '⚡' },
    { name: 'Alireza Beiranvand', number: 1, position: 'Goalkeeper', rating: 79, photo: '🧤' },
  ],
  IRQ: [
    { name: 'Yaser Kasim', number: 8, position: 'Midfielder', rating: 73, photo: '👟' },
    { name: 'Mohammed Hameed', number: 1, position: 'Goalkeeper', rating: 73, photo: '🧤' },
  ],
  MAR: [
    { name: 'Achraf Hakimi', number: 2, position: 'Defender', rating: 85, photo: '🛡️' },
    { name: 'Hakim Ziyech', number: 7, position: 'Midfielder', rating: 83, photo: '👟' },
    { name: 'Yassine Bounou', number: 1, position: 'Goalkeeper', rating: 84, photo: '🧤' },
  ],
  EGY: [
    { name: 'Mohamed Salah', number: 11, position: 'Forward', rating: 88, photo: '⚡' },
    { name: 'Mohamed Elneny', number: 17, position: 'Midfielder', rating: 76, photo: '👟' },
    { name: 'Mohamed Ab Gaber', number: 1, position: 'Goalkeeper', rating: 75, photo: '🧤' },
  ],
  TUN: [
    { name: 'Youssef Msakni', number: 7, position: 'Forward', rating: 76, photo: '⚡' },
    { name: 'Aymen Dahmen', number: 1, position: 'Goalkeeper', rating: 76, photo: '🧤' },
  ],
  SEN: [
    { name: 'Sadio Mané', number: 10, position: 'Forward', rating: 85, photo: '⚡' },
    { name: 'Édouard Mendy', number: 16, position: 'Goalkeeper', rating: 84, photo: '🧤' },
    { name: 'Idrissa Gueye', number: 5, position: 'Midfielder', rating: 79, photo: '👟' },
  ],
  NGA: [
    { name: 'Victor Osimhen', number: 9, position: 'Forward', rating: 84, photo: '⚡' },
    { name: 'Wilfred Ndidi', number: 4, position: 'Midfielder', rating: 80, photo: '👟' },
    { name: 'Francis Uzoho', number: 1, position: 'Goalkeeper', rating: 75, photo: '🧤' },
  ],
  GHA: [
    { name: 'Thomas Partey', number: 5, position: 'Midfielder', rating: 83, photo: '👟' },
    { name: 'André Ayew', number: 10, position: 'Forward', rating: 79, photo: '⚡' },
    { name: 'Richard Ofori', number: 1, position: 'Goalkeeper', rating: 74, photo: '🧤' },
  ],
  CMR: [
    { name: 'Eric Maxim Choupo-Moting', number: 13, position: 'Forward', rating: 79, photo: '⚡' },
    { name: 'André-Frank Zambo Anguissa', number: 8, position: 'Midfielder', rating: 82, photo: '👟' },
    { name: 'Devis Epassy', number: 1, position: 'Goalkeeper', rating: 75, photo: '🧤' },
  ],
  CIV: [
    { name: 'Wilfried Zaha', number: 11, position: 'Forward', rating: 82, photo: '⚡' },
    { name: 'Franck Kessié', number: 8, position: 'Midfielder', rating: 83, photo: '👟' },
    { name: 'Boubacar Barry', number: 1, position: 'Goalkeeper', rating: 76, photo: '🧤' },
  ],
  ALG: [
    { name: 'Riyad Mahrez', number: 7, position: 'Forward', rating: 83, photo: '⚡' },
    { name: 'Ismaël Bennacer', number: 22, position: 'Midfielder', rating: 80, photo: '👟' },
    { name: 'Raïs M\'Bolhi', number: 23, position: 'Goalkeeper', rating: 78, photo: '🧤' },
  ],
  NZL: [
    { name: 'Chris Wood', number: 9, position: 'Forward', rating: 75, photo: '⚡' },
    { name: 'Marcel Klonz', number: 1, position: 'Goalkeeper', rating: 74, photo: '🧤' },
  ],
  MLI: [
    { name: 'Yves Bissouma', number: 10, position: 'Midfielder', rating: 77, photo: '👟' },
    { name: 'Moussa Djenepo', number: 7, position: 'Forward', rating: 74, photo: '⚡' },
    { name: 'Djigui Diarra', number: 1, position: 'Goalkeeper', rating: 74, photo: '🧤' },
  ],
  BFA: [
    { name: 'Bertrand Traoré', number: 10, position: 'Forward', rating: 76, photo: '⚡' },
    { name: 'Blati Touré', number: 8, position: 'Midfielder', rating: 73, photo: '👟' },
  ],
  RSA: [
    { name: 'Percy Tau', number: 10, position: 'Forward', rating: 75, photo: '⚡' },
    { name: 'Themba Zwane', number: 11, position: 'Forward', rating: 74, photo: '⚡' },
    { name: 'Ronwen Williams', number: 1, position: 'Goalkeeper', rating: 77, photo: '🧤' },
  ],
  TAH: [
    { name: 'Teaonui Tehau', number: 10, position: 'Forward', rating: 70, photo: '⚡' },
    { name: 'Michele Hmae', number: 1, position: 'Goalkeeper', rating: 69, photo: '🧤' },
  ],
  UZB: [
    { name: 'Jaloliddin Masharipov', number: 7, position: 'Forward', rating: 74, photo: '⚡' },
    { name: 'Odiljon Hamrobekov', number: 9, position: 'Midfielder', rating: 73, photo: '👟' },
  ],
  IND: [
    { name: 'Sunil Chhetri', number: 11, position: 'Forward', rating: 72, photo: '⚡' },
    { name: 'Gurpreet Singh Sandhu', number: 1, position: 'Goalkeeper', rating: 72, photo: '🧤' },
  ],
  CHN: [
    { name: 'Wu Lei', number: 7, position: 'Forward', rating: 71, photo: '⚡' },
    { name: 'Zhang Linpeng', number: 5, position: 'Defender', rating: 70, photo: '🛡️' },
  ],
  FIJ: [
    { name: 'Roy Krishna', number: 8, position: 'Forward', rating: 71, photo: '⚡' },
    { name: 'Simione Tamanisau', number: 1, position: 'Goalkeeper', rating: 68, photo: '🧤' },
  ],
}

const teamMeta = {
  ARG: { name: 'Argentina', flag: '🇦🇷', rank: 1 },
  BRA: { name: 'Brazil', flag: '🇧🇷', rank: 2 },
  FRA: { name: 'France', flag: '🇫🇷', rank: 3 },
  ESP: { name: 'Spain', flag: '🇪🇸', rank: 4 },
  ENG: { name: 'England', flag: '🏴󠁧󠁢󠁥󠁮󠁧󠁿', rank: 5 },
  GER: { name: 'Germany', flag: '🇩🇪', rank: 6 },
  NED: { name: 'Netherlands', flag: '🇳🇱', rank: 7 },
  POR: { name: 'Portugal', flag: '🇵🇹', rank: 8 },
  BEL: { name: 'Belgium', flag: '🇧🇪', rank: 9 },
  ITA: { name: 'Italy', flag: '🇮🇹', rank: 10 },
  CRO: { name: 'Croatia', flag: '🇭🇷', rank: 11 },
  URU: { name: 'Uruguay', flag: '🇺🇾', rank: 12 },
  SUI: { name: 'Switzerland', flag: '🇨🇭', rank: 13 },
  DEN: { name: 'Denmark', flag: '🇩🇰', rank: 14 },
  SRB: { name: 'Serbia', flag: '🇷🇸', rank: 15 },
  JPN: { name: 'Japan', flag: '🇯🇵', rank: 16 },
  KOR: { name: 'South Korea', flag: '🇰🇷', rank: 17 },
  AUS: { name: 'Australia', flag: '🇦🇺', rank: 18 },
  KSA: { name: 'Saudi Arabia', flag: '🇸🇦', rank: 19 },
  IRN: { name: 'Iran', flag: '🇮🇷', rank: 20 },
  IRQ: { name: 'Iraq', flag: '🇮🇶', rank: 21 },
  MAR: { name: 'Morocco', flag: '🇲🇦', rank: 22 },
  EGY: { name: 'Egypt', flag: '🇪🇬', rank: 23 },
  TUN: { name: 'Tunisia', flag: '🇹🇳', rank: 24 },
  SEN: { name: 'Senegal', flag: '🇸🇳', rank: 25 },
  NGA: { name: 'Nigeria', flag: '🇳🇬', rank: 26 },
  GHA: { name: 'Ghana', flag: '🇬🇭', rank: 27 },
  CMR: { name: 'Cameroon', flag: '🇨🇲', rank: 28 },
  CIV: { name: 'Ivory Coast', flag: '🇨🇮', rank: 29 },
  ALG: { name: 'Algeria', flag: '🇩🇿', rank: 30 },
  NZL: { name: 'New Zealand', flag: '🇳🇿', rank: 31 },
  MLI: { name: 'Mali', flag: '🇲🇱', rank: 32 },
  BFA: { name: 'Burkina Faso', flag: '🇧🇫', rank: 33 },
  RSA: { name: 'South Africa', flag: '🇿🇦', rank: 34 },
  TAH: { name: 'Tahiti', flag: '🇵🇫', rank: 35 },
  UZB: { name: 'Uzbekistan', flag: '🇺🇿', rank: 36 },
  IND: { name: 'India', flag: '🇮🇳', rank: 37 },
  CHN: { name: 'China', flag: '🇨🇳', rank: 38 },
  FIJ: { name: 'Fiji', flag: '🇫🇯', rank: 39 },
  MEX: { name: 'Mexico', flag: '🇲🇽', rank: 40 },
  CAN: { name: 'Canada', flag: '🇨🇦', rank: 41 },
  JAM: { name: 'Jamaica', flag: '🇯🇲', rank: 42 },
  USA: { name: 'United States', flag: '🇺🇸', rank: 43 },
  CRC: { name: 'Costa Rica', flag: '🇨🇷', rank: 44 },
  PAN: { name: 'Panama', flag: '🇵🇦', rank: 45 },
  COL: { name: 'Colombia', flag: '🇨🇴', rank: 46 },
  CHI: { name: 'Chile', flag: '🇨🇱', rank: 47 },
}

const code = computed(() => route.params.code?.toUpperCase())
const meta = computed(() => teamMeta[code.value] || { name: 'Team', flag: '🏆', rank: 0 })
const players = computed(() => allPlayers[code.value] || [])

const positions = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

const positionColor = {
  'Goalkeeper': { bg: 'bg-yellow-500/15', border: 'border-yellow-500/30', text: 'text-yellow-400', icon: '🧤' },
  'Defender': { bg: 'bg-blue-500/15', border: 'border-blue-500/30', text: 'text-blue-400', icon: '🛡️' },
  'Midfielder': { bg: 'bg-green-500/15', border: 'border-green-500/30', text: 'text-green-400', icon: '👟' },
  'Forward': { bg: 'bg-red-500/15', border: 'border-red-500/30', text: 'text-red-400', icon: '⚡' },
}

const groupedPlayers = computed(() => {
  const groups = {}
  positions.forEach(pos => { groups[pos] = [] })
  players.value.forEach(p => {
    if (groups[p.position]) groups[p.position].push(p)
  })
  return Object.entries(groups).filter(([_, pts]) => pts.length > 0)
})
</script>

<template>
  <div class="space-y-6">
    <button @click="$router.back()" class="flex items-center gap-2 text-surface-400 hover:text-yellow-400 transition-colors group">
      <span class="group-hover:-translate-x-1 transition-transform text-lg">←</span>
      <span class="text-sm font-bold">Back to Teams</span>
    </button>

    <div v-if="!players.length" class="text-center py-16 glass rounded-2xl">
      <TeamFlag :code="code" :flag="meta.flag" :name="meta.name" size="2xl" class="mx-auto" />
      <p class="text-surface-400 text-lg font-medium">Squad details coming soon for {{ meta.name }}</p>
      <p class="text-surface-600 text-sm mt-1">Check back for player profiles and positions</p>
    </div>

    <template v-else>
      <div class="glass-gold rounded-3xl p-6 sm:p-8 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-500 via-green-500 to-yellow-500"></div>
        <div class="flex flex-col sm:flex-row items-center gap-6">
          <div class="relative">
            <TeamFlag :code="code" :flag="meta.flag" :name="meta.name" size="2xl" class="mx-auto" />
            <div class="absolute -bottom-1 -right-1 w-10 h-10 rounded-full bg-yellow-500 text-black text-sm font-black flex items-center justify-center">
              #{{ meta.rank }}
            </div>
          </div>
          <div class="text-center sm:text-left">
            <h1 class="text-2xl sm:text-3xl font-black text-gradient-gold">{{ meta.name }}</h1>
            <p class="text-surface-400 text-sm mt-2 font-medium">{{ players.length }} players · Full squad roster</p>
            <div class="flex flex-wrap justify-center sm:justify-start gap-2 mt-4">
              <span class="px-3 py-1.5 rounded-xl bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs font-bold">🌍 Group</span>
              <span class="px-3 py-1.5 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-bold">⚽ Ready</span>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-8">
        <div v-for="[position, posPlayers] in groupedPlayers" :key="position" class="animate-slide-up">
          <div class="flex items-center gap-3 mb-4">
            <span class="text-3xl">{{ positionColor[position].icon }}</span>
            <h3 class="text-lg sm:text-xl font-black text-white">{{ position }}s</h3>
            <span class="text-[10px] font-bold px-2.5 py-1 rounded-lg" :class="positionColor[position].bg + ' ' + positionColor[position].text">
              {{ posPlayers.length }} player{{ posPlayers.length > 1 ? 's' : '' }}
            </span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div
              v-for="(player, idx) in posPlayers"
              :key="player.number"
              class="glass-holographic rounded-2xl p-4 sm:p-5 card-hover relative overflow-hidden group animate-slide-up"
              :style="{ animationDelay: idx * 0.05 + 's' }"
            >
              <div class="scan-line"></div>
              <div class="relative z-10 flex items-center gap-4">
                <div class="relative flex-shrink-0">
                  <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-br from-surface-800/80 to-surface-900/80 flex items-center justify-center text-3xl sm:text-4xl border border-surface-700/20 group-hover:scale-105 transition-transform duration-300">
                    {{ player.photo }}
                  </div>
                  <div class="absolute -top-1 -right-1 w-7 h-7 rounded-full bg-yellow-500 text-black text-xs font-black flex items-center justify-center">
                    {{ player.number }}
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="font-black text-sm sm:text-base text-white truncate">{{ player.name }}</h4>
                  <p class="text-[10px] uppercase tracking-widest font-bold mt-0.5" :class="positionColor[player.position].text">
                    {{ player.position }}
                  </p>
                  <div class="flex items-center gap-2 mt-2">
                    <div class="flex-1 h-1.5 rounded-full bg-surface-800/60 overflow-hidden">
                      <div class="h-full rounded-full bg-gradient-to-r from-yellow-500 to-green-500" :style="{ width: player.rating + '%' }"></div>
                    </div>
                    <span class="text-xs font-black text-yellow-400 tabular-nums">{{ player.rating }}</span>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-black text-gradient-gold">{{ player.rating }}</div>
                  <div class="text-[9px] text-surface-500 font-bold uppercase">OVR</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
