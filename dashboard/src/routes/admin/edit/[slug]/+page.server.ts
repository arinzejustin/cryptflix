import type { PageServerLoad } from '../../$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

export const load = (async ({ params, cookies }) => {

    const token = cookies.get('token') ?? ''

    try {
        const req = await API.post('/profile', JSON.stringify({ uuid: params.slug }), { Authorization: token, UUID: uuid, SSID: ssid })
        // if (!req.status) throw redirect(307, '/0auth/login');
    } catch (err: any) {
        console.log(err)
        throw redirect(307, '/0auth/login');
    }

    return {
        user: {
            title: `Referred by ${params.slug} as user id`
        }
    };
}) satisfies PageServerLoad;