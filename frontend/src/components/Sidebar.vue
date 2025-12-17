<template>
  <div class="sidebar-container">
    <!-- 头部 -->
    <div class="sidebar-header">
      <div class="sidebar-title">
        <span class="dot"></span>
        <h3>对话列表</h3>
        <span class="count" v-if="store.conversations.length">
          共 {{ store.conversations.length }} 个
        </span>
      </div>

      <el-button
        type="primary"
        size="small"
        round
        @click="openDialog"
      >
        <el-icon class="btn-icon"><Plus /></el-icon>
        新对话
      </el-button>
    </div>

    <!-- 列表区域 -->
    <div class="sidebar-list">
      <el-scrollbar class="scroll-area">
        <el-menu
          :default-active="store.currentId"
          class="chat-list"
          @select="store.switchConversation"
        >
          <el-menu-item
            v-for="conv in store.conversations"
            :key="conv.id"
            :index="conv.id"
            class="chat-item"
          >
            <div class="chat-item-main">
              <el-icon class="chat-icon"><ChatDotRound /></el-icon>
              <span
                class="chat-title"
                :title="conv.title"
              >
                {{ conv.title }}
              </span>
            </div>
            <div class="chat-item-actions">
              <el-button
                class="delete-button"
                text
                size="small"
                @click.stop="deleteConversation(conv.id)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </div>

    <!-- 新对话标题弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="输入对话标题"
      width="380px"
    >
      <div class="dialog-body">
        <p class="dialog-tip">
          为这次对话起一个便于识别的名字，例如「周报总结」或「论文润色」。
        </p>
        <el-input
          v-model="newTitle"
          placeholder="请输入对话标题"
          maxlength="40"
          show-word-limit
          clearable
        />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmNew">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/store/chatStore'
import { Plus, ChatDotRound, Delete } from '@element-plus/icons-vue'

const store = useChatStore()
const dialogVisible = ref(false)
const newTitle = ref('')

function openDialog() {
  newTitle.value = ''
  dialogVisible.value = true
}

function confirmNew() {
  const title = newTitle.value.trim() || '新对话'
  store.newConversation(title)
  dialogVisible.value = false
}

function deleteConversation(id) {
  store.deleteConversation(id)
}
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  padding: 16px 12px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(circle at 0 0, rgba(56, 189, 248, 0.12), transparent 55%),
    radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.12), transparent 55%),
    #020617;
  border-right: 1px solid rgba(148, 163, 184, 0.35);
}

/* 头部 */
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 4px 4px 8px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sidebar-title h3 {
  margin: 0;
  font-size: 15px;
  color: #e5e7eb;
  font-weight: 600;
}

.sidebar-title .dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.9);
}

.count {
  font-size: 12px;
  color: #9ca3af;
}

/* 列表外壳 */
.sidebar-list {
  flex: 1;
  overflow: hidden;
  border-radius: 12px;
  background: rgba(15, 23, 42, 0.85);
  padding: 6px;
  box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.9);
}

.scroll-area {
  height: 100%;
}

/* el-menu 基础样式 */
.chat-list {
  border-right: none;
  background-color: transparent;
}

/* 单个 item 效果 */
:deep(.el-menu-item.chat-item) {
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  margin-bottom: 4px;
  padding-inline: 8px;
  display: flex;
  align-items: center;
}

:deep(.el-menu-item.chat-item:hover) {
  background: rgba(30, 64, 175, 0.55);
}

:deep(.el-menu-item.chat-item.is-active) {
  background: linear-gradient(
    90deg,
    rgba(59, 130, 246, 0.22),
    rgba(129, 140, 248, 0.4)
  );
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.35);
}

/* 内容区：左标题 + 右按钮 */
.chat-item-main {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.chat-icon {
  font-size: 16px;
  color: #9ca3af;
}

:deep(.el-menu-item.is-active .chat-icon) {
  color: #e5e7eb;
}

.chat-title {
  flex: 1;
  font-size: 13px;
  color: #e5e7eb;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-item-actions {
  opacity: 0;
  transition: opacity 0.15s ease;
}

:deep(.el-menu-item.chat-item:hover .chat-item-actions),
:deep(.el-menu-item.chat-item.is-active .chat-item-actions) {
  opacity: 1;
}

/* 删除按钮 */
.delete-button {
  margin-left: 4px;
  padding: 0;
}

:deep(.delete-button .el-icon) {
  font-size: 16px;
  color: #f97373;
}

/* 弹窗 */
.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.dialog-tip {
  font-size: 13px;
  color: #6b7280;
  margin: 0 0 4px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
