import { defineStore } from 'pinia'
import { ref } from 'vue'
import { petApi } from '@/api'

export const usePetStore = defineStore('pet', () => {
  const pets = ref([])
  const currentPet = ref(null)

  async function fetchPets() {
    const res = await petApi.getPets()
    pets.value = res
    return res
  }

  async function fetchPet(id) {
    const res = await petApi.getPet(id)
    currentPet.value = res
    return res
  }

  async function createPet(data) {
    const res = await petApi.createPet(data)
    pets.value.push(res)
    return res
  }

  async function updatePet(id, data) {
    const res = await petApi.updatePet(id, data)
    const index = pets.value.findIndex(p => p.id === id)
    if (index !== -1) {
      pets.value[index] = res
    }
    if (currentPet.value?.id === id) {
      currentPet.value = res
    }
    return res
  }

  async function deletePet(id) {
    await petApi.deletePet(id)
    pets.value = pets.value.filter(p => p.id !== id)
    if (currentPet.value?.id === id) {
      currentPet.value = null
    }
  }

  async function addWeight(id, data) {
    const res = await petApi.addWeight(id, data)
    if (currentPet.value?.id === id) {
      currentPet.value.weight_records.push(res)
      currentPet.value.weight = data.weight
    }
    return res
  }

  async function addVaccine(id, data) {
    const res = await petApi.addVaccine(id, data)
    if (currentPet.value?.id === id) {
      currentPet.value.vaccine_records.push(res)
    }
    return res
  }

  async function addPhoto(id, data) {
    const res = await petApi.addPhoto(id, data)
    if (currentPet.value?.id === id) {
      currentPet.value.photos.push(res)
    }
    return res
  }

  function setCurrentPet(pet) {
    currentPet.value = pet
  }

  return {
    pets,
    currentPet,
    fetchPets,
    fetchPet,
    createPet,
    updatePet,
    deletePet,
    addWeight,
    addVaccine,
    addPhoto,
    setCurrentPet
  }
})
