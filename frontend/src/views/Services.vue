<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">服务导航</h2>
      <div class="flex-center" style="gap: 10px">
        <el-button @click="seedServices">
          <el-icon><Refresh /></el-icon> 初始化数据
        </el-button>
      </div>
    </div>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="4" v-for="cat in categories" :key="cat.value">
        <div
          class="category-card cursor-pointer"
          :class="{ active: currentCategory === cat.value }"
          @click="currentCategory = cat.value"
        >
          <el-icon :size="32" :color="currentCategory === cat.value ? '#409EFF' : '#909399'">
            <component :is="cat.icon" />
          </el-icon>
          <span class="category-name">{{ cat.label }}</span>
        </div>
      </el-col>
    </el-row>

    <div class="flex-between mb-20">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索服务机构名称..."
        style="width: 300px"
        clearable
      >
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
      <el-select v-model="sortBy" placeholder="排序方式" style="width: 150px">
        <el-option label="距离最近" value="distance" />
        <el-option label="评分最高" value="rating" />
        <el-option label="价格最低" value="price" />
      </el-select>
    </div>

    <el-row :gutter="20">
      <el-col :span="12" v-for="service in filteredServices" :key="service.id">
        <el-card class="service-card card-shadow">
          <div class="service-header">
            <img :src="service.image_url" :alt="service.name" class="service-image" />
            <div class="service-info">
              <div class="flex-between">
                <h3 class="service-name">{{ service.name }}</h3>
                <el-tag :type="getCategoryType(service.category)" size="small">
                  {{ getCategoryLabel(service.category) }}
                </el-tag>
              </div>
              <div class="service-rating">
                <el-rate v-model="service.rating" disabled :max="5" :size="small" />
                <span class="rating-text">{{ service.rating }} 分</span>
                <span class="review-count">({{ service.review_count || 0 }}条评价)</span>
              </div>
              <div class="service-address">
                <el-icon color="#909399"><Location /></el-icon>
                <span>{{ service.address }}</span>
              </div>
              <div class="service-distance" v-if="service.distance !== undefined">
                <el-icon color="#409EFF"><Position /></el-icon>
                <span>{{ service.distance }} km</span>
              </div>
              <div class="service-phone" v-if="service.phone">
                <el-icon color="#67C23A"><Phone /></el-icon>
                <span>{{ service.phone }}</span>
              </div>
            </div>
          </div>

          <div class="service-tags mt-15" v-if="service.tags?.length > 0">
            <el-tag
              v-for="(tag, index) in service.tags.slice(0, 5)"
              :key="index"
              size="small"
              type="info"
              effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>

          <div class="service-description mt-15" v-if="service.description">
            {{ service.description }}
          </div>

          <div class="service-hours mt-15" v-if="service.business_hours">
            <el-icon color="#E6A23C"><Clock /></el-icon>
            <span>营业时间：{{ formatBusinessHours(service.business_hours) }}</span>
          </div>

          <div class="service-price mt-15" v-if="service.price_range">
            <el-icon color="#F56C6C"><Money /></el-icon>
            <span>价格范围：{{ service.price_range }}</span>
          </div>

          <div class="service-actions mt-20 flex-between">
            <el-button size="small" @click="viewServiceDetail(service)">
              查看详情
            </el-button>
            <div class="action-buttons">
              <el-button size="small" type="success" @click="callService(service)" v-if="service.phone">
                <el-icon><Phone /></el-icon> 电话
              </el-button>
              <el-button size="small" type="primary" @click="navigateTo(service)" v-if="service.address">
                <el-icon><Location /></el-icon> 导航
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="filteredServices.length === 0" description="暂无服务数据" />

    <el-dialog v-model="showDetailDialog" title="服务详情" width="700px">
      <div v-if="selectedService">
        <div class="detail-header">
          <img :src="selectedService.image_url" :alt="selectedService.name" class="detail-image" />
          <div class="detail-info">
            <h2>{{ selectedService.name }}</h2>
            <el-tag :type="getCategoryType(selectedService.category)" class="mb-10">
              {{ getCategoryLabel(selectedService.category) }}
            </el-tag>
            <div class="detail-rating">
              <el-rate v-model="selectedService.rating" disabled :max="5" />
              <span class="rating-text">{{ selectedService.rating }} 分</span>
              <span class="review-count">({{ selectedService.review_count || 0 }}条评价)</span>
            </div>
          </div>
        </div>

        <el-descriptions :column="2" border class="mt-20">
          <el-descriptions-item label="地址">{{ selectedService.address || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ selectedService.phone || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="营业时间">{{ formatBusinessHours(selectedService.business_hours) || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="价格范围">{{ selectedService.price_range || '暂无' }}</el-descriptions-item>
          <el-descriptions-item label="距离" v-if="selectedService.distance !== undefined">
            {{ selectedService.distance }} km
          </el-descriptions-item>
          <el-descriptions-item label="评分">{{ selectedService.rating }} / 5.0</el-descriptions-item>
        </el-descriptions>

        <div class="mt-20" v-if="selectedService.description">
          <h4>机构介绍</h4>
          <p class="description">{{ selectedService.description }}</p>
        </div>

        <div class="mt-20" v-if="selectedService.tags?.length > 0">
          <h4>服务项目</h4>
          <div class="tags-list">
            <el-tag v-for="(tag, index) in selectedService.tags" :key="index" size="large">
              {{ tag }}
            </el-tag>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button type="success" @click="callService(selectedService)" v-if="selectedService?.phone">
          <el-icon><Phone /></el-icon> 拨打电话
        </el-button>
        <el-button type="primary" @click="navigateTo(selectedService)" v-if="selectedService?.address">
          <el-icon><Location /></el-icon> 前往导航
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw } from 'vue'
import { serviceApi } from '@/api'
import { ElMessage } from 'element-plus'

const currentCategory = ref('')
const searchKeyword = ref('')
const sortBy = ref('distance')
const services = ref([])
const categories = ref([
  { value: '', label: '全部', icon: markRaw('Grid') },
  { value: 'hospital', label: '宠物医院', icon: markRaw('Plus') },
  { value: 'grooming', label: '美容店', icon: markRaw('MagicStick') },
  { value: 'boarding', label: '寄养中心', icon: markRaw('HomeFilled') },
  { value: 'training', label: '训练学校', icon: markRaw('Medal') },
  { value: 'shop', label: '用品商店', icon: markRaw('Goods') }
])
const showDetailDialog = ref(false)
const selectedService = ref(null)

const filteredServices = computed(() => {
  let result = [...services.value]

  if (currentCategory.value) {
    result = result.filter(s => s.category === currentCategory.value)
  }

  if (searchKeyword.value) {
    result = result.filter(s =>
      s.name.includes(searchKeyword.value) ||
      s.address?.includes(searchKeyword.value)
    )
  }

  if (sortBy.value === 'distance') {
    result.sort((a, b) => (a.distance || 999) - (b.distance || 999))
  } else if (sortBy.value === 'rating') {
    result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
  } else if (sortBy.value === 'price') {
    result.sort((a, b) => {
      const aPrice = parseInt(a.price_range) || 9999
      const bPrice = parseInt(b.price_range) || 9999
      return aPrice - bPrice
    })
  }

  return result
})

function formatBusinessHours(hours) {
  if (typeof hours === 'string') return hours
  if (typeof hours === 'object' && hours !== null) {
    return Object.entries(hours).map(([k, v]) => `${k}: ${v}`).join('，')
  }
  return ''
}

function getCategoryType(category) {
  const types = {
    hospital: 'danger',
    grooming: 'success',
    boarding: 'warning',
    training: 'primary',
    shop: 'info'
  }
  return types[category] || 'info'
}

function getCategoryLabel(category) {
  const labels = {
    hospital: '宠物医院',
    grooming: '美容店',
    boarding: '寄养中心',
    training: '训练学校',
    shop: '用品商店'
  }
  return labels[category] || category
}

async function loadServices() {
  try {
    services.value = await serviceApi.getServices()
  } catch (e) {
    ElMessage.error('加载服务失败')
  }
}

async function seedServices() {
  try {
    await serviceApi.seedServices()
    ElMessage.success('数据初始化成功')
    loadServices()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '初始化失败')
  }
}

function viewServiceDetail(service) {
  selectedService.value = service
  showDetailDialog.value = true
}

function callService(service) {
  if (service.phone) {
    window.open(`tel:${service.phone}`)
  }
}

function navigateTo(service) {
  if (service.address) {
    window.open(`https://maps.google.com/?q=${encodeURIComponent(service.address)}`)
  }
}

onMounted(() => {
  loadServices()
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

.mt-15 {
  margin-top: 15px;
}

.mt-20 {
  margin-top: 20px;
}

.mb-10 {
  margin-bottom: 10px;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  border: 2px solid transparent;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);

  &:hover {
    border-color: #409EFF;
    transform: translateY(-2px);
  }

  &.active {
    border-color: #409EFF;
    background: #ecf5ff;
  }

  .category-name {
    margin-top: 10px;
    font-size: 14px;
    color: #606266;
  }
}

.service-card {
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .service-header {
    display: flex;
    gap: 16px;

    .service-image {
      width: 120px;
      height: 120px;
      object-fit: cover;
      border-radius: 8px;
      flex-shrink: 0;
    }

    .service-info {
      flex: 1;
      min-width: 0;

      .service-name {
        margin: 0 0 8px;
        font-size: 18px;
      }

      .service-rating {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;

        .rating-text {
          color: #E6A23C;
          font-weight: 500;
        }

        .review-count {
          color: #909399;
          font-size: 12px;
        }
      }

      .service-address,
      .service-distance,
      .service-phone {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #606266;
        font-size: 13px;
        margin-bottom: 5px;
      }
    }
  }

  .service-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .service-description {
    color: #606266;
    font-size: 13px;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .service-hours,
  .service-price {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #606266;
    font-size: 13px;
  }

  .service-actions {
    .action-buttons {
      display: flex;
      gap: 10px;
    }
  }
}

.detail-header {
  display: flex;
  gap: 20px;

  .detail-image {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .detail-info {
    flex: 1;

    h2 {
      margin: 0 0 10px;
    }

    .detail-rating {
      display: flex;
      align-items: center;
      gap: 10px;

      .rating-text {
        color: #E6A23C;
        font-weight: 500;
      }

      .review-count {
        color: #909399;
      }
    }
  }
}

.description {
  line-height: 1.8;
  color: #606266;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

:deep(.el-descriptions__label) {
  width: 100px;
}
</style>
