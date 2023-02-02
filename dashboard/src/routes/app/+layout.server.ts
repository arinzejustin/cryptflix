import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

let avi: string;

export const load = (async ({ cookies, locals }) => {
    const UUID = cookies.get('UUID');

    // if (!UUID || !locals.user) {
    //     throw redirect(307, '0auth/login');
    // }

    try {
        const req = await API.get('/gravatar', JSON.stringify({ email: 'justindiceyyo19@gmail.com' }))
        avi = req.gravatar;
    } catch (err) {
        avi = '/logo.png'
    }

    return {
        user: {
            gravatar: avi
        }
    }

}) satisfies LayoutServerLoad;