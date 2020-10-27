import endpoints from '@/services/http/endpoints'

const fetchAbsolute = require('fetch-absolute')
export const fetchApi = fetchAbsolute(fetch)(endpoints.baseAddress)

/**
 * Fetch pipeline function which validates if the response is OK [status = 200]
 * @param response
 * @returns {{ok}|*}
 */
function validate(response) {
  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

/**
 * Fetch pipeline function which converts response to JSON
 * @param response
 * @returns {*}
 */
function jsonify(response) {
  return response.json()
}

/**
 * Fetch pipeline function which logs an error
 * @param error
 */
function dump(error) {
  console.log('There was a problem: \n', error)
}

/**
 * Wrapped fetch call with a predetermined pipeline of validate and convert to JSON,
 * and in case of error - log to the console
 * @param url {String|URL}
 * @param method {String}
 * @param data {*}
 * @returns {Promise<postcss.Result|any|undefined>}
 */
export async function fetchAsync(url, method, data = null) {
  return fetchApi(url, { method: method, body: data, credentials: 'include' })
    .then(validate)
    .then(jsonify)
    .catch(dump)
}

/**
 * Wrapped fetch call which does not expect any JSON response, only OK (200).
 * It validates the response and in case of error - logs to the console.
 * @param {*} url {String|URL}
 * @param {*} method {String}
 */
export async function sendAsync(url, method) {
  return fetchApi(url, { method: method, credentials: 'include' })
    .then(validate)
    .catch(dump)
}

/**
 * Enumeration of viable fetch methods
 * @type {{DELETE: string, POST: string, GET: string, PUT: string}}
 */
export const methods = {
  GET: 'GET',
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE'
}

/**
 * Builds a URL object with query parameters
 * @param endpoint {String}
 * @param params {*}
 * @returns {URL}
 */
export function buildUrlParams(endpoint, params) {
  const address = endpoints.baseAddress + endpoint
  const url = new URL(address)
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
  return url
}
