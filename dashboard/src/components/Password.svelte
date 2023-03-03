<script lang="ts">
	import API from '$lib/api';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import Ripple from '@smui/ripple';
	import Alert from '$lib/Alert.svelte';

	export let change = false, onClose: any;

	let msg: string,
		err: boolean,
		alert: boolean,
		pass: string,
		next = () => {},
		load__ = false;

	var toast = (message: any, error: boolean) => {
		msg = message;
		err = error;
		alert = true;
		setTimeout(() => (alert = false), 4400);
	};
</script>

{#if change}
	<div
		in:fly={{ y: 200 }}
		out:fly={{ y: -400 }}
		tabindex="-1"
		class="fixed top-0 bottom-0 left-0 right-0 z-[999999] w-full p-4 bg-black/50 backdrop-blur-sm overflow-x-hidden overflow-y-auto md:inset-0 h-modal md:h-full"
	>
		<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
		<div class="relative w-full mx-auto my-auto h-full max-w-md md:h-auto">
			<div
				class="relative top-1/2 bg-white rounded-lg border border-solid border-color shadow-lg dark:shadow-md dark:bg-black"
			>
				<div
					class="flex items-center justify-between p-5 border-b border-solid border-color rounded-t-lg"
				>
					<h3 class="text-xl font-medium text-center font-mono">Change Password</h3>
					<button
						on:click={onClose}
						type="button"
						class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white"
					>
						<svg
							aria-hidden="true"
							class="w-5 h-5"
							fill="currentColor"
							viewBox="0 0 20 20"
							xmlns="http://www.w3.org/2000/svg"
							><path
								fill-rule="evenodd"
								d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
								clip-rule="evenodd"
							/></svg
						>
						<span class="sr-only">Close modal</span>
					</button>
				</div>
				<div class="py-3">
					<p class="text-center pb-4 font-semibold font-open">Enter Current Password</p>
					<input
						type="text"
						bind:value={pass}
						class="rounded-md border-solid border-color border w-9/10 mx-4 py-2 bg-transparent"
					/>
				</div>
				<div
					class="grid grid-cols-2 items-center align-middle mt-2 border-t border-solid border-color"
				>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						on:click={() => (change = false)}
						class="text-gray-400 py-4 text-center text-base border-r border-solid border-color"
						>Cancel</button
					>
					<button
						use:Ripple={{ surface: true, color: 'secondary' }}
						tabindex="0"
						on:click={next}
						class="text-black dark:text-white py-4 text-center text-base border-l border-solid border-color"
					>
						{#if !load__}
							<span>Next</span>
						{:else}
							<Loader width={'20px'} height={'20px'} />
						{/if}
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
