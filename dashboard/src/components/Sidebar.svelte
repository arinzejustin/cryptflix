<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	export let open: boolean = true;

	let navbar = [
			{
				url: '/app',
				class: '',
				name: 'Dashboard',
				viewBox: '24 24'
			},
			{
				url: '/app/inbox',
				class: 'mb-4',
				name: 'Inbox',
				viewBox: '24 24'
			},
			{
				url: '/app/transaction/withdraw',
				class: 'mt-4',
				name: 'Withdraw',
				viewBox: '512 512'
			},
			{
				url: '/app/transaction/deposit',
				class: '',
				name: 'Invest',
				viewBox: '512 512'
			},
			{
				url: '/app/transaction/market',
				class: 'mb-4',
				name: 'Markets',
				viewBox: '48 48'
			},
			{
				url: '/app/news',
				class: 'mt-3',
				name: 'News',
				viewBox: '24 24'
			}
		],
		aside = (duration: number) => {};

	onMount(() => {
		aside = (duration: number) => {
			var side = document.querySelector('aside')!,
				slot = document.querySelector('#slot')!,
				header = document.querySelector('#header')!;
			setTimeout(() => {
				if (!open) {
					side.classList.remove('mdc-drawer--open');
					slot.classList.remove('hidden');
					header.classList.remove('hidden');
				}
			}, duration);
		};
	});
</script>

