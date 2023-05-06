import type { Handle } from '@sveltejs/kit'
import Api from '$lib/api'

let user: any = null;

export const handle: Handle = async ({ event, resolve }) => {
console.log('ruuned at ', Date.now())
  const session = event.cookies.get('S_ID')

  if (!session) {
    return await resolve(event)
  }

  try {
    const req = await Api.post('/verify', JSON.stringify({ token: session }))
    user = req.user
  } catch (err) {
    return await resolve(event)
  }

  if (user) {
    event.locals.user = {
      uuid: user.uuid,
      authorization: user.authorization,
      role: user.role,
      email: user.email
    }
  }

  return await resolve(event)
}
