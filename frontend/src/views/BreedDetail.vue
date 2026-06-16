<template>
  <div class="page-container" v-if="breed">
    <div class="mb-20">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="10">
        <el-card class="card-shadow">
          <img :src="breed.image_url" :alt="breed.name" class="breed-image" />
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card class="card-shadow">
          <div class="breed-header">
            <h1 class="breed-name">{{ breed.name }}</h1>
            <div class="breed-tags">
              <el-tag :type="breed.species === 'dog' ? 'primary' : 'success'">
                {{ breed.species === 'dog' ? '狗狗' : '猫咪' }}
              </el-tag>
              <el-tag type="info">{{ breed.origin || '未知' }}</el-tag>
              <el-tag type="warning">{{ breed.lifespan || '未知' }}</el-tag>
            </div>
          </div>

          <el-descriptions :column="2" border class="mt-20">
            <el-descriptions-item label="体重范围">{{ breed.weight_range || '未知' }}</el-descriptions-item>
            <el-descriptions-item label="身高范围">{{ breed.height_range || '未知' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><User /></el-icon> 性格特点</span>
          </template>
          <p class="section-content">{{ breed.temperament || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><Picture /></el-icon> 外观特征</span>
          </template>
          <p class="section-content">{{ breed.appearance || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span class="section-title"><el-icon><Dish /></el-icon> 喂养指南</span>
          </template>
          <p class="section-content">{{ breed.feeding_guide || '暂无信息' }}</p>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><FirstAidKit /></el-icon> 常见健康问题</span>
          </template>
          <p class="section-content">{{ breed.health_issues || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="section-title"><el-icon><Service /></el-icon> 护理要点</span>
          </template>
          <p class="section-content">{{ breed.care_guide || '暂无信息' }}</p>
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span class="section-title"><el-icon><TrendCharts /></el-icon> 运动需求</span>
          </template>
          <p class="section-content">{{ breed.exercise_needs || '暂无信息' }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
  <el-empty v-else description="加载中..." />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { encyclopediaApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const breed = ref(null)

async function loadBreed() {
  try {
    breed.value = await encyclopediaApi.getBreed(route.params.id)
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

onMounted(() => {
  loadBreed()
})
</script>

<style scoped lang="scss">
.breed-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
}

.breed-header {
  .breed-name {
    margin: 0 0 15px;
    font-size: 32px;
  }

  .breed-tags {
    display: flex;
    gap: 10px;
  }
}

.mt-20 {
  margin-top: 20px;
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
}
</style>