<div class="overflow-y-auto relative">
	{#if !open}
		<div class="absolute top-1 right-2">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<svg
				on:click={() => {
					aside(1);
				}}
				class="w-8 h-8 text-slate-700 dark:text-slate-50"
				xmlns="http://www.w3.org/2000/svg"
				width="1em"
				height="1em"
				viewBox="0 0 24 24"
				><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
					fill="currentColor"
					d="m12 13.4l-4.9 4.9q-.275.275-.7.275q-.425 0-.7-.275q-.275-.275-.275-.7q0-.425.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7q0-.425.275-.7q.275-.275.7-.275q.425 0 .7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275q.425 0 .7.275q.275.275.275.7q0 .425-.275.7L13.4 12l4.9 4.9q.275.275.275.7q0 .425-.275.7q-.275.275-.7.275q-.425 0-.7-.275Z"
				/></svg
			>
		</div>
	{/if}
	<div class="mb-8 mt-6 pt-4 grid grid-row-2 gap-2">
		<img src="/logo.png" alt="" class="w-16 h-16 mx-auto" />
		<p class="text-xs uppercase font-mono text-center">Lifting souls through crypto</p>
	</div>
	<div class="mt-5 pt-4">
		{#each navbar as links}
			<div class="py-3 group/item px-3 font-open">
				<!-- svelte-ignore a11y-missing-content -->
				<a
					on:click={() => {
						aside(500);
					}}
					href={links.url}
					class="{$page.url.pathname === links.url
						? 'bg-yellow-100 theme-text-app dark:bg-yellow-100/20 transform group-hover/item:bg-bg-yellow-100 dark:group-hover/item:bg-yellow-100/20'
						: 'group-hover/item:bg-slate-500/10 group-hover/item:translate-x-2 dark:group-hover/item:bg-slate-500/30'} flex flex-auto px-2 items-center rounded-md transition-all duration-100 py-3.5 {links.class}"
				>
					<svg
						class="w-6 h-6 mx-2 {$page.url.pathname === links.url
							? 'theme-text-app'
							: 'text-slate-700 dark:text-slate-50'}"
						xmlns="http://www.w3.org/2000/svg"
						width="1.13em"
						height="1em"
						viewBox="0 0 {links.viewBox}"
					>
						{#if links.name == 'Dashboard'}
							<rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M11.943.182c1.872 0 3.654.43 5.252 1.197c.251.113.503.248.753.384l-1.096.97l-1.643-1.692l-2.832 2.483L10.71 1.74L5.503 6.368l3.334 3.635l-1.302 1.128l3.29 3.635l-1.302 1.128l4.704 5.17l2.785-2.529l2.421 2.71c-.48.361-1.005.723-1.575 1.039a12.042 12.042 0 0 1-5.892 1.534C5.366 23.817 0 18.512 0 11.99C-.023 5.51 5.343.182 11.943.182zM9.75 11.268l2.855-2.529l2.558 2.822l-2.855 2.529zm2.033 4.876l2.832-2.55l2.58 2.821l-2.855 2.529zM7.72 6.46l2.854-2.529l2.557 2.822l-2.854 2.528zm5.228-1.355l2.124-1.896l1.919 2.099l-2.124 1.919zm3.792 8.691l2.123-1.896l1.918 2.121l-2.124 1.898zm1.872 4.267l2.124-1.897l1.917 2.1l-2.123 1.918zm.868-9.753l1.415-1.264l1.279 1.4l-1.416 1.264zm-1.827-4.176l1.416-1.286l1.28 1.422l-1.418 1.264zm3.63 8.353l1.416-1.264l1.302 1.4l-1.438 1.264zm-6.37-3.138l2.124-1.896l1.918 2.099l-2.124 1.897Z"
							/>
						{:else if links.name == 'News'}
							<rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M4 21q-.825 0-1.412-.587Q2 19.825 2 19V3l1.675 1.675L5.325 3L7 4.675L8.675 3l1.65 1.675L12 3l1.675 1.675L15.325 3L17 4.675L18.675 3l1.65 1.675L22 3v16q0 .825-.587 1.413Q20.825 21 20 21Zm0-2h7v-6H4v6Zm9 0h7v-2h-7Zm0-4h7v-2h-7Zm-9-4h16V8H4Z"
							/>
						{:else if links.name == 'Inbox'}
							<rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M5 21q-.825 0-1.413-.587Q3 19.825 3 19V5q0-.825.587-1.413Q4.175 3 5 3h14q.825 0 1.413.587Q21 4.175 21 5v14q0 .825-.587 1.413Q19.825 21 19 21Zm7-5q.95 0 1.725-.55Q14.5 14.9 14.8 14H19V5H5v9h4.2q.3.9 1.075 1.45Q11.05 16 12 16Zm0-2l-4-4l1.4-1.45l1.6 1.6V6h2v4.15l1.6-1.6L16 10Z"
							/>
						{:else if links.name == 'Invest'}
							<rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M298.9 24.31c-14.9.3-25.6 3.2-32.7 8.4l-97.3 52.1l-54.1 73.59c-11.4 17.6-3.3 51.6 32.3 29.8l39-51.4c49.5-42.69 150.5-23.1 102.6 62.6c-23.5 49.6-12.5 73.8 17.8 84l13.8-46.4c23.9-53.8 68.5-63.5 66.7-106.9l107.2 7.7l-1-112.09l-194.3-1.4zM244.8 127.7c-17.4-.3-34.5 6.9-46.9 17.3l-39.1 51.4c10.7 8.5 21.5 3.9 32.2-6.4c12.6 6.4 22.4-3.5 30.4-23.3c3.3-13.5 8.2-23 23.4-39zm-79.6 96c-.4 0-.9 0-1.3.1c-3.3.7-7.2 4.2-9.8 12.2c-2.7 8-3.3 19.4-.9 31.6c2.4 12.1 7.4 22.4 13 28.8c5.4 6.3 10.4 8.1 13.7 7.4c3.4-.6 7.2-4.2 9.8-12.1c2.7-8 3.4-19.5 1-31.6c-2.5-12.2-7.5-22.5-13-28.8c-4.8-5.6-9.2-7.6-12.5-7.6zm82.6 106.8c-7.9.1-17.8 2.6-27.5 7.3c-11.1 5.5-19.8 13.1-24.5 20.1c-4.7 6.9-5.1 12.1-3.6 15.2c1.5 3 5.9 5.9 14.3 6.3c8.4.5 19.7-1.8 30.8-7.3c11.1-5.5 19.8-13 24.5-20c4.7-6.9 5.1-12.2 3.6-15.2c-1.5-3.1-5.9-5.9-14.3-6.3c-1.1-.1-2.1-.1-3.3-.1zm-97.6 95.6c-4.7.1-9 .8-12.8 1.9c-8.5 2.5-13.4 7-15 12.3c-1.7 5.4 0 11.8 5.7 18.7c5.8 6.8 15.5 13.3 27.5 16.9c11.9 3.6 23.5 3.5 32.1.9c8.6-2.5 13.5-7 15.1-12.3c1.6-5.4 0-11.8-5.8-18.7c-5.7-6.8-15.4-13.3-27.4-16.9c-6.8-2-13.4-2.9-19.4-2.8z"
							/>
						{:else if links.name == 'Markets'}
							<rect x="0" y="0" width="48" height="48" fill="none" stroke="none" /><g
								fill="none"
								stroke="currentColor"
								stroke-linejoin="round"
								stroke-width="4"
								><path d="M6 16h8v16H6z" /><path stroke-linecap="round" d="M10 6v10m0 16v10" /><path
									d="M34 16h8v16h-8z"
								/><path stroke-linecap="round" d="M38 6v10m0 16v10" /><path
									d="M20 14h8v16h-8z"
								/><path stroke-linecap="round" d="M24 4v10m0 16v10" /></g
							>
						{:else if links.name == 'Withdraw'}
							<rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M258 21.89c-.5 0-1.2 0-1.8.12c-4.6.85-10.1 5.1-13.7 14.81c-3.8 9.7-4.6 23.53-1.3 38.34c3.4 14.63 10.4 27.24 18.2 34.94c7.6 7.7 14.5 9.8 19.1 9c4.8-.7 10.1-5.1 13.7-14.7c3.8-9.64 4.8-23.66 1.4-38.35c-3.5-14.8-10.4-27.29-18.2-34.94c-6.6-6.8-12.7-9.22-17.4-9.22zM373.4 151.4c-11 .3-24.9 3.2-38.4 8.9c-15.6 6.8-27.6 15.9-34.2 24.5c-6.6 8.3-7.2 14.6-5.1 18.3c2.2 3.7 8.3 7.2 20 7.7c11.7.7 27.5-2.2 43-8.8c15.5-6.7 27.7-15.9 34.3-24.3c6.6-8.3 7.1-14.8 5-18.5c-2.1-3.8-8.3-7.1-20-7.5c-1.6-.3-3-.3-4.6-.3zm-136.3 92.9c-6.6.1-12.6.9-18 2.3c-11.8 3-18.6 8.4-20.8 14.9c-2.5 6.5 0 14.3 7.8 22.7c8.2 8.2 21.7 16.1 38.5 20.5c16.7 4.4 32.8 4.3 44.8 1.1c12.1-3.1 18.9-8.6 21.1-15c2.3-6.5 0-14.2-8.1-22.7c-7.9-8.2-21.4-16.1-38.2-20.4c-9.5-2.5-18.8-3.5-27.1-3.4zm160.7 58.1L336 331.7c4.2.2 14.7.5 14.7.5l6.6 8.7l54.7-28.5l-14.2-10zm-54.5.1l-57.4 27.2c5.5.3 18.5.5 23.7.8l49.8-23.6l-16.1-4.4zm92.6 10.8l-70.5 37.4l14.5 18.7l74.5-44.6l-18.5-11.5zm-278.8 9.1a40.33 40.33 0 0 0-9 1c-71.5 16.5-113.7 17.9-126.2 17.9H18v107.5s11.6-1.7 30.9-1.8c37.3 0 103 6.4 167 43.8c3.4 2.1 10.7 2.9 19.8 2.9c24.3 0 61.2-5.8 69.7-9C391 452.6 494 364.5 494 364.5l-32.5-28.4s-79.8 50.9-89.9 55.8c-91.1 44.7-164.9 16.8-164.9 16.8s119.9 3 158.4-27.3l-22.6-34s-82.8-2.3-112.3-6.2c-15.4-2-48.7-18.8-73.1-18.8z"
							/>
						{/if}
					</svg>
					<span class="text-center ml-4 text-base">{links.name}</span>
				</a>
			</div>
		{/each}
		<div class="grid grid-cols-4 gap-4 items-center align-middle mx-3 my-5">
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-yellow-300 md:ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="1.2rem" height="1.2rem" viewBox="0 0 24 24"
					><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
						fill="none"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M7 10v4h3v7h4v-7h3l1-4h-4V8a1 1 0 0 1 1-1h3V3h-3a5 5 0 0 0-5 5v2H7"
					/></svg
				>
			</div>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-yellow-300 md:ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="1.2rem" height="1.2rem" viewBox="0 0 24 24"
					><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
						fill="currentColor"
						d="m14.792 10.775l-3.668-2.112A1.417 1.417 0 0 0 9 9.89v4.222c-.003.506.267.974.706 1.224a1.41 1.41 0 0 0 1.419.002l3.667-2.112a1.413 1.413 0 0 0 0-2.45zm-.5 1.582l-3.666 2.113a.414.414 0 0 1-.419 0a.408.408 0 0 1-.207-.36V9.89a.408.408 0 0 1 .207-.359a.402.402 0 0 1 .418 0l3.667 2.113a.41.41 0 0 1 0 .714zM19 4H5a3.003 3.003 0 0 0-3 3v10a3.003 3.003 0 0 0 3 3h14a3.003 3.003 0 0 0 3-3V7a3.003 3.003 0 0 0-3-3zm2 13a2.003 2.003 0 0 1-2 2H5a2.003 2.003 0 0 1-2-2V7a2.003 2.003 0 0 1 2-2h14a2.003 2.003 0 0 1 2 2v10z"
					/></svg
				>
			</div>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-yellow-300 md:ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="1.2rem" height="1.2rem" viewBox="0 0 24 24"
					><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
						fill="currentColor"
						fill-rule="evenodd"
						d="M18.483 19.79v-.002l.018-.043L21.5 4.625v-.048c0-.377-.14-.706-.442-.903c-.265-.173-.57-.185-.784-.169a2.681 2.681 0 0 0-.586.12a3.23 3.23 0 0 0-.24.088l-.013.005l-16.72 6.559l-.005.002a1.353 1.353 0 0 0-.149.061a2.27 2.27 0 0 0-.341.19c-.215.148-.624.496-.555 1.048c.057.458.372.748.585.899a2.062 2.062 0 0 0 .403.22l.032.014l.01.003l.007.003l2.926.985c-.01.183.008.37.057.555l1.465 5.559a1.5 1.5 0 0 0 2.834.196l2.288-2.446l3.929 3.012l.056.024c.357.156.69.205.995.164c.305-.042.547-.17.729-.315a1.742 1.742 0 0 0 .49-.635l.008-.017l.003-.006l.001-.003ZM7.135 13.875a.3.3 0 0 1 .13-.33l9.921-6.3s.584-.355.563 0c0 0 .104.062-.209.353c-.296.277-7.071 6.818-7.757 7.48a.278.278 0 0 0-.077.136L8.6 19.434l-1.465-5.56Z"
						clip-rule="evenodd"
					/></svg
				>
			</div>
			<div
				class="bg-yellow-200 dark:bg-yellow-100/30 rounded-full items-center text-slate-900 dark:text-slate-50 text-center p-3 ring-1 ring-yellow-300 md:ring-transparent hover:ring-yellow-300 ring-offset-2 ring-offset-transparent"
			>
				<svg xmlns="http://www.w3.org/2000/svg" width="1.2rem" height="1.2rem" viewBox="0 0 256 256"
					><rect x="0" y="0" width="256" height="256" fill="none" stroke="none" /><path
						fill="currentColor"
						d="M243.7 70.5A4 4 0 0 0 240 68h-32.8a44 44 0 0 0-38.6-24A44.4 44.4 0 0 0 124 88v11.2c-44.1-9.4-80.8-45.7-81.2-46a3.9 3.9 0 0 0-6.7 2.1c-8.6 46.8 5.4 78.1 18.7 96.1a101.8 101.8 0 0 0 27.4 25.8c-15.7 20.4-43.3 30.9-43.6 31.1a4 4 0 0 0-2.4 2.5a3.8 3.8 0 0 0 .5 3.4c.2.4 2.8 4 9.5 7.4c8.5 4.2 19.9 6.4 33.8 6.4c68.9 0 126.5-53.5 131.6-122l31.2-31.2a3.8 3.8 0 0 0 .9-4.3Zm-38.8 30.9a4.2 4.2 0 0 0-1.2 2.6c-4.1 65.1-58.5 116-123.7 116c-17.8 0-27.6-3.9-32.5-6.9c10.4-4.8 31.5-16.3 43.8-34.9a3.7 3.7 0 0 0 .6-3.2a4.2 4.2 0 0 0-2.1-2.6c-.2-.1-15.3-7.8-28.6-25.8C44.6 124 38.4 96.3 42.8 64c12.8 11.3 45.8 37.5 84.5 43.9a4.2 4.2 0 0 0 3.3-.8a4.1 4.1 0 0 0 1.4-3.1V88a36.4 36.4 0 0 1 36.5-36A36.1 36.1 0 0 1 201 73.6a3.9 3.9 0 0 0 3.7 2.4h25.6Z"
					/></svg
				>
			</div>
		</div>
	</div>
</div>

<style>
</style>
