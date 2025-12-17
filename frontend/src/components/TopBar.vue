<template>
  <div class="top-bar-wrapper">
    <el-row align="middle" justify="space-between" class="top-bar">
      <!-- 左侧：品牌 + 模型选择 -->
      <div class="top-bar-left">
        <div class="brand">
          <span class="brand-logo">Λ</span>
          <span class="brand-title">AI 控制面板</span>
        </div>

        <div class="model-block">
          <span class="field-label">模型来源</span>
          <el-radio-group
            v-model="store.currentModelSource"
            size="small"
            @change="handleModelSourceChange"
          >
            <el-radio-button label="local">本地模型</el-radio-button>
            <el-radio-button label="api">调用 API</el-radio-button>
          </el-radio-group>

          <el-divider direction="vertical" class="divider" />

          <span class="field-label">当前模型</span>
          <el-select
            :key="store.currentModelSource"          
            v-model="store.currentModel"
            size="small"
            class="model-select"
            placeholder="请选择模型"
            :disabled="loading"
            clearable
            @change="onChange"
          >
            <el-option
              v-for="opt in currentOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </div>
      </div>

      <!-- 右侧：头像 / 用户菜单 -->
      <div class="user-avatar">
        <el-dropdown @command="handleDropdownCommand">
          <div class="avatar-wrapper">
            <el-avatar
              size="large"
              src="src\assets\OIP.jpg"
            />
            <span class="user-name">欢迎你</span>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="退出">退出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-row>

    <!-- API 密钥弹窗 -->
    <el-dialog
      v-model="showApiKeyDialog"
      title="配置 API 密钥"
      width="420px"
      :close-on-click-modal="false"
    >
      <div class="api-dialog-body">
        <p class="tip">
          请选择 API 模型前，请先填写用于调用大模型服务的 API Key。
          我们会将其安全传给后端，仅用于本系统的接口请求。
        </p>
        <el-input
          v-model="apiKey"
          type="password"
          placeholder="例如：sk-xxxxxxxxxxxxxxxx"
          show-password
          autocomplete="off"
        />
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleApiKeyCancel">取消</el-button>
          <el-button
            type="primary"
            :loading="savingApiKey"
            @click="handleApiKeyConfirm"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage, ElLoading } from 'element-plus'
import { useModelStore } from '@/store/model'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useModelStore()

const loading = ref(false)          // 模型加载状态
const savingApiKey = ref(false)     // API 密钥保存状态
let loadingInstance = null          // Loading 实例

// 本地模型选项
const options = [
  { label: '通义千问', value: '通义千问' },
  { label: '百川', value: '百川' },
  { label: 'Yi', value: 'Yi' },
  { label: '九格', value: '九格' },
  { label: 'mistral', value: 'mistral' },
  { label: 'zephyr', value: 'zephyr' },
]

// API 模型选项
const apiOptions = [
  { label: 'deepseek', value: 'deepseek' },
]

// 当前下拉显示的 options，随来源切换
const currentOptions = computed(() =>
  store.currentModelSource === 'local' ? options : apiOptions
)

// API 密钥弹窗相关
const showApiKeyDialog = ref(false)
const apiKey = ref('')

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

// 页面初始化，获取当前模型状态
onMounted(async () => {
  try {
    const res = await axios.get('/api/get_model')
    if (res.data?.model) {
      store.setModel(res.data.model)
    }

    if (res.data?.loading) {
      loading.value = true
      loadingInstance = ElLoading.service({
        lock: true,
        text: '模型加载中，请稍候...',
        background: 'rgba(15, 23, 42, 0.35)',
        spinner: 'el-icon-loading'
      })
      pollModelStatus()
    }
  } catch (err) {
    console.error('获取模型失败', err)
    ElMessage.error('获取模型失败')
  }
})

// 切换模型
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
      background: 'rgba(15, 23, 42, 0.35)',
      spinner: 'el-icon-loading'
    })

    await axios.post('/api/set_model', { model: val })
    // 切换模型后也启动轮询检测
    pollModelStatus()
    ElMessage.success('模型切换成功')
  } catch (err) {
    console.error(err)
    ElMessage.error('模型切换失败')
    loading.value = false
    loadingInstance?.close()
  }
}

