import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { getContext, setContext } from 'svelte';

interface User {
    uuid: string,
    authorization: string,
    email: string,
    role: string
}

export const load = (async ({ locals }) => {

}) satisfies LayoutServerLoad;