import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

let gravatar: string;

export const load = (async ({ cookies, locals }) => {
    const UUID = cookies.get('UUID');

    // if (!UUID || !locals.user) {
    //     throw redirect(307, '0auth/login');
    // }

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: locals.user.email }))
        gravatar = req.gravatar;
    } catch (err) {
        gravatar = '/default.png'
    }

    return {
        user: {
            gravatar: gravatar
        }
    }

}) satisfies LayoutServerLoad;