<template>
  <el-container class="layout-container">
    <el-aside :width="sidebarCollapsed ? '64px' : '220px'" class="sidebar">
      <div class="logo flex-center">
        <el-icon v-if="sidebarCollapsed" :size="28" color="#409EFF"><PawPrint /></el-icon>
        <span v-else class="logo-text">宠物社交平台</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="sidebarCollapsed"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/home">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/pets">
          <el-icon><Collection /></el-icon>
          <template #title>宠物档案</template>
        </el-menu-item>
        <el-menu-item index="/posts">
          <el-icon><Promotion /></el-icon>
          <template #title>动态广场</template>
        </el-menu-item>
        <el-menu-item index="/matches">
          <el-icon><Connection /></el-icon>
          <template #title>智能配对</template>
        </el-menu-item>
        <el-menu-item index="/encyclopedia">
          <el-icon><Reading /></el-icon>
          <template #title>宠物百科</template>
        </el-menu-item>
        <el-menu-item index="/nearby">
          <el-icon><Location /></el-icon>
          <template #title>附近宠物</template>
        </el-menu-item>
        <el-menu-item index="/services">
          <el-icon><Service /></el-icon>
          <template #title>服务导航</template>
        </el-menu-item>
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <template #title>个人中心</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header flex-between">
        <div class="header-left flex-center">
          <el-icon class="toggle-btn" @click="toggleSidebar" :size="20">
            <Fold v-if="!sidebarCollapsed" />
            <Expand v-else />
          </el-icon>
          <span class="page-title">{{ pageTitle }}</span>
        </div>
        <div class="header-right flex-center">
          <el-dropdown @command="handleCommand">
            <div class="user-info flex-center cursor-pointer">
              <el-avatar :size="32" :src="userInfo?.avatar">
                {{ userInfo?.username?.[0]?.toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userInfo?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()

const sidebarCollapsed = computed(() => appStore.sidebarCollapsed)
const userInfo = computed(() => userStore.userInfo)
const activeMenu = computed(() => route.path)
const pageTitle = computed(() => route.meta?.title || '')

function toggleSidebar() {
  appStore.toggleSidebar()
}

function handleCommand(command) {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      ElMessage.success('退出成功')
      router.push('/login')
    }).catch(() => {})
  }
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  transition: width 0.3s;

  .logo {
    height: 60px;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    background-color: #2b2f3a;

    .logo-text {
      background: linear-gradient(90deg, #409EFF, #67C23A);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  :deep(.el-menu) {
    border-right: none;
  }
}

.header {
  height: 60px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;

  .header-left {
    gap: 15px;

    .toggle-btn {
      cursor: pointer;
      color: #606266;
      transition: color 0.3s;

      &:hover {
        color: #409EFF;
      }
    }

    .page-title {
      font-size: 18px;
      font-weight: 500;
      color: #303133;
    }
  }

  .header-right {
    .user-info {
      gap: 10px;

      .username {
        color: #606266;
      }
    }
  }
}

.main-content {
  background-color: #f0f2f5;
  padding: 0;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
