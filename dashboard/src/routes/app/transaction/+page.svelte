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
		token = getStorage('token');
		transactions();
	});
</script>

<div in:fly={{ x: 400, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="container">
	<div class="override">
		<div class="bg-slate-100 dark:bg-accent py-3 w-full rounded-sm {loading ? 'mb-16' : ''}">
			<p class="text-center font-medium uppercase text-xs sm:text-sm md:text-base lg:text-lg">
				Created account on 12/01/2023 at 12:48:01 pm
			</p>
		</div>
		{#if error}
			{#if loading}
			<div class="mt-10 pt-8" out:fly={{ y: -400 }}>
				<Loader width={'50px'} height={'50px'} />
				<p class="text-center pt-8">Loading Transaction History ......</p>
			</div>
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
				<div in:fly={{ y: 400 }}
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
									viewBox="0 0 128 128"
									><rect x="0" y="0" width="128" height="128" fill="none" stroke="none" /><circle
										cx="64"
										cy="66.58"
										r="57.36"
										fill="#D68F30"
									/><path
										fill="#BC6F00"
										d="M10.54 81.48v5.86c.6 1.55 1.27 3.08 2 4.56V81.48h-2zm6.54 11.03v7.04c.8 1.13 1.63 2.24 2.5 3.31V92.51h-2.5zm8.66 9.2v7.59c.97.87 1.97 1.7 3 2.5v-10.09h-3zm10.66 6.99v8.16c.98.54 1.98 1.05 3 1.54v-9.7h-3zm12.09 4.45v8.64c.99.28 1.99.53 3 .76v-9.4h-3zm14.15 1.54v9.21c.45.01.9.03 1.36.03c.55 0 1.1-.03 1.64-.04v-9.2h-3zm14.15-1.61v9.4c1.01-.23 2.01-.49 3-.77v-8.63h-3zm12.06-4.51v9.71c1.02-.49 2.02-1.02 3-1.57v-8.14h-3zm10.63-7.05v10.1a55.52 55.52 0 0 0 3-2.52v-7.58h-3zm11.61-9.23h-2.5v10.35c.87-1.08 1.71-2.19 2.5-3.33v-7.02zm6.5-11.07h-2v10.44c.73-1.51 1.4-3.06 2-4.63v-5.81z"
									/><circle cx="64" cy="61.42" r="57.36" fill="#FFF176" /><circle
										cx="64"
										cy="61.42"
										r="52.25"
										fill="#F2BC1A"
									/><path
										fill="#E08F00"
										d="M11.65 63.42c-.37-6.88.82-13.86 3.22-20.4c2.5-6.52 6.33-12.55 11.16-17.67C35.73 15.09 49.81 9.14 64 9.07c14.19.08 28.28 6.02 37.96 16.29c4.84 5.11 8.66 11.15 11.16 17.66c2.41 6.55 3.6 13.52 3.22 20.4h-.2a52.756 52.756 0 0 0-4-20a52.834 52.834 0 0 0-11.29-16.97a52.255 52.255 0 0 0-16.9-11.38a51.805 51.805 0 0 0-39.92 0a52.255 52.255 0 0 0-16.9 11.38a52.671 52.671 0 0 0-11.29 16.97a52.756 52.756 0 0 0-4 20h-.19z"
									/><path
										fill="#FFF176"
										d="M64 4.07c-31.68 0-57.36 25.68-57.36 57.36S32.32 118.79 64 118.79s57.36-25.68 57.36-57.36S95.68 4.07 64 4.07zm0 109.61c-28.86 0-52.25-23.39-52.25-52.25C11.75 32.56 35.14 9.17 64 9.17s52.25 23.39 52.25 52.25S92.86 113.68 64 113.68z"
									/><path
										fill="#D38200"
										d="m37.99 21.35l1.27 3.93l4.14-1.58v1.58l-3.35 2.43l1.28 2.34v1.59l-3.34-2.43l-3.35 2.43v-1.59l1.28-2.34l-3.34-2.43V23.7l4.13 1.58zM22.01 43.91l1.28 3.93l4.13-1.58v1.58l-3.34 2.43l1.28 2.35v1.58l-3.35-2.43l-3.34 2.43v-1.58l1.28-2.35l-3.35-2.43v-1.58l4.14 1.58zm-.47 27.81l1.28 3.93l4.13-1.58v1.58l-3.34 2.43l1.28 2.35v1.58l-3.35-2.43l-3.34 2.43v-1.58l1.28-2.35l-3.35-2.43v-1.58l4.14 1.58zM38.6 93.8l1.28 3.93l4.13-1.58v1.58l-3.34 2.43l1.28 2.34v1.59l-3.35-2.43l-3.34 2.43v-1.59l1.28-2.34l-3.35-2.43v-1.58l4.14 1.58zm51.41-72.45l-1.27 3.93l-4.14-1.58v1.58l3.35 2.43l-1.28 2.34v1.59l3.34-2.43l3.35 2.43v-1.59l-1.28-2.34l3.34-2.43V23.7l-4.13 1.58zm15.98 22.56l-1.28 3.93l-4.13-1.58v1.58l3.34 2.43l-1.28 2.35v1.58l3.35-2.43l3.34 2.43v-1.58l-1.28-2.35l3.35-2.43v-1.58l-4.14 1.58zm.47 27.81l-1.28 3.93l-4.13-1.58v1.58l3.34 2.43l-1.28 2.35v1.58l3.35-2.43l3.34 2.43v-1.58l-1.28-2.35l3.35-2.43v-1.58l-4.14 1.58zM89.4 93.8l-1.28 3.93l-4.13-1.58v1.58l3.34 2.43l-1.28 2.34v1.59l3.35-2.43l3.34 2.43v-1.59l-1.28-2.34l3.35-2.43v-1.58l-4.14 1.58z"
									/><path
										fill="#FFF176"
										d="m89.4 92.21l1.27 3.93h4.14l-3.35 2.43l1.28 3.93l-3.34-2.43l-3.35 2.43l1.28-3.93l-3.34-2.43h4.13zm17.06-22.07l1.27 3.93h4.14l-3.35 2.43l1.28 3.93l-3.34-2.43l-3.35 2.43l1.28-3.93l-3.34-2.43h4.13zm-.47-27.81l1.27 3.93h4.14l-3.35 2.43l1.28 3.93l-3.34-2.43l-3.35 2.43l1.28-3.93l-3.34-2.43h4.13zM90.01 19.76l1.28 3.93h4.13l-3.34 2.43l1.28 3.93l-3.35-2.43l-3.34 2.43l1.28-3.93l-3.35-2.43h4.14z"
									/><path
										fill="#D38200"
										d="m64.05 102.5l1.28 3.93l4.13-1.58v1.58l-3.34 2.43l1.28 2.35v1.58l-3.35-2.43l-3.34 2.43v-1.58l1.28-2.35l-3.35-2.43v-1.58l4.14 1.58z"
									/><path
										fill="#FFF176"
										d="m64.05 100.4l1.28 3.93h4.13l-3.34 2.43l1.28 3.93l-3.35-2.43l-3.34 2.43l1.28-3.93l-3.35-2.43h4.14z"
									/><path
										fill="#D38200"
										d="m64.05 12.89l1.28 3.93l4.13-1.58v1.58l-3.34 2.43l1.28 2.35v1.58l-3.35-2.43l-3.34 2.43V21.6l1.28-2.35l-3.35-2.43v-1.58l4.14 1.58z"
									/><path
										fill="#FFF176"
										d="m64.05 11.31l1.28 3.93h4.13l-3.34 2.43l1.28 3.93l-3.35-2.43l-3.34 2.43l1.28-3.93l-3.35-2.43h4.14zM38.6 92.21l-1.27 3.93h-4.14l3.35 2.43l-1.28 3.93l3.34-2.43l3.35 2.43l-1.28-3.93l3.34-2.43h-4.13zM21.54 70.14l-1.27 3.93h-4.14l3.35 2.43l-1.28 3.93L21.54 78l3.35 2.43l-1.28-3.93l3.34-2.43h-4.13zm.47-27.81l-1.27 3.93H16.6l3.35 2.43l-1.28 3.93l3.34-2.43l3.35 2.43l-1.28-3.93l3.34-2.43h-4.13zm15.98-22.57l-1.28 3.93h-4.13l3.34 2.43l-1.28 3.93l3.35-2.43l3.34 2.43l-1.28-3.93l3.35-2.43h-4.14z"
									/><path
										fill="#D38200"
										d="M95.22 48.2c0-.35-62.38 0-62.38 0l-.56 1.68v2.87c0 .52.42.94.94.94h61.56c.52 0 .94-.42.94-.94v-2.79l-.5-1.76zm.09 37.3H33.1l-4.16 2.09l.05 2.69c.01.29.25.53.55.53h68.93c.29 0 .54-.23.55-.53l.05-2.64l-3.76-2.14z"
									/><path
										fill="#D38200"
										d="M43.13 77.32h-3.58c-.59 0-1.07-1.86-1.07-2.45l5.71-.18c0 .59-.48 2.63-1.06 2.63zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.47-3.93h8.83l-.4 3.93c-.12.43-.51.73-.96.73zm-6.03 20.5h6.03c.45 0 1.34.28 1.46.71c0 0-.03 1.87-.03 2.61s-.3 1.28-.97 1.28h-6.95c-.67 0-.97-.6-.97-1.28s-.03-2.59-.03-2.59c.13-.43 1.01-.73 1.46-.73zm51.31-1.19h-3.58c-.59 0-1.07-1.86-1.07-2.45l5.71-.18c0 .59-.47 2.63-1.06 2.63zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.47-3.93h8.83l-.4 3.93c-.12.43-.51.73-.96.73zm-6.03 20.5h6.03c.45 0 1.34.28 1.46.71c0 0-.03 1.87-.03 2.61s-.3 1.28-.97 1.28h-6.95c-.67 0-.97-.6-.97-1.28s-.03-2.59-.03-2.59c.13-.43 1.01-.73 1.46-.73zm-10.69-1.19h-3.58c-.59 0-1.07-1.86-1.07-2.45l5.71-.18c0 .59-.47 2.63-1.06 2.63zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.47-3.93h8.83l-.4 3.93c-.12.43-.51.73-.96.73zm-6.03 20.5h6.03c.45 0 1.34.28 1.46.71c0 0-.03 1.87-.03 2.61s-.3 1.28-.97 1.28h-6.95c-.67 0-.97-.6-.97-1.28s-.03-2.59-.03-2.59c.13-.43 1.01-.73 1.46-.73zm-10.69-1.19h-3.58c-.59 0-1.07-1.86-1.07-2.45l5.71-.18c0 .59-.47 2.63-1.06 2.63zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.47-3.93h8.83l-.4 3.93c-.12.43-.51.73-.96.73zm-6.03 20.5h6.03c.45 0 1.34.28 1.46.71c0 0-.03 1.87-.03 2.61s-.3 1.28-.97 1.28h-6.95c-.67 0-.97-.6-.97-1.28s-.03-2.59-.03-2.59c.13-.43 1.01-.73 1.46-.73z"
									/><path
										fill="#FFF176"
										d="M95.67 45.52c0-.35-.18-.68-.45-.84l-31.18-17.7l-31.22 17.68c-.3.18-.49.51-.49.86l-.05 4.37c0 .55.45 1 1 1h61.43c.55 0 1-.45 1-1l-.04-4.37z"
									/><path fill="#F2BC1A" d="M87.84 44.33L64 30.8L40.16 44.33z" /><path
										fill="#FFF176"
										d="M79.07 42.68L64 34.12l-15.07 8.56zm14.32 39.34H34.61c-.58 0-1.13.25-1.52.68l-4.04 4.51c-.28.31-.06.8.36.8h69.18c.41 0 .63-.49.36-.8L94.9 82.7c-.38-.43-.94-.68-1.51-.68zm-3.76-6.51h-3.58c-.59 0-1.07-.48-1.07-1.07V58.46c0-.59.48-1.07 1.07-1.07h3.58c.59 0 1.07.48 1.07 1.07v15.99c0 .59-.48 1.06-1.07 1.06zm1.23-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.46-1.59c-.19-.64.3-1.28.97-1.28h6.95c.67 0 1.15.64.97 1.28l-.46 1.59c-.13.43-.53.73-.97.73zm-6.04 20.51h6.03c.45 0 .84.3.97.73l.46 1.59c.19.64-.3 1.28-.97 1.28h-6.95c-.67 0-1.15-.64-.97-1.28l.46-1.59c.13-.44.53-.73.97-.73zm-41.69-1.2h-3.58c-.59 0-1.07-.48-1.07-1.07V58.46c0-.59.48-1.07 1.07-1.07h3.58c.59 0 1.07.48 1.07 1.07v15.99c-.01.59-.49 1.06-1.07 1.06zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.46-1.59c-.19-.64.3-1.28.97-1.28h6.95c.67 0 1.15.64.97 1.28l-.46 1.59c-.13.43-.52.73-.97.73zm-6.03 20.51h6.03c.45 0 .84.3.97.73l.46 1.59c.19.64-.3 1.28-.97 1.28h-6.95c-.67 0-1.15-.64-.97-1.28l.46-1.59c.13-.44.52-.73.97-.73zm20.31-1.2h-3.58c-.59 0-1.07-.48-1.07-1.07V58.46c0-.59.48-1.07 1.07-1.07h3.58c.59 0 1.07.48 1.07 1.07v15.99a1.07 1.07 0 0 1-1.07 1.06zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.46-1.59c-.19-.64.3-1.28.97-1.28h6.95c.67 0 1.15.64.97 1.28l-.46 1.59c-.13.43-.52.73-.97.73zm-6.03 20.51h6.03c.45 0 .84.3.97.73l.46 1.59c.19.64-.3 1.28-.97 1.28h-6.95c-.67 0-1.15-.64-.97-1.28l.46-1.59c.13-.44.52-.73.97-.73zm20.31-1.2h-3.58c-.59 0-1.07-.48-1.07-1.07V58.46c0-.59.48-1.07 1.07-1.07h3.58c.59 0 1.07.48 1.07 1.07v15.99a1.07 1.07 0 0 1-1.07 1.06zm1.22-19.31h-6.03c-.45 0-.84-.3-.97-.73l-.46-1.59c-.19-.64.3-1.28.97-1.28h6.95c.67 0 1.15.64.97 1.28l-.46 1.59c-.13.43-.52.73-.97.73zm-6.03 20.51h6.03c.45 0 .84.3.97.73l.46 1.59c.19.64-.3 1.28-.97 1.28h-6.95c-.67 0-1.15-.64-.97-1.28l.46-1.59c.13-.44.53-.73.97-.73z"
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
