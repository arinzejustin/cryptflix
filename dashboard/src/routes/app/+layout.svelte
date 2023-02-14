<script lang="ts">
	import Header from '../../components/Header.svelte';
	import Footer from '../../components/Footer.svelte';
	import Interactive from '../../components/Interactive.svelte';
	import Sidebar from '../../components/Sidebar.svelte';
	import Mini from '../../components/Mini.svelte';
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
		hidden = true,
		token: any;

	$: height = h + 20;

	onMount(() => {
		if (window.matchMedia('(min-width: 768px)').matches) open = true;
		onresize = () => {
			if (window.matchMedia('(min-width: 768px)').matches) {
				open = true;
				small = false;
				hidden = true;
			} else {
				open = false;
				small = true;
				hidden = false;
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
		token = getStorage('token') || '';
	});
</script>

<cryptflixinvest-dashboard class="flex overflow-hidden w-full flex-col">
	<Drawer
		variant="dismissible"
		bind:open
		class="shadow-lg dark:border-slate-500 border-slate-300 dark:bg-black"
	>
		<Sidebar />
	</Drawer>
	<AppContent class="app-content {open && small ? '-right-[256px] fixed' : ''}">
		<div>
			<Header
				src={data.user.gravatar}
				loading={data.user.load}
				plan={data.user.plan}
				{open}
				bind:height={h}
			/>
		</div>
		<div class="grid grid-cols-4 gap-4" id="slot">
			<div class="w-full col-span-4 xl:col-span-3">
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
			{#if hidden}
				<div
					in:fly={{ x: 300 }}
					style="--mt-2: {h + 'px'}; --wid: {w + 'px'}"
					class="top-[var(--mt-2)] xl:w-[var(--wid)] bg-white dark:bg-black fixed right-0 hidden xl:flex h-screen -z-[1] overflow-y-hidden border-color border-l border-solid"
				>
					<div class="grid grid-rows-[repeat(7,_minmax(0,_1fr))] w-full align-middle items-start">
						<div
							class="h-full row-span-3 overflow-x-hidden overflow-y-auto border-b border-solid border-color"
						>
							<Mini
								{token}
								find={data.user.find}
								transaction={data.user.transaction}
								error={data.user.error}
							/>
						</div>
						<div
							class="h-full row-span-2 overflow-x-hidden overflow-y-auto border-b border-solid border-color"
						>
							<Interactive />
						</div>
						<div class="text-center overflow-y-auto row-span-2">
							<button
								class="bg-yellow-100 my-4 px-4 py-2 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
								>Need Technical Help</button
							>
						</div>
					</div>
				</div>
			{/if}
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
