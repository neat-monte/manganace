import { fetchJSON, methods } from './base'

const extraEndpoint = "/extras";

export const getGendersOptions = async () => {
    return await fetchJSON(`${extraEndpoint}/genders`, methods.GET);
}

export const getEducationsOptions = async () => {
    return await fetchJSON(`${extraEndpoint}/educations`, methods.GET);
}