<template>
  <div class="file-upload">
    <el-upload
      :http-request="uploadFile"
      accept=".txt,.md"
      :show-file-list="false"
    >
      <el-button type="primary" icon="Upload">上传文件</el-button>
    </el-upload>

    <!-- 上传成功后显示文件名 -->
    <div v-if="fileName" class="file-name">文件名：{{ fileName }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useChatStore } from '@/store/chatStore'
axios.defaults.withCredentials = true
const store = useChatStore()
const fileName = ref('')
const uploaded = ref(false)

async function uploadFile({ file, onSuccess, onError }) {
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await axios.post('/api/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      withCredentials: true
    })

    fileName.value = file.name
    uploaded.value = true
    console.log('用户 ID:', res.data.user_id)
    onSuccess(res.data)
  } catch (err) {
    console.error('上传失败:', err)
    onError(err)
  }
}

// 回车事件监听：清除文件名
function handleKeyPress(event) {
  if (event.key === 'Enter') {
    fileName.value = ''
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress)
})
</script>

<style scoped>
.el-upload .el-button {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 30px;
  box-shadow: 0 4px 10px rgba(0, 242, 255, 0.3);
  transition: all 0.3s ease;
}

.el-upload .el-button:hover {
  background: linear-gradient(135deg, #00dbde 0%, #fc00ff 100%);
  box-shadow: 0 6px 14px rgba(252, 0, 255, 0.4);
  transform: translateY(-2px);
}

.file-name {
  margin-top: 10px;
  font-size: 14px;
  color: #409eff;
  font-weight: 500;
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.2);
}


</style>
