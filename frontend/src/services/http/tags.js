import endpoints from './endpoints'
import { fetchAsync, methods } from './base'

export default {
  async get (id) {
    const endpoint = `${endpoints.tags}/${id}`
    const url = new URL(endpoint)
    return await fetchAsync(url, methods.GET)
  },
  async getAll () {
    const url = new URL(endpoints.tags)
    return await fetchAsync(url, methods.GET)
  },
  async create () {
    const url = new URL(endpoints.tags)
    // TODO: add data
    return await fetchAsync(url, methods.POST)
  },
  async update () {
    const url = new URL(endpoints.tags)
    // TODO: add data
    return await fetchAsync(url, methods.PUT)
  },
  async delete (id) {
    const endpoint = `${endpoints.tags}/${id}`
    const url = new URL(endpoint)
    return await fetchAsync(url, methods.DELETE)
  }
}
