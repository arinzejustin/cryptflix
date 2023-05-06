import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import API from '$lib/api'

let gravatar: string,
    transaction: any,
    plan: any,
    error: boolean = false,
    find: boolean = false;

export const load = (async ({ cookies }) => {

    const email = cookies.get('user');
    const ssid = cookies.get('uuid');
    const authorization = cookies.get('token');
    const role = cookies.get('card');

    if (!authorization || !email || !role) {
        throw redirect(307, '/0auth/login');
    }

    if (role == 'admin') throw redirect(307, '/admin')

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: email }))
        gravatar = req.gravatar;
    } catch (err: any) {
        gravatar = '/img/pp.png'
    }

    try {
        const req = await API.post('/history', JSON.stringify({ user: email, server: true, mini: true }))
        transaction = req.transaction;
        find = req.find
    } catch (err: any) {
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