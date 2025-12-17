<template>
    <el-drawer v-model="drawerVisible" title="设置" size="500px">
      <el-form label-position="top" :model="parameters" label-width="120px">
        <el-alert title="参数设置" type="success" :closable="false" />
        <!-- Temperature 参数设置 -->
        <el-form-item label="Temperature">
          <el-slider v-model="parameters.temperature" :min="0" :max="1" :step="0.01" />
          <el-input-number v-model="parameters.temperature" :min="0" :max="1" :step="0.01" />
        </el-form-item>

        <!-- Top-k 参数设置 -->
        <el-form-item label="Top-k">
          <el-slider v-model="parameters.top_k" :min="0" :max="100" :step="1" />
          <el-input-number v-model="parameters.top_k" :min="0" :max="100" :step="1" />
        </el-form-item>

        <!-- Top-p 参数设置 -->
        <el-form-item label="Top-p">
          <el-slider v-model="parameters.top_p" :min="0" :max="1" :step="0.01" />
          <el-input-number v-model="parameters.top_p" :min="0" :max="1" :step="0.01" />
        </el-form-item>

        <!-- Max Tokens 参数设置 -->
        <el-form-item label="Max Tokens">
          <el-input-number v-model="parameters.max_length" :min="1" :max="100000" :step="1" />
        </el-form-item>
        <!-- 发送参数按钮 -->
        <el-form-item>
          <el-button type="primary" @click="sendParameters">完成设置</el-button>
        </el-form-item>

        <el-alert title="导入/导出" type="success" :closable="false" />
          <el-form label-position="top">
            <el-form-item label="导出对话记录">
              <el-row style="width: 100%">
                <el-col :span="11">
                  <el-button style="width: 100%" type="primary" @click="downloadMdHandle">导出为 MarkDown</el-button>
                </el-col>
                <el-col :span="11" :offset="1">
                  <el-button style="width: 100%" type="primary" @click="downloadJsonHandle">导出为 JSON</el-button>
                </el-col>
              </el-row>
            </el-form-item>
          </el-form>
      </el-form>
    </el-drawer>
</template>

<script setup>
import { ref, computed, onMounted} from 'vue'
import { storeToRefs } from 'pinia';
import axios from 'axios'
import { useSettingStore } from '@/store/setting';
import { useChatStore } from '@/store/chatStore';
import { ElMessage } from 'element-plus'
const settingStore = useSettingStore()
const parameters = computed({
  get: () => settingStore.parameters,
  set: (val) => settingStore.parameters = val
})

const drawerVisible = ref(true)
// 定义模型参数，初始值
// const parameters = ref({
//   temperature: 1.0,
//   top_k: 20,
//   top_p: 1.0,
//   max_length: 1024,
//   thinking: true
// })
onMounted(async () => {
  try {
    const res = await axios.get('/api/get_parameters')
    // 后端返回参数，更新 store
    if (res.data && typeof res.data === 'object') {
      // 逐个字段更新，避免覆盖掉持久化中已有字段
      for (const key in res.data) {
        if (res.data.hasOwnProperty(key)) {
          settingStore.setParameter(key, res.data[key])
        }
      }
    }
  } catch (err) {
    console.error('获取参数失败', err)
    ElMessage.warning('获取模型参数失败，使用本地默认值')
  }
})

const sendParameters = async () => {
  try {
    const response = await axios.post('/api/change_parameters', parameters.value)
    ElMessage.success(`参数应用成功：${response.data.message}`)
  } catch (error) {
    console.error('发送参数时出错:', error)
    ElMessage.error('发送参数时出错，请重试')
  }
}

// 导出Markdown
function downloadMdHandle() {
  const chatStore = useChatStore()
  const result = chatStore.exportCurrentConversationAsMarkdown()
  if (!result) {
    ElMessage.error('没有可导出的会话内容')
    return
  }
  downloadFn(result.url, result.filename)
}

// 导出JSON
function downloadJsonHandle() {
  const chatStore = useChatStore()
  const result = chatStore.exportCurrentConversationAsJson()
  if (!result) {
    ElMessage.error('没有可导出的会话内容')
    return
  }
  downloadFn(result.url, result.filename)
}

// 下载文件
function downloadFn(href, fileName) {
  const link = document.createElement('a') // 创建下载链接
  link.style.display = 'none'
  link.download = fileName
  link.href = href
  link.click() 
  link.remove() 
}
</script>

<style lang="scss">
.drawer-wrapper {
  background-image: url('/static/bg-sprite.png');
  background-position: 0% 0%;
  background-size: 300% 200%;

  .el-drawer__header {
    margin-bottom: 10px;
    --el-drawer-padding-primary: 16px 20px 0;
  }

  .el-drawer__body {
    --el-drawer-padding-primary: 16px 20px;
  }
}
</style>

<style lang="scss" scoped>
:deep(.el-alert) {
  margin-bottom: 12px;
}

:deep(.el-alert__content) {
  margin: 0 auto;
}
</style>