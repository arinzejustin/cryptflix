import type { PageLoad } from '../$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

export const load = (async ({ params }) => {
    try {
        const req = await API.post('/ref', JSON.stringify({ user: params.slug }))
        throw redirect(307, '/0auth/onboard')
    } catch (err: any) {
        throw redirect(307, '/0auth/onboard')
    }

    return {
        post: {
            title: `Referred by ${params.slug} as user id`
        }
    };
}) satisfies PageLoad;