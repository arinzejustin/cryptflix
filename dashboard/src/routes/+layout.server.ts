import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load = (async ({ cookies, locals, getClientAddress }) => {

    const UUID = cookies.get('uuid');

    const ip = getClientAddress();

    cookies.set('client', ip, {
        httpOnly: true,
        maxAge: 60 * 60 * 24 * 14,
        path: '/',
        priority: 'high',
        secure: true
    })
    console.log('hello runned')

}) satisfies LayoutServerLoad;