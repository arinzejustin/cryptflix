<script lang="ts">
	import Header from '../../components/Header.svelte';
	import Footer from '../../components/Footer.svelte';
	import Navbar from '../../components/Navbar.svelte';
	import Drawer, { AppContent } from '@smui/drawer';
	import Loader from '$lib/Loader.svelte';
	import { fade, slide } from 'svelte/transition';
	import { onMount } from 'svelte';
	import type { LayoutData } from './$types';
	import { getStorage } from '$lib/storage';

	export let data: LayoutData;

	let open = false,
		small = false,
		pageLoading = true,
		h = 0;

	$: height = h + 20;

	onMount(() => {
		if (window.matchMedia('(min-width: 768px)').matches) open = true;
		onresize = () => {
			if (window.matchMedia('(min-width: 768px)').matches) {
				open = true;
				small = false;
			} else {
				open = false;
				small = true;
			}
		};
		pageLoading = false;
		var mode = getStorage('mode');
		document.documentElement.classList.add(mode);
	});
</script>

<cryptflixinvest-dashboard class="flex overflow-hidden w-full flex-col">
	<Drawer
		variant="dismissible"
		bind:open
		class="shadow-lg dark:border-slate-500 border-slate-300 dark:bg-black"
	>
		<Navbar />
	</Drawer>
	<AppContent class="app-content {open && small ? '-right-[256px] fixed' : ''}">
		<div>
			<Header src={data.user.gravatar} loading={data.user.load} {open} bind:height={h} />
		</div>
		{#if pageLoading}
			<div out:fade class="transform -translate-y-1/2 -translate-x-1/2 top-1/2 left-1/2 fixed">
				<Loader width={'55px'} height={'55px'} />
			</div>
		{:else}
			<div in:slide class="px-2 slot" style="--mt: {height + 'px'}">
				<slot />
			</div>
		{/if}
		<div class="hidden">
			{h} : {height}
		</div>
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
	.slot {
		margin-top: var(--mt);
	}
</style>
