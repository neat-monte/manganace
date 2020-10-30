import endpoints from './endpoints'
import { fetchAsync, buildUrlParams, methods } from './base'

export const get = async (id) => {
  const endpoint = `${endpoints.collections}/${id}`;
  return await fetchAsync(endpoint, methods.GET);
}

export const getAllWithoutRelations = async () => {
  return await fetchAsync(endpoints.collections, methods.GET);
}

export const getRange = async (skip = 0, limit = 100) => {
  const params = { skip: skip, limit: limit };
  const url = buildUrlParams(endpoints.collections, params);
  return await fetchAsync(url, methods.GET);
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