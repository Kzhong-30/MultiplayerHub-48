<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">附近宠物</h2>
      <div class="flex-center" style="gap: 10px">
        <el-button type="primary" @click="showMeetupDialog = true">
          <el-icon><Plus /></el-icon> 发起聚会
        </el-button>
      </div>
    </div>

    <el-alert
      v-if="!userLocationSet"
      title="请先设置您的地理位置"
      type="warning"
      :closable="false"
      show-icon
      class="mb-20"
    >
      <template #default>
        <p>为了查看附近的宠物和聚会，请先在个人中心设置您的地理位置。</p>
        <el-button type="primary" size="small" @click="$router.push('/profile')">去设置</el-button>
      </template>
    </el-alert>

    <el-tabs v-model="activeTab" v-else>
      <el-tab-pane label="附近宠物" name="pets">
        <div class="mb-20">
          <el-slider v-model="radius" :min="1" :max="50" :step="1" style="width: 300px">
            <template #default="{ value }">
              <span>搜索范围：{{ value }} 公里</span>
            </template>
          </el-slider>
        </div>

        <el-row :gutter="20">
          <el-col :span="8" v-for="item in nearbyPets" :key="item.pet.id">
            <el-card class="pet-card card-shadow">
              <div class="pet-header">
                <el-avatar :size="80" :src="item.pet.avatar">
                  {{ item.pet.name?.[0] }}
                </el-avatar>
                <div class="pet-info">
                  <h3 class="pet-name">{{ item.pet.name }}</h3>
                  <div class="pet-breed">
                    <el-tag size="small" type="info">{{ item.pet.breed }}</el-tag>
                    <el-tag size="small" type="success" v-if="item.pet.age">
                      {{ item.pet.age }}岁
                    </el-tag>
                  </div>
                  <div class="pet-distance">
                    <el-icon color="#409EFF"><Location /></el-icon>
                    <span>{{ item.distance }} km</span>
                  </div>
                </div>
              </div>

              <div class="owner-info mt-20">
                <div class="owner-header">
                  <el-avatar :size="32" :src="item.user.avatar">
                    {{ item.user.username?.[0]?.toUpperCase() }}
                  </el-avatar>
                  <div class="owner-detail">
                    <span class="owner-name">{{ item.user.username }}</span>
                    <span class="owner-bio" v-if="item.user.bio">{{ item.user.bio }}</span>
                  </div>
                </div>
              </div>

              <div class="pet-actions mt-20">
                <el-button type="primary" size="small" @click="sendMatchToUser(item.user.id)">
                  <el-icon><Connection /></el-icon> 发起配对
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="nearbyPets.length === 0" description="附近暂无宠物" />
      </el-tab-pane>

      <el-tab-pane label="线下聚会" name="meetups">
        <div class="flex-between mb-20">
          <el-select v-model="meetupStatus" placeholder="状态筛选" style="width: 150px" clearable>
            <el-option label="即将开始" value="upcoming" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已结束" value="ended" />
          </el-select>
        </div>

        <el-row :gutter="20">
          <el-col :span="12" v-for="meetup in filteredMeetups" :key="meetup.id">
            <el-card class="meetup-card card-shadow">
              <div class="meetup-header">
                <h3 class="meetup-title">{{ meetup.title }}</h3>
                <el-tag :type="getMeetupStatusType(meetup)" size="small">
                  {{ getMeetupStatusText(meetup) }}
                </el-tag>
              </div>

              <div class="meetup-info">
                <div class="info-item">
                  <el-icon><Calendar /></el-icon>
                  <span>{{ formatDate(meetup.meetup_date) }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Location /></el-icon>
                  <span>{{ meetup.location }}</span>
                </div>
                <div class="info-item" v-if="meetup.distance !== undefined">
                  <el-icon color="#409EFF"><Position /></el-icon>
                  <span>{{ meetup.distance }} km</span>
                </div>
                <div class="info-item">
                  <el-icon><User /></el-icon>
                  <span>发起人：{{ meetup.organizer?.username }}</span>
                </div>
                <div class="info-item">
                  <el-icon><UserFilled /></el-icon>
                  <span>{{ meetup.participants?.length || 0 }} 人参加</span>
                </div>
              </div>

              <div class="meetup-description" v-if="meetup.description">
                {{ meetup.description }}
              </div>

              <div class="meetup-participants" v-if="meetup.participants?.length > 0">
                <div class="participants-label">已报名：</div>
                <div class="participants-list">
                  <el-avatar
                    v-for="p in meetup.participants.slice(0, 5)"
                    :key="p.id"
                    :size="32"
                    :src="p.pet?.avatar"
                  >
                    {{ p.pet?.name?.[0] }}
                  </el-avatar>
                  <span v-if="meetup.participants.length > 5" class="more-count">
                    +{{ meetup.participants.length - 5 }}
                  </span>
                </div>
              </div>

              <div class="meetup-actions flex-between mt-20">
                <el-button size="small" @click="viewMeetupDetail(meetup)">
                  查看详情
                </el-button>
                <template v-if="meetup.organizer?.id !== currentUserId && isUpcoming(meetup)">
                  <el-button
                    v-if="!isJoined(meetup)"
                    type="primary"
                    size="small"
                    @click="joinMeetup(meetup)"
                  >
                    <el-icon><Check /></el-icon> 报名参加
                  </el-button>
                  <el-button
                    v-else
                    size="small"
                    type="danger"
                    @click="leaveMeetup(meetup.id)"
                  >
                    取消报名
                  </el-button>
                </template>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="filteredMeetups.length === 0" description="暂无聚会" />
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showMeetupDialog" title="发起聚会" width="500px">
      <el-form :model="meetupForm" ref="meetupFormRef" label-width="100px">
        <el-form-item label="聚会标题" prop="title">
          <el-input v-model="meetupForm.title" placeholder="请输入聚会标题" />
        </el-form-item>
        <el-form-item label="时间" prop="meetup_date">
          <el-date-picker
            v-model="meetupForm.meetup_date"
            type="datetime"
            placeholder="选择聚会时间"
            style="width: 100%"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="地点" prop="location">
          <el-input v-model="meetupForm.location" placeholder="请输入聚会地点" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="meetupForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述一下聚会内容..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMeetupDialog = false">取消</el-button>
        <el-button type="primary" @click="submitMeetup">发布</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showJoinDialog" title="选择参加的宠物" width="400px">
      <el-radio-group v-model="selectedPetId">
        <el-radio
          v-for="pet in myPets"
          :key="pet.id"
          :label="pet.id"
          class="pet-radio"
        >
          <el-avatar :size="32" :src="pet.avatar" style="margin-right: 10px">
            {{ pet.name?.[0] }}
          </el-avatar>
          {{ pet.name }}
        </el-radio>
      </el-radio-group>
      <template #footer>
        <el-button @click="showJoinDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmJoin" :disabled="!selectedPetId">
          确认报名
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showDetailDialog" title="聚会详情" width="600px">
      <div v-if="selectedMeetup">
        <h3>{{ selectedMeetup.title }}</h3>
        <div class="meetup-meta">
          <div class="meta-item"><el-icon><Calendar /></el-icon> {{ formatDate(selectedMeetup.meetup_date) }}</div>
          <div class="meta-item"><el-icon><Location /></el-icon> {{ selectedMeetup.location }}</div>
        </div>
        <p class="mt-20" v-if="selectedMeetup.description">{{ selectedMeetup.description }}</p>
        <div class="mt-20" v-if="selectedMeetup.participants?.length > 0">
          <h4>报名列表</h4>
          <div class="participant-list">
            <div v-for="p in selectedMeetup.participants" :key="p.id" class="participant-item">
              <el-avatar :size="40" :src="p.pet?.avatar">{{ p.pet?.name?.[0] }}</el-avatar>
              <div class="participant-info">
                <div class="pet-name">{{ p.pet?.name }}</div>
                <div class="owner-name">主人：{{ p.user?.username }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePetStore } from '@/stores/pet'
import { nearbyApi, matchApi } from '@/api'
import dayjs from 'dayjs'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const petStore = usePetStore()

const activeTab = ref('pets')
const radius = ref(10)
const nearbyPets = ref([])
const meetups = ref([])
const meetupStatus = ref('')
const showMeetupDialog = ref(false)
const showJoinDialog = ref(false)
const showDetailDialog = ref(false)
const selectedMeetup = ref(null)
const currentMeetupId = ref(null)
const selectedPetId = ref(null)
const myPets = computed(() => petStore.pets)
const currentUserId = computed(() => userStore.userInfo?.id)

const userLocationSet = computed(() => {
  return userStore.userInfo?.latitude && userStore.userInfo?.longitude
})

const meetupForm = ref({
  title: '',
  meetup_date: null,
  location: '',
  description: ''
})

const filteredMeetups = computed(() => {
  if (!meetupStatus.value) return meetups.value
  return meetups.value.filter(m => {
    if (meetupStatus.value === 'upcoming') return isUpcoming(m)
    if (meetupStatus.value === 'ongoing') return isOngoing(m)
    if (meetupStatus.value === 'ended') return isEnded(m)
    return true
  })
})

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function getMeetupStatusType(meetup) {
  if (isEnded(meetup)) return 'info'
  if (isOngoing(meetup)) return 'success'
  return 'warning'
}

function getMeetupStatusText(meetup) {
  if (isEnded(meetup)) return '已结束'
  if (isOngoing(meetup)) return '进行中'
  return '即将开始'
}

function isUpcoming(meetup) {
  return dayjs(meetup.meetup_date).isAfter(dayjs())
}

function isOngoing(meetup) {
  const now = dayjs()
  const meetupTime = dayjs(meetup.meetup_date)
  return now.isAfter(meetupTime) && now.isBefore(meetupTime.add(2, 'hour'))
}

function isEnded(meetup) {
  return dayjs(meetup.meetup_date).add(2, 'hour').isBefore(dayjs())
}

function isJoined(meetup) {
  return meetup.participants?.some(p => p.user_id === currentUserId.value)
}

async function loadNearbyPets() {
  try {
    nearbyPets.value = await nearbyApi.getNearbyPets({ radius: radius.value })
  } catch (e) {
    ElMessage.error('加载附近宠物失败')
  }
}

async function loadMeetups() {
  try {
    meetups.value = await nearbyApi.getNearbyMeetups({ radius: 50 })
  } catch (e) {
    ElMessage.error('加载聚会失败')
  }
}

async function sendMatchToUser(userId) {
  try {
    await ElMessageBox.confirm('确定要向该用户发起配对请求吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    await matchApi.createMatch({ target_user_id: userId })
    ElMessage.success('配对请求已发送')
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.detail || '发送失败')
    }
  }
}

