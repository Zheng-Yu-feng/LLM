<template>
    <div class="app-container">
      <header class="header">
        <h1 class="title">懂你的AI助手</h1>
        <p class="subtitle">阅书万卷，我是你的知识宝典</p>
      </header>
  
      <main class="main-content">
        <section class="introduction">
          <h2>关于语言模型</h2>
          <p>旨在理解和生成自然语言。通过深度学习技术，能够提供智能对话、文本分析和语言翻译等服务。</p>
        </section>
  
        <section class="features">
          <h2>功能介绍</h2>
          <ul class="feature-list">
            <li><strong>智能对话：</strong>与用户进行流畅的对话，解答问题和提供信息。</li>
            <li><strong>文本分析：</strong>分析文本内容，提取关键信息和情感倾向。</li>
            <li><strong>语言翻译：</strong>支持多种语言之间的即时翻译。</li>
            <li><strong>知识检索：</strong>快速检索大量信息，为用户提供准确的答案。</li>
          </ul>
        </section>
  
        <section class="get-started">
          <button class="start-conversation-btn" @click="startConversation">开始对话</button>
        </section>
  
        <section class="api-trial">
          <a href="https://api.example.com/trial" class="api-trial-link" target="_blank">API免费试用</a>
        </section>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home',
    methods: {
      startConversation() {
        return this.$router.push('/conversation');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Container */
  .app-container {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    padding: 50px 20px;
    font-family: 'Arial', sans-serif;
    color: #444;
  }
  
  /* Header */
  .header {
    margin-bottom: 40px;
  }
  
  .title {
    font-size: 2.5rem;
    color: #007bff;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .subtitle {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 30px;
  }
  
  /* Sections */
  .main-content h2 {
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 20px;
    border-bottom: 2px solid #007bff;
    display: inline-block;
    padding-bottom: 5px;
  }
  
  .introduction p {
    font-size: 1rem;
    line-height: 1.6;
    color: #555;
  }
  
  /* Feature List */
  .feature-list {
    list-style: none;
    padding: 0;
  }
  
  .feature-list li {
    margin-bottom: 10px;
    font-size: 1rem;
    color: #333;
    line-height: 1.5;
  }
  
  .feature-list li strong {
    color: #007bff;
  }
  
  /* Buttons and Links */
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
  
  .start-conversation-btn:hover {
    background-color: #0056b3;
    transform: translateY(-3px);
  }
  
  .api-trial-link {
    display: inline-block;
    margin-top: 20px;
    color: #007bff;
    text-decoration: none;
    font-size: 1rem;
    transition: color 0.3s ease;
  }
  
  .api-trial-link:hover {
    color: #0056b3;
    text-decoration: underline;
  }
  </style>
  