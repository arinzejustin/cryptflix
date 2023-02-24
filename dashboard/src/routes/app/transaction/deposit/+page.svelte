<script lang="ts">
	import { fly } from 'svelte/transition';
	import { BTC_WALLET, ETH_WALLET, USDT_WALLET } from '$lib/env';

	let wallets = [
		{
			name: 'Bitcoin',
			wallet: BTC_WALLET
		},
		{
			name: 'USDT',
			wallet: ETH_WALLET
		},
		{
			name: 'Ethereum',
			wallet: USDT_WALLET
		}
	];
</script>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-3 pt-3 md:pt-5"
>
	<div class="override">
		<div class="py-2">
			<p class="text-3xl uppercase pb-2 font-bold">Invest</p>
			<p class="text-sm text-gray-400">
				Take a bold towards making yourself <span class="text-[green]">100%</span> financially stable
			</p>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
			{#each wallets as option}
				<div />
			{/each}
		</div>
		<div class="flex flex-row justify-start  w-full align-middle">
			<p class="font-black text-base pr-2">N.B:</p>
			<p>
				In some scenario it might take up 2 - 6 hours for your payment to reflect in your account
			</p>
		</div>
	</div>
</div>
