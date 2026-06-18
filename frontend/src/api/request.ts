import axios, { AxiosError, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error: AxiosError) => {
    const data = error.response?.data as any
    const msg = data?.detail || error.message || '请求失败'
    ElMessage.error(String(msg))
    return Promise.reject(error)
  }
)

export default request
