<script lang="ts">
	import { fly, slide } from 'svelte/transition';
	import { onMount } from 'svelte';
	import { getStorage, setStorage } from '$lib/storage';
	import API from '$lib/api';
	import Ripple from '@smui/ripple';
	import Switch from '@smui/switch';
	import FormField from '@smui/form-field';
	import Alert from '$lib/Alert.svelte';
	import Loader from '$lib/Loader.svelte';
	import { goto } from '$app/navigation';

	let mode: any,
		token: string = '',
		theme = () => {},
		magic = '<<token>>',
		id = 'Loading ....',
		getOS = () => {},
		copy = () => {},
		on: boolean = true,
		click = false,
		mail = false,
		plan = '',
		load = true,
		withdraw = true,
		news = true,
		del = false,
		delin = false;

	let msg: string,
		err: boolean,
		alert: boolean,
		pass: string = '';

	var gen = async () => {
			load = false;
			try {
				const req = await API.post('/magic_auth', JSON.stringify({}), { Authorization: token });
				if (req.status) magic = req.token;
				load = true;
			} catch (err) {
				load = true;
				console.log(err);
			}
		},
		verify = () => {
			alert = false;
			if (plan !== 'Share 2') {
				mail = false;
				toast('Upgrade your account', !mail);
			}
		},
		toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		},
		del_user = async () => {
			if (pass == '') {
				toast('Enter your password', true);
				return;
			}
			delin = true;
			try {
				const del = await API.post('/remove', JSON.stringify({ password: pass }), {
					Authorization: token
				});
				toast(del.message, !del.status);
				delin = false;
				if (del.status) setTimeout(() => goto('/0auth/logout', { replaceState: true }), 4000);
			} catch (err) {
				delin = false;
				//@ts-ignore
				toast(err.message, true);
			}
		};

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
		copy = () => {
			navigator.clipboard.writeText(`https://app.cryptflixinvest.com/?/${magic}`);
			click = true;
			setTimeout(() => (click = false), 2000);
		};
	});
