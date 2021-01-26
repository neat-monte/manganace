// import { nextTick } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import Generator from '@/views/Generator.vue'
import Library from '@/views/Library.vue'
import Research from '@/views/Research.vue'
import ResearchSession from '@/views/ResearchSession.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  {
    path: "/",
    alias: "/library",
    name: "Collections",
    component: Library,
    meta: { title: 'Manganace - Library' }
  },
  {
    path: "/generator",
    name: "Generator",
    component: Generator,
    meta: { title: 'Manganace - Generator' }
  },
  {
    path: "/research",
    name: "Research",
    component: Research,
    meta: { title: 'Manganace - Research' }
  },
  {
    path: "/research/session",
    name: "ResearchSession",
    component: ResearchSession,
    meta: { title: 'Manganace - Session' }
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound,
    meta: { title: 'Manganace - 404' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.afterEach((to) => {
  document.title = to.meta.title ?? "Manganace"
})

export default router
