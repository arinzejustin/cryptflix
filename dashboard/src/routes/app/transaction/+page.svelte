<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	import API from '$lib/api';
	import Loader from '$lib/Loader.svelte';
	import Alert from '$lib/Alert.svelte';
	import { getStorage } from '$lib/storage';

	let msg: string,
		err: boolean,
		alert: boolean,
		error: boolean,
		find: boolean,
		token: string,
		loading = false;

	var transactions = async () => {
			try {
				list = [];
				const req = await API.post('/transactions', JSON.stringify({ email: '' }), {
					Authorization: token
				});
                console.log(req)
			} catch (error) {
                //@ts-ignore
                toast(error.message, true)
            }
		},
		list: any[] = [],
		toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		};

	onMount(() => {
		transactions();
		token = getStorage('token');
	});
</script>

<div in:fly={{ x: 400, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="container">
	<div class="">
        <div class="bg-slate-100 dark:bg-accent py-3 w-full rounded-sm">
            <p class="text-center uppercase text-lg">Created account on 12/01/2023 at 12:48:01 pm</p>
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
			{#each list as act}
				<div class="px-1">
					<div>{act.date}</div>
					<div>{act.name}</div>
				</div>
			{/each}
		{:else}
			<p class="text-lg font-semibold mt-16 text-center font-mono">No Transaction Activity Exists</p>
		{/if}
        <div class="bg-white w-full dark:hover:bg-accent my-6 hover:bg-slate-50 cursor-pointer dark:bg-black app-shadow rounded-md border-color border-solid border p-2 shadow-lg dark:shadow-lg dark:shadow-slate-100/30">
            <div class="flex flex-row justify-between align-middle items-center">
                <div class="flex flex-nowrap align-middle items-center">
                    <div
                        class="rounded-full border-solid border-color border bg-transparent flex justify-center items-center m-1 object-contain"
                    >
                        <img
                            src=''
                            alt=''
                            srcset=" 2x"
                            loading="lazy"
                            width="32px"
                            height="32px"
                        />
                    </div>
                    <div class="ml-2 overflow-hidden">
                        <div
                            class="p-0 m-0 upperacse font-open text-xl overflow-hidden font-semibold text-ellipsis whitespace-nowrap"
                        >
                            Withdrawal
                        </div>
                        <div
                            class="m-0 p-0 font-nunito opacity-70 text-sm overflow-hidden font-semibold text-ellipsis whitespace-nowrap mt-2"
                        >
                            
                        </div>
                    </div>
                </div>
                <div class="flex flex-col items-end align-middle gap-4">
                    <p class="text-lg font-mono">-$2,000</p>
                    <p class="text-sm">12-12-2023, 02:10:59 PM</p>
                </div>
            </div>
        </div>
        <div class="bg-white w-full dark:hover:bg-accent my-6 hover:bg-slate-50 cursor-pointer dark:hover:shadow-md dark:bg-black hover:app-shadow rounded-md border-color border-solid border p-2 shadow-lg dark:shadow-md dark:shadow-slate-100/30">
            <div class="flex flex-row justify-between align-middle items-center">
                <div>
                </div>
                <div class="flex flex-col items-end align-middle gap-4">
                    <p class="text-lg font-mono">-$2,000</p>
                    <p class="text-sm">12-12-2023, 02:10:59 PM</p>
                </div>
            </div>
        </div>
	</div>
</div>