</script>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-3 pt-3 md:pt-5"
>
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
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
				<div
					class="grid grid-cols-2  items-center align-middle justify-between my-2 pt-2 md:my-3 lg:mx-10"
				>
					<div>
						<p>Withdrawal Passcode</p>
					</div>
					<div class="text-right my-1 py-1">
						<div class="ml-1">
							<FormField align="end">
								<Switch color="secondary" bind:checked={withdraw} />
							</FormField>
						</div>
					</div>
					<div>
						<p>Login Verification Mail</p>
					</div>
					<div class="text-right my-1 py-1">
						<div class="ml-1">
							<FormField align="end">
								<Switch
									color="secondary"
									on:SMUISwitch:change={(e) => verify()}
									bind:checked={mail}
									on:click={() => {
										verify();
									}}
								/>
							</FormField>
						</div>
					</div>
				</div>
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
						<p class="mr-1">v1.25.0</p>
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
					<div class="my-1 py-1">
						<p>Auto Save Changes</p>
					</div>
					<div class="text-right my-1 py-1">
						<div class="ml-1">
							<FormField align="end">
								<Switch disabled={true} color="secondary" bind:checked={on} />
							</FormField>
						</div>
					</div>
					<div class="my-1 mt-2 py-1 pt-2">
						<p>Language</p>
					</div>
					<div class="text-right my-1 mt-2 py-1 pt-2">
						<p class="mr-1">English</p>
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
						copy();
					}}
					id="link"
					class="text-center mt-8 truncate rounded-full bg-gray-300 border-solid border border-color dark:bg-accent cursor-pointer py-2 px-1"
					use:Ripple={{ surface: true, color: 'secondary' }}
					tabindex="0"
				>
					https://app.cryptflixinvest.com/magic/{magic}
				</p>
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<p
					on:click={() => {
						copy();
					}}
					class="text-center text-gray-400 py-2 cursor-pointer"
				>
					{click ? 'Copied ✔' : 'Click to copy'}
				</p>
			</div>
			<div
				class="grid grid-cols-3 gap-2 md:gap-4 lg:grid-cols-5 items-center align-middle justify-between my-1 md:my-3 lg:mx-10"
			>
				<div class="col-span-2 lg:col-span-4">
					<input
						disabled
						class="border-solid text-xs md:text-sm bg-slate-400 dark:bg-accent border border-color rounded-full py-2 w-full pl-2"
						type="text"
						bind:value={magic}
						id="magic"
					/>
				</div>
				<div>
					<button
						on:click={gen}
						class="bg-blue-600 text-white rounded-full w-full ml-1 md:ml-2 text-sm py-1.5 md:py-2.5 float-right px-5 ring-offset-2 hover:ring-2 ring-blue-500 hover:shadow-lg"
					>
						{#if load}
							<span>Generate</span>
						{:else}
							<Loader width={'20px'} height={'20px'} />
						{/if}
					</button>
				</div>
			</div>
			<div class="mt-4 pt-3">
				<p class="text-xl lg:text-3xl font-bold font-mono uppercase">newsletter</p>
				<p class="text-gray-400 text-sm">Subscribe to our newsletters</p>
				<div
					class="grid grid-cols-2  items-center align-middle justify-between my-2 pt-2 md:my-3 lg:mx-10"
				>
					<div>
						<p>In For News Update</p>
					</div>
					<div class="text-right">
						<div class="ml-1">
							<FormField align="end">
								<Switch color="secondary" bind:checked={news} />
							</FormField>
						</div>
					</div>
				</div>
			</div>
			<div class="mt-4 pt-3">
				<button
					on:click={() => (del = true)}
					use:Ripple={{ surface: true, color: 'secondary' }}
					tabindex="0"
					class="w-full border border-solid rounded-lg border-red-500 mx-auto p-3 text-center bg-red-100 text-red-500 dark:bg-red-100/30 text-lg uppercase"
					>Delete Account</button
				>
			</div>
		</div>
	</div>
</div>
{#if del}
	<div
		in:fly={{ y: 200 }}
		out:fly={{ y: -400 }}
		tabindex="-1"
		class="fixed top-0 bottom-0 left-0 right-0 z-[999999] w-full p-4 bg-black/50 backdrop-blur-sm overflow-x-hidden overflow-y-auto md:inset-0 h-modal md:h-full"
	>
		<div class="relative w-full mx-auto my-auto h-full max-w-md md:h-auto">
			<div
				class="relative top-1/2 bg-white rounded-lg border border-solid border-color shadow-lg dark:shadow-md dark:bg-black"
			>
				<div
					class="flex items-center justify-between p-5 border-b border-solid border-color rounded-t-lg"
				>
					<h3 class="text-xl font-medium text-center text-[red] font-mono">Dangerous Action</h3>
					<button
						on:click={() => (del = false)}
						type="button"
						class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white"
					>
						<svg
							aria-hidden="true"
							class="w-5 h-5"
							fill="currentColor"
							viewBox="0 0 20 20"
							xmlns="http://www.w3.org/2000/svg"
							><path
								fill-rule="evenodd"
								d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
								clip-rule="evenodd"
							/></svg
						>
						<span class="sr-only">Close modal</span>
					</button>
				</div>
				<div class="py-3">
					<p class="text-center pb-4 font-semibold font-open">Please Enter Your Password</p>
					<input
						type="text"
						bind:value={pass}
						class="rounded-md border-solid border-color border w-9/10 mx-4 py-2 bg-transparent"
					/>
				</div>
				<div
					class="grid grid-cols-2 items-center align-middle mt-2 border-t border-solid border-color"
				>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						on:click={() => (del = false)}
						class="text-gray-400 py-4 text-center text-base border-r border-solid border-color"
						>Cancel</button
					>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						on:click={del_user}
						class="text-[red] py-4 text-center text-base border-l border-solid border-color"
					>
						{#if !delin}
							<span>Delete</span>
						{:else}
							<Loader width={'20px'} height={'20px'} />
						{/if}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
