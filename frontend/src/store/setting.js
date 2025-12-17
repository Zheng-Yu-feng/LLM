// store/setting.ts
import { defineStore } from 'pinia'

export const useSettingStore = defineStore('setting', {
  state: () => ({
    parameters: {
      temperature: 1.0,
      top_k: 20,
      top_p: 1.0,
      max_length: 1024
    }
  }),
  actions: {
    setParameter(key, value) {
      this.parameters[key] = value
    }
  },
  persist: true  // <--- 关键一步：开启持久化
})
