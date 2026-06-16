<template>
  <div class="page-container">
    <div class="flex-between mb-20">
      <h2 class="page-title">动态广场</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Edit /></el-icon> 发布动态
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="18">
        <el-card v-for="post in posts" :key="post.id" class="card-shadow mb-20 post-card">
          <div class="post-header">
            <el-avatar :size="44" :src="post.author?.avatar">
              {{ post.author?.username?.[0]?.toUpperCase() }}
            </el-avatar>
            <div class="post-author-info">
              <div class="post-author">{{ post.author?.username }}</div>
              <div class="post-meta">
                <span>{{ formatDate(post.created_at) }}</span>
                <span v-if="post.location_name" class="location">
                  <el-icon><Location /></el-icon> {{ post.location_name }}
                </span>
              </div>
            </div>
          </div>

          <div class="post-content">{{ post.content }}</div>

          <div v-if="post.media_url" class="post-media">
            <img v-if="post.media_type === 'image'" :src="post.media_url" alt="" @click="previewImage(post.media_url)" />
            <video v-else-if="post.media_type === 'video'" :src="post.media_url" controls />
          </div>

          <div class="post-tags" v-if="post.tags?.length">
            <el-tag v-for="tag in post.tags" :key="tag" size="small" type="info" effect="plain" class="cursor-pointer" @click="filterByTag(tag)">
              #{{ tag }}
            </el-tag>
          </div>

          <div v-if="post.pet" class="post-pet">
            <el-tag type="success" effect="light">
              <el-avatar :size="20" :src="post.pet.avatar">{{ post.pet.name[0] }}</el-avatar>
              {{ post.pet.name }}
            </el-tag>
          </div>

          <div class="post-actions flex-between">
            <div class="action-group">
              <span class="action-item cursor-pointer" :class="{ active: post.is_liked }" @click="toggleLike(post)">
                <el-icon>{{ post.is_liked ? 'StarFilled' : 'Star' }}</el-icon>
                <span>{{ post.likes_count }}</span>
              </span>
              <span class="action-item cursor-pointer" @click="showComments(post)">
                <el-icon><ChatDotRound /></el-icon>
                <span>{{ post.comments_count }}</span>
              </span>
            </div>
          </div>

          <div v-if="showCommentsPostId === post.id" class="comments-section">
            <el-input
              v-model="commentContent"
              placeholder="发表评论..."
              @keyup.enter="submitComment(post.id)"
            >
              <template #append>
                <el-button @click="submitComment(post.id)">发送</el-button>
              </template>
            </el-input>
            <div class="comments-list mt-20" v-if="postComments.length > 0">
              <div v-for="comment in postComments" :key="comment.id" class="comment-item">
                <el-avatar :size="32" :src="comment.author?.avatar">
                  {{ comment.author?.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <div class="comment-content">
                  <div class="comment-header">
                    <span class="comment-author">{{ comment.author?.username }}</span>
                    <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <p>{{ comment.content }}</p>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <div v-if="loading" class="text-center mb-20">
          <el-icon :size="32" class="is-loading"><Loading /></el-icon>
        </div>

        <div v-if="hasMore && !loading" class="text-center">
          <el-button @click="loadMore">加载更多</el-button>
        </div>
      </el-col>

      <el-col :span="6">
        <el-card class="card-shadow mb-20">
          <template #header>
            <span class="card-title">热门话题</span>
          </template>
          <div class="hot-tags">
            <el-tag v-for="tag in hotTags" :key="tag.name" size="large" effect="plain" class="mb-10 cursor-pointer" @click="filterByTag(tag.name)">
              #{{ tag.name }}
              <span class="tag-count">{{ tag.count }}</span>
            </el-tag>
          </div>
        </el-card>

        <el-card class="card-shadow">
          <template #header>
            <span class="card-title">推荐用户</span>
          </template>
          <div class="recommend-users">
            <div v-for="user in recommendUsers" :key="user.id" class="user-item flex-between">
              <div class="flex-center" style="gap: 10px">
                <el-avatar :src="user.avatar">{{ user.username?.[0]?.toUpperCase() }}</el-avatar>
                <div>
                  <div class="username">{{ user.username }}</div>
                  <div class="user-bio text-ellipsis">{{ user.bio || '暂无简介' }}</div>
                </div>
              </div>
              <el-button size="small" type="primary" plain @click="followUser(user)">关注</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showCreateDialog" title="发布动态" width="600px">
      <el-form :model="postForm" label-width="80px">
        <el-form-item label="内容">
          <el-input v-model="postForm.content" type="textarea" :rows="4" placeholder="分享你的养宠日常..." />
        </el-form-item>
        <el-form-item label="话题标签">
          <el-select v-model="postForm.tags" multiple allow-create filterable placeholder="选择或输入话题">
            <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联宠物">
          <el-select v-model="postForm.pet_id" placeholder="选择宠物（可选）">
            <el-option v-for="pet in pets" :key="pet.id" :label="pet.name" :value="pet.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="媒体类型">
          <el-radio-group v-model="postForm.media_type">
            <el-radio value="image">图片</el-radio>
            <el-radio value="video">视频</el-radio>
            <el-radio value="none">无</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="postForm.media_type !== 'none'" label="媒体URL">
          <el-input v-model="postForm.media_url" placeholder="请输入图片或视频URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createPost">发布</el-button>
      </template>
    </el-dialog>

    <el-image-viewer v-if="previewUrl" :url-list="[previewUrl]" @close="previewUrl = ''" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { usePetStore } from '@/stores/pet'
import { postApi, commentApi } from '@/api'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

const petStore = usePetStore()

const posts = ref([])
const pets = ref([])
const loading = ref(false)
const hasMore = ref(true)
const skip = ref(0)
const currentTag = ref('')
const showCreateDialog = ref(false)
const showCommentsPostId = ref(null)
const postComments = ref([])
const commentContent = ref('')
const previewUrl = ref('')

const hotTags = ref([
  { name: '日常', count: 128 },
  { name: '萌宠', count: 96 },
  { name: '遛狗', count: 75 },
  { name: '猫咪', count: 89 },
  { name: '训练', count: 45 },
  { name: '美容', count: 38 },
  { name: '健康', count: 52 }
])

const allTags = ['日常', '萌宠', '搞笑', '遛狗', '猫咪', '训练', '美容', '健康', '饮食', '医疗', '出行', '用品']

const recommendUsers = ref([
  { id: 2, username: 'catfan', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100', bio: '猫咪爱好者' },
  { id: 3, username: 'dogdad', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100', bio: '哈士奇铲屎官' }
])

const postForm = reactive({
  content: '',
  tags: [],
  pet_id: null,
  media_type: 'image',
  media_url: 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600'
})

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function previewImage(url) {
  previewUrl.value = url
}

function filterByTag(tag) {
  currentTag.value = tag
  posts.value = []
  skip.value = 0
  hasMore.value = true
  loadPosts()
}

async function loadPosts() {
  loading.value = true
  try {
    const params = { skip: skip.value, limit: 10 }
    if (currentTag.value) params.tag = currentTag.value
    const res = await postApi.getPosts(params)
    if (res.length < 10) hasMore.value = false
    posts.value = [...posts.value, ...res]
    skip.value += 10
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function loadMore() {
  loadPosts()
}

async function toggleLike(post) {
  try {
    const res = await postApi.likePost(post.id)
    post.is_liked = res.liked
    post.likes_count = res.likes_count
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function showComments(post) {
  if (showCommentsPostId.value === post.id) {
    showCommentsPostId.value = null
    postComments.value = []
  } else {
    showCommentsPostId.value = post.id
    postComments.value = await commentApi.getComments(post.id)
  }
}

async function submitComment(postId) {
  if (!commentContent.value.trim()) return
  try {
    await commentApi.createComment({ post_id: postId, content: commentContent.value })
    ElMessage.success('评论成功')
    commentContent.value = ''
    postComments.value = await commentApi.getComments(postId)
    const post = posts.value.find(p => p.id === postId)
    if (post) post.comments_count++
  } catch (e) {
    ElMessage.error('评论失败')
  }
}

async function createPost() {
  if (!postForm.content.trim()) {
    ElMessage.warning('请输入动态内容')
    return
  }
  try {
    await postApi.createPost(postForm)
    ElMessage.success('发布成功')
    showCreateDialog.value = false
    Object.assign(postForm, {
      content: '',
      tags: [],
      pet_id: null,
      media_type: 'image',
      media_url: 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600'
    })
    posts.value = []
    skip.value = 0
    hasMore.value = true
    loadPosts()
  } catch (e) {
    ElMessage.error('发布失败')
  }
}

function followUser(user) {
  ElMessage.success(`已关注 ${user.username}`)
}

onMounted(async () => {
  pets.value = await petStore.fetchPets()
  loadPosts()
})
</script>

<style scoped lang="scss">
.page-title {
  font-size: 24px;
  font-weight: 500;
}

.card-title {
  font-weight: 500;
}

.post-card {
  .post-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;

    .post-author-info {
      .post-author {
        font-weight: 500;
        margin-bottom: 2px;
      }
      .post-meta {
        color: #909399;
        font-size: 12px;
        display: flex;
        gap: 15px;
        align-items: center;

        .location {
          display: flex;
          align-items: center;
          gap: 3px;
        }
      }
    }
  }

  .post-content {
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 15px;
  }

  .post-media {
    margin-bottom: 15px;

    img {
      max-height: 400px;
      border-radius: 8px;
      cursor: pointer;
    }
    video {
      max-height: 400px;
      border-radius: 8px;
    }
  }

  .post-tags {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
  }

  .post-pet {
    margin-bottom: 15px;
  }

  .post-actions {
    padding-top: 15px;
    border-top: 1px solid #ebeef5;

    .action-group {
      display: flex;
      gap: 30px;

      .action-item {
        display: flex;
        align-items: center;
        gap: 5px;
        color: #909399;
        transition: color 0.3s;

        &.active, &:hover {
          color: #409EFF;
        }
      }
    }
  }

  .comments-section {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    .comment-item {
      display: flex;
      gap: 10px;
      margin-bottom: 15px;

      .comment-content {
        flex: 1;
        background: #f5f7fa;
        padding: 10px 12px;
        border-radius: 8px;

        .comment-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 5px;

          .comment-author {
            font-weight: 500;
          }
          .comment-time {
            color: #909399;
            font-size: 12px;
          }
        }

        p {
          margin: 0;
          color: #606266;
        }
      }
    }
  }
}

.hot-tags {
  .mb-10 {
    margin-bottom: 10px;
    margin-right: 8px;

    .tag-count {
      margin-left: 8px;
      color: #909399;
      font-size: 12px;
    }
  }
}

.recommend-users {
  .user-item {
    padding: 12px 0;
    border-bottom: 1px solid #ebeef5;

    &:last-child {
      border-bottom: none;
    }

    .username {
      font-weight: 500;
    }

    .user-bio {
      color: #909399;
      font-size: 12px;
      max-width: 120px;
    }
  }
}
</style>
