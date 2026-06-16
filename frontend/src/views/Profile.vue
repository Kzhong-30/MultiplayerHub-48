<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">个人中心</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="card-shadow">
          <div class="profile-header text-center">
            <el-avatar :size="120" :src="userStore.userInfo?.avatar" class="profile-avatar">
              {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
            </el-avatar>
            <h2 class="username mt-15">{{ userStore.userInfo?.username }}</h2>
            <p class="email">{{ userStore.userInfo?.email }}</p>
            <p class="bio" v-if="userStore.userInfo?.bio">{{ userStore.userInfo?.bio }}</p>

            <el-divider />

            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-value">{{ petCount }}</div>
                <div class="stat-label">宠物数量</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ postCount }}</div>
                <div class="stat-label">发布动态</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ matchCount }}</div>
                <div class="stat-label">配对成功</div>
              </div>
            </div>
          </div>
        </el-card>

        <el-card class="card-shadow mt-20">
          <template #header>
            <span class="section-title"><el-icon><Location /></el-icon> 地理位置</span>
          </template>
          <div v-if="userStore.userInfo?.latitude && userStore.userInfo?.longitude">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="纬度">{{ userStore.userInfo.latitude }}</el-descriptions-item>
              <el-descriptions-item label="经度">{{ userStore.userInfo.longitude }}</el-descriptions-item>
            </el-descriptions>
            <el-button type="primary" class="mt-10" size="small" @click="showLocationDialog = true">
              <el-icon><Edit /></el-icon> 修改位置
            </el-button>
          </div>
          <el-empty v-else description="暂未设置地理位置">
            <el-button type="primary" @click="showLocationDialog = true">设置位置</el-button>
          </el-empty>
        </el-card>

        <el-card class="card-shadow mt-20">
          <template #header>
            <span class="section-title"><el-icon><Key /></el-icon> 修改密码</span>
          </template>
          <el-form :model="passwordForm" ref="passwordFormRef" label-width="80px">
            <el-form-item label="原密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
            </el-form-item>
            <el-button type="primary" @click="changePassword">修改密码</el-button>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-card class="card-shadow">
          <template #header>
            <span class="section-title"><el-icon><Edit /></el-icon> 基本信息</span>
          </template>
          <el-form :model="profileForm" label-width="100px">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="用户名">
                  <el-input v-model="profileForm.username" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱">
                  <el-input v-model="profileForm.email" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="头像URL">
              <el-input v-model="profileForm.avatar" placeholder="输入头像图片链接" />
            </el-form-item>
            <el-form-item label="个人简介">
              <el-input
                v-model="profileForm.bio"
                type="textarea"
                :rows="3"
                placeholder="介绍一下自己和你的宠物..."
              />
            </el-form-item>
            <div class="form-actions">
              <el-button type="primary" @click="updateProfile" :loading="updating">保存修改</el-button>
            </div>
          </el-form>
        </el-card>

        <el-card class="card-shadow mt-20">
          <template #header>
            <span class="section-title"><el-icon><Picture /></el-icon> 我的动态</span>
          </template>
          <div v-if="myPosts.length > 0">
            <div v-for="post in myPosts" :key="post.id" class="post-item">
              <div class="post-header">
                <el-avatar :size="40" :src="userStore.userInfo?.avatar">
                  {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <div class="post-info">
                  <div class="post-author">{{ userStore.userInfo?.username }}</div>
                  <div class="post-time">{{ formatDate(post.created_at) }}</div>
                </div>
                <el-button
                  size="small"
                  type="danger"
                  text
                  @click="deletePost(post.id)"
                >
                  <el-icon><Delete /></el-icon> 删除
                </el-button>
              </div>
              <div class="post-content mt-10">{{ post.content }}</div>
              <div class="post-media mt-10" v-if="post.media_url">
                <img
                  :src="post.media_url"
                  class="post-image"
                />
              </div>
              <div class="post-tags mt-10" v-if="post.tags?.length > 0">
                <el-tag
                  v-for="(tag, index) in post.tags"
                  :key="index"
                  size="small"
                  type="primary"
                  effect="plain"
                >
                  #{{ tag }}
                </el-tag>
              </div>
              <div class="post-stats mt-10">
                <span class="stat">
                  <el-icon color="#F56C6C"><Star /></el-icon>
                  {{ post.likes_count || 0 }}
                </span>
                <span class="stat">
                  <el-icon color="#909399"><ChatDotRound /></el-icon>
                  {{ post.comments_count || 0 }}
                </span>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无动态">
            <el-button type="primary" @click="$router.push('/posts')">去发布动态</el-button>
          </el-empty>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showLocationDialog" title="设置地理位置" width="500px">
      <el-form :model="locationForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="纬度">
              <el-input-number
                v-model="locationForm.latitude"
                :precision="6"
                :min="-90"
                :max="90"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="经度">
              <el-input-number
                v-model="locationForm.longitude"
                :precision="6"
                :min="-180"
                :max="180"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-alert
          title="提示"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <p>可以使用谷歌地图或手机定位获取经纬度坐标。例如：北京 纬度39.9042，经度116.4074</p>
            <el-button size="small" type="primary" link @click="useDefaultLocation">使用默认位置（北京）</el-button>
          </template>
        </el-alert>
      </el-form>
      <template #footer>
        <el-button @click="showLocationDialog = false">取消</el-button>
        <el-button type="primary" @click="saveLocation">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePetStore } from '@/stores/pet'
