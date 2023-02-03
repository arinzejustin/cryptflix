import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load = (async ({}) => {

    throw redirect(307, 'app')

    return {
        
    }

}) satisfies LayoutServerLoad;