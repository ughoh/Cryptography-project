import { ref, computed } from 'vue'
import axios from 'axios'

export function useCrypto() {
  const mode = ref('encrypt')
  const file = ref(null)
  const password = ref('')
  const loading = ref(false)
  const error = ref('')
  const isDragging = ref(false)

  const buttonText = computed(() => {
    if (loading.value) return 'Processing...'
    return mode.value === 'encrypt' ? 'Encrypt File' : 'Decrypt File'
  })

  const setMode = (newMode) => {
    mode.value = newMode
    error.value = ''
  }

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files.length > 0) {
      file.value = event.target.files[0]
    }
  }

  const handleFileDrop = (event) => {
    isDragging.value = false
    error.value = ''

    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      file.value = event.dataTransfer.files[0]
    }
  }

  const submitForm = async () => {
    if (!file.value || !password.value) return
    loading.value = true
    error.value = ''

    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('password', password.value)

    const endpoint = mode.value === 'encrypt' ? '/api/v1/encrypt' : '/api/v1/decrypt'

    try {
      const response = await axios.post(endpoint, formData, { responseType: 'blob' })
      const contentDisposition = response.headers['content-disposition']
      let filename = mode.value === 'encrypt' ? 'file.enc' : 'decoded_file'

      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename\*=UTF-8''(.+)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = decodeURIComponent(filenameMatch[1])
        }
      }

      const blob = new Blob([response.data], { type: response.headers['content-type'] })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = filename
      link.click()
      URL.revokeObjectURL(link.href)
    } catch (err) {
      console.error(err)

      if (err.response) {
        const status = err.response.status

        if (status === 422) {
          error.value = 'Password is too short (minimum 8 characters).'
        } else if (status === 400) {
          error.value = 'Incorrect password or the file is corrupted.'
        } else {
          error.value = 'Server error. Please try again later.'
        }

      } else {
        error.value = 'Network error. Server is unreachable.'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    mode,
    file,
    password,
    loading,
    error,
    isDragging,
    buttonText,
    setMode,
    handleFileChange,
    handleFileDrop,
    submitForm
  }
}