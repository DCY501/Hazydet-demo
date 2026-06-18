import request from './request'

export function detectImage(formData: FormData) {
  return request.post('/detect', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function compareModels(formData: FormData) {
  return request.post('/compare', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getIntermediate(formData: FormData) {
  return request.post('/intermediate', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function detectVideo(formData: FormData) {
  return request.post('/video', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 600000,
  })
}

export function addHaze(formData: FormData) {
  return request.post('/haze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
