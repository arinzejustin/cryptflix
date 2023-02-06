<script>
	import { fly } from 'svelte/transition';
	export let active = false;
</script>

{#if active}
	<div
		in:fly={{ y: 600 }}
		out:fly={{ y: -200 }}
		class="bg-white fixed transform -translate-x-1/2 -translate-y-1/2  top-1/2 left-1/2 dark:bg-black border-color border-solid border rounded-lg shadow-md dark:shadow-slate-400 p-2"
	/>
{/if}
