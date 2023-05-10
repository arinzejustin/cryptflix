import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load = (async ({ params, cookies }) => {
    const options = {
        maxAge: -3600,
        path: '/',
        priority: 'high' as const,
        secure: true,
        httpOnly: true,
        sameSite: 'lax' as const
    }
    cookies.set('uuid', '', options);
    cookies.set('user', '', options);
    cookies.set('token', '', options);
    cookies.set('card', '', options);
    cookies.set('ssid', '', options);
    throw redirect(307, '/0auth/login')
}) satisfies PageServerLoad;