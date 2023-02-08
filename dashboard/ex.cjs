var req = {
    find: false,
    transaction: [
        {
            name: 'Arinze',
            age: 18
        },
        {
            name: 'Justin',
            age: 18
        }
    ]
}

if ('find' in req) console.log(req.transaction); else console.log('can\'t find it')