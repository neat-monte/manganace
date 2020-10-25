import endpoints from './endpoints'
import { fetchAsync, sendAsync, methods } from './base'

export const initialize = async () => {
    return await sendAsync(endpoints.generator, methods.GET);
}

export const generate = async (data) => {
    return await fetchAsync(endpoints.generator, methods.POST, data);
}