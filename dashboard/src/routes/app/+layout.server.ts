import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import API from '$lib/api'

let gravatar: string,
    ero: any;

export const load = (async ({ cookies, locals }) => {
    const UUID = cookies.get('UUID');

    // if (!UUID || !locals.user) {
    //     throw redirect(307, '/0auth/login');
    // }

    // if (locals.user.role == 'admin') throw redirect(304, 'admin')

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: 'justindiceyyo19@gmail.com' }))
        gravatar = req.gravatar;
    } catch (err) {
        gravatar = '/dart.jpg'
        ero = err
    }

    return {
        user: {
            gravatar: gravatar,
            load: false,
            plan: 'Plan 2',
            error: JSON.stringify({ error: ero })
        }
    }

}) satisfies LayoutServerLoad;