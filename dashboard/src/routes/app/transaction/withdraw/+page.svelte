<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import Ripple from '@smui/ripple';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let msg: string,
		err: boolean,
		alert: boolean,
		verify = true,
		proceed = false,
		code: string,
		load__ = false,
		wallet = data.user.wallet,
		address = '',
		token: string,
		amount = '',
		hidden = false;

	var toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		},
		wallets = [
			{
				name: 'Bitcoin',
				svg: '0 0 32 32',
				abbr: 'BTC'
			},
			{
				name: 'USDT',
				svg: '0 0 32 32',
				abbr: 'USDT'
			},
			{
				name: 'Ethereum',
				svg: '0 0 256 417',
				abbr: 'ETH'
			}
		],
		coin = 'BTC',
		swi = (abbr: string) => {
			coin = abbr;
		},
		proceeds = async () => {
			if (amount == '' || address == '') return;
			var con = data.user.balance.split('$')[1];
			if (data.user.plan == 'Plan 1') {
				toast('Account still on demo, Upgrade your account', true);
				return;
			}
			if (amount > con) {
				toast('Available balance too low', true);
				return;
			}
			hidden = true;
			try {
				const req = await API.post(
					'/add_trans',
					JSON.stringify({
						uuid: '******',
						amount: `-$${amount}`,
						address: address,
						wallet: data.user.wallet,
						type: 'Withdrawal',
						coin: coin
					}),
					{
						Authorization: token
					}
				);
				if ('status' in req) {
					toast(req.message, !req.status);
					hidden = false;
				}
				//@ts-ignore
				if(req.status) data.user.balance = `$${con - amount}.00`;
			} catch (err: any) {
				toast('Withdrawal failed', true);
				hidden = false;
			}
		};
	onMount(() => {
		token = getStorage('token') ?? '';
	});
</script>

