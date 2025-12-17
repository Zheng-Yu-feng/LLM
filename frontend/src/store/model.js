import { defineStore } from 'pinia'

export const useModelStore = defineStore('model', {
  state: () => ({
    currentModel: 'qwen',  // 默认值
    currentModelSource: 'local'  // 默认值
  }),
  actions: {
    setModel(val) {
      this.currentModel = val
    },
    setModelSource(val) {
      this.currentModelSource = val
    },
    
  },
  persist: true  // ✅ 开启持久化
})