function joinMeetup(meetup) {
  if (myPets.value.length === 0) {
    ElMessage.warning('请先添加宠物档案')
    return
  }
  currentMeetupId.value = meetup.id
  selectedPetId.value = myPets.value[0]?.id || null
  showJoinDialog.value = true
}

async function confirmJoin() {
  if (!selectedPetId.value) {
    ElMessage.warning('请选择宠物')
    return
  }
  try {
    await nearbyApi.joinMeetup(currentMeetupId.value, selectedPetId.value)
    ElMessage.success('报名成功')
    showJoinDialog.value = false
    loadMeetups()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '报名失败')
  }
}

async function leaveMeetup(meetupId) {
  try {
    await ElMessageBox.confirm('确定要取消报名吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await nearbyApi.leaveMeetup(meetupId)
    ElMessage.success('已取消报名')
    loadMeetups()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.detail || '操作失败')
    }
  }
}

function viewMeetupDetail(meetup) {
  selectedMeetup.value = meetup
  showDetailDialog.value = true
}

async function submitMeetup() {
  if (!meetupForm.value.title || !meetupForm.value.meetup_date || !meetupForm.value.location) {
    ElMessage.warning('请填写完整信息')
    return
  }
  try {
    await nearbyApi.createMeetup(meetupForm.value)
    ElMessage.success('聚会发布成功')
    showMeetupDialog.value = false
    meetupForm.value = { title: '', meetup_date: null, location: '', description: '' }
    loadMeetups()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '发布失败')
  }
}

