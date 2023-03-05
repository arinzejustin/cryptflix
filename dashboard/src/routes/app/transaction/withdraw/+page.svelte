<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';

	let msg: string, err: boolean, alert: boolean;

	var toast = (message: any, error: boolean) => {
		msg = message;
		err = error;
		alert = true;
		setTimeout(() => (alert = false), 4400);
	};
</script>

<div
	in:fly={{ x: 300, delay: 1000 }}
	out:fly={{ x: -400, duration: 800 }}
	class="mt-4 pt-5"
>
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div
		class="flex rounded-lg shadow-lg bg-gray-100 dark:bg-accent border border-solid border-color flex-row md:mr-2 override w-full items-center align-middle justify-between mb-4 p-4"
	>
		<div class="w-auto">
			<p class="font-nunito lg:pl-8 text-xl lg:text-2xl font-bold uppercase text-black dark:text-white">
				Account Balance 
			</p>
		</div>
		<div></div>
	</div>
	<div class="my-4 py-2 md:pl-3">
		<p class="text-xl text-center md:text-left font-medium font-mono uppercase">Withdrawal Request</p>
	</div>
	<div class="w-9/10 md:w-3/4 lg:w-2/3 mx-auto">
		<div></div>
	</div>
</div>
