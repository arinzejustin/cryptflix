<script>
	import { onMount } from 'svelte';

	onMount(() => {
		document.documentElement.classList.remove('dark');
	});
</script>

<cryptoflixinvest-auth>
	<slot />
</cryptoflixinvest-auth>

<style>
	:global(body) {
		@apply bg-white;
	}
</style>
