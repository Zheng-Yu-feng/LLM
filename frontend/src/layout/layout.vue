<template>
  <div class="common-layout">
    <el-container style="height: 100vh">
      <!-- Header 部分 -->
      <el-header style="text-align: right; font-size: 36px; padding: 10px; background-color: #e0f7fa;">
        <div class="toolbar">
          <div style="display: flex; justify-content: space-between; align-items: center; background-color: #e6f7ff; padding: 10px 20px;">
            <!-- 左上部分 -->
            <div class="header-left" style="display: flex; align-items: center; margin-top: -10px">
              <span style="font-size: 30px; font-weight: bold;">大语言模型对话系统</span>
            </div>

            <!-- 右上部分 -->
            <div class="user-avatar" style="display: flex; align-items: center;">
              <el-dropdown @command="handleDropdownCommand">
                <el-avatar 
                  size="large" 
                  src="src\img\OIP.jpg" 
                  style="cursor: pointer; height: 52px; width: 56px; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); margin-top: -8px; margin-right: 30px;"/>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="首页">首页</el-dropdown-item>
                    <el-dropdown-item command="退出">退出</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div> 
      </el-header>

      <el-container>
        <!-- Aside 部分 -->
        <el-aside width="300px" style="background-color: #72b6e4;">
          <el-scrollbar style="background-color: #72b6e4;">
            <el-menu @select="handleSelect" style="background-color: #72b6e4;">
              <el-sub-menu index="1" style="background-color: #72b6e4;">
                <template #title>
                  <el-icon><ChatDotSquare /></el-icon>生成式智能服务
                </template>
                  <el-menu-item index="home" style="background-color: #72b6e4">对话问答</el-menu-item >
                  <el-menu-item index="about" style="background-color: #72b6e4">其它</el-menu-item >
              </el-sub-menu>
              <el-sub-menu index="2">
                <template #title>
                  <el-icon><Stamp /></el-icon>单比特水印
                </template>
                  <el-menu-item index="model" style="background-color: #72b6e4">单比特水印嵌入</el-menu-item>
                  <el-menu-item index="parameter" style="background-color: #72b6e4">单比特水印提取</el-menu-item>
              </el-sub-menu>
              <el-sub-menu index="3" style="background-color: #72b6e4;">
                <template #title>
                  <el-icon><Stamp /></el-icon>多比特水印
                </template>
                  <el-menu-item index="more_bit_embed" style="background-color: #72b6e4">多比特水印嵌入</el-menu-item >
                  <el-menu-item index="more_bit_extract" style="background-color: #72b6e4">多比特水印提取</el-menu-item >
              </el-sub-menu>
              <el-sub-menu index="4" style="background-color: #72b6e4;">
                <template #title>
                  <el-icon><InfoFilled /></el-icon>算法概述
                </template>
              </el-sub-menu>
              <el-sub-menu index="5" style="background-color: #72b6e4;">
                <template #title>
                  <el-icon><User /></el-icon>团队简介
                </template>
              </el-sub-menu>
              <el-sub-menu index="6" style="background-color: #72b6e4;">
                <template #title>
                  <el-icon><Setting /></el-icon>用户管理
                </template>
              </el-sub-menu>
            </el-menu>
          </el-scrollbar>
        </el-aside>

        <!-- Main 部分 -->
        <el-main style="background-color: #fafafa;">
          <router-view /> <!-- 渲染不同页面的内容 -->
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue' 
import { ChatDotSquare, Stamp, InfoFilled, User, ChatLineSquare, Document, DocumentChecked, PriceTag, PieChart, Wallet, Setting as SettingIcon } from '@element-plus/icons-vue'

// 路由实例
const router = useRouter()
// Method to handle dropdown commands
function handleDropdownCommand(command) {
  switch (command) {
    case 'view':
      // Add functionality for view
      console.log('View clicked')
      break
    case '首页':
      // Add functionality for add
      router.push('/home')
      break
    case '退出':
      // Redirect to login on delete
      router.push('/login')
      break
    default:
      break
  }
}
// 处理选择菜单项跳转
const handleSelect = (index) => {
  router.push({ name: index })
}
</script>

<style scoped>
.common-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.el-header {
  background-color: #e0f7fa; /* 浅蓝色 */
  padding: 10px;
  text-align: right;
  font-size: 36px;
}

.el-aside {
  background-color: #72b6e4;
  padding: 20px;
  box-sizing: border-box;
}

.el-main {
  padding: 20px;
  background-color: #0529c7;
}

.user-avatar .el-avatar {
  cursor: pointer;
}
</style>

