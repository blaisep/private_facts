import { env } from '$env/dynamic/private'

export const createAlias = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const url = `${env.TAHOE_API}/uri?t=mkdir`
      const response = await fetch(url, { method: 'POST' })
      const capKey = await response.json()

      return resolve({ capKey })
    } catch (error) {
      return reject(error)
    }
  })
}

export const listDirectories = (capKey) => {
  return new Promise(async (resolve, reject) => {
    try {
      const url = `${env.TAHOE_API}/uri/${capKey}?t=json`
      const response = await fetch(url, { method: 'GET' })
      const list = await response.json()

      return resolve({ list })
    } catch (error) {
      return reject(error)
    }
  })
}

export const createDirectory = (path, dirName) => {
  return new Promise(async (resolve, reject) => {
    try {
      const url = `${env.TAHOE_API}/uri/${path}?t=mkdir&name=${dirName}`
      const response = await fetch(url, { method: 'POST' })

      if (response.status !== 200) {
        return json({ success: false, status: response.status, message: response.statusText })
      }

      const cap = await response.json()

      return resolve({ cap })
    } catch (error) {
      return reject(error)
    }
  })
}

export const uploadFile = (path, file) => {
  return new Promise(async (resolve, reject) => {
    const url = `${env.TAHOE_API}/uri/${path}`

    try {
      const response = await fetch(url, {
        method: 'PUT',
        body: file
      })

      return resolve()
    } catch (error) {
      console.log({ error })
      return reject(error)
    }
  })
}

export const unlink = (path) => {
  return new Promise(async (resolve, reject) => {
    try {
      const url = `${env.TAHOE_API}/uri/${path}`
      const response = await fetch(url, { method: 'DELETE' })

      return resolve()
    } catch (error) {
      return reject(error)
    }
  })
}
