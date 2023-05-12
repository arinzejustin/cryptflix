import type { PageServerLoad } from '../../$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

let wallet: string,
    balance: string,
    name: string,
    uid: string;

export const load = (async ({ params, cookies }) => {

    const token = cookies.get('token') ?? '',
        uuid = cookies.get('uuid') ?? '',
        ssid = cookies.get('ssid') ?? '';

    try {
        const user = await API.post('/user/profile', JSON.stringify({ uuid: params.slug }), { Authorization: token, UUID: uuid, SSID: ssid })
        if (!user.status) throw redirect(307, '/0auth/login');
        var client = user.data;
        name = client.name;
        balance = client.balance;
        uid = params.slug;
        wallet = client.wallet
    } catch (err: any) {
        console.log(err)
        throw redirect(307, '/0auth/login')
    }

    return {
        client: {
            wallet: wallet,
            balance: balance,
            uid: uid,
            name: name
        }
    }
}) satisfies PageServerLoad;