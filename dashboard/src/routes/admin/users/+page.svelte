<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import gravatar from 'gravatar';

	let loading = true,
		token: string,
		error = true,
		empty = false,
		find: boolean,
		fetch_users = async () => {
			loading = true;
			try {
				users = [];
				const fetch = await API.post('/users__', JSON.stringify({ uuid: '******' }), {
					Authorization: token
				});
				if (!fetch.status) {
					empty = true;
					error = true;
					loading = false;
					return;
				}
				users = [...users, fetch.users];
				setTimeout(() => {
					error = false;
					loading = false;
					find = true;
				}, 3000);
			} catch (err) {
				error = true;
				loading = false;
			}
		},
		users: any[] = [],
		dp = (email: string) => {
			var url = gravatar.url(email, { s: '50', r: 'x', d: 'robohash', f: 'y' }, true);
			return url;
		};

	onMount(() => {
		token = getStorage('token') ?? '';
		fetch_users();
	});
</script>

<svelte:head>
	<title>Users List | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<div class="override">
		{#if error}
			{#if loading}
				<div class="mt-10 pt-8" out:fly={{ y: -400 }}>
					<Loader width={'50px'} height={'50px'} />
					<p class="text-center pt-8">Loading List Of Users ......</p>
				</div>
			{:else}
				<div class="text-center mt-8">
					<p class="text-sm font-open">
						{empty ? 'No Registered User' : "Error: Can't Load List Of Users"}
					</p>
					<button
						on:click={fetch_users}
						class="bg-yellow-100 my-4 px-3.5 py-1 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
						>Retry</button
					>
				</div>
			{/if}
		{:else if find && !error}
			{#each users[0] as user}
				<div
					class="grid grid-cols-1 md:grid-cols-2 align-middle items-baseline gap-8 justify-evenly"
				>
					<div
						in:fly={{ y: 400 }}
						class="bg-white w-full dark:hover:bg-accent my-6 override hover:bg-slate-50 cursor-pointer dark:bg-black rounded-md border-color border-solid border p-2 shadow-lg dark:shadow-md hover:shadow-xl dark:hover:shadow-lg dark:hover:shadow-slate-100/30 dark:shadow-slate-100/30 py-4"
					>
						<div class="flex flex-row justify-between align-middle items-center">
							<div class="flex flex-nowrap align-middle items-center">
								<div
									class="rounded-full p-2 border-solid border-color border bg-transparent flex justify-center items-center m-1 object-contain"
								>
									<img
										class="w-10 h-10"
										loading="lazy"
										src={dp(user.email)}
										srcset={`${dp(user.email)} 2x`}
										alt={`${user.name} profile pics`}
									/>
								</div>
								<div class="ml-2 overflow-hidden">
									<div
										class="p-0 m-0 font-nunito text-black dark:text-white uppercase text-base md:text-xl overflow-hidden font-semibold text-ellipsis whitespace-nowrap"
									>
										{user.name}
									</div>
									<div
										class="m-0 p-0 uppercase font-nunito opacity-70 text-sm overflow-hidden font-semibold text-ellipsis whitespace-nowrap mt-2"
									>
										{user.a_type}
									</div>
								</div>
							</div>
							<div class="flex flex-col items-end align-middle gap-4">
								<p class="text-sm font-open">
									<a href={`./edit/${user.uuid}`} class="theme-text-app hover:underline"
										>Edit User</a
									>
								</p>
								<div class="flex flex-row justify-start items-center align-middle">
									<div class="iti__flag iti__{user.country ? user.country : 'us'} mr-1 h-scale" />
									<span class="text-sm">{user.country.toUpperCase()}</span>
								</div>
							</div>
						</div>
						<div class="mt-3 mb-0.5 flex flex-row items-center align-middle justify-between">
							<p class="text-sm font-open">
								<a href={`./history/${user.uuid}`} class="theme-text-app hover:underline"
									>Transaction History</a
								>
							</p>
							<p class="text-sm font-open">
								<a href={`./deposit/${user.uuid}`} class="theme-text-app hover:underline"
									>Add Deposit</a
								>
							</p>
						</div>
					</div>
				</div>
			{/each}
		{:else}
			<p class="text-lg font-semibold mt-16 text-center font-mono">No Registered User</p>
		{/if}
	</div>
</div>
