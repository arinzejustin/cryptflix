<script lang="ts">
	import { fly } from 'svelte/transition';
	import { BTC_WALLET, ETH_WALLET, USDT_WALLET } from '$lib/env';
    import Alert from '$lib/Alert.svelte'

	let wallets = [
		{
			name: 'Bitcoin',
			wallet: BTC_WALLET,
			svg: '0 0 32 32'
		},
		{
			name: 'USDT',
			wallet: ETH_WALLET,
			svg: '0 0 32 32'
		},
		{
			name: 'Ethereum',
			wallet: USDT_WALLET,
			svg: '0 0 256 417'
		}
	], msg: string, err: boolean, alert: boolean;

    var copy = ({name, wallet}: any) => {
        alert = false;
        navigator.clipboard.writeText(wallet)
        toast(`${name} Wallet Copied`, false)
    },
    toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		};
</script>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-3 pt-3 md:pt-5"
>
<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div class="override">
		<div class="py-2">
			<p class="text-3xl uppercase pb-2 font-bold">Invest</p>
			<p class="text-sm text-gray-400">
				Take a bold towards making yourself <span class="text-[green]">100%</span> financially stable
			</p>
		</div>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 py-4 pb-8">
			{#each wallets as option}
				<div class="border border-solid rounded-lg border-color pt-2">
					<div
						class="flex flex-row px-1 py-2 justify-start align-middle items-center border-b border-solid border-color"
					>
						<div class="truncate mr-1">
							<p class="truncate">{option.wallet}</p>
						</div>
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<div class="opacity-70 hover:opacity-100 focus:opacity-100" on:click={() => {copy({name: option.name, wallet : option.wallet})}}>
							<svg
								class="mx-auto w-8 h-8"
								xmlns="http://www.w3.org/2000/svg"
								width="24"
								height="24"
								viewBox="0 0 24 24"
								><path
									fill="currentColor"
									d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"
								/></svg
							>
						</div>
					</div>
					<div
						class="p-2 text-center bg-slate-200 dark:bg-accent rounded-b-lg flex flex-row justify-between align-middle items-center"
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
							<p class="uppercase text-xl font-mono font-medium">{option.name}</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
		<div class="flex flex-row justify-start  w-full align-middle pt-6">
			<p class="font-black text-base pr-2">N.B:</p>
			<p>
				In some scenario it might take up 2 - 6 hours for your payment to reflect in your account
			</p>
		</div>
	</div>
</div>
