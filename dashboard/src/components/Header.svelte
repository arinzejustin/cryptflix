<script lang="ts">
	import Loader from '$lib/Loader.svelte';
	import { onMount } from 'svelte';

	export let loading = true,
		src: string,
		open: boolean,
		height: number;

	let shadow = false,
		menu = false;

	onMount(() => {
		addEventListener('scroll', () => {
			if (window.scrollY > 50) shadow = true;
			else shadow = false;
		});
		if (window.scrollY > 50) shadow = true;
		//@ts-ignore
		height = document.querySelector('#header')!.offsetHeight;
		onresize = () => {
			//@ts-ignore
			height = document.querySelector('#header')!.offsetHeight;
		};
	});
</script>

<header class="relative">
	<div
		id="header"
		class="fixed bg-white transition-all duration-500 dark:bg-black text-slate-700 dark:text-slate-100 right-0 top-0 border-solid border-b border-color {open
			? 'left-[256px]'
			: 'left-0'} {shadow
			? 'shadow-lg dark:shadow-md dark:shadow-slate-400 backdrop-blur-md bg-white/[0.75] dark:bg-black/[0.65]'
			: ''}"
	>
		<div class="flex flex-row items-center align-middle justify-between mx-4 py-3.5 md:py-4">
			<div class="flex flex-row items-center align-middle justify-between">
				<div class="md:hidden">
					<svg
						class="text-slate-700 dark:text-white w-8 h-8"
						xmlns="http://www.w3.org/2000/svg"
						width="1em"
						height="1em"
						viewBox="0 0 24 24"
						><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
							fill="currentColor"
							d="M4 18q-.425 0-.712-.288Q3 17.425 3 17t.288-.712Q3.575 16 4 16h16q.425 0 .712.288q.288.287.288.712t-.288.712Q20.425 18 20 18Zm0-5q-.425 0-.712-.288Q3 12.425 3 12t.288-.713Q3.575 11 4 11h16q.425 0 .712.287q.288.288.288.713t-.288.712Q20.425 13 20 13Zm0-5q-.425 0-.712-.287Q3 7.425 3 7t.288-.713Q3.575 6 4 6h16q.425 0 .712.287Q21 6.575 21 7t-.288.713Q20.425 8 20 8Z"
						/></svg
					>
				</div>
				<div />
			</div>
			<div class="md:mr-4 relative">
				{#if loading}
					<div class="mr-4 md:mr-6">
						<Loader width={'30px'} height={'30px'} />
					</div>
				{:else}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						class="flex flex-row justify-between cursor-pointer align-middle items-center"
						on:click={() => (menu = !menu)}
					>
						<img
							on:load={() => window.alert('hello')}
							{src}
							srcset="{src} 2x"
							alt=""
							class="border-solid border-2 border-color w-8 h-8 md:w-10 md:h-10 rounded-full"
						/>
						<div>
							<svg
								class="text-slate-700 dark:text-slate-500 w-4 h-4 ml-1.5 md:ml-3"
								xmlns="http://www.w3.org/2000/svg"
								width="1em"
								height="1em"
								viewBox="0 0 24 24"
								><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
									transform="rotate({menu ? '90' : '-90'} 12 12)"
									><path
										fill="currentColor"
										d="M15.125 21.1L6.7 12.7q-.15-.15-.212-.325q-.063-.175-.063-.375t.063-.375q.062-.175.212-.325l8.425-8.425q.35-.35.875-.35t.9.375q.375.375.375.875t-.375.875L9.55 12l7.35 7.35q.35.35.35.862q0 .513-.375.888t-.875.375q-.5 0-.875-.375Z"
									/></g
								></svg
							>
						</div>
					</div>
					{#if menu}
						<div
							data-popover
							data-popper-placement="bottom"
							role="tooltip"
							class="absolute z-10 app-inset m-0 left-0 right-0 top-0 border-solid py-2 dark:shadow-slate-400 inline-block w-64 text-sm font-light text-slate-700 transition-opacity duration-300 bg-white dark:bg-black border rounded-md shadow-md dark:text-slate-50 border-color"
							style="transform: translate(-202px, 55px)"
						>
							<div class="py-2">
								<div class="flex flex-row justify-between align-middle items-center border-b p-2 border-solid border-color">
									<div>
										<p class="text-slate-700 dark:text-slate-50"></p>
									</div>
									<div>
										<button class="bg-blue-600 rounded-md text-sm p-1 hover:shadow-lg">Upgrade</button>
									</div>
								</div>
							</div>
							<div data-popper-arrow style="transform: translate(210px, 0px)" class="absolute left-0" />
						</div>
					{/if}
				{/if}
			</div>
		</div>
	</div>
</header>

<style>
	[data-popper-arrow]::after,
	[data-popper-arrow]::before {
		@apply content-[''] visible transform rotate-45;
	}
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow] {
		@apply -top-[7px] shadow-md;
	}
	[data-popper-arrow],
	[data-popper-arrow]::before {
		@apply h-3 absolute w-3 bg-inherit;
	}
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow]::after,
	[data-popover][role='tooltip'][data-popper-placement^='bottom'] > [data-popper-arrow]::before {
		@apply border-l-2 border-t-2;
	}
	
	[data-popper-arrow]::after {
		@apply absolute w-[14px] bg-inherit h-[14px];
	}
</style>
