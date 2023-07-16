<script lang="ts">
	import { fly } from 'svelte/transition';
	import type { PageData } from './$types';

	export let data: PageData;

	let newusers = data.admin.newUser,
		deposits = data.admin.deposit,
		balance = data.admin.balance,
		users = data.admin.users,
		date = data.admin.date;
</script>

<svelte:head>
	<title>Admin Dashboard | cryptoflixinvest.org</title>
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<div class="override">
		<div
			class="grid grid-cols-1 mb-6 md:grid-cols-2 gap-8 items-baseline align-middle justify-evenly"
		>
			<div
				class="bg-slate-50 dark:shadow-slate-400 dark:shadow-md dark:bg-accent border-color border-solid border shadow-lg rounded-lg px-3 py-4"
			>
				<p class="uppercase pb-5 text-2xl font-semibold font-mono">total users deposit</p>
				<p class="text-right pt-5 text-lg font-medium">{deposits}</p>
			</div>
			<div
				class="bg-slate-50 dark:shadow-slate-400 dark:shadow-md dark:bg-accent border-color border-solid border shadow-lg rounded-lg px-3 py-4"
			>
				<p class="uppercase pb-5 text-2xl font-semibold font-mono">total users balance</p>
				<p class="text-right pt-5 text-lg font-medium">{balance}</p>
			</div>
			<div
				class="bg-slate-50 dark:shadow-slate-400 dark:shadow-md dark:bg-accent border-color border-solid border shadow-lg rounded-lg px-3 py-4"
			>
				<p class="uppercase pb-5 text-2xl font-semibold font-mono">total users</p>
				<p class="text-right pt-5 text-lg font-medium">
					{Number(users) > 1 ? `${users} Users` : `${users} User`}
				</p>
			</div>
			<div
				class="bg-slate-50 dark:shadow-slate-400 dark:shadow-md dark:bg-accent border-color border-solid border shadow-lg rounded-lg px-3 py-4"
			>
				<div class="flex flex-row justify-between align-middle items-center">
					<p class="uppercase pb-5 text-2xl font-semibold font-mono">New users</p>
					<p class="uppercase pb-5 text-base font-medium font-nunito">{date}</p>
				</div>
				<p class="text-right pt-5 text-lg font-medium">
					{Number(newusers) > 1 ? `${newusers} Users` : `${newusers} User`}
				</p>
			</div>
		</div>
	</div>
</div>