// 切换模型来源（local / api）
function handleModelSourceChange(val) {
  // 更新来源
  store.setModelSource(val)

  // 当前来源对应的合法模型 value 列表
  const targetOptions = val === 'local' ? options : apiOptions
  const validValues = targetOptions.map(o => o.value)

  // 如果当前选中的模型不属于该来源，就清空
  if (!validValues.includes(store.currentModel)) {
    store.setModel('')   // ✅ 让下拉回到“请选择模型”
  }

  // 选择 API 时弹出密钥输入框
  if (val === 'api') {
    apiKey.value = ''
    showApiKeyDialog.value = true
  }
}

// 确认保存 API 密钥
async function handleApiKeyConfirm() {
  if (!apiKey.value.trim()) {
    ElMessage.warning('请输入 API 密钥')
    return
  }

  try {
    savingApiKey.value = true
    await axios.post('/api/set_api_key', {
      api_key: apiKey.value.trim(),
    })
    ElMessage.success('API 密钥已保存')
    showApiKeyDialog.value = false
  } catch (err) {
    console.error('保存 API 密钥失败', err)
    ElMessage.error('保存 API 密钥失败')
  } finally {
    savingApiKey.value = false
  }
}

// 取消配置 API 密钥（仅关闭弹窗，不改变当前 radio 状态）
function handleApiKeyCancel() {
  showApiKeyDialog.value = false
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

<style scoped>
/* 整体背景偏淡蓝，适配对话区淡蓝背景 */
.top-bar-wrapper {
  padding: 14px 20px;
  background: linear-gradient(90deg, #e0f2ff, #f3f7ff);
}

/* 顶部卡片：白色略透明，柔和阴影 */
.top-bar {
  width: 100%;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 18px;
  padding: 12px 22px;
  box-shadow: 0 10px 30px rgba(148, 163, 184, 0.35);
  border: 1px solid rgba(191, 219, 254, 0.85);
  box-sizing: border-box;
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 28px;
}

/* 左侧品牌区域 */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-logo {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  background: radial-gradient(circle at 30% 10%, #38bdf8, #3b82f6 50%, #22c55e);
  color: #f9fafb;
  box-shadow: 0 0 14px rgba(59, 130, 246, 0.7);
}

.brand-title {
  font-size: 20px;
  font-weight: 650;
  color: #0f172a;
  letter-spacing: 0.06em;
}

/* 模型块：柔和边框 + 圆角胶囊 */
.model-block {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(239, 246, 255, 0.95);
  border: 1px solid rgba(191, 219, 254, 0.9);
}

.field-label {
  font-size: 14px;
  color: #64748b;
  margin-right: 4px;
  white-space: nowrap;
  font-weight: 500;
}

.model-select {
  min-width: 170px;
}

.divider {
  height: 24px;
}

/* 右侧头像区域 */
.user-avatar {
  display: flex;
  align-items: center;
}

.avatar-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  cursor: pointer;
  background: linear-gradient(
    135deg,
    rgba(219, 234, 254, 0.9),
    rgba(224, 242, 254, 0.9)
  );
  border: 1px solid rgba(191, 219, 254, 0.9);
  transition: box-shadow 0.15s ease, transform 0.15s ease;
}

.avatar-wrapper:hover {
  box-shadow: 0 8px 18px rgba(148, 163, 184, 0.45);
  transform: translateY(-1px);
}

.avatar-wrapper :deep(.el-avatar) {
  border: 2px solid #ffffff;
  box-shadow: 0 3px 8px rgba(148, 163, 184, 0.7);
}

.user-name {
  font-size: 15px;
  color: #1f2937;
  font-weight: 500;
}

/* 弹窗内容 */
.api-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.api-dialog-body .tip {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* —— 放大 Element Plus 内部字体/间距（不改组件逻辑） —— */
:deep(.el-radio-button__inner) {
  font-size: 14px;
  padding: 6px 18px;
}

:deep(.el-select .el-input__inner) {
  font-size: 14px;
  height: 32px;
}

:deep(.el-input__inner) {
  font-size: 14px;
}
</style>
