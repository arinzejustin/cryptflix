<script lang="ts">
	import Header from '../../components/Header.svelte';
	import Footer from '../../components/Footer.svelte';
	import Sidebar from '../../components/Sidebar.svelte';
	import Drawer, { AppContent } from '@smui/drawer';
	import Loader from '$lib/Loader.svelte';
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import type { LayoutData } from './$types';
	import { getStorage } from '$lib/storage';


	export let data: LayoutData;

	let open = false,
		small = false,
		pageLoading = true,
		h = 0,
		w = 270,
		token: any,
		aside = () => {
			var slot = document.querySelector('#slot')!,
				header = document.querySelector('#header')!;
			slot.classList.remove('hidden');
			header.classList.remove('hidden');
		};

	$: height = h + 20;

	onMount(() => {
		token = getStorage('token') || '';
		if (window.matchMedia('(min-width: 768px)').matches) open = true;
		onresize = () => {
			if (window.matchMedia('(min-width: 768px)').matches) {
				open = true;
				small = false;
				aside();
			} else {
				open = false;
				small = true;
			}
			w =
				//@ts-ignore
				document.querySelector('#slot')!.offsetWidth -
				//@ts-ignore
				document.querySelector('#slot-1')!.offsetWidth -
				10;
		};
		pageLoading = false;
		var mode = getStorage('mode');
		//@ts-ignore
		document.documentElement.classList.add(mode);
		setTimeout(() => {
			w = //@ts-ignore
				document.querySelector('#slot')!.offsetWidth -
				//@ts-ignore
				document.querySelector('#slot-1')!.offsetWidth -
				10;
		}, 2000);
	});
</script>

<cryptflixinvest-dashboard class="flex overflow-hidden w-full flex-col">
	<Drawer
		variant="dismissible"
		bind:open
		class="shadow-lg dark:border-slate-500 border-slate-300 dark:bg-black"
	>
		<Sidebar {open} />
	</Drawer>
	<AppContent class="app-content">
		<div>
			<Header
				src={data.user.gravatar}
				loading={data.user.load}
				plan={data.user.plan}
				bind:height={h}
			/>
		</div>
		<div class="overflow-y-auto overflow-x-hidden" id="slot">
			<div class="w-full">
				{#if pageLoading}
					<div
						id="slot-1"
						out:fly={{ y: -300 }}
						class=" transform -translate-y-1/2 -translate-x-1/2 top-1/2 left-1/2 fixed"
					>
						<Loader width={'55px'} height={'55px'} />
					</div>
				{:else}
					<div
						id="slot-1"
						in:fly={{ y: 500 }}
						class="px-2 mt-[var(--mt)] transition-all duration-200"
						style="--mt: {height + 'px'}"
					>
						<slot />
					</div>
				{/if}
				<Footer />
			</div>
		</div>
		<div class="hidden">
			{h} : {height} : {open} : {w}
		</div>
	</AppContent>
</cryptflixinvest-dashboard>

<style>
	:global(body) {
		@apply bg-white text-slate-700;
	}
	:global(.dark body) {
		@apply bg-black text-slate-50;
	}
	* :global(.app-content) {
		@apply flex-auto overflow-x-hidden overflow-y-auto relative flex-grow;
	}
</style>
