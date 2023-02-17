<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import Receipt from '../../../components/Receipt.svelte';

	let date: string,
		wallet: string,
		status: string,
		error = true,
		find: boolean,
		token: string,
		loading = false,
		open = false,
		session: string,
		amount: string,
		name = 'Arinze Justin',
		detail: string;

	var transactions = async () => {
			loading = true;
			try {
				list = [];
				const req = await API.post('/transactions', JSON.stringify({ email: '' }), {
					Authorization: token
				});
				list = [...list, req.data];
				setTimeout(() => {
					error = false;
					loading = false;
					find = true;
				}, 3000);
			} catch {
				error = true;
				loading = false;
			}
		},
		list: any[] = [];

	const receipt = ({ date_, amount_, detail_, status_ }: any) => {
		open = true;
		date = date_;
		amount = amount_;
		detail = detail_;
		status = status_;
	};

	onMount(() => {
		transactions();
		token = getStorage('token');
	});
</script>

<div in:fly={{ x: 400, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="container">
	<div class="">
		<div class="bg-slate-100 dark:bg-accent py-3 w-full rounded-sm {loading ? 'mb-16' : ''}">
			<p class="text-center font-medium uppercase text-xs sm:text-sm md:text-base lg:text-lg">
				Created account on 12/01/2023 at 12:48:01 pm
			</p>
		</div>
		{#if error}
			{#if loading}
				<Loader width={'50px'} height={'50px'} />
			{:else}
				<div class="text-center mt-8">
					<p class="text-sm font-open">Error: Can't Load Your Transaction Histroy</p>
					<button
						on:click={transactions}
						class="bg-yellow-100 my-4 px-3.5 py-1 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
						>Retry</button
					>
				</div>
			{/if}
		{:else if find && !error}
			{#each list[0] as act}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div
					on:click={() =>
						receipt({
							date_: act.time,
							detail_: act.type_,
							status_: act.status,
							amount_: act.amount
						})}
					class="bg-white w-full dark:hover:bg-accent my-6 override hover:bg-slate-50 cursor-pointer dark:bg-black rounded-md border-color border-solid border p-2 shadow-lg dark:shadow-md hover:shadow-xl dark:hover:shadow-lg dark:hover:shadow-slate-100/30 dark:shadow-slate-100/30 py-4"
				>
					<div class="flex flex-row justify-between align-middle items-center">
						<div class="flex flex-nowrap align-middle items-center">
							<div
								class="rounded-full p-2 border-solid border-color border bg-transparent flex justify-center items-center m-1 object-contain"
							>
								<svg
									class="w-8 h-8"
									xmlns="http://www.w3.org/2000/svg"
									width="1em"
									height="1em"
									viewBox="0 0 24 24"
									><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
										fill="currentColor"
										d="M17.12 9.88a2.997 2.997 0 1 0-4.24 4.24a2.997 2.997 0 1 0 4.24-4.24M7 6v12h16V6H7m14 8c-.53 0-1.04.21-1.41.59c-.38.37-.59.88-.59 1.41h-8c0-.53-.21-1.04-.59-1.41c-.37-.38-.88-.59-1.41-.59v-4c.53 0 1.04-.21 1.41-.59c.38-.37.59-.88.59-1.41h8c0 .53.21 1.04.59 1.41c.37.38.88.59 1.41.59v4M5 8H3c-.55 0-1-.45-1-1s.45-1 1-1h2v2m0 5H2c-.55 0-1-.45-1-1s.45-1 1-1h3v2m0 5H1c-.552 0-1-.45-1-1s.448-1 1-1h4v2Z"
									/></svg
								>
							</div>
							<div class="ml-2 overflow-hidden">
								<div
									class="p-0 m-0 text-black dark:text-white upperacse font-open text-base md:text-xl overflow-hidden font-semibold text-ellipsis whitespace-nowrap"
								>
									{act.type_}
								</div>
								<div
									class="{act.status == 'failed' ? 'text-red-500' : 'text-green-500'} {act.status ==
									'pending'
										? 'text-yellow-500'
										: ''} m-0 p-0 uppercase font-nunito opacity-70 text-sm overflow-hidden font-semibold text-ellipsis whitespace-nowrap mt-2"
								>
									{act.status}
								</div>
							</div>
						</div>
						<div class="flex flex-col items-end align-middle gap-4">
							<p
								class="text-lg font-mono {act.status == 'failed'
									? 'text-red-500'
									: 'text-green-500'} {act.status == 'pending' ? 'text-yellow-500' : ''}"
							>
								{act.amount}
							</p>
							<p class="text-xs md:text-sm">{act.time}</p>
						</div>
					</div>
				</div>
			{/each}
		{:else}
			<p class="text-lg font-semibold mt-16 text-center font-mono">
				No Transaction Activity Exists
			</p>
		{/if}
	</div>
</div>
<Receipt
	{session}
	{name}
	{detail}
	{open}
	{status}
	{wallet}
	{amount}
	{date}
	onClose={() => (open = false)}
/>
