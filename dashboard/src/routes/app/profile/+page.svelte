<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';
	import Ripple from '@smui/ripple';

	let msg: string,
		err: boolean,
		alert: boolean,
		fileinput: HTMLInputElement,
		avi: string = '/img/default.png';

	var toast = (message: any, error: boolean) => {
		msg = message;
		err = error;
		alert = true;
		setTimeout(() => (alert = false), 4400);
	};
	const onFileSelected = (e: Event) => {
		//@ts-ignore
		let image = e.target.files[0];
		let reader = new FileReader();
		reader.readAsDataURL(image);
		reader.onload = (e) => {
			//@ts-ignore
			avi = e.target.result;
			window.alert('Image Set');
		};
		reader.onerror = (e) => {
			window.alert('ERROR: ' + e);
		};
	};
</script>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div class="md:mr-2 override w-full mb-4 pb-4">
		<div class="grid grid-cols-1 lg:grid-cols-5 gap-6 align-middle">
			<div class="lg:col-span-2 lg:ml-2">
				<p class="pb-6 text-2xl hidden text-left pl-4 lg:block">Profile Picture</p>
				<div class="relative">
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<img
						on:click={() => {
							fileinput.click();
						}}
						src={avi}
						class="rounded-full cursor-pointer peer ring-2 ring-offset-4 ring-offset-transparent ring-gray-400 border-color  w-44 h-44 md:w-60 md:h-60 lg:w-72 lg:h-72 mx-auto"
						alt=""
						srcset="{avi} 2x"
					/>
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						on:click={() => {
							fileinput.click();
						}}
						class="absolute peer-hover:opacity-100 opacity-0 hover:opacity-100 transition-all duration-300 bg-slate-100 dark:bg-accent border-solid border border-color rounded p-1 px-2 cursor-pointer left-2/3 bottom-8"
					>
						<svg
							class="w-4 h-4 inline"
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
								fill="currentColor"
								d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"
							/></svg
						>
						<span class="inline text-sm">Change</span>
					</div>
				</div>
				<input
					type="file"
					accept=".jpg,.jpeg,.png"
					class="hidden"
					on:change={(e) => onFileSelected(e)}
					bind:this={fileinput}
				/>
			</div>
			<div class="lg:col-span-3 mt-4 lg:mt-0">
				<p class="pb-6 text-2xl text-center lg:text-left pl-4">Profile Details</p>
				<div class="py-4" />
			</div>
		</div>
	</div>
</div>
