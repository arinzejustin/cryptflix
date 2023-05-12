import type { PageLoad } from './$types';
var countryCode: string = 'us';

export const prerender: boolean = false;

export const load = (({ params }) => {
    return {
        code: {
            intl: countryCode
        }
    };
}) satisfies PageLoad;