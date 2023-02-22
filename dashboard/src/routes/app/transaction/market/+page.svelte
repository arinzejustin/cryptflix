<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';

	let msg: string, err: boolean, alert: boolean;

	var market: any[] = [],
		token: string,
		loading: boolean = true,
		hour = true,
		cap: any,
		volume: any,
		capper: any,
		volper: any;
	var ticker = async (show: boolean = false) => {
			var name: any[] = [],
				coin: any;
			try {
				const req = await API.post(
					'/market',
					JSON.stringify({ path: 'coin/data/ticker', query: 'ticker' }),
					{ Authorization: token }
				);
				if (req.status) {
					market = [];
					name = req.data.rankedIds;
					coin = req.data.byId;
					name.forEach((coinName, index) => {
						if (index > 59) return;
						market = [...market, req.data.byId[`${coinName}`]];
					});
					loading = false;
					return;
				}
				if (show) {
					toast(req.message, !req.status);
				}
			} catch (error) {
				if (show) {
					//@ts-ignore
					toast(error.message, true);
				}
			}
		},
		hourly = async () => {
			try {
				const req = await API.post(
					'/market',
					JSON.stringify({ path: 'metadata/historical/aggregated/hourly', query: 'hourly' }),
					{ Authorization: token }
				);
				if (req.status) {
					hour = false;
					capper = req.data.percentageMove.marketCapChange;
					volper = req.data.percentageMove.volumeChange;
					cap = req.data.metadata[0].marketCap;
					volume = req.data.metadata[0].volume;
				}
			} catch (error) {}
		},
		toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		},
		format = (value: any, money: boolean = false) => {};
	onMount(() => {
		token = getStorage('token');
		ticker(true);
		hourly();
		format = (value: any, money: boolean = false) => {
			if (money) {
				var formatter = new Intl.NumberFormat('en-US', {
					style: 'currency',
					currency: 'USD',
					notation: 'compact'
				});
				return formatter.format(value);
			}
			var formatter = new Intl.NumberFormat('en-US', {
				style: 'currency',
				currency: 'USD'
			});
			return formatter.format(value);
		};
		var t = 200,
			interval: any;
		run();
		function changeTimer() {
			t = t * 2.5;
		}
		function run() {
			clearInterval(interval);
			ticker();
			hourly();
			changeTimer();
			interval = setInterval(run, t);
		}
	});
	ononline = () => {
		ticker();
		hourly();
	};
</script>

<svelte:head>
	<script src="https://widgets.coingecko.com/coingecko-coin-price-marquee-widget.js"></script>
