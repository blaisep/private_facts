import { json } from '@sveltejs/kit'
import { env } from '$env/dynamic/private'

export const POST = async ({ params, request }) => {
  const { slug } = params
  const body = await request.json()

  switch (slug) {
    case 'createAlias': {
      try {
        const url = `${env.TAHOE_API}/uri?t=mkdir`
        const response = await fetch(url, { method: 'POST' })
        const capKey = await response.json()

        return json({ success: true, capKey })
      } catch (error) {
        console.log({ error })
        return json({ success: false, code: 500, error })
      }
    }

    case 'listDirectories': {
      try {
        const encodedCapKey = body.capKey.replace(/:/g, '%3A')
        const url = `${env.TAHOE_API}/uri/${encodedCapKey}?t=json`
        const response = await fetch(url, { method: 'GET' })
        const list = await response.json()

        return json({ success: true, list })
      } catch (error) {
        console.log({ error })
        return json({ success: false, code: 500, error, message: error.cause.message })
      }
    }

    default: {
      return json({ success: true })
    }
  }
}
