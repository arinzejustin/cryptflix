import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import API from '$lib/api'

let gravatar: string,
    error: boolean = false,
    find: boolean = false,
    name: string,
    users: string,
    newUser: string,
    balance: string,
    user: string,
    deposit: string,
    date: string;

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

    if (role == 'user') throw redirect(307, '/app')

    try {
        const req = await API.get('/gravatar', JSON.stringify({ user: email }))
        gravatar = req.gravatar;
    } catch (err: any) {
        gravatar = '/img/pp.png'
    }

    try {
        const req = await API.post('/user', JSON.stringify({ uuid: '******' }), { Authorization: token, UUID: uuid, SSID: ssid })
        if (!req.status) throw redirect(307, '/0auth/login');
        user = req.user;
        name = req.name
    } catch (err: any) {
        console.log(err)
        throw redirect(307, '/0auth/login');
    }

    try {
        const req = await API.post('/admin__', JSON.stringify({ uuid: '******' }), { Authorization: token, UUID: uuid, SSID: ssid })
        console.log(req)
        if (!req.status) throw redirect(307, '/0auth/login');
        users = req.user;
        balance = req.balance;
        newUser = req.newUser;
        deposit = req.deposit;
        date = req.date
    } catch (err: any) {
        console.log(err)
        throw redirect(307, '/0auth/login');
    }

    return {
        user: {
            gravatar: gravatar,
            load: false,
            error: error,
            find: find,
            name: name,
            admin: true,
            user: user
        },
        admin : {
            balance: balance,
            newUser: newUser,
            users: users,
            deposit: deposit,
            date: date
        }
    }

}) satisfies LayoutServerLoad;