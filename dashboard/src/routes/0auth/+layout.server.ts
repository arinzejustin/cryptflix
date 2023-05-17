import type { LayoutServerLoad } from './$types';

export const load = (async ({ cookies }) => {
    const options = {
        maxAge: -3600,
        path: '/',
        priority: 'high' as const,
        secure: true,
        httpOnly: true,
        sameSite: 'none' as const,
        domain: ''
    }
    cookies.set('uuid', '', options);
    cookies.set('user', '', options);
    cookies.set('token', '', options);
    cookies.set('card', '', options);
    cookies.set('ssid', '', options);
}) satisfies LayoutServerLoad;