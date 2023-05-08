<script lang="ts">
	import { fly } from 'svelte/transition';
    import type { PageData } from './$types';

	export let data: PageData;
</script>
<svelte:head>
	<title>Dashboard | cryptflixinvest.com</title>
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
    div>
</div>