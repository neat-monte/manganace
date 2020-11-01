import endpoints from './endpoints'
import { fetchAsync, methods } from './base'

export const getAll = async () => {
  return await fetchAsync(endpoints.tags, methods.GET);
}

export const create = async (data) => {
  return await fetchAsync(endpoints.tags, methods.POST, data);
}

export const update = async (id, data) => {
  const endpoint = `${endpoints.tags}/${id}`
  return await fetchAsync(endpoint, methods.PUT, data);
}

export const remove = async (id) => {
  const endpoint = `${endpoints.tags}/${id}`
  return await fetchAsync(endpoint, methods.DELETE);
}