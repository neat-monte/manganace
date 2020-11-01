import endpoints from './endpoints'
import { fetchAsync, methods } from './base'

export const getAllWithoutRelations = async () => {
  return await fetchAsync(endpoints.collections, methods.GET);
}

export const create = async (data) => {
  return await fetchAsync(endpoints.collections, methods.POST, data);
}

export const update = async (id, data) => {
  const endpoint = `${endpoints.collections}/${id}`
  return await fetchAsync(endpoint, methods.PUT, data);
}

export const destroy = async (id) => {
  const endpoint = `${endpoints.collections}/${id}`;
  return await fetchAsync(endpoint, methods.DELETE);
}