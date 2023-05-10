import type { PageServerLoad } from '../../$types';
import { redirect } from '@sveltejs/kit';
import API from '$lib/api'

let name: string,
    status: string,
    id: string,
    tel: string,
    country: string,
    email: string,
    type: string,
    balance: string,
    deposit: string,
    referral: string,
    created: string;


export const load = (async ({ params, cookies }) => {

    const token = cookies.get('token') ?? '',
        uuid = cookies.get('uuid') ?? '',
        ssid = cookies.get('ssid') ?? '';

    try {
        const user = await API.post('/user/profile', JSON.stringify({ uuid: params.slug }), { Authorization: token, UUID: uuid, SSID: ssid })
        if (!user.status) throw redirect(307, '/0auth/login');
        var data = user.data
        status = data.acct_status;
        balance = data.balance;
        country = data.country;
        deposit = data.deposit;
        email = data.email;
        id = data.id;
        referral = data.referral;
        tel = data.tel;
        type = data.type;
        name = data.name;
        created = data.created
    } catch (err: any) {
        console.log(err)
        throw redirect(307, '/0auth/login');
    }

    return {
        user: {
            title: `Profile detail for ${name}`,
            name: name,
            type: type,
            email: email,
            id: id,
            referral: referral,
            deposit: deposit,
            balance: balance,
            country: country,
            status: status,
            created: created
        }
    };
}) satisfies PageServerLoad;