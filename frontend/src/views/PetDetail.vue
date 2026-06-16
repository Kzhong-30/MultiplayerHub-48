<template>
  <div class="page-container">
    <div v-if="pet" class="pet-detail">
      <div class="flex-between mb-20">
        <div class="flex-center" style="gap: 15px">
          <el-button @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
          </el-button>
          <h2 class="page-title">{{ pet.name }} 的档案</h2>
        </div>
      </div>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="card-shadow mb-20">
            <div class="pet-avatar-section text-center">
              <el-avatar :size="150" :src="pet.avatar" shape="square">
                {{ pet.name[0] }}
              </el-avatar>
              <h2 class="pet-name">{{ pet.name }}</h2>
              <div class="pet-tags mt-20">
                <el-tag :type="pet.species === 'dog' ? 'primary' : 'success'">
                  {{ pet.species === 'dog' ? '狗狗' : '猫咪' }}
                </el-tag>
                <el-tag type="info">{{ pet.breed }}</el-tag>
                <el-tag :type="pet.gender === 'male' ? 'warning' : 'danger'">
                  {{ pet.gender === 'male' ? '公' : '母' }}
                </el-tag>
              </div>
            </div>
            <el-descriptions :column="1" border class="mt-20">
              <el-descriptions-item label="生日">{{ pet.birthday || '--' }}</el-descriptions-item>
              <el-descriptions-item label="年龄">{{ getAge(pet.birthday) }}</el-descriptions-item>
              <el-descriptions-item label="体重">{{ pet.weight || '--' }} kg</el-descriptions-item>
              <el-descriptions-item label="简介">{{ pet.bio || '暂无' }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <el-card class="card-shadow">
            <template #header>
              <div class="flex-between">
                <span>快捷操作</span>
              </div>
            </template>
            <div class="quick-actions">
              <el-button type="primary" @click="showWeightDialog = true" style="width: 100%; margin-bottom: 10px">
                <el-icon><TrendCharts /></el-icon> 记录体重
              </el-button>
              <el-button type="success" @click="showVaccineDialog = true" style="width: 100%; margin-bottom: 10px">
                <el-icon><FirstAidKit /></el-icon> 接种疫苗
              </el-button>
              <el-button type="warning" @click="showPhotoDialog = true" style="width: 100%">
                <el-icon><Picture /></el-icon> 添加照片
              </el-button>
            </div>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-tabs v-model="activeTab" class="detail-tabs">
            <el-tab-pane label="体重曲线" name="weight">
              <el-card class="card-shadow">
                <div v-if="pet.weight_records?.length > 0">
                  <v-chart :option="weightChartOption" style="height: 400px" autoresize />
                </div>
                <el-empty v-else description="暂无体重记录">
                  <el-button type="primary" @click="showWeightDialog = true">记录第一次体重</el-button>
                </el-empty>
              </el-card>
            </el-tab-pane>

            <el-tab-pane label="疫苗接种" name="vaccine">
              <el-card class="card-shadow">
                <div v-if="pet.vaccine_records?.length > 0" class="vaccine-timeline">
                  <el-timeline>
                    <el-timeline-item
                      v-for="record in sortedVaccineRecords"
                      :key="record.id"
                      :timestamp="formatDate(record.vaccine_date)"
                      :type="getVaccineType(record)"
                    >
                      <el-card shadow="hover">
                        <h4>{{ record.vaccine_name }}</h4>
                        <p>接种医院：{{ record.hospital || '--' }}</p>
                        <p v-if="record.next_due_date">下次接种：{{ record.next_due_date }}</p>
                        <p v-if="record.note">备注：{{ record.note }}</p>
                      </el-card>
                    </el-timeline-item>
                  </el-timeline>
                </div>
                <el-empty v-else description="暂无疫苗记录">
                  <el-button type="primary" @click="showVaccineDialog = true">添加第一次疫苗</el-button>
                </el-empty>
              </el-card>
            </el-tab-pane>

            <el-tab-pane label="专属相册" name="photos">
              <el-card class="card-shadow">
                <div v-if="pet.photos?.length > 0" class="photo-gallery">
                  <el-row :gutter="12">
                    <el-col :span="8" v-for="photo in pet.photos" :key="photo.id">
                      <div class="photo-item">
                        <el-image :src="photo.url" :preview-src-list="[photo.url]" fit="cover" style="width: 100%; height: 180px" />
                        <div class="photo-info flex-between">
                          <span class="photo-desc text-ellipsis">{{ photo.description || '暂无描述' }}</span>
                          <el-tag v-if="photo.is_avatar" size="small" type="success">头像</el-tag>
                        </div>
                      </div>
                    </el-col>
                  </el-row>
                </div>
                <el-empty v-else description="暂无照片">
                  <el-button type="primary" @click="showPhotoDialog = true">上传第一张照片</el-button>
                </el-empty>
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>

    <el-dialog v-model="showWeightDialog" title="记录体重" width="400px">
      <el-form :model="weightForm" label-width="80px">
        <el-form-item label="体重">
          <el-input-number v-model="weightForm.weight" :min="0" :precision="1" :step="0.1" />
          <span style="margin-left: 10px; color: #909399">kg</span>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="weightForm.record_date" type="date" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="weightForm.note" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showWeightDialog = false">取消</el-button>
        <el-button type="primary" @click="saveWeight">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showVaccineDialog" title="记录疫苗" width="400px">
      <el-form :model="vaccineForm" label-width="100px">
        <el-form-item label="疫苗名称">
          <el-input v-model="vaccineForm.vaccine_name" placeholder="如：狂犬疫苗" />
        </el-form-item>
        <el-form-item label="接种日期">
          <el-date-picker v-model="vaccineForm.vaccine_date" type="date" style="width: 100%" />
        </el-form-item>
        <el-form-item label="下次日期">
          <el-date-picker v-model="vaccineForm.next_due_date" type="date" style="width: 100%" />
        </el-form-item>
        <el-form-item label="接种医院">
          <el-input v-model="vaccineForm.hospital" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="vaccineForm.note" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showVaccineDialog = false">取消</el-button>
        <el-button type="primary" @click="saveVaccine">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showPhotoDialog" title="添加照片" width="400px">
      <el-form :model="photoForm" label-width="80px">
        <el-form-item label="图片URL">
          <el-input v-model="photoForm.url" placeholder="请输入图片URL" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="photoForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="设为头像">
          <el-switch v-model="photoForm.is_avatar" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPhotoDialog = false">取消</el-button>
        <el-button type="primary" @click="savePhoto">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePetStore } from '@/stores/pet'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent])

