<template>
  <div class="login-container">
    <div class="login-bg"></div>
    <div class="login-card card-shadow">
      <div class="login-header text-center">
        <el-icon :size="48" color="#409EFF"><PawPrint /></el-icon>
        <h1 class="title">宠物社交平台</h1>
        <p class="subtitle">连接爱宠人士，分享养宠乐趣</p>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" size="large">
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" show-password>
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" @click="handleLogin" style="width: 100%">
            登录
          </el-button>
        </el-form-item>
        <div class="text-center">
          还没有账号？<router-link to="/register" class="link">立即注册</router-link>
        </div>
      </el-form>
      <el-divider>测试账号</el-divider>
      <div class="test-accounts">
        <el-tag v-for="(acc, idx) in testAccounts" :key="idx" class="mb-10" style="width: 100%">
          {{ acc.username }} / 123456
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const testAccounts = [
  { username: 'petlover' },
  { username: 'catfan' },
  { username: 'dogdad' }
]

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  try {
    await formRef.value.validate()
    loading.value = true
    await userStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/home')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: -1;

  &::before {
    content: '';
    position: absolute;
    top: 10%;
    left: 10%;
    width: 300px;
    height: 300px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 10%;
    right: 10%;
    width: 400px;
    height: 400px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
  }
}

.login-card {
  width: 420px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
}

.login-header {
  margin-bottom: 30px;

  .title {
    margin: 15px 0 8px;
    font-size: 28px;
    background: linear-gradient(90deg, #409EFF, #67C23A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    color: #909399;
    font-size: 14px;
  }
}

.login-form {
  .link {
    color: #409EFF;
  }
}

.test-accounts {
  display: flex;
  flex-direction: column;
  gap: 8px;

  .mb-10 {
    margin-bottom: 8px;
  }
}
</style>
