<template>
  <el-row align="middle" justify="space-between" class="top-bar">
    <!-- 模型来源选择 -->
    <el-radio-group v-model="modelSource" size="small" @change="onSourceChange">
      <el-radio-button label="local">本地模型</el-radio-button>
      <el-radio-button label="api">API模型</el-radio-button>
    </el-radio-group>

    <!-- 模型下拉，根据来源不同显示不同列表 -->
    <el-select
      v-if="modelSource === 'local'"
      v-model="store.currentModel"
      size="small"
      @change="onChange"
      :disabled="loading"
      class="model-select"
    >
      <el-option
        v-for="opt in localOptions"
        :key="opt.value"
        :label="opt.label"
        :value="opt.value"
      />
    </el-select>

    <el-select
      v-else
      v-model="store.currentModel"
      size="small"
      @change="onChangeApi"
      :disabled="loading"
      class="model-select"
    >
      <el-option
        v-for="opt in apiOptions"
        :key="opt.value"
        :label="opt.label"
        :value="opt.value"
      />
    </el-select>

    <!-- 用户头像 -->
    <div class="user-avatar" style="display: flex; align-items: center;">
      <el-dropdown @command="handleDropdownCommand">
        <el-avatar 
          size="large" 
          src="src/img/OIP.jpg" 
          style="cursor: pointer; height: 52px; width: 56px; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); margin-top: -8px; margin-right: 30px;"
        />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="首页">首页</el-dropdown-item>
            <el-dropdown-item command="退出">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import { useModelStore } from '@/store/model'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useModelStore()
const loading = ref(false)
let loadingInstance = null

// 模型来源
const modelSource = ref('local') // local / api

// 模型选项
const localOptions = [
  { label: '通义千问', value: 'qwen' },
  { label: '百川', value: 'baichuan' },
  { label: 'Yi', value: 'Yi' },
  { label: '九格', value: '9ge' },
  { label: 'mistral', value: 'mistral' },
  { label: 'zephyr', value: 'zephyr' },
]

const apiOptions = [
  { label: 'GPT', value: 'gpt' },
  { label: 'DeepSeek', value: 'deepseek' },
  { label: 'Claude', value: 'claude' },
]

// 模型来源切换
function onSourceChange(val) {
  store.currentModel = null
}

// 轮询检查模型加载状态
async function pollModelStatus() {
  const interval = setInterval(async () => {
    try {
      const res = await axios.get('/api/get_model')
      if (!res.data.loading) {
        loading.value = false
        loadingInstance?.close()
        clearInterval(interval)
        if (res.data.model) store.setModel(res.data.model)
      }
    } catch (err) {
      console.error(err)
      loading.value = false
      loadingInstance?.close()
      clearInterval(interval)
    }
  }, 1000)
}

// 页面初始化
onMounted(async () => {
  try {
    const res = await axios.get('/api/get_model')
    if (res.data?.model) store.setModel(res.data.model)

    if (res.data?.loading) {
      loading.value = true
      loadingInstance = ElLoading.service({
        lock: true,
        text: '模型加载中，请稍候...',
        background: 'rgba(0, 0, 0, 0.4)',
        spinner: 'el-icon-loading'
      })
      pollModelStatus()
    }
  } catch (err) {
    console.error('获取模型失败', err)
    ElMessage.error('获取模型失败')
  }
})

// 本地模型切换
async function onChange(val) {
  if (loading.value) {
    ElMessage.warning('模型正在加载，请稍等...')
    return
  }
  try {
    loading.value = true
    loadingInstance = ElLoading.service({
      lock: true,
      text: '模型加载中，请稍候...',
      background: 'rgba(0, 0, 0, 0.4)',
      spinner: 'el-icon-loading'
    })
    await axios.post('/api/set_model', { model: val })
    pollModelStatus()
    ElMessage.success('模型切换成功')
  } catch (err) {
    console.error(err)
    ElMessage.error('模型切换失败')
    loading.value = false
    loadingInstance?.close()
  }
}

// API模型切换
function onChangeApi(val) {
  store.currentModel = val
  ElMessage.success(`已选择 API 模型: ${val}`)
}

// 用户菜单
function handleDropdownCommand(command) {
  switch (command) {
    case '首页':
      router.push('/home')
      break
    case '退出':
      router.push('/login')
      break
    default:
      break
  }
}
</script>
