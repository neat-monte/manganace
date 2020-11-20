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
    component: Library
  },
  {
    path: "/library/:collectionId",
    name: "CollectionImages",
    component: Library
  },
  {
    path: "/generator",
    name: "Generator",
    component: Generator
  },
  {
    path: "/research",
    name: "Research",
    component: Research
  },
  {
    path: "/research/session",
    name: "ResearchSession",
    component: ResearchSession
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
