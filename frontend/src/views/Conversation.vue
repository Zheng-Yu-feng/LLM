// Conversation.vue
<template>
  <div class="conversation-page">
    <Sidebar class="sidebar" />
    <div class="main-area">
      <TopBar />
      <Chat class="chat-view" />
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
import Chat from '@/components/Chat.vue'
import TopBar from '@/components/TopBar.vue'
</script>

<style scoped>
.conversation-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
.sidebar {
  width: 360px;
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
}
.chat-view {
  flex: 1;
  position: relative;
  overflow: hidden;
}
.main-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100vh;
  overflow: hidden; /* 防止双滚动条 */
}

</style>