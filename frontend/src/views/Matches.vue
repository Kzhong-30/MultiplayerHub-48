<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">智能配对</h2>
      <div class="flex-center" style="gap: 10px">
        <el-tag type="info">基于品种、年龄、位置智能匹配</el-tag>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="card-shadow mb-20" v-if="!userLocationSet">
          <el-alert
            title="请先设置您的地理位置"
            type="warning"
            :closable="false"
            show-icon
          >
            <template #default>
              <p>为了更好的配对推荐，请在个人中心设置您的地理位置。</p>
              <el-button type="primary" size="small" @click="$router.push('/profile')">去设置</el-button>
            </template>
          </el-alert>
        </el-card>

        <el-card class="card-shadow mb-20" v-else-if="!hasPets">
          <el-alert
            title="请先添加宠物档案"
            type="warning"
            :closable="false"
            show-icon
          >
            <template #default>
              <p>为您的宠物添加档案后，即可获取智能配对推荐。</p>
              <el-button type="primary" size="small" @click="$router.push('/pets')">添加宠物</el-button>
            </template>
          </el-alert>
        </el-card>

        <el-card class="card-shadow" v-else>
          <template #header>
            <div class="flex-between">
              <span>为您推荐的玩伴</span>
              <el-button type="primary" size="small" @click="loadRecommendations" :loading="loading">
                <el-icon><Refresh /></el-icon> 刷新
              </el-button>
            </div>
          </template>

          <div v-if="recommendations.length > 0">
            <div v-for="rec in recommendations" :key="rec.target_user.id" class="match-card">
              <div class="match-header">
                <el-avatar :size="64" :src="rec.target_user.avatar">
                  {{ rec.target_user.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <div class="user-info">
                  <h3>{{ rec.target_user.username }}</h3>
                  <p class="user-bio">{{ rec.target_user.bio || '暂无简介' }}</p>
                  <div class="user-location">
                    <el-icon><Location /></el-icon>
                    <span>{{ rec.target_user.distance }} km</span>
                  </div>
                </div>
                <div class="match-score">
                  <el-progress
                    type="dashboard"
                    :percentage="rec.match_score"
                    :width="100"
                    :color="getScoreColor(rec.match_score)"
                  />
                  <div class="score-label">匹配度</div>
                </div>
              </div>

              <div class="match-pets mt-20">
                <h4>TA的宠物</h4>
                <div class="pets-list">
                  <div v-for="pet in rec.target_pets" :key="pet.id" class="pet-item">
                    <el-avatar :size="48" :src="pet.avatar">{{ pet.name[0] }}</el-avatar>
                    <div class="pet-info">
                      <div class="pet-name">{{ pet.name }}</div>
                      <el-tag size="small" type="info">{{ pet.breed }}</el-tag>
                    </div>
                  </div>
                </div>
              </div>

              <div class="match-details mt-20">
                <el-row :gutter="12">
                  <el-col :span="8">
                    <div class="detail-item">
                      <el-icon color="#409EFF"><Medal /></el-icon>
                      <span>品种匹配</span>
                      <el-tag type="primary" effect="plain">{{ rec.breed_compatibility }}%</el-tag>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <div class="detail-item">
                      <el-icon color="#67C23A"><Clock /></el-icon>
                      <span>年龄相近</span>
                      <el-tag type="success" effect="plain">{{ rec.age_similarity }}%</el-tag>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <div class="detail-item">
                      <el-icon color="#E6A23C"><Location /></el-icon>
                      <span>距离得分</span>
                      <el-tag type="warning" effect="plain">{{ rec.distance_score }}%</el-tag>
                    </div>
                  </el-col>
                </el-row>
              </div>

              <div class="match-actions mt-20 flex-between">
                <el-button type="primary" @click="sendMatch(rec.target_user.id)">
                  <el-icon><Connection /></el-icon> 发起配对
                </el-button>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无合适的配对推荐" />
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span>收到的配对请求</span>
          </template>
          <div v-if="receivedMatches.length > 0">
            <div v-for="match in receivedMatches" :key="match.id" class="match-request">
              <div class="request-header flex-between">
                <div class="flex-center" style="gap: 10px">
                  <el-avatar :size="40" :src="match.user?.avatar">
                    {{ match.user?.username?.[0]?.toUpperCase() }}
                  </el-avatar>
                  <div>
                    <div class="username">{{ match.user?.username }}</div>
                    <div class="match-time">{{ formatDate(match.created_at) }}</div>
                  </div>
                </div>
                <el-tag :type="getStatusType(match.status)" size="small">
                  {{ getStatusText(match.status) }}
                </el-tag>
              </div>
              <div v-if="match.message" class="message mt-10">
                {{ match.message }}
              </div>
              <div class="request-score mt-10 flex-center" style="gap: 10px">
                <span>匹配度：</span>
                <el-progress :percentage="match.match_score" :stroke-width="10" style="width: 120px" />
              </div>
              <div v-if="match.status === 'pending'" class="request-actions mt-10">
                <el-button size="small" type="success" @click="acceptMatch(match.id)">接受</el-button>
                <el-button size="small" type="danger" @click="rejectMatch(match.id)">拒绝</el-button>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无配对请求" :image-size="80" />
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span>我发起的请求</span>
          </template>
          <div v-if="sentMatches.length > 0">
            <div v-for="match in sentMatches" :key="match.id" class="match-request">
              <div class="request-header flex-between">
                <div class="flex-center" style="gap: 10px">
                  <el-avatar :size="40" :src="match.target_user?.avatar">
                    {{ match.target_user?.username?.[0]?.toUpperCase() }}
                  </el-avatar>
                  <div>
                    <div class="username">{{ match.target_user?.username }}</div>
                    <div class="match-time">{{ formatDate(match.created_at) }}</div>
                  </div>
                </div>
                <el-tag :type="getStatusType(match.status)" size="small">
                  {{ getStatusText(match.status) }}
                </el-tag>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无发起的请求" :image-size="80" />
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showMatchDialog" title="发起配对请求" width="400px">
      <el-form :model="matchForm">
        <el-form-item label="留言">
          <el-input v-model="matchForm.message" type="textarea" :rows="3" placeholder="可以说点什么...（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMatchDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmMatch">发送</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePetStore } from '@/stores/pet'
import { matchApi } from '@/api'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const petStore = usePetStore()

const recommendations = ref([])
const receivedMatches = ref([])
const sentMatches = ref([])
const loading = ref(false)
const showMatchDialog = ref(false)
const targetUserId = ref(null)

const matchForm = ref({
  message: ''
})

const userLocationSet = computed(() => {
  return userStore.userInfo?.latitude && userStore.userInfo?.longitude
})

const hasPets = computed(() => petStore.pets.length > 0)

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function getScoreColor(score) {
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#409EFF'
  if (score >= 40) return '#E6A23C'
  return '#F56C6C'
}

function getStatusType(status) {
  const types = {
    pending: 'warning',
    accepted: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

function getStatusText(status) {
  const texts = {
    pending: '待处理',
    accepted: '已接受',
    rejected: '已拒绝'
  }
  return texts[status] || status
}

async function loadRecommendations() {
  loading.value = true
  try {
    recommendations.value = await matchApi.getRecommendations()
  } catch (e) {
    ElMessage.error('加载推荐失败')
  } finally {
    loading.value = false
  }
}

async function loadMatches() {
  try {
    const [received, sent] = await Promise.all([
      matchApi.getReceivedMatches(),
      matchApi.getSentMatches()
    ])
    receivedMatches.value = received
    sentMatches.value = sent
  } catch (e) {
    console.error('加载配对请求失败', e)
  }
}

function sendMatch(userId) {
  targetUserId.value = userId
  matchForm.value.message = ''
  showMatchDialog.value = true
}

async function confirmMatch() {
  try {
    await matchApi.createMatch({
      target_user_id: targetUserId.value,
      message: matchForm.value.message
    })
    ElMessage.success('配对请求已发送')
    showMatchDialog.value = false
    loadMatches()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '发送失败')
  }
}

async function acceptMatch(id) {
  try {
    await matchApi.acceptMatch(id)
    ElMessage.success('已接受配对')
    loadMatches()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function rejectMatch(id) {
  try {
    await matchApi.rejectMatch(id)
    ElMessage.success('已拒绝配对')
    loadMatches()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

onMounted(async () => {
  await petStore.fetchPets()
  if (userLocationSet.value && hasPets.value) {
    loadRecommendations()
  }
  loadMatches()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
}

.match-card {
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .match-header {
    display: flex;
    align-items: center;
    gap: 20px;

    .user-info {
      flex: 1;

      h3 {
        margin: 0 0 5px;
        font-size: 18px;
      }

      .user-bio {
        color: #909399;
        margin-bottom: 5px;
      }

      .user-location {
        display: flex;
        align-items: center;
        gap: 5px;
        color: #606266;
        font-size: 13px;
      }
    }

    .match-score {
      text-align: center;

      .score-label {
        font-size: 12px;
        color: #909399;
        margin-top: -10px;
      }
    }
  }

  .match-pets {
    h4 {
      margin-bottom: 10px;
      color: #606266;
    }

    .pets-list {
      display: flex;
      gap: 20px;

      .pet-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        background: #f5f7fa;
        border-radius: 8px;

        .pet-name {
          font-weight: 500;
          margin-bottom: 3px;
        }
      }
    }
  }

  .match-details {
    .detail-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 12px;
      background: #f5f7fa;
      border-radius: 8px;
    }
  }

  .mt-10 {
    margin-top: 10px;
  }

  .mt-20 {
    margin-top: 20px;
  }
}

.match-request {
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;

  &:last-child {
    border-bottom: none;
  }

  .username {
    font-weight: 500;
  }

  .match-time {
    color: #909399;
    font-size: 12px;
  }

  .message {
    padding: 10px;
    background: #f5f7fa;
    border-radius: 6px;
    font-size: 13px;
  }

  .mt-10 {
    margin-top: 10px;
  }
}
</style>