const route = useRoute()
const petStore = usePetStore()

const pet = ref(null)
const activeTab = ref('weight')
const showWeightDialog = ref(false)
const showVaccineDialog = ref(false)
const showPhotoDialog = ref(false)

const weightForm = reactive({
  weight: null,
  record_date: new Date(),
  note: ''
})

const vaccineForm = reactive({
  vaccine_name: '',
  vaccine_date: new Date(),
  next_due_date: null,
  hospital: '',
  note: ''
})

const photoForm = reactive({
  url: '',
  description: '',
  is_avatar: false
})

const sortedVaccineRecords = computed(() => {
  if (!pet.value?.vaccine_records) return []
  return [...pet.value.vaccine_records].sort((a, b) =>
    dayjs(b.vaccine_date).valueOf() - dayjs(a.vaccine_date).valueOf()
  )
})

const weightChartOption = computed(() => {
  if (!pet.value?.weight_records) return {}
  const records = [...pet.value.weight_records].sort((a, b) =>
    dayjs(a.record_date).valueOf() - dayjs(b.record_date).valueOf()
  )
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: records.map(r => r.record_date)
    },
    yAxis: {
      type: 'value',
      name: '体重 (kg)'
    },
    series: [{
      name: '体重',
      type: 'line',
      smooth: true,
      data: records.map(r => r.weight),
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64, 158, 255, 0.5)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
          ]
        }
      },
      lineStyle: { color: '#409EFF', width: 3 },
      itemStyle: { color: '#409EFF' }
    }]
  }
})

function getAge(birthday) {
  if (!birthday) return '--'
  const years = dayjs().diff(dayjs(birthday), 'year')
  if (years > 0) return `${years}岁`
  const months = dayjs().diff(dayjs(birthday), 'month')
  return `${months}个月`
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}

function getVaccineType(record) {
  if (record.next_due_date && dayjs().isAfter(dayjs(record.next_due_date))) {
    return 'danger'
  }
  return 'primary'
}

async function saveWeight() {
  if (!weightForm.weight) {
    ElMessage.warning('请输入体重')
    return
  }
  try {
    await petStore.addWeight(pet.value.id, weightForm)
    ElMessage.success('保存成功')
    showWeightDialog.value = false
    weightForm.weight = null
    weightForm.record_date = new Date()
    weightForm.note = ''
    loadPet()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

async function saveVaccine() {
  if (!vaccineForm.vaccine_name) {
    ElMessage.warning('请输入疫苗名称')
    return
  }
  try {
    await petStore.addVaccine(pet.value.id, vaccineForm)
    ElMessage.success('保存成功')
    showVaccineDialog.value = false
    Object.assign(vaccineForm, {
      vaccine_name: '',
      vaccine_date: new Date(),
      next_due_date: null,
      hospital: '',
      note: ''
    })
    loadPet()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

async function savePhoto() {
  if (!photoForm.url) {
    ElMessage.warning('请输入图片URL')
    return
  }
  try {
    await petStore.addPhoto(pet.value.id, photoForm)
    ElMessage.success('保存成功')
    showPhotoDialog.value = false
    Object.assign(photoForm, { url: '', description: '', is_avatar: false })
    loadPet()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

async function loadPet() {
  pet.value = await petStore.fetchPet(route.params.id)
}

onMounted(() => {
  loadPet()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
}

.pet-avatar-section {
  .pet-name {
    font-size: 24px;
    margin: 15px 0 10px;
  }

  .pet-tags {
    display: flex;
    justify-content: center;
    gap: 8px;
  }
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.detail-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
}

.vaccine-timeline {
  padding: 20px 0;
}

.photo-gallery {
  .photo-item {
    margin-bottom: 15px;

    .photo-info {
      padding: 8px;
      background: #f5f7fa;
      border-radius: 0 0 6px 6px;
      font-size: 13px;
    }
  }
}
</style>
