<template>
  <div class="app-container">
    <!-- 顶部标题 -->
    <header class="header">
      <h1 class="title">文件解析助手</h1>
      <p class="subtitle">精准提取内容，智能解析文件</p>
    </header>

    <!-- 主体内容 -->
    <main class="main-content">
      <!-- 文件解析介绍 -->
      <section class="introduction">
        <h2>关于文件解析</h2>
        <p>
          我们的文件解析工具支持多种格式，如 PDF、Word 和 TXT，能够快速提取关键内容并生成摘要，为您提供高效的信息处理体验。
        </p>
      </section>

      <!-- 功能模块 -->
      <section class="features">
        <h2>主要功能</h2>
        <ul class="feature-list">
          <li><strong>多格式支持：</strong>解析 PDF、Word 和 TXT 文件，适应多种办公需求。</li>
          <li><strong>快速提取：</strong>从文件中提取标题、段落、表格等关键信息。</li>
          <li><strong>智能摘要：</strong>基于文件内容生成精准摘要，助您快速获取要点。</li>
          <li><strong>在线解析：</strong>无需下载，直接上传文件即可解析，安全高效。</li>
        </ul>
      </section>
      
      <section class="get-started">
          <button class="start-conversation-btn" @click="startConversation">开始对话</button>
      </section>

      <!-- 试用 API -->
      <!-- <section class="api-trial">
        <a href="https://api.example.com/trial" class="api-trial-link" target="_blank">API 免费试用</a>
      </section> -->
    </main>
  </div>
</template>
<script>
  export default {
    name: 'About',
    methods: {
      startConversation() {
        return this.$router.push('/FileChat');
      },
    },
  }
</script>
<style scoped>
/* 页面整体布局 */
.app-container {
  font-family: 'Arial', sans-serif;
  color: #333;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.start-conversation-btn {
    padding: 12px 24px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    transition: all 0.3s ease;
    box-shadow: 0px 4px 8px rgba(0, 123, 255, 0.2);
    margin-top: 20px;
  }

/* 顶部标题样式 */
.header {
  text-align: center;
  margin-bottom: 30px;
}
.title {
  font-size: 2rem;
  color: #2c3e50;
  font-weight: bold;
}
.subtitle {
  font-size: 1rem;
  color: #7f8c8d;
}

/* 主要内容样式 */
.main-content section {
  margin-bottom: 20px;
}
.introduction p,
.features ul {
  line-height: 1.8;
  font-size: 1rem;
  color: #34495e;
}
.features ul {
  list-style: none;
  padding: 0;
}
.features ul li {
  margin-bottom: 10px;
}
.features ul li strong {
  color: #3498db;
}

/* 文件上传样式 */
.file-upload {
  text-align: center;
  margin-top: 20px;
}
.upload-file .el-button {
  margin-right: 10px;
}
.analyze-btn {
  margin-top: 15px;
}

/* 试用 API 样式 */
.api-trial-link {
  display: block;
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #27ae60;
  margin-top: 30px;
  text-decoration: none;
}
.api-trial-link:hover {
  color: #2ecc71;
}
</style>