import { postApi, authApi } from '@/api'
import dayjs from 'dayjs'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const petStore = usePetStore()

const updating = ref(false)
const myPosts = ref([])
const showLocationDialog = ref(false)
const petCount = computed(() => petStore.pets.length)
const postCount = computed(() => myPosts.value.length)
const matchCount = ref(0)

const profileForm = reactive({
  username: '',
  email: '',
  avatar: '',
  bio: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const locationForm = reactive({
  latitude: null,
  longitude: null
})

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function loadUserInfo() {
  if (userStore.userInfo) {
    profileForm.username = userStore.userInfo.username
    profileForm.email = userStore.userInfo.email
    profileForm.avatar = userStore.userInfo.avatar || ''
    profileForm.bio = userStore.userInfo.bio || ''
    locationForm.latitude = userStore.userInfo.latitude
    locationForm.longitude = userStore.userInfo.longitude
  }
}

async function loadMyPosts() {
  try {
    myPosts.value = await postApi.getUserPosts(userStore.userInfo?.id) || []
  } catch (e) {
    console.error('加载我的动态失败', e)
  }
}

async function updateProfile() {
  if (!profileForm.username || !profileForm.email) {
    ElMessage.warning('用户名和邮箱不能为空')
    return
  }
  updating.value = true
  try {
    await userStore.updateUserInfo({
      username: profileForm.username,
      email: profileForm.email,
      avatar: profileForm.avatar,
      bio: profileForm.bio
    })
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    updating.value = false
  }
}

async function changePassword() {
  if (!passwordForm.oldPassword || !passwordForm.newPassword || !passwordForm.confirmPassword) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.warning('两次输入的新密码不一致')
    return
  }
  if (passwordForm.newPassword.length < 6) {
    ElMessage.warning('新密码长度不能少于6位')
    return
  }
  try {
    await authApi.updateMe({
      old_password: passwordForm.oldPassword,
      password: passwordForm.newPassword
    })
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '修改失败')
  }
}

async function saveLocation() {
  if (locationForm.latitude === null || locationForm.longitude === null) {
    ElMessage.warning('请填写完整的经纬度')
    return
  }
  try {
    await userStore.updateUserInfo({
      latitude: locationForm.latitude,
      longitude: locationForm.longitude
    })
    ElMessage.success('位置保存成功')
    showLocationDialog.value = false
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  }
}

function useDefaultLocation() {
  locationForm.latitude = 39.9042
  locationForm.longitude = 116.4074
}

async function deletePost(postId) {
  try {
    await ElMessageBox.confirm('确定要删除这条动态吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await postApi.deletePost(postId)
    ElMessage.success('删除成功')
    loadMyPosts()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(async () => {
  loadUserInfo()
  await petStore.fetchPets()
  loadMyPosts()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
}

.mb-20 {
  margin-bottom: 20px;
}

.mt-10 {
  margin-top: 10px;
}

.mt-15 {
  margin-top: 15px;
}

.mt-20 {
  margin-top: 20px;
}

.text-center {
  text-align: center;
}

.profile-header {
  .profile-avatar {
    border: 4px solid #ecf5ff;
  }

  .username {
    margin: 0;
    font-size: 24px;
    font-weight: 500;
  }

  .email {
    color: #909399;
    margin: 5px 0;
  }

  .bio {
    color: #606266;
    font-size: 14px;
  }
}

.profile-stats {
  display: flex;
  justify-content: space-around;

  .stat-item {
    text-align: center;

    .stat-value {
      font-size: 24px;
      font-weight: 500;
      color: #409EFF;
    }

    .stat-label {
      color: #909399;
      font-size: 13px;
    }
  }
}

.section-title {
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-actions {
  text-align: right;
}

.post-item {
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .post-header {
    display: flex;
    align-items: center;
    gap: 12px;

    .post-info {
      flex: 1;

      .post-author {
        font-weight: 500;
      }

      .post-time {
        color: #909399;
        font-size: 12px;
      }
    }
  }

  .post-content {
    color: #303133;
    line-height: 1.6;
  }

  .post-images {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    .post-image {
      width: 120px;
      height: 120px;
      object-fit: cover;
      border-radius: 6px;
    }
  }

  .post-tags {
    display: flex;
    gap: 8px;
  }

  .post-stats {
    display: flex;
    gap: 20px;
    color: #909399;
    font-size: 13px;

    .stat {
      display: flex;
      align-items: center;
      gap: 5px;
    }
  }
}
</style>
