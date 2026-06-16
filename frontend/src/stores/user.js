import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(username, password) {
    const res = await authApi.login(username, password)
    token.value = res.access_token
    localStorage.setItem('token', res.access_token)
    await fetchUserInfo()
    return res
  }

  async function register(data) {
    return await authApi.register(data)
  }

  async function fetchUserInfo() {
    const res = await authApi.getMe()
    userInfo.value = res
    localStorage.setItem('user', JSON.stringify(res))
    return res
  }

  async function updateUserInfo(data) {
    const res = await authApi.updateMe(data)
    userInfo.value = res
    localStorage.setItem('user', JSON.stringify(res))
    return res
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    updateUserInfo,
    logout
  }
})
