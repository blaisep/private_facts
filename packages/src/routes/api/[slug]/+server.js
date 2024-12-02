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
      } catch (err) {
        console.log({ err })
        return json({ success: false, code: 500, error: err })
      }
    }

    case 'listDirectories': {
      try {
        const encodedCapKey = body.capKey.replace(/:/g, '%3A')
        const url = `${env.TAHOE_API}/uri/${encodedCapKey}?t=json`
        const response = await fetch(url, { method: 'GET' })
        const list = await response.json()
        console.log({ url, list })

        return json({ success: true, list })
      } catch (err) {
        console.log({ err })
        return json({ success: false, code: 500, error: err })
      }
    }

    default: {
      return json({ success: true })
    }
  }
}