</svelte:head>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="container mt-4 pt-5"
>
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div
		class="flex flex-row md:mr-2 override w-full items-center align-middle justify-between mb-4 pb-4"
	>
		<div class="w-auto">
			<p class="font-nunito text-xl lg:text-2xl font-bold uppercase text-black dark:text-white">
				Markets
			</p>
		</div>
		<div class="w-auto">
			<a
				href="/app/transaction/deposit"
				class="rounded-lg w-16 inline px-4 py-3 bg-blue-700 text-white hover:ring-blue-600 transition-all duration-300 ring-2 ring-offset-2 ring-offset-transparent ring-transparent"
			>
				<svg
					class="w-6 h-6 mx-2 text-white inline"
					xmlns="http://www.w3.org/2000/svg"
					width="1.13em"
					height="1em"
					viewBox="0 0 512 512"
				>
					<rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
						fill="currentColor"
						d="M298.9 24.31c-14.9.3-25.6 3.2-32.7 8.4l-97.3 52.1l-54.1 73.59c-11.4 17.6-3.3 51.6 32.3 29.8l39-51.4c49.5-42.69 150.5-23.1 102.6 62.6c-23.5 49.6-12.5 73.8 17.8 84l13.8-46.4c23.9-53.8 68.5-63.5 66.7-106.9l107.2 7.7l-1-112.09l-194.3-1.4zM244.8 127.7c-17.4-.3-34.5 6.9-46.9 17.3l-39.1 51.4c10.7 8.5 21.5 3.9 32.2-6.4c12.6 6.4 22.4-3.5 30.4-23.3c3.3-13.5 8.2-23 23.4-39zm-79.6 96c-.4 0-.9 0-1.3.1c-3.3.7-7.2 4.2-9.8 12.2c-2.7 8-3.3 19.4-.9 31.6c2.4 12.1 7.4 22.4 13 28.8c5.4 6.3 10.4 8.1 13.7 7.4c3.4-.6 7.2-4.2 9.8-12.1c2.7-8 3.4-19.5 1-31.6c-2.5-12.2-7.5-22.5-13-28.8c-4.8-5.6-9.2-7.6-12.5-7.6zm82.6 106.8c-7.9.1-17.8 2.6-27.5 7.3c-11.1 5.5-19.8 13.1-24.5 20.1c-4.7 6.9-5.1 12.1-3.6 15.2c1.5 3 5.9 5.9 14.3 6.3c8.4.5 19.7-1.8 30.8-7.3c11.1-5.5 19.8-13 24.5-20c4.7-6.9 5.1-12.2 3.6-15.2c-1.5-3.1-5.9-5.9-14.3-6.3c-1.1-.1-2.1-.1-3.3-.1zm-97.6 95.6c-4.7.1-9 .8-12.8 1.9c-8.5 2.5-13.4 7-15 12.3c-1.7 5.4 0 11.8 5.7 18.7c5.8 6.8 15.5 13.3 27.5 16.9c11.9 3.6 23.5 3.5 32.1.9c8.6-2.5 13.5-7 15.1-12.3c1.6-5.4 0-11.8-5.8-18.7c-5.7-6.8-15.4-13.3-27.4-16.9c-6.8-2-13.4-2.9-19.4-2.8z"
					/>
				</svg>
				<span>Invest</span>
			</a>
		</div>
	</div>
	<div class="w-full override">
		<coingecko-coin-price-marquee-widget
			class="override"
			coin-ids="bitcoin,eos,ethereum,litecoin,ripple,solana,stellar,safemoon-2,saitama-inu,usdd,algorand,dogecoin,render-token,wemix-token,vechain,binancecoin,quant-network,zoid-pay,osmosis,y2k,cardano,nucypher,nexo,edgecoin-2,euler,bitdao,binancecoin"
			currency="usd"
			background-color="trasparent"
			locale="en"
		/>
	</div>
	<div class="override w-full grid grid-cols-1 md:grid-cols-2 gap-4 my-4 md:py-3">
		<div
			class="rounded-lg border dark:border-solid border-color app-shadow dark:shadow-md dark:shadow-slate-100/30 p-4 dark:bg-black/60"
		>
			<p class="tex-lg font-open uppercase mb-5 font-semibold">Market Cap</p>
			<div class="flex flex-row items-center align-middle justify-between">
				{#if hour}
					<Loader width={'20px'} height={'20px'} auto={'0px'} />
					<Loader width={'20px'} height={'20px'} auto={'0px'} />
				{:else}
					<p>{format(cap, true)}</p>
					<p
						class={capper < 0
							? 'text-red-400 dark:text-red-700'
							: 'text-green-400 dark:text-green-700'}
					>
						{capper < 0 ? '' : '+'}{parseFloat(capper.toFixed(2))}%
					</p>
				{/if}
			</div>
		</div>
		<div
			class="rounded-lg border dark:border-solid border-color app-shadow dark:shadow-md dark:shadow-slate-100/30 p-4 dark:bg-black/60"
		>
			<p class="tex-lg font-open uppercase mb-5 font-semibold">Total Volume</p>
			<div class="flex flex-row items-center align-middle justify-between">
				{#if hour}
					<Loader width={'20px'} height={'20px'} auto={'0px'} />
					<Loader width={'20px'} height={'20px'} auto={'0px'} />
				{:else}
					<p>{format(volume, true)}</p>
					<p
						class={volper < 0
							? 'text-red-400 dark:text-red-700'
							: 'text-green-400 dark:text-green-700'}
					>
						{volper < 0 ? '' : '+'}{parseFloat(volper.toFixed(2))}%
					</p>
				{/if}
			</div>
		</div>
	</div>
	<div class="override pt-6 my-3">
		<div
			class="relative overflow-x-auto overflow-y-hidden shadow-lg dark:shadow-md dark:shadow-slate-100/30 sm:rounded-lg border-solid border-color border"
		>
			<table
				class="{loading
					? 'h-48 md:h-36'
					: ''} w-full relative text-sm text-left text-slate-700 dark:text-slate-50"
			>
				<thead
					class="text-base sticky border-b border-solid border-color font-nunito text-slate-700 uppercase bg-gray-50 dark:bg-accent dark:text-slate-50"
				>
					<tr>
						<th scope="col" class="px-6 py-3"> Rank </th>
						<th scope="col" class="px-6 py-3"> Coin </th>
						<th scope="col" class="px-6 py-3"> Price (USD) </th>
						<th scope="col" class="px-6 py-3"> 24h Volume </th>
						<th scope="col" class="px-6 py-3"> Price Graph (7d) </th>
						<th scope="col" class="px-6 py-3"> Market Cap </th>
					</tr>
				</thead>
				{#if loading}
					<div
						out:fly={{ y: -400 }}
						class="absolute -translate-x-1/2 -translate-y-1/2 transform top-2/3 md:top-1/2 left-1/3 md:left-1/2 my-4 py-4"
					>
						<Loader width={'40px'} height={'40px'} />
					</div>
				{:else}
					<tbody in:fly={{ y: 400 }} class="font-mono">
						{#each market as coin}
							<tr
								class="bg-white border-b dark:bg-black border-color border-solid hover:bg-slate-50 dark:hover:bg-accent"
							>
								<th
									scope="row"
									class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
								>
									<span class="dark:bg-accent p-2 rounded-md bg-slate-100">{coin.rank}</span>
								</th>
								<td class="px-6 py-4">
									<div class="flex flex-nowrap align-middle items-center">
										<div
											class="rounded-full bg-transparent flex justify-center items-center m-1 object-contain"
										>
											<img
												src={coin.imageUrl}
												alt={coin.name}
												srcset="{coin.imageUrl} 2x"
												loading="lazy"
												width="32px"
												height="32px"
											/>
										</div>
										<div class="ml-2 overflow-hidden">
											<div
												class="p-0 m-0 font-nunito text-base overflow-hidden font-semibold text-ellipsis whitespace-nowrap"
											>
												{coin.name}
											</div>
											<div
												class="m-0 p-0 font-nunito opacity-70 text-sm overflow-hidden font-semibold text-ellipsis whitespace-nowrap mt-2"
											>
												{coin.symbol}
											</div>
										</div>
									</div>
								</td>
								<td class="px-6 py-4">
									<div class="flex flex-col align-middle justify-start">
										<p
											class="text-base overflow-hidden font-semibold text-ellipsis whitespace-nowrap"
										>
											{format(coin.priceUsd)}
										</p>
										<p
											class="{coin.percentChange24h < 0
												? 'text-red-400 dark:text-red-700'
												: 'text-green-400 dark:text-green-700'} font-open text-sm"
										>
											{coin.percentChange24h < 0 ? '' : '+'}{parseFloat(
												coin.percentChange24h.toFixed(2)
											)}% last 24hr
										</p>
									</div>
								</td>
								<td class="px-6 py-4">
									{format(coin['24hVolumeUsd'], true)}
								</td>
								<td class="px-6 py-4">
									<img
										width="135"
										height="50"
										loading="lazy"
										src="https://www.coingecko.com/coins/{coin.rank}/sparkline"
										srcset="https://www.coingecko.com/coins/{coin.rank}/sparkline 2x"
										alt="({coin.name}) 7d chart"
									/>
								</td>
								<td class="px-6 py-4">
									{format(coin.marketCapUsd, true)}
								</td>
							</tr>
						{/each}
					</tbody>
				{/if}
			</table>
		</div>
	</div>
</div>
