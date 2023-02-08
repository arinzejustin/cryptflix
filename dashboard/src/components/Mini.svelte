<script lang="ts">
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';

	export let transaction: any[],
		error: boolean,
		find: boolean,
		token: string;
	let loading = false;
	var retry = async () => {
		loading = true;
		try {
			const req = await API.post('/history', { uuid: '', mini: true }, { Authorization: token });
			if ('find' in req) {
				find = req.find;
				error = false;
				transaction = req.transaction
			} else loading = false;
		} catch (error) {
			setTimeout(() => loading = false, 3000)
		}
	};
</script>

<div class="mx-auto relative">
	<p class="text-base sticky top-1 py-1 mt-1 mb-2.5 bg-slate-100 dark:bg-gray-900 text-center">
		Transaction History
	</p>
	{#if error}
		{#if loading}
			<Loader width={'50px'} height={'50px'} />
		{:else}
			<div class="text-center mt-8">
				<p class="text-sm font-open">Error: Can't Load Your Transaction Histroy</p>
				<button
					on:click={retry}
					class="bg-yellow-100 my-4 px-3.5 py-1 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
					>Retry</button
				>
			</div>
		{/if}
	{:else if find && !error}
		{#each transaction as act}
			<div class="px-1">
				<div>{act.date}</div>
				<div>{act.name}</div>
			</div>
		{/each}
	{:else}
		<p class="text-sm mt-8 text-center font-open">No Record Exist</p>
	{/if}
</div>
