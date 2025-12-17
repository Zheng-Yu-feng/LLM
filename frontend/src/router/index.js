import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/layout.vue'
import Home from '@/components/home.vue'
import About from '@/components/about.vue'
import { negate } from 'lodash-es'
import login from '@/components/login.vue'
import Chat from '@/components/chat.vue'
import ConversationVue from '@/views/Conversation.vue'
const routes = [
  {
    path: '/',
    redirect: '/login' 
  },
  {
    path: '/conversation',
    name: 'Conversation',
    component: ConversationVue,
  },
  {
    path: "/login",
    name: 'login',
    component: login,
  },
  // {

  //   path: '/',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'home',
  //       name: 'home',
  //       component: Home
  //     },
  //     {
  //       path: 'about',
  //       name: 'about',
  //       component: About
  //     },


  //   ]
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
