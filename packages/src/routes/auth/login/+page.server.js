import qrcode from 'qrcode'
import { totp } from '$lib/utils'

export const load = () => {
  const { token, seconds, uri } = totp()

  return { token, seconds, uri }
}

export const actions = {
  getTotp: async ({ request }) => {
    const { token, seconds, uri } = totp()

    return { token, seconds, uri }
  }
}
