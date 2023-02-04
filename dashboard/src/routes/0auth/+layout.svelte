<script>
	import { onMount } from 'svelte';

	onMount(() => {
		document.documentElement.classList.remove('dark');
	});
</script>

<cryptflixinvest-auth>
	<slot />
</cryptflixinvest-auth>

<style>
	:global(body) {
		@apply bg-white;
	}
</style>
