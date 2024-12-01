import { fail } from '@sveltejs/kit'

export const actions = {
  createCapKey: async ({ request }) => {
    try {
      return { success: true, endpoint: 'createCapKey', capKey: 123 }
    } catch (err) {
      console.log({ err })
      return fail(500, { endpoint: 'createCapKey', error: err })
    }
  }
}
