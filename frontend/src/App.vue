<script setup>
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import Chat from '@/components/Chat.vue'
import login from '@/components/login.vue';

import home from './components/home.vue';
import about from './components/about.vue';
import Sidebar from './components/Sidebar.vue'
import Conversation from './views/Conversation.vue';
</script>

<template>
  <el-config-provider :locale="zhCn">
    <router-view></router-view> 
  </el-config-provider>
</template>

<style lang="scss">
* {
  -webkit-tap-highlight-color: transparent;
}

html,
body,
div,
p,
section {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

ul {
  margin: 4px 0;
}

body {
  background-image: url('/static/bg-sprite.png');
  background-position: 0% 0%;
  background-size: 300% 200%;
}
</style>
