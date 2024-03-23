import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

http.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

http.interceptors.response.use(
  (response) => {
    const { ok } = response.data
    if (!ok) return Promise.reject(response.data)
    return response.data
  },
  (error) => {
    return Promise.reject(error)
  }
)

export { http }
