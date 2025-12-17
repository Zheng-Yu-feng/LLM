import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { nanoid } from 'nanoid'  // 用于生成唯一 ID


export const useChatStore = defineStore('chat', () => {
  const conversations = ref([
    {
      id: nanoid(),
      title: 'welcome',
      messages: [
        { role: 'assistant', content: '您好，有什么可以帮您的？' }
      ]
    }
  ])
  const currentId = ref(conversations.value[0].id)

  const currentConversation = computed(() =>
    conversations.value.find(conv => conv.id === currentId.value)
  )

  const currentMessages = computed(() =>
    currentConversation.value?.messages || []
  )

  function newConversation(title) {
    const newId = nanoid()
    conversations.value.unshift({
      id: newId,
      title: title,
      messages: [{ role: 'assistant', content: '您好，有什么可以帮您的？'}]
    })
    currentId.value = newId
  }

  function switchConversation(id) {
    currentId.value = id
  }

  // function addMessage(message) {
  //   const conv = conversations.value.find(c => c.id === currentId.value)
  //   if (conv) conv.messages.push(message)
  // }
  function addMessage(message) {
    const conv = conversations.value.find(c => c.id === currentId.value)
    if (conv) {
      const safeMsg = {
        role: message.role,
        content: message.content,
        gen_time: message.gen_time || null  // 确保字段存在，避免 undefined
      }
      conv.messages.push(safeMsg)
    }
  }
  function deleteMessage(index) {
    const conv = currentConversation.value
    if (conv && conv.messages[index]) {
      conv.messages.splice(index, 1)
    }
  }
  function exportCurrentConversationAsMarkdown() {
    const conv = conversations.value.find(c => c.id === currentId.value)
    if (!conv) return null
    const messages = conv.messages
    const markdown = messages.reduce((acc, msg) => {
      return `${acc}> ${msg.role}\n\n${msg.content}\n\n`
    }, '')

    const filename = `chat-history-${conv.title}-${Date.now()}.md`
    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    return { url, filename }
  }
  function exportCurrentConversationAsJson() {
    const conv = conversations.value.find(c => c.id === currentId.value)
    if (!conv) return null
    const messages = conv.messages
    const filename = `chat-history-${conv.title}-${Date.now()}.json`
    const blob = new Blob([JSON.stringify(messages)], { type: "application/json" });
    const url = URL.createObjectURL(blob)
    return { url, filename }
  }
  function deleteConversation(id) {
  const index = conversations.value.findIndex(conv => conv.id === id)
  if (index !== -1) {
    conversations.value.splice(index, 1)
    // 如果当前对话被删除，则切换到第一个对话（或清空）
    if (currentId.value === id) {
      currentId.value = conversations.value[0]?.id || null
    }
  }
}

  return {
    conversations,
    currentId,
    currentConversation,
    currentMessages,
    newConversation,
    switchConversation,
    addMessage,
    deleteMessage,
    exportCurrentConversationAsMarkdown,
    exportCurrentConversationAsJson,
    deleteConversation
  }
},{
  persist: true
})
