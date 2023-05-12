<script lang="ts">
	import { fly } from 'svelte/transition';
	import type { PageData } from '../../$types';
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import gravatar from 'gravatar';
	import { onMount } from 'svelte';
	import Alert from '$lib/Alert.svelte';

	export let data: PageData;

	let token: string,
		name = data.user.name,
		email = data.user.email,
		deposit = data.user.deposit,
		balance = data.user.balance,
		status = data.user.status,
		plan = data.user.type,
		msg: string,
		err: boolean,
		aler: boolean,
		loading = false,
		dp = (email: string) => {
			var url = gravatar.url(email, { s: '50', r: 'x', d: 'robohash', f: 'y' }, true);
			return url;
		},
		update = async () => {
			loading = true;
			try {
				const todate = await API.post('/admin/update', JSON.stringify({id: data.user.id, status: status, deposit: deposit, balance: balance, plan: plan}), {Authorization: token})
				toast(todate.message, !todate.status);
				loading = false;
			} catch (err: any) {
				loading = false;
				console.log(err)
				toast(err.message, true);
			}
		};
	var toast = (message: any, error: boolean) => {
		msg = message;
		err = error;
		aler = true;
		setTimeout(() => (aler = false), 4400);
	};

	onMount(() => {
		token = getStorage('token') ?? '';
	});
</script>

<svelte:head>
	<title>{data.user.title} | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert alert={aler} message={msg} error={err} onClose={() => (aler = false)} />
	<div class="override">
		<div class="w-full mb-8 mt-2">
			<div
				class="rounded-full w-36 h-36 mx-auto p-2 border-solid border-color border bg-transparent flex justify-center items-center m-1 object-contain"
			>
				<img
					class="w-36 h-36"
					loading="lazy"
					src={dp(data.user.email)}
					srcset={`${dp(data.user.email)} 2x`}
					alt={`${data.user.name} profile pics`}
				/>
			</div>
		</div>
		<div class="rounded-md border-solid border-color border py-4 mb-6">
			<div class="bg-slate-100 dark:bg-accent py-3 w-full rounded-sm">
				<p class="text-center font-medium uppercase text-xs sm:text-sm md:text-base lg:text-lg">
					Created account on {data.user.created ?? '12/01/2023 at 12:48:01'}
				</p>
			</div>
			<div
				class="grid my-4 grid-cols-1 md:grid-cols-2 gap-8 align-middle items-basline justify-between"
			>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="display" class="block mb-2 text-base font-nunito text-center"
						>User Display Name</label
					>
					<input
						type="text"
						name="display"
						id=""
						disabled
						bind:value={name}
						class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
					/>
				</div>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="email" class="block mb-2 text-base font-nunito text-center"
						>User Email Address</label
					>
					<input
						type="text"
						name="email"
						id=""
						disabled
						bind:value={email}
						class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
					/>
				</div>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="deposit" class="block mb-2 text-base font-nunito text-center"
						>User Total Deposit</label
					>
					<input
						type="text"
						name="deposit"
						id=""
						bind:value={deposit}
						class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
					/>
				</div>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="balance" class="block mb-2 text-base font-nunito text-center"
						>User Total Balance</label
					>
					<input
						type="text"
						name="balance"
						id=""
						bind:value={balance}
						class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
					/>
				</div>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="plan" class="block mb-2 text-base font-nunito text-center">Company Plan</label
					>
					<select
						bind:value={plan}
						id="plan"
						class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-gray-400 dark:border-gray-300 border-solid focus:outline-none focus:ring-0 focus:border-gray-200 peer"
					>
						<option value="Plan 1">Plan 1</option>
						<option value="Plan 2">Plan 2</option>
						<option value="Plan 3">Plan 3</option>
						<option value="V I P">V I P</option>
						<option value="Share 1">Share 1</option>
						<option value="Share 2">Share 2</option>
					</select>
				</div>
				<div class="py-1 w-9/10 md:w-full md:px-2 mx-auto">
					<label for="status" class="block mb-2 text-base font-nunito text-center"
						>User Account Status</label
					>
					<select
						bind:value={status}
						id="status"
						class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-solid border-gray-700 appearance-none dark:text-gray-400 dark:border-gray-300 focus:outline-none focus:ring-0 focus:border-gray-200 peer"
					>
						<option value="verified">Verified</option>
						<option value="suspended">Suspended</option>
					</select>
				</div>
			</div>
			<div class="py-3 my-2 px-2 flex flex-row justify-between items-center align-middle">
				<div class="">
					<p class="block mb-2 text-base font-mono">Country</p>
					<div class="flex flex-row justify-start items-center align-middle">
						<div class="iti__flag iti__{data.user.country} mr-1 h-scale" />
						<span>{data.user.country.toUpperCase()}</span>
					</div>
				</div>
				<div class="">
					<p class="block mb-2 text-base font-mono">Referrals</p>
					<p>
						{Number(data.user.referral) > 1
							? `${data.user.referral} Referral's`
							: `${data.user.referral} Referral`}
					</p>
				</div>
			</div>
			<button
				on:click={update}
				class="bg-yellow-100 my-4 w-full text-center px-3.5 py-3 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
			>
				{#if loading}
					<Loader width={'20px'} height={'20px'} />
				{:else}
					Update
				{/if}
			</button>
		</div>
	</div>
</div>
