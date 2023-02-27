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
	class="container mt-4 pt-5"
>
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div
		class="md:mr-2 override w-full mb-4 pb-4"
	>
		<div class="grid grid-cols-1 lg:grid-cols-5 gap-6 align-middle">
			<div class="lg:col-span-2 lg:ml-2 relative">
                <img src="/img/default.png" class="rounded-full ring-2 ring-offset-4 ring-offset-transparent ring-gray-400 border-color  w-44 h-44 md:w-60 md:h-60 lg:w-72 lg:h-72 mx-auto" alt="" srcset="">
            </div>
            <div class="lg:col-span-3">

            </div>
		</div>
	</div>
</div>
