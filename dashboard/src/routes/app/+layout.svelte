<script>
	import Header from '../../components/Header.svelte';
	import Footer from '../../components/Footer.svelte';
</script>

<cryptflixinvest-dashboard>
	<div>
		<Header />
	</div>
	<slot />
	<div>
		<Footer />
	</div>
</cryptflixinvest-dashboard>

<style>
    :global(body) {
        @apply bg-white transition-all duration-500;
    }
    :global(.dark body) {
        @apply bg-black duration-500 transition-all;
    }
</style>