import * as OTPAuth from 'otpauth'

export const totp = () => {
  let totp = new OTPAuth.TOTP({
    issuer: 'Private data',
    label: 'otp',
    algorithm: 'SHA1',
    digits: 6,
    period: 300,
  })

  let token = totp.generate()
  let seconds = totp.period - (Math.floor(Date.now() / 1000) % totp.period)
  let uri = totp.toString()

  return { token, seconds, uri }
}
