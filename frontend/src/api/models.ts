import request from './request'

export function getModels() {
  return request.get('/detect/models')
}
