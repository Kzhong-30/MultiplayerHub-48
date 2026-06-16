<template>
  <div class="page-container">
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card class="card-shadow mb-20">
          <template #header>
            <div class="flex-between">
              <span class="card-title">欢迎回来，{{ userInfo?.username }}！</span>
              <el-tag type="primary">🎉 养宠第 {{ daysWithPet }} 天</el-tag>
            </div>
          </template>
          <div class="welcome-content">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="stat-item">
                  <el-icon :size="32" color="#409EFF"><Collection /></el-icon>
                  <div class="stat-info">
                    <div class="stat-value">{{ pets.length }}</div>
                    <div class="stat-label">宠物数量</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <el-icon :size="32" color="#67C23A"><Promotion /></el-icon>
                  <div class="stat-info">
                    <div class="stat-value">{{ myPosts.length }}</div>
                    <div class="stat-label">发布动态</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <el-icon :size="32" color="#E6A23C"><Connection /></el-icon>
                  <div class="stat-info">
                    <div class="stat-value">{{ matches.length }}</div>
                    <div class="stat-label">配对请求</div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <div class="flex-between">
              <span class="card-title">我的宠物</span>
              <el-button type="primary" size="small" @click="$router.push('/pets')">
                查看全部
              </el-button>
            </div>
          </template>
          <el-row :gutter="20" v-if="pets.length > 0">
            <el-col :span="8" v-for="pet in pets.slice(0, 3)" :key="pet.id" class="mb-20">
              <div class="pet-card cursor-pointer" @click="$router.push(`/pets/${pet.id}`)">
                <el-avatar :size="80" :src="pet.avatar" shape="square">
                  {{ pet.name[0] }}
                </el-avatar>
                <div class="pet-info">
                  <div class="pet-name">{{ pet.name }}</div>
                  <div class="pet-breed">{{ pet.breed }}</div>
                  <el-tag size="small" :type="pet.gender === 'male' ? 'primary' : 'danger'">
                    {{ pet.gender === 'male' ? '公' : '母' }}
                  </el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-empty v-else description="还没有宠物，快去添加吧！">
            <el-button type="primary" @click="$router.push('/pets')">添加宠物</el-button>
          </el-empty>
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <div class="flex-between">
              <span class="card-title">最新动态</span>
              <el-button type="primary" size="small" @click="$router.push('/posts')">
                查看全部
              </el-button>
            </div>
          </template>
          <div v-if="latestPosts.length > 0">
            <div v-for="post in latestPosts.slice(0, 3)" :key="post.id" class="post-preview">
              <div class="post-header">
                <el-avatar :src="post.author?.avatar">
                  {{ post.author?.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <div class="post-author-info">
                  <div class="post-author">{{ post.author?.username }}</div>
                  <div class="post-time">{{ formatDate(post.created_at) }}</div>
                </div>
              </div>
              <div class="post-content">{{ post.content }}</div>
              <div v-if="post.media_url" class="post-media">
                <img v-if="post.media_type === 'image'" :src="post.media_url" alt="" />
                <video v-else-if="post.media_type === 'video'" :src="post.media_url" controls />
              </div>
              <div class="post-tags" v-if="post.tags?.length">
                <el-tag v-for="tag in post.tags" :key="tag" size="small" type="info" effect="plain">
                  #{{ tag }}
                </el-tag>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无动态" />
        </el-card>
      </el-col>

      <el-col :span="6">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="card-title">快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="showPostDialog = true" style="width: 100%; margin-bottom: 10px">
              <el-icon><Edit /></el-icon> 发布动态
            </el-button>
            <el-button type="success" @click="$router.push('/matches')" style="width: 100%; margin-bottom: 10px">
              <el-icon><Connection /></el-icon> 智能配对
            </el-button>
            <el-button type="warning" @click="$router.push('/nearby')" style="width: 100%; margin-bottom: 10px">
              <el-icon><Location /></el-icon> 附近宠物
            </el-button>
            <el-button type="info" @click="$router.push('/services')" style="width: 100%">
              <el-icon><Service /></el-icon> 服务导航
            </el-button>
          </div>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="card-title">附近聚会</span>
          </template>
          <div v-if="meetups.length > 0">
            <div v-for="meetup in meetups.slice(0, 3)" :key="meetup.id" class="meetup-item">
              <div class="meetup-title">{{ meetup.title }}</div>
              <div class="meetup-info">
                <el-icon><Location /></el-icon>
                <span>{{ meetup.location }}</span>
              </div>
              <div class="meetup-info">
                <el-icon><Clock /></el-icon>
                <span>{{ formatDate(meetup.meetup_date) }}</span>
              </div>
              <div class="meetup-info">
                <el-icon><User /></el-icon>
                <span>{{ meetup.current_participants }}/{{ meetup.max_participants }}人</span>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无聚会" :image-size="80" />
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span class="card-title">服务推荐</span>
          </template>
          <div v-if="services.length > 0">
            <div v-for="service in services.slice(0, 3)" :key="service.id" class="service-item">
              <img :src="service.image_url" alt="" class="service-image" />
              <div class="service-info">
                <div class="service-name">{{ service.name }}</div>
                <div class="service-category">
                  <el-tag size="small">{{ service.category }}</el-tag>
                  <el-rate v-model="service.rating" disabled size="small" />
                </div>
                <div class="service-distance">{{ service.distance }}km</div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无服务数据" :image-size="80" />
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showPostDialog" title="发布动态" width="500px">
      <el-form :model="postForm">
        <el-form-item label="内容">
          <el-input v-model="postForm.content" type="textarea" :rows="4" placeholder="分享你的养宠日常..." />
        </el-form-item>
        <el-form-item label="话题标签">
          <el-select v-model="postForm.tags" multiple placeholder="选择或输入话题">
            <el-option v-for="tag in hotTags" :key="tag" :label="tag" :value="tag" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联宠物">
          <el-select v-model="postForm.pet_id" placeholder="选择宠物（可选）">
            <el-option v-for="pet in pets" :key="pet.id" :label="pet.name" :value="pet.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPostDialog = false">取消</el-button>
        <el-button type="primary" @click="createPost">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePetStore } from '@/stores/pet'
import { postApi, nearbyApi, serviceApi, matchApi } from '@/api'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const petStore = usePetStore()

const userInfo = computed(() => userStore.userInfo)
const pets = computed(() => petStore.pets)
const daysWithPet = computed(() => {
  if (pets.value.length > 0) {
    const earliest = pets.value.reduce((min, p) => {
      const date = dayjs(p.created_at)
      return date.isBefore(min) ? date : min
    }, dayjs())
    return dayjs().diff(earliest, 'day')
  }
  return 0
})

const latestPosts = ref([])
const myPosts = ref([])
const meetups = ref([])
const services = ref([])
const matches = ref([])
const showPostDialog = ref(false)
const hotTags = ['日常', '萌宠', '搞笑', '遛狗', '猫咪', '训练', '美容', '健康']

const postForm = ref({
  content: '',
  tags: [],
  pet_id: null,
  media_type: 'image',
  media_url: 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600'
})

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function loadData() {
  try {
    await petStore.fetchPets()
    const [postsRes, myPostsRes, meetupsRes, servicesRes, matchesRes] = await Promise.all([
      postApi.getPosts({ limit: 5 }),
      userInfo.value ? postApi.getUserPosts(userInfo.value.id) : [],
      nearbyApi.getNearbyMeetups({ radius_km: 50 }),
      serviceApi.getServices({ radius_km: 50 }),
      matchApi.getReceivedMatches()
    ])
    latestPosts.value = postsRes
    myPosts.value = myPostsRes
    meetups.value = meetupsRes
    services.value = servicesRes
    matches.value = matchesRes
  } catch (e) {
    console.error('加载数据失败', e)
  }
}

async function createPost() {
  if (!postForm.value.content.trim()) {
    ElMessage.warning('请输入动态内容')
    return
  }
  try {
    await postApi.createPost(postForm.value)
    ElMessage.success('发布成功')
    showPostDialog.value = false
    postForm.value = { content: '', tags: [], pet_id: null, media_type: 'image', media_url: '' }
    loadData()
  } catch (e) {
    ElMessage.error('发布失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.card-title {
  font-size: 16px;
  font-weight: 500;
}

.welcome-content {
  padding: 10px 0;

  .stat-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background: #f5f7fa;
    border-radius: 8px;

    .stat-info {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #303133;
      }
      .stat-label {
        color: #909399;
        font-size: 14px;
      }
    }
  }
}

.pet-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .pet-info {
    .pet-name {
      font-size: 16px;
      font-weight: 500;
      margin-bottom: 4px;
    }
    .pet-breed {
      color: #909399;
      font-size: 13px;
      margin-bottom: 6px;
    }
  }
}

.post-preview {
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .post-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;

    .post-author-info {
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
    margin-bottom: 10px;
    line-height: 1.6;
  }

  .post-media {
    margin-bottom: 10px;

    img, video {
      max-height: 200px;
      border-radius: 8px;
    }
  }

  .post-tags {
    display: flex;
    gap: 8px;
  }
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.meetup-item {
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .meetup-title {
    font-weight: 500;
    margin-bottom: 6px;
  }
  .meetup-info {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #909399;
    font-size: 13px;
    margin-bottom: 4px;
  }
}

.service-item {
  display: flex;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .service-image {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 6px;
  }

  .service-info {
    flex: 1;

    .service-name {
      font-weight: 500;
      margin-bottom: 4px;
    }
    .service-category {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
    }
    .service-distance {
      color: #409EFF;
      font-size: 13px;
    }
  }
}
</style>
