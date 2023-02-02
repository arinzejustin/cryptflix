<script>
	import Header from '../../components/Header.svelte';
	import Footer from '../../components/Footer.svelte';
	import Navbar from '../../components/Navbar.svelte';
	import Drawer, { AppContent } from '@smui/drawer';
	import { onMount } from 'svelte';

	let open = false,
		small = false;

	onMount(() => {
		if (window.matchMedia('(min-width: 768px)').matches) open = true;
		onresize = () => {
			if (window.matchMedia('(min-width: 768px)').matches) {
                open = true;
                small = false
            }
			else {
                open = false;
                small = true
            }
		};
	});
</script>

<cryptflixinvest-dashboard class="flex overflow-hidden w-full flex-col">
	<Drawer variant="dismissible" bind:open>
		<Navbar />
	</Drawer>
	<AppContent class="app-content {!open && small ? '-right-[256px] fixed bg-black/[0.55] backdrop-blur-md' : ''}">
		<Header src={'hello'} {open} />
		<slot />
		<Footer />
	</AppContent>
</cryptflixinvest-dashboard>

<style>
	:global(body) {
		@apply bg-white transition-all duration-500;
	}
	:global(.dark body) {
		@apply bg-black duration-500 transition-all;
	}
	* :global(.app-content) {
		flex: auto;
		overflow: auto;
		position: relative;
		flex-grow: 1;
	}
</style>