<svelte:head>
	<title>Withdrawal | cryptoflixinvest.org</title>
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div
		class="flex rounded-lg shadow-lg bg-gray-100 dark:bg-accent border border-solid border-color flex-row md:mr-2 override w-full items-center align-middle justify-between mb-4 p-4"
	>
		<div class="w-auto">
			<p
				class="font-nunito lg:pl-8 text-xl lg:text-2xl font-bold uppercase text-black dark:text-white"
			>
				Account Balance
			</p>
		</div>
		<div>
			<p
				class="font-nunito lg:pl-8 text-xl lg:text-2xl font-bold uppercase text-black dark:text-white"
			>
				{data.user.balance}
			</p>
		</div>
	</div>
	<div class="my-4 py-2 md:pl-3">
		<p class="text-xl text-center md:text-left font-medium font-mono uppercase">
			Withdrawal Request
		</p>
	</div>
	<div class="w-9/10 md:w-[85%] mx-auto">
		<div class="my-4 py-3 flex flex-col md:flex-row justify-between items-center align-middle">
			<div class="py-1 my-2 w-full md:mx-2">
				<label for="wallet" class="block mb-2 text-base font-mono">Your Account Wallet</label>
				<input
					disabled
					type="text"
					name="wallet"
					id=""
					bind:value={wallet}
					class="w-full py-2.5 pl-2 truncate rounded-lg border-2 dark:bg-accent border-solid border-color"
				/>
			</div>
			<div class="py-1 my-2 w-full md:mx-2">
				<label for="amount" class="block mb-2 text-base font-mono">Amount</label>
				<input
					type="number"
					name="amount"
					step="any"
					pattern="\d+"
					id=""
					bind:value={amount}
					class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
				/>
			</div>
			<div class="py-1 my-2 w-full md:mx-2">
				<label for="amount" class="block mb-2 text-base font-mono">Your {coin} Address</label>
				<input
					type="text"
					name="address"
					id=""
					bind:value={address}
					class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
				/>
			</div>
		</div>
		<div class="my-2 py-1">
			<div class="grid grid-cols-3 gap-2 md:gap-3 lg:gap-6 py-2 pb-8">
				{#each wallets as option}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						on:click={() => {
							swi(option.abbr);
						}}
						class="border-solid trnasition-all duration-200 rounded-lg bg-slate-200 dark:bg-accent border-color {coin ==
						option.abbr
							? 'border-4 cursor-not-allowed'
							: 'cursor-pointer border'}"
					>
						<div
							class="p-2 text-center rounded-lg flex flex-row justify-center md:justify-between align-middle items-center"
						>
							<div>
								<svg
									class="w-9 h-9"
									xmlns="http://www.w3.org/2000/svg"
									width="32"
									height="32"
									viewBox={option.svg}
								>
									{#if option.name == 'Bitcoin'}
										<g fill="none" fill-rule="evenodd"
											><circle cx="16" cy="16" r="16" fill="#F7931A" /><path
												fill="#FFF"
												fill-rule="nonzero"
												d="M23.189 14.02c.314-2.096-1.283-3.223-3.465-3.975l.708-2.84l-1.728-.43l-.69 2.765c-.454-.114-.92-.22-1.385-.326l.695-2.783L15.596 6l-.708 2.839c-.376-.086-.746-.17-1.104-.26l.002-.009l-2.384-.595l-.46 1.846s1.283.294 1.256.312c.7.175.826.638.805 1.006l-.806 3.235c.048.012.11.03.18.057l-.183-.045l-1.13 4.532c-.086.212-.303.531-.793.41c.018.025-1.256-.313-1.256-.313l-.858 1.978l2.25.561c.418.105.828.215 1.231.318l-.715 2.872l1.727.43l.708-2.84c.472.127.93.245 1.378.357l-.706 2.828l1.728.43l.715-2.866c2.948.558 5.164.333 6.097-2.333c.752-2.146-.037-3.385-1.588-4.192c1.13-.26 1.98-1.003 2.207-2.538zm-3.95 5.538c-.533 2.147-4.148.986-5.32.695l.95-3.805c1.172.293 4.929.872 4.37 3.11zm.535-5.569c-.487 1.953-3.495.96-4.47.717l.86-3.45c.975.243 4.118.696 3.61 2.733z"
											/></g
										>
									{:else if option.name == 'Ethereum'}
										<path
											fill="#343434"
											d="m127.961 0l-2.795 9.5v275.668l2.795 2.79l127.962-75.638z"
										/><path fill="#8C8C8C" d="M127.962 0L0 212.32l127.962 75.639V154.158z" /><path
											fill="#3C3C3B"
											d="m127.961 312.187l-1.575 1.92v98.199l1.575 4.601l128.038-180.32z"
										/><path fill="#8C8C8C" d="M127.962 416.905v-104.72L0 236.585z" /><path
											fill="#141414"
											d="m127.961 287.958l127.96-75.637l-127.96-58.162z"
										/><path fill="#393939" d="m.001 212.321l127.96 75.637V154.159z" />
									{:else if option.name == 'USDT'}
										<g fill="none" fill-rule="evenodd"
											><circle cx="16" cy="16" r="16" fill="#26A17B" /><path
												fill="#FFF"
												d="M17.922 17.383v-.002c-.11.008-.677.042-1.942.042c-1.01 0-1.721-.03-1.971-.042v.003c-3.888-.171-6.79-.848-6.79-1.658c0-.809 2.902-1.486 6.79-1.66v2.644c.254.018.982.061 1.988.061c1.207 0 1.812-.05 1.925-.06v-2.643c3.88.173 6.775.85 6.775 1.658c0 .81-2.895 1.485-6.775 1.657m0-3.59v-2.366h5.414V7.819H8.595v3.608h5.414v2.365c-4.4.202-7.709 1.074-7.709 2.118c0 1.044 3.309 1.915 7.709 2.118v7.582h3.913v-7.584c4.393-.202 7.694-1.073 7.694-2.116c0-1.043-3.301-1.914-7.694-2.117"
											/></g
										>
									{/if}
								</svg>
							</div>
							<div>
								<p class="uppercase hidden md:block text-xl font-mono font-medium">{option.name}</p>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
		<div class="my-2 py-3 {hidden ? 'hidden' : ''}">
			<div class="intro-y flex items-center justify-center mt-5 group/item">
				<a
					on:click={(e) => {
						e.preventDefault(), proceeds();
					}}
					class="transition p-4 w-full theme-text-app font-medium rounded-lg flex items-center justify-around bg-yellow-100 dark:bg-yellow-100/30 hover:ring-yellow-200 ring-2 ring-offset-2 ring-offset-transparent ring-transparent"
					href="/transaction/withdraw"
					>Proceed <svg
						viewBox="0 0 24 24"
						aria-hidden="true"
						focusable="false"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="inline-block overflow-hidden animate-bounce-x transition-all duration-200 align-middle w-6 h-6"
						><line x1="5" x2="19" y1="12" y2="12" /><polyline points="12 5 19 12 12 19" /></svg
					></a
				>
			</div>
		</div>
	</div>
</div>
{#if proceed}
	<div
		in:fly={{ y: 200 }}
		out:fly={{ y: -200 }}
		tabindex="-1"
		class="fixed top-0 bottom-0 left-0 right-0 z-[999999] w-full p-4 bg-black/50 backdrop-blur-sm overflow-x-hidden overflow-y-auto md:inset-0 h-modal md:h-full"
	>
		<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
		<div class="relative w-full mx-auto my-auto h-full max-w-md md:h-auto">
			<div
				class="relative top-1/2 bg-white rounded-lg border border-solid border-color shadow-lg dark:shadow-md dark:bg-black"
			>
				<div
					class="flex items-center justify-between p-5 border-b border-solid border-color rounded-t-lg"
				>
					<h3 class="text-xl font-medium text-center font-mono">Authorize Withdrawal</h3>
					<button
						on:click={() => (proceed = false)}
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
					<p class="text-center pb-4 font-semibold text-sm font-open">
						Authorization code has been sent to the email associated with this account
					</p>
					<input
						type="text"
						bind:value={code}
						placeholder="Verification Code"
						class="rounded-md pl-2 border-solid border-color border w-9/10 mx-4 py-2 bg-transparent"
					/>
				</div>
				<div
					class="grid grid-cols-2 items-center align-middle mt-2 border-t border-solid border-color"
				>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						on:click={() => (proceed = false)}
						class="text-gray-400 py-4 text-center text-base border-r border-solid border-color"
						>Cancel</button
					>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						class="text-black dark:text-white py-4 text-center text-base border-l border-solid border-color"
					>
						{#if !load__}
							<span>Withdraw</span>
						{:else}
							<Loader width={'20px'} height={'20px'} />
						{/if}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
