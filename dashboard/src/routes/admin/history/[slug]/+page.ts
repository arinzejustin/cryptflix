import type { PageLoad } from '../../$types';

export const load = (async ({ params }) => {

    return {
        uid: {
            id: `${params.slug}`
        }
    };
}) satisfies PageLoad;