import type { PageLoad } from '../../$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

export const load = (async ({ params }) => {

    return {
        post: {
            title: `Referred by ${params.slug} as user id`
        }
    };
}) satisfies PageLoad;