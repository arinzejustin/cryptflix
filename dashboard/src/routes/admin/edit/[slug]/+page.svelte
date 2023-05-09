<script lang="ts">
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import gravatar from 'gravatar';
	import { onMount } from 'svelte';

	export let data: PageData;

	let token: string,
		dp = (email: string) => {
			var url = gravatar.url(email, { s: '50', r: 'x', d: 'robohash', f: 'y' }, true);
			return url;
		};

	onMount(() => {
		token = getStorage('token') ?? '';
	});
</script>

<svelte:head>
	<title>{data.user.title} | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>
