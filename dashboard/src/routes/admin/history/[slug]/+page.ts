import type { PageLoad } from '../../$types';

export const prerender: boolean = false;

export const load = (async ({ params }) => {

    return {
        uid: {
            id: `${params.slug}`
        }
    };
}) satisfies PageLoad;