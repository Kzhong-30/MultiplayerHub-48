<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">宠物百科</h2>
    </div>

    <el-tabs v-model="activeTab" class="encyclopedia-tabs">
      <el-tab-pane label="品种大全" name="breeds">
        <div class="flex-between mb-20">
          <el-radio-group v-model="speciesFilter" size="large">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="dog">狗狗</el-radio-button>
            <el-radio-button value="cat">猫咪</el-radio-button>
          </el-radio-group>
          <el-input
            v-model="searchKeyword"
            placeholder="搜索品种..."
            style="width: 250px"
            clearable
          >
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>

        <el-row :gutter="20">
          <el-col :span="6" v-for="breed in filteredBreeds" :key="breed.id">
            <el-card class="breed-card card-shadow cursor-pointer" @click="viewBreed(breed.id)">
              <div class="breed-image">
                <img :src="breed.image_url" :alt="breed.name" />
              </div>
              <div class="breed-info">
                <h3 class="breed-name">{{ breed.name }}</h3>
                <div class="breed-meta">
                  <el-tag size="small" :type="breed.species === 'dog' ? 'primary' : 'success'">
                    {{ breed.species === 'dog' ? '狗狗' : '猫咪' }}
                  </el-tag>
                  <span class="lifespan">{{ breed.lifespan }}</span>
                </div>
                <p class="breed-temperament text-ellipsis">{{ breed.temperament }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="filteredBreeds.length === 0" description="暂无数据" />
      </el-tab-pane>

      <el-tab-pane label="疾病自查" name="diseases">
        <div class="flex-between mb-20">
          <el-select v-model="severityFilter" placeholder="严重程度" style="width: 150px" clearable>
            <el-option label="轻微" value="low" />
            <el-option label="中等" value="moderate" />
            <el-option label="严重" value="high" />
          </el-select>
          <el-input
            v-model="diseaseSearch"
            placeholder="搜索疾病名称或症状..."
            style="width: 300px"
            clearable
          >
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>

        <el-row :gutter="20">
          <el-col :span="12" v-for="disease in filteredDiseases" :key="disease.id">
            <el-card class="disease-card card-shadow cursor-pointer" @click="viewDisease(disease.id)">
              <div class="disease-header flex-between">
                <h3 class="disease-name">{{ disease.name }}</h3>
                <el-tag :type="getSeverityType(disease.severity)" size="small">
                  {{ getSeverityText(disease.severity) }}
                </el-tag>
              </div>
              <div class="disease-species" v-if="disease.species">
                <el-icon color="#909399"><PawPrint /></el-icon>
                <span>{{ disease.species }}</span>
              </div>
              <div class="disease-symptoms">
                <span class="label">常见症状：</span>
                <span class="symptoms">{{ disease.symptoms }}</span>
              </div>
              <div class="disease-footer flex-between">
                <span class="more">查看详情 <el-icon><ArrowRight /></el-icon></span>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-empty v-if="filteredDiseases.length === 0" description="暂无数据" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { encyclopediaApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const activeTab = ref('breeds')
const breeds = ref([])
const diseases = ref([])
const speciesFilter = ref('')
const searchKeyword = ref('')
const severityFilter = ref('')
const diseaseSearch = ref('')

const filteredBreeds = computed(() => {
  return breeds.value.filter(b => {
    const matchSpecies = !speciesFilter.value || b.species === speciesFilter.value
    const matchSearch = !searchKeyword.value ||
      b.name.includes(searchKeyword.value) ||
      b.breed?.includes(searchKeyword.value)
    return matchSpecies && matchSearch
  })
})

const filteredDiseases = computed(() => {
  return diseases.value.filter(d => {
    const matchSeverity = !severityFilter.value || d.severity === severityFilter.value
    const matchSearch = !diseaseSearch.value ||
      d.name.includes(diseaseSearch.value) ||
      d.symptoms?.includes(diseaseSearch.value)
    return matchSeverity && matchSearch
  })
})

function getSeverityType(severity) {
  const types = { low: 'success', moderate: 'warning', high: 'danger' }
  return types[severity] || 'info'
}

function getSeverityText(severity) {
  const texts = { low: '轻微', moderate: '中等', high: '严重' }
  return texts[severity] || severity
}

function viewBreed(id) {
  router.push(`/encyclopedia/breed/${id}`)
}

function viewDisease(id) {
  router.push(`/encyclopedia/disease/${id}`)
}

async function loadData() {
  try {
    const [breedsRes, diseasesRes] = await Promise.all([
      encyclopediaApi.getBreeds(),
      encyclopediaApi.getDiseases()
    ])
    breeds.value = breedsRes
    diseases.value = diseasesRes
  } catch (e) {
    ElMessage.error('加载数据失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
}

.encyclopedia-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
}

.breed-card {
  transition: all 0.3s;
  overflow: hidden;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .breed-image {
    height: 180px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s;
    }
  }

  &:hover .breed-image img {
    transform: scale(1.05);
  }

  .breed-info {
    padding: 15px;

    .breed-name {
      margin: 0 0 8px;
      font-size: 16px;
    }

    .breed-meta {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;

      .lifespan {
        color: #909399;
        font-size: 12px;
      }
    }

    .breed-temperament {
      color: #606266;
      font-size: 13px;
      line-height: 1.5;
    }
  }
}

.disease-card {
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .disease-header {
    margin-bottom: 10px;

    .disease-name {
      margin: 0;
      font-size: 16px;
    }
  }

  .disease-species {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #606266;
    font-size: 13px;
    margin-bottom: 10px;
  }

  .disease-symptoms {
    margin-bottom: 12px;
    font-size: 13px;
    line-height: 1.6;

    .label {
      color: #909399;
    }

    .symptoms {
      color: #606266;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }

  .disease-footer {
    .more {
      color: #409EFF;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 3px;
    }
  }
}
</style>
