import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import API from '$lib/api'

let _id: string,
    magic_auth: string;

export const load = (async ({ cookies }) => {
    const token = cookies.get('token') ?? '',
        uuid = cookies.get('uuid') ?? '',
        ssid = cookies.get('ssid') ?? '';

    try {
        const req = await API.post('/user', JSON.stringify({ uuid: '******' }), { Authorization: token, UUID: uuid, SSID: ssid })
        // if (!req.status) throw redirect(307, '/0auth/login');
        console.log(req)
        _id = req._id;
        magic_auth = req.magic_auth
    } catch (err: any) {
        console.log(err)
    }
    return {
        device_id: _id,
        magic_auth: magic_auth
    };
}) satisfies PageServerLoad;