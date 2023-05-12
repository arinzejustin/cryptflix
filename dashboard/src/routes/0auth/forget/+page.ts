import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load = (({ params }) => {
    throw redirect(307, '/0auth/login')
}) satisfies PageLoad;