import { createApp } from 'vue'
// import { createPinia } from 'pinia';
import App from './App.vue'
import router from './router'
import { setupStore } from './store'
import 'animate.css';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// import ElementUI from 'element-ui';
// import 'element-ui/lib/theme-chalk/index.css';
const app = createApp(App)
// app.use(router); 
// // const pinia = createPinia();
// // app.use(pinia);
// app.use(createPinia())
// setupStore(app)
// app.mount('#app')
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
// setupStore(app)  // 如果你有 extra store 初始化
app.mount('#app')