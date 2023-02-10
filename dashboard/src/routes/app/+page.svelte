<script>
	import { fly } from 'svelte/transition';
</script>

<svelte:head />

<div in:fly={{ x: 400 }} out:fly={{ x: -400 }} class="flex container">
	<div class="bg-yellow-100 dark:bg-yellow-100/30 theme-text-app border border-solid border-yellow-200 shadow-lg rounded-md p-4"></div>
</div>
