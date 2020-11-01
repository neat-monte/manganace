import endpoints from './endpoints'
import { fetchAsync, methods } from './base'

export const getAll = async () => {
  return await fetchAsync(endpoints.tags, methods.GET);
}

export const create = async (data) => {
  return await fetchAsync(endpoints.tags, methods.POST, data);
}