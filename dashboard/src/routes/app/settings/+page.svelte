<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import { getStorage, setStorage } from '$lib/storage';
	import API from '$lib/api';
	import Ripple from '@smui/ripple';

	let mode: any,
		token: any,
		theme = () => {},
		magic = '<<token>>',
		id = 'Loading ....',
		getOS = () => {},
		copy = (ele: string) => {};

	onMount(() => {
		theme = () => {
			//@ts-ignore
			const mode = document.querySelector('#theme')!.value;
			setStorage('mode', mode);
			if (mode == 'dark') {
				document.documentElement.classList.add(mode);
			} else {
				document.documentElement.classList.remove('dark');
			}
		};
		token = getStorage('token') || '';
		mode = getStorage('mode') || 'light';
		getOS = () => {
			//@ts-ignore
			var uA = navigator.userAgent || navigator.vendor || window.opera;
			if (
				//@ts-ignore
				(/iPad|iPhone|iPod/.test(uA) && !window.MSStream) ||
				(uA.includes('Mac') && 'ontouchend' in document)
			)
				return 'iPhone';

			var i,
				os = ['Windows', 'Android', 'Unix', 'Mac', 'Linux', 'BlackBerry'];
			for (i = 0; i < os.length; i++) if (new RegExp(os[i], 'i').test(uA)) return os[i];
		};
		copy = (ele: string) => {
            var element = document.getElementById(ele)!;
            console.log(element)
			element.select();
			// element.setSelectionRange(0, 999999);
			// navigator.clipboard.writeText(`https://app.cryptflixinvest.com/?/${magic}`);
		};
	});
</script>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-3 pt-3 md:pt-5"
>
	<div class="override">
		<div
			class="grid gap-6 lg:gap-8 grid-cols-1 justify-between align-middle items-center my-4 mt-2 mx-2 lg:mx-5"
		>
			<div class="">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">Theme</p>
				<p class="text-gray-400 text-sm">Change the app appearance</p>
			</div>
			<div class="flex flex-row items-center align-middle justify-between my-1 md:my-3 lg:mx-10">
				<div>
					<p>Select app theme</p>
				</div>
				<div>
					<labal for="theme" class="peer-hover:opacity-100 opacity-75 hover:opacity-100">
						<div class="relative flex items-center align-center text-slate-700 dark:text-slate-50">
							<span
								class="inline-flex left-3 absolute pointer-events-none text-slate-700 dark:text-slate-50"
							>
								<svg
									fill="none"
									height="16"
									shape-rendering="geometricPrecision"
									stroke="currentColor"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="1.5"
									viewBox="0 0 24 24"
									width="16"
									style="color: currentcolor;"
								>
									{#if mode == 'dark'}
										<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
									{:else}
										<circle cx="12" cy="12" r="5" /><path d="M12 1v2" /><path d="M12 21v2" /><path
											d="M4.22 4.22l1.42 1.42"
										/><path d="M18.36 18.36l1.42 1.42" /><path d="M1 12h2" /><path
											d="M21 12h2"
										/><path d="M4.22 19.78l1.42-1.42" /><path d="M18.36 5.64l1.42-1.42" />
									{/if}
								</svg>
							</span>
							<select
								on:change={(e) => {
									theme();
								}}
								bind:value={mode}
								id="theme"
								class="text-sm h-8 leading-5 px-12 cursor-pointer appearance-none rounded-md text-slate-700 dark:text-slate-50 border border-solid border-color bg-white dark:bg-black transition-all duration-500 pr-[calc(1.5_*_32px)] pl-[calc(1.5_*_24px)] py-0"
							>
								<option value="light">Light</option>
								<option value="dark">Dark</option>
							</select>
							<span
								class="absolute right-3 inline-flex pointer-events-none text-slate-700 dark:text-slate-50"
							>
								<svg
									fill="none"
									height="16"
									shape-rendering="geometricPrecision"
									stroke="currentColor"
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="1.5"
									viewBox="0 0 24 24"
									width="16"
									style="color: currentcolor;"
									><path d="M17 8.517L12 3 7 8.517M7 15.48l5 5.517 5-5.517" /></svg
								>
							</span>
						</div>
					</labal>
				</div>
			</div>
			<div class="mt-4 pt-3">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">account Security</p>
				<p class="text-gray-400 text-sm">Secure your account</p>
			</div>
			<div class="mt-4 pt-3">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">my Device</p>
				<p class="text-gray-400 text-sm">About my device</p>
				<div
					class="grid grid-cols-2  items-center align-middle justify-between my-2 pt-2 md:my-3 lg:mx-10"
				>
					<div>
						<p>APP Version</p>
					</div>
					<div class="text-right">
						<p class="mr-1">V1.0.0</p>
					</div>
					<div class="my-1 mt-2 py-1 pt-2">
						<p>Device Name</p>
					</div>
					<div class="text-right my-1 mt-2 py-1 pt-2">
						<p class="mr-1">{getOS()}</p>
					</div>
					<div class="my-1 py-1">
						<p>Device ID</p>
					</div>
					<div class="text-right my-1 py-1">
						<p class="mr-1">{id}</p>
					</div>
				</div>
			</div>
			<div class="mt-4 pt-3">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">secure token</p>
				<p class="text-gray-400 text-sm">Generate magic login token</p>
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<p
					on:click={() => {
						copy('link');
					}}
					id="link"
					class="text-center mt-3 rounded-full bg-gray-300 dark:bg-accent cursor-pointer py-2"
					use:Ripple={{ surface: true, color: 'secondary' }}
					tabindex="0"
				>
					https://app.cryptflixinvest.com/?/{magic}
				</p>
			</div>
			<div class="flex flex-row items-center align-middle justify-between my-1 md:my-3 lg:mx-20">
				<div />
				<div>
					<button
						class="bg-blue-600 text-white rounded-full text-sm p-1.5 px-5 ring-offset-2 hover:ring-2 ring-blue-500 hover:shadow-lg"
						>Generate</button
					>
				</div>
			</div>
			<div class="mt-4 pt-3">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">newsletter</p>
				<p class="text-gray-400 text-sm">Subscribe to our newsletters</p>
			</div>
			<div class="mt-4 pt-3">
				<button
					use:Ripple={{ surface: true, color: 'secondary' }}
					tabindex="0"
					class="w-full border border-solid rounded-lg border-red-500 mx-auto p-3 text-center bg-red-100 text-red-500 dark:bg-red-100/30 text-lg uppercase"
					>Delete Account</button
				>
			</div>
		</div>
	</div>
</div>