onMounted(async () => {
  await petStore.fetchPets()
  if (userLocationSet.value) {
    loadNearbyPets()
    loadMeetups()
  }
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

.mt-20 {
  margin-top: 20px;
}

.pet-card {
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .pet-header {
    display: flex;
    gap: 16px;
    align-items: center;

    .pet-info {
      .pet-name {
        margin: 0 0 8px;
        font-size: 18px;
      }

      .pet-breed {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
      }

      .pet-distance {
        display: flex;
        align-items: center;
        gap: 4px;
        color: #409EFF;
        font-size: 13px;
      }
    }
  }

  .owner-info {
    padding-top: 15px;
    border-top: 1px solid #ebeef5;

    .owner-header {
      display: flex;
      gap: 10px;
      align-items: center;

      .owner-detail {
        display: flex;
        flex-direction: column;

        .owner-name {
          font-weight: 500;
        }

        .owner-bio {
          color: #909399;
          font-size: 12px;
        }
      }
    }
  }

  .pet-actions {
    display: flex;
    justify-content: flex-end;
  }
}

.meetup-card {
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .meetup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;

    .meetup-title {
      margin: 0;
      font-size: 18px;
    }
  }

  .meetup-info {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 20px;
    margin-bottom: 15px;

    .info-item {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #606266;
      font-size: 13px;
    }
  }

  .meetup-description {
    color: #606266;
    line-height: 1.6;
    margin-bottom: 15px;
    font-size: 14px;
  }

  .meetup-participants {
    display: flex;
    align-items: center;
    gap: 10px;

    .participants-label {
      color: #909399;
      font-size: 13px;
    }

    .participants-list {
      display: flex;
      align-items: center;
      gap: 5px;

      .more-count {
        color: #909399;
        font-size: 13px;
        margin-left: 5px;
      }
    }
  }
}

.pet-radio {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.meetup-meta {
  display: flex;
  gap: 20px;
  margin-top: 10px;

  .meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #606266;
  }
}

.participant-list {
  margin-top: 10px;

  .participant-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #ebeef5;

    &:last-child {
      border-bottom: none;
    }

    .participant-info {
      .pet-name {
        font-weight: 500;
      }

      .owner-name {
        color: #909399;
        font-size: 12px;
      }
    }
  }
}
</style>
