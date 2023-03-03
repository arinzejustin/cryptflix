<script lang="ts">
	import API from '$lib/api';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import Loader from '$lib/Loader.svelte';
	import Password from '../../../components/Password.svelte';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';

	let msg: string,
		err: boolean,
		alert: boolean,
		fileinput: HTMLInputElement,
		avi: string = '/img/default.png',
		verified = true,
		country = 'ng',
		change = false;

	var toast = (message: any, error: boolean) => {
		msg = message;
		err = error;
		alert = true;
		setTimeout(() => (alert = false), 4400);
	};
	const onFileSelected = (e: Event) => {
		//@ts-ignore
		let image = e.target.files[0];
		let type = ['image/png', 'image/jpg', 'image/jpeg']
		if(!type.includes(image.type)) {
			console.log(image.type, type)
			toast('Files format not supported', true)
			return
		}
		let reader = new FileReader();
		reader.readAsDataURL(image);
		reader.onload = (e) => {
			//@ts-ignore
			avi = e.target.result;
		};
		reader.onerror = (e) => {
			toast(`ERROR: ${e}`, true);
		};
	};
</script>

<svelte:head>
	<title>Profile | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div class="md:mr-2 override w-full mb-4 pb-4">
		<div class="grid grid-cols-1 lg:grid-cols-5 gap-6 align-middle">
			<div class="lg:col-span-2 lg:ml-2">
				<p class="pb-6 text-xl hidden text-left pl-4 lg:block font-mono font-medium">
					Profile Picture
				</p>
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
				<p class="pb-6 text-xl text-center lg:text-left pl-4 font-mono font-medium">
					Profile Details
				</p>
				<div class="py-4 mx-2 md:mx-3 lg:mx-4">
					<div class="py-3 my-2">
						<label for="display" class="block mb-2 text-base font-mono">Display Name</label>
						<input
							type="text"
							name="display"
							id=""
							class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
						/>
					</div>
					<div class="py-3 my-2">
						<label for="email" class="block mb-2 text-base font-mono">Email</label>
						<input
							type="text"
							name="email"
							id=""
							disabled
							class="w-full py-2.5 pl-2 rounded-lg border-2 dark:bg-accent border-solid border-color"
						/>
						{#if verified}
							<p
								class="dark:bg-green-500/30 bg-green-500/80 text-white w-1/3 md:w-[25%] lg:w-[20%] text-center mx-auto px-2 py-1 rounded-md my-2"
							>
								<svg
									class="w-5 h-5 inline mr-2"
									xmlns="http://www.w3.org/2000/svg"
									width="32"
									height="32"
									viewBox="0 0 32 32"
									><rect x="0" y="0" width="32" height="32" fill="none" stroke="none" /><path
										fill="currentColor"
										d="M16 3C8.8 3 3 8.8 3 16s5.8 13 13 13s13-5.8 13-13c0-1.4-.188-2.794-.688-4.094L26.688 13.5c.2.8.313 1.6.313 2.5c0 6.1-4.9 11-11 11S5 22.1 5 16S9.9 5 16 5c3 0 5.694 1.194 7.594 3.094L25 6.688C22.7 4.388 19.5 3 16 3zm11.28 4.28L16 18.563l-4.28-4.28l-1.44 1.437l5 5l.72.686l.72-.687l12-12l-1.44-1.44z"
									/></svg
								>
								<span>Verified</span>
							</p>
						{:else}
							<p
								class="dark:bg-yellow-500/30 bg-yellow-200 theme-text-app dark:text-white  cursor-pointer w-[45%] lg:w-1/3 text-center mx-auto px-2 py-1 rounded-md my-2"
							>
								<svg
									class="w-5 h-5 inline mr-2"
									xmlns="http://www.w3.org/2000/svg"
									width="1024"
									height="1024"
									viewBox="0 0 1024 1024"
									><rect x="0" y="0" width="1024" height="1024" fill="none" stroke="none" /><path
										fill="currentColor"
										d="M928.99 755.83L574.6 203.25c-12.89-20.16-36.76-32.58-62.6-32.58s-49.71 12.43-62.6 32.58L95.01 755.83c-12.91 20.12-12.9 44.91.01 65.03c12.92 20.12 36.78 32.51 62.59 32.49h708.78c25.82.01 49.68-12.37 62.59-32.49c12.91-20.12 12.92-44.91.01-65.03zM554.67 768h-85.33v-85.33h85.33V768zm0-426.67v298.66h-85.33V341.32l85.33.01z"
									/></svg
								>
								<span>Verify Email</span>
							</p>
						{/if}
					</div>
					<div class="py-3 my-2 flex flex-row justify-between items-center align-middle">
						<div class="">
							<p class="block mb-2 text-base font-mono">Country</p>
							<div class="flex flex-row justify-start items-center align-middle">
								<div class="iti__flag iti__{country} mr-1 h-scale" />
								<span>{country.toUpperCase()}</span>
							</div>
						</div>
						<div class="">
							<p class="block mb-2 text-base font-mono">Currency</p>
							<p>USD - (Dollar)</p>
						</div>
					</div>
					<div class="py-3 my-2">
						<div class="intro-y flex items-center justify-center mt-5 group/item">
							<a
								on:click={(e) => {e.preventDefault(), change = true}}
								class="transition p-4 w-full theme-text-app font-medium rounded-lg flex items-center justify-around bg-yellow-100 dark:bg-yellow-100/30 hover:ring-yellow-200 ring-2 ring-offset-2 ring-offset-transparent ring-transparent"
								href="/0auth/change-password"
								>Change Password <svg
									viewBox="0 0 24 24"
									aria-hidden="true"
									focusable="false"
									fill="none"
									xmlns="http://www.w3.org/2000/svg"
									stroke="currentColor"
									stroke-linecap="round"
									stroke-linejoin="round"
									class="inline-block overflow-hidden animate-bounce-x transition-all duration-200 align-middle w-6 h-6"
									><line x1="5" x2="19" y1="12" y2="12" /><polyline
										points="12 5 19 12 12 19"
									/></svg
								></a
							>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
<Password {change} onClose={() => (change = false)} />