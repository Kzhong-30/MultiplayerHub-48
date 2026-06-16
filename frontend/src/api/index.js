import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (username, password) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    return request.post('/auth/login', formData)
  },
  register: data => request.post('/auth/register', data),
  getMe: () => request.get('/auth/me'),
  updateMe: data => request.put('/auth/me', data)
}

export const petApi = {
  getPets: () => request.get('/pets'),
  getPet: id => request.get(`/pets/${id}`),
  createPet: data => request.post('/pets', data),
  updatePet: (id, data) => request.put(`/pets/${id}`, data),
  deletePet: id => request.delete(`/pets/${id}`),
  addWeight: (id, data) => request.post(`/pets/${id}/weight`, data),
  addVaccine: (id, data) => request.post(`/pets/${id}/vaccine`, data),
  addPhoto: (id, data) => request.post(`/pets/${id}/photos`, data),
  deletePhoto: (petId, photoId) => request.delete(`/pets/${petId}/photos/${photoId}`)
}

export const postApi = {
  getPosts: (params = {}) => request.get('/posts', { params }),
  getPost: id => request.get(`/posts/${id}`),
  createPost: data => request.post('/posts', data),
  updatePost: (id, data) => request.put(`/posts/${id}`, data),
  deletePost: id => request.delete(`/posts/${id}`),
  likePost: id => request.post(`/posts/${id}/like`),
  getUserPosts: (userId, params = {}) => request.get(`/posts/user/${userId}`, { params })
}

export const commentApi = {
  getComments: postId => request.get(`/comments/post/${postId}`),
  createComment: data => request.post('/comments', data),
  deleteComment: id => request.delete(`/comments/${id}`)
}

export const matchApi = {
  getRecommendations: () => request.get('/matches/recommendations'),
  createMatch: data => request.post('/matches', data),
  getSentMatches: () => request.get('/matches/sent'),
  getReceivedMatches: () => request.get('/matches/received'),
  acceptMatch: id => request.put(`/matches/${id}/accept`),
  rejectMatch: id => request.put(`/matches/${id}/reject`)
}

export const encyclopediaApi = {
  getBreeds: (params = {}) => request.get('/encyclopedia/breeds', { params }),
  getBreed: id => request.get(`/encyclopedia/breeds/${id}`),
  getDiseases: (params = {}) => request.get('/encyclopedia/diseases', { params }),
  getDisease: id => request.get(`/encyclopedia/diseases/${id}`)
}

export const nearbyApi = {
  getNearbyPets: (params = {}) => request.get('/nearby/pets', { params }),
  getNearbyMeetups: (params = {}) => request.get('/nearby/meetups', { params }),
  createMeetup: data => request.post('/nearby/meetups', data),
  getMeetup: id => request.get(`/nearby/meetups/${id}`),
  joinMeetup: (id, petId) => request.post(`/nearby/meetups/${id}/join`, null, { params: { pet_id: petId } }),
  leaveMeetup: id => request.delete(`/nearby/meetups/${id}/join`)
}

export const serviceApi = {
  getServices: (params = {}) => request.get('/services', { params }),
  getServiceCategories: () => request.get('/services/categories'),
  getService: id => request.get(`/services/${id}`),
  seedServices: () => request.post('/services/seed')
}

export default request
