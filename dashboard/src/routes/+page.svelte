<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Loader from '$lib/Loader.svelte';
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';

	export let data: PageData;

	onMount(() => goto('/app', { noScroll: true, keepFocus: true, replaceState: true }));
</script>

<svelte:head>
	<title>Loading Dashboard | cryptoflixinvest.org</title>
</svelte:head>

<div
	out:fly={{ y: -200, opacity: 0 }}
	class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
>
	<Loader width={'80px'} height={'80px'} />
</div>
<div class="mt-8 text-center absolute bottom-1/3 w-full">
	<p
		class="uppercase text-center mt-2 text-base md:text-lg lg:text-xl text-slate-700 dark:text-slate-50 font-mono font-semibold lg:font-extrabold"
	>
		Loading {data.role.admin} Dashboard .....
	</p>
</div>
