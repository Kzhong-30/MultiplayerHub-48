<template>
  <div class="page-container" v-if="disease">
    <div class="mb-20">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <el-card class="card-shadow mb-20">
      <div class="disease-header">
        <div class="flex-between">
          <h1 class="disease-name">{{ disease.name }}</h1>
          <el-tag :type="getSeverityType(disease.severity)" size="large">
            {{ getSeverityText(disease.severity) }}
          </el-tag>
        </div>
        <div class="disease-meta mt-10" v-if="disease.species">
          <el-icon color="#909399"><Guide /></el-icon>
          <span class="meta-text">适用宠物：{{ disease.species }}</span>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><Warning /></el-icon> 常见症状</span>
          </template>
          <div class="symptoms-list">
            <el-tag v-for="(symptom, index) in symptomsList" :key="index" class="symptom-tag" size="large">
              {{ symptom }}
            </el-tag>
          </div>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><QuestionFilled /></el-icon> 发病原因</span>
          </template>
          <p class="section-content">{{ disease.causes || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span class="section-title"><el-icon><Files /></el-icon> 诊断方法</span>
          </template>
          <p class="section-content">{{ disease.diagnosis || '暂无信息' }}</p>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><FirstAidKit /></el-icon> 治疗方案</span>
          </template>
          <p class="section-content">{{ disease.treatment || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><CircleCheck /></el-icon> 预防措施</span>
          </template>
          <p class="section-content">{{ disease.prevention || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow" v-if="disease.severity === 'high' || disease.severity === 'moderate'">
          <template #header>
            <span class="section-title"><el-icon><InfoFilled /></el-icon> 温馨提示</span>
          </template>
          <div class="tips-content">
            <el-alert
              :title="disease.severity === 'high' ? '此疾病较为严重，发现相关症状请尽快就医，切勿自行用药' : '此疾病需注意观察，如有疑似症状建议及时咨询兽医'"
              type="warning"
              :closable="false"
              show-icon
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
  <el-empty v-else description="加载中..." />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { encyclopediaApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const disease = ref(null)

const symptomsList = computed(() => {
  if (!disease.value?.symptoms) return []
  return disease.value.symptoms.split(/[,，、]/).map(s => s.trim()).filter(Boolean)
})

function getSeverityType(severity) {
  const types = { low: 'success', moderate: 'warning', high: 'danger' }
  return types[severity] || 'info'
}

function getSeverityText(severity) {
  const texts = { low: '轻微', moderate: '中等', high: '严重' }
  return texts[severity] || severity
}

async function loadDisease() {
  try {
    disease.value = await encyclopediaApi.getDisease(route.params.id)
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

onMounted(() => {
  loadDisease()
})
</script>

<style scoped lang="scss">
.disease-header {
  .disease-name {
    margin: 0;
    font-size: 32px;
  }

  .disease-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #606266;
  }

  .meta-text {
    font-size: 14px;
  }
}

.section-title {
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-content {
  line-height: 1.8;
  color: #606266;
  font-size: 14px;
}

.symptoms-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  .symptom-tag {
    padding: 0 16px;
    height: 36px;
    line-height: 34px;
    font-size: 14px;
  }
}

.tips-content {
  :deep(.el-alert__title) {
    line-height: 1.8;
  }
}

.mb-20 {
  margin-bottom: 20px;
}

.mt-10 {
  margin-top: 10px;
}
</style>
