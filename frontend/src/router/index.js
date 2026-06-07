import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TeamsView from '../views/TeamsView.vue'
import MatchDetailView from '../views/MatchDetailView.vue'
import CountryDetailView from '../views/CountryDetailView.vue'
import GalleryView from '../views/GalleryView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/teams', name: 'Teams', component: TeamsView },
  { path: '/match/:id', name: 'MatchDetail', component: MatchDetailView, props: true },
  { path: '/country/:code', name: 'CountryDetail', component: CountryDetailView, props: true },
  { path: '/gallery', name: 'Gallery', component: GalleryView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
