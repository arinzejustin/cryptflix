import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import API from '$lib/api'

let gravatar: string,
    transaction: any,
    plan: any,
    error: boolean = false,
    find: boolean = false,
    _id: string,
    magic_auth: string,
    wallet: string,
    referral: string,
    name: string,
    email_u: string,
    balance: string,
    deposit: string,
    created: string | undefined;

export const load = (async ({ cookies }) => {

    const email = cookies.get('user');
    const ssid = cookies.get('ssid');
    const authorization = cookies.get('token');
    const role = cookies.get('card');
    const token = cookies.get('token') ?? '',
        uuid = cookies.get('uuid') ?? '';

    if (!authorization || !email || !role) {
        throw redirect(307, '/0auth/login');
    }

    if (role == 'admin') throw redirect(307, '/admin')

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: email }))
        gravatar = req.gravatar;
    } catch (err: any) {
        gravatar = '/img/pp.png'
    }

    try {
        const req = await API.post('/user', JSON.stringify({ uuid: '******' }), { Authorization: token, UUID: uuid, SSID: ssid })
        if (!req.status) throw redirect(307, '/0auth/login');
        console.log(req)
        _id = req.device_id;
        magic_auth = req.magic;
        plan = req.account;
        wallet = req.wallet;
        referral = req.referral;
        name = req.name;
        email_u = req.email;
        balance = req.balance;
        deposit = req.deposit;
        created = req.created ?? undefined
    } catch (err: any) {
        console.log(err)
    }

    return {
        user: {
            gravatar: gravatar,
            load: false,
            plan: plan,
            transaction: transaction,
            error: error,
            find: find,
            device_id: _id,
            magic_auth: magic_auth,
            wallet: wallet,
            referral: referral,
            name: name,
            email: email_u,
            balance: balance,
            deposit: deposit,
            created: created
        }
    }

}) satisfies LayoutServerLoad;