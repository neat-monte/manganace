import { createRouter, createWebHashHistory } from 'vue-router'
import Generator from '@/views/Generator.vue'
import Library from '@/views/Library.vue'

const routes = [
  {
    path: "/",
    alias: "/library",
    name: "Collections",
    component: Library
  },
  {
    path: "/library/:collectionId",
    name: "ImagesOfCollection",
    component: Library
  },
  {
    path: "/generator",
    name: "Generator",
    component: Generator
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
