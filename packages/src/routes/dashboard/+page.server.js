import { fail } from '@sveltejs/kit'
import { createAlias, createDirectory, listDirectories, unlink, uploadFile } from '$lib/utils/tahoe'

export const actions = {
  createCapKey: async ({ request, fetch }) => {
    try {
      const { capKey } = await createAlias()

      return { endpoint: 'createCapKey', capKey }
    } catch (error) {
      console.log({ error })
      return fail(500, { endpoint: 'createCapKey', error })
    }
  },

  listDirectories: async ({ request, fetch }) => {
    const formData = await request.formData()
    const capKey = formData.get('capKeyInput')
    const encoded = encodeURIComponent(capKey)

    try {
      const { list } = await listDirectories(capKey)

      return { endpoint: 'listDirectories', list, capKey }
    } catch (error) {
      if (error.cause.message.includes('ECONNREFUSED')) {
        return { error: 'Tahoe server may be offline.' }
      }

      console.log({ error })
      return fail(500, { endpoint: 'listDirectories', error })
    }
  },

  createDirectory: async ({ request, fetch }) => {
    const formData = await request.formData()
    const capKey = formData.get('capKey')
    const encoded = encodeURIComponent(capKey)
    const dirName= formData.get('dirName')
    let path = formData.get('path')

    if (path.length === 0) path = '/'
    if (path.slice(0, 1) !== '/') path = '/' + path
    if (path.slice(-1) !== '/') path = path + '/'

    path = encoded + encodeURI(path)

    try {
      const { cap } = await createDirectory(path, dirName)

      return { success: true, endpoint: 'uploadFile' }
    } catch (error) {
      console.log({ error })
      return fail(500, { endpoint: 'uploadFile', error})
    }
  },

  uploadFile: async ({ request, fetch }) => {
    const formData = await request.formData()
    const capKey = formData.get('capKey')
    const encoded = encodeURIComponent(capKey)
    const file = formData.get('file')
    let path = formData.get('path')

    if (path.length === 0) path = '/'
    if (path.slice(0, 1) !== '/') path = '/' + path
    if (path.slice(-1) !== '/') path = path + '/'

    path = encoded + encodeURI(path + file.name)

    try {
      await uploadFile(path, file.name, file)

      return { success: true, endpoint: 'uploadFile' }
    } catch (error) {
      console.log({ error })
      return fail(500, { endpoint: 'uploadFile', error})
    }
  },

  deletePath: async ({ request, fetch }) => {
    const formData = await request.formData()
    const capKey = formData.get('capKey')
    const encoded = encodeURIComponent(capKey)
    const partialPath = formData.get('path')
    const slash = partialPath.slice(0, 1) === '/' ? '' : '/'
    const path = encoded + slash + partialPath

    if (partialPath.length === 0) {
      return { success: false, endpoint: 'deletePath', error: 'Path cannot be empty.'}
    }

    try {
      await unlink(path)

      return { success: true, endpoint: 'deletePath' }
    } catch (error) {
      console.log({ error })
      return json({ success: false, code: 500, error })
    }
  }
}
