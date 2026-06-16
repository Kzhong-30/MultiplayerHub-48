<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">宠物档案</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon> 添加宠物
      </el-button>
    </div>

    <el-row :gutter="20" v-if="pets.length > 0">
      <el-col :span="8" v-for="pet in pets" :key="pet.id">
        <el-card class="pet-card card-shadow cursor-pointer" @click="viewPetDetail(pet)">
          <div class="pet-header">
            <el-avatar :size="100" :src="pet.avatar" shape="square">
              {{ pet.name[0] }}
            </el-avatar>
            <div class="pet-actions">
              <el-button size="small" type="primary" @click.stop="editPet(pet)">
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button size="small" type="danger" @click.stop="deletePet(pet)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="pet-body">
            <h3 class="pet-name">{{ pet.name }}</h3>
            <div class="pet-tags">
              <el-tag size="small" :type="pet.species === 'dog' ? 'primary' : 'success'">
                {{ pet.species === 'dog' ? '狗狗' : '猫咪' }}
              </el-tag>
              <el-tag size="small" type="info">{{ pet.breed }}</el-tag>
              <el-tag size="small" :type="pet.gender === 'male' ? 'warning' : 'danger'">
                {{ pet.gender === 'male' ? '公' : '母' }}
              </el-tag>
            </div>
            <div class="pet-stats">
              <div class="stat">
                <span class="stat-label">体重</span>
                <span class="stat-value">{{ pet.weight || '--' }} kg</span>
              </div>
              <div class="stat">
                <span class="stat-label">生日</span>
                <span class="stat-value">{{ pet.birthday || '--' }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">年龄</span>
                <span class="stat-value">{{ getAge(pet.birthday) }}</span>
              </div>
            </div>
            <div class="pet-bio" v-if="pet.bio">{{ pet.bio }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-else description="还没有添加宠物档案">
      <el-button type="primary" @click="showCreateDialog = true">添加第一只宠物</el-button>
    </el-empty>

    <el-dialog v-model="showCreateDialog" :title="isEditing ? '编辑宠物' : '添加宠物'" width="600px">
      <el-form ref="petFormRef" :model="petForm" :rules="petRules" label-width="80px">
        <el-form-item label="昵称" prop="name">
          <el-input v-model="petForm.name" placeholder="宠物昵称" />
        </el-form-item>
        <el-form-item label="物种" prop="species">
          <el-select v-model="petForm.species" placeholder="选择物种" style="width: 100%">
            <el-option label="狗狗" value="dog" />
            <el-option label="猫咪" value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="品种" prop="breed">
          <el-input v-model="petForm.breed" placeholder="如：金毛寻回犬" />
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="petForm.gender">
            <el-radio value="male">公</el-radio>
            <el-radio value="female">母</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="生日">
          <el-date-picker v-model="petForm.birthday" type="date" placeholder="选择生日" style="width: 100%" />
        </el-form-item>
        <el-form-item label="体重">
          <el-input-number v-model="petForm.weight" :min="0" :precision="1" :step="0.1" />
          <span style="margin-left: 10px; color: #909399">kg</span>
        </el-form-item>
        <el-form-item label="头像">
          <el-input v-model="petForm.avatar" placeholder="头像图片URL" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="petForm.bio" type="textarea" :rows="3" placeholder="宠物简介" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="savePet">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePetStore } from '@/stores/pet'
import dayjs from 'dayjs'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const petStore = usePetStore()

const pets = ref([])
const showCreateDialog = ref(false)
const isEditing = ref(false)
const editingPetId = ref(null)
const petFormRef = ref()

const petForm = reactive({
  name: '',
  species: '',
  breed: '',
  gender: 'male',
  birthday: null,
  weight: null,
  avatar: '',
  bio: ''
})

const petRules = {
  name: [{ required: true, message: '请输入宠物昵称', trigger: 'blur' }],
  species: [{ required: true, message: '请选择物种', trigger: 'change' }],
  breed: [{ required: true, message: '请输入品种', trigger: 'blur' }]
}

function getAge(birthday) {
  if (!birthday) return '--'
  const years = dayjs().diff(dayjs(birthday), 'year')
  if (years > 0) return `${years}岁`
  const months = dayjs().diff(dayjs(birthday), 'month')
  return `${months}个月`
}

function viewPetDetail(pet) {
  router.push(`/pets/${pet.id}`)
}

function editPet(pet) {
  isEditing.value = true
  editingPetId.value = pet.id
  Object.assign(petForm, pet)
  petForm.birthday = pet.birthday ? dayjs(pet.birthday).toDate() : null
  showCreateDialog.value = true
}

function deletePet(pet) {
  ElMessageBox.confirm(`确定要删除 ${pet.name} 的档案吗？`, '提示', {
    type: 'warning',
    confirmButtonText: '删除',
    cancelButtonText: '取消'
  }).then(async () => {
    await petStore.deletePet(pet.id)
    ElMessage.success('删除成功')
    loadPets()
  }).catch(() => {})
}

async function savePet() {
  await petFormRef.value.validate()
  try {
    if (isEditing.value) {
      await petStore.updatePet(editingPetId.value, petForm)
      ElMessage.success('更新成功')
    } else {
      await petStore.createPet(petForm)
      ElMessage.success('添加成功')
    }
    showCreateDialog.value = false
    resetForm()
    loadPets()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

function resetForm() {
  isEditing.value = false
  editingPetId.value = null
  Object.assign(petForm, {
    name: '',
    species: '',
    breed: '',
    gender: 'male',
    birthday: null,
    weight: null,
    avatar: '',
    bio: ''
  })
}

async function loadPets() {
  pets.value = await petStore.fetchPets()
}

onMounted(() => {
  loadPets()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
}

.pet-card {
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .pet-header {
    position: relative;
    text-align: center;
    padding: 20px 0;

    .pet-actions {
      position: absolute;
      top: 10px;
      right: 10px;
      opacity: 0;
      transition: opacity 0.3s;
    }
  }

  &:hover .pet-actions {
    opacity: 1;
  }

  .pet-body {
    .pet-name {
      text-align: center;
      font-size: 20px;
      margin-bottom: 10px;
    }

    .pet-tags {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 15px;
    }

    .pet-stats {
      display: flex;
      justify-content: space-around;
      padding: 15px 0;
      border-top: 1px solid #ebeef5;
      border-bottom: 1px solid #ebeef5;
      margin-bottom: 15px;

      .stat {
        text-align: center;

        .stat-label {
          display: block;
          color: #909399;
          font-size: 12px;
          margin-bottom: 4px;
        }

        .stat-value {
          font-weight: 500;
        }
      }
    }

    .pet-bio {
      color: #606266;
      font-size: 14px;
      line-height: 1.6;
    }
  }
}
</style>
