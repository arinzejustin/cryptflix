<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { getStorage } from '$lib/storage';

	let token: any;
	var news = (token: string) => {
        try {
		var d = new Date(),
			day = d.toLocaleDateString();
		var today = day.split(',')[0],
			pre_format = `${today.split('/')[2]}-${today.split('/')[0]}-${today.split('/')[1]}`;
		d.setDate(d.getDate() - 10);
		var ago = d.toLocaleString(),
			// eslint-disable-next-line no-redeclare
			ago = ago.split(',')[0],
			ago_format = `${ago.split('/')[2]}-${ago.split('/')[0]}-${ago.split('/')[1]}`;
		// const req = API.post(
		// 	'/news',
		// 	JSON.stringify({ query: 'cryptocurrency', from: ago_format, to: pre_format }),
		// 	{ Authorization: token }
		// );
		console.log(req)
	} catch (error) {}
}

	onMount(() => {
        news(token)
		//@ts-ignore
		token = getStorage(token) || '';
	});
</script>
