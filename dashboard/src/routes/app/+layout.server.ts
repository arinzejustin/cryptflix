import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import API from '$lib/api'

let gravatar: string,
    transaction: any,
    plan: any,
    error: boolean = false,
    find: boolean = false;

export const load = (async ({ cookies, locals, getClientAddress }) => {
    const UUID = cookies.get('UUID');
    const ip = getClientAddress();

    if (!UUID || !locals.user) {
        throw redirect(307, '/0auth/login');
    }

    if (locals.user.role == 'admin') throw redirect(304, '/admin')

    cookies.set('client', ip, {
        httpOnly: true,
        maxAge: 60 * 60 * 24 * 14,
        path: '/',
        priority: 'high',
        secure: true
    })

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: 'justindiceyyo19@gmail.com' }))
        gravatar = req.gravatar;
    } catch (err) {
        gravatar = '/dart.jpg'
    }

    try {
        const req = await API.post('/history', JSON.stringify({ user: 'justindiceyyo19@gmail.com', server: true, mini: true }))
        transaction = req.transaction;
        find = req.find
    } catch (err) {
        error = true
    }

    return {
        user: {
            gravatar: gravatar,
            load: false,
            plan: 'Plan 2',
            transaction: transaction,
            error: error,
            find: find
        }
    }

}) satisfies LayoutServerLoad;