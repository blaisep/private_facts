import { fail } from '@sveltejs/kit'

export const actions = {
  createCapKey: async ({ request, fetch }) => {
    try {
      const response = await fetch('/api/createAlias', { method: 'POST' })
      const jsonResponse = await response.json()

      return { endpoint: 'createCapKey', capKey: jsonResponse.capKey }
    } catch (err) {
      console.log({ err })
      return fail(500, { endpoint: 'createCapKey', error: err })
    }
  },

  listDirectories: async ({ request, fetch }) => {
    const formData = await request.formData()
    const capKey = formData.get('capKeyInput')
    const encoded = encodeURIComponent(capKey)

    try {
      const response = await fetch('/api/listDirectories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ capKey: encoded })
      })
      const jsonResponse = await response.json()
      if (!jsonResponse.success) throw new Error(jsonResponse.error)

      return { endpoint: 'listDirectories', list: jsonResponse.list, capKey }
    } catch (err) {
      console.log({ err })
      return fail(500, { endpoint: 'listDirectories', error: err })
    }
  }
}
