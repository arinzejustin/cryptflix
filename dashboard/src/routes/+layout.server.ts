import type { LayoutServerLoad } from './$types';
let admin: string;

export const load = (async ({ cookies }) => {

    const role = cookies.get('card');

    if (role && role == 'admin')
        admin = 'admin';
    else
        admin = '';

    return {
        role: {
            admin: admin
        }
    }

}) satisfies LayoutServerLoad;