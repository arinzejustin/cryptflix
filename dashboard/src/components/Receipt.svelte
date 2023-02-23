<script lang="ts">
	import { fade } from 'svelte/transition';
	export let status: string,
		date: string,
		wallet: string,
		amount: string,
		name: string,
		onClose: any,
		detail: string,
		open: boolean = false,
        session: string;
</script>

{#if open}
	<div
		in:fade
		out:fade
		tabindex="-1"
		class="fixed top-0 left-0 right-0 z-[999999999] w-full p-4 bg-black/50 backdrop-blur-sm overflow-x-hidden overflow-y-auto md:inset-0 h-modal md:h-full"
	>
		<div class="relative w-full mx-auto my-auto h-full max-w-md md:h-auto">
			<div
				class="relative bg-white rounded-lg border border-solid border-color shadow-lg dark:shadow-md dark:bg-black"
			>
				<div
					class="flex items-center justify-between p-5 border-b border-solid border-color rounded-t-lg"
				>
					<h3 class="text-xl font-medium text-center text-black dark:text-white">
						Transaction Details
					</h3>
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
				<div class="p-6  flex flex-row justify-between align-middle items-center">
					<p class="text-lg uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
						{detail}
					</p>
					<p class="text-base leading-relaxed text-black dark:text-white">
						{amount}
					</p>
				</div>
				<div class="flex justify-center w-full items-center align-middle my-4 mx-auto">
					<div
						class="flex w-full align-middle items-center before:border-color after:border-color before:border-b before:border-solid after:border-solid after:content-[''] before:w-1/4 before:content-[''] before:inline-block before:h-1 after:w-1/4 after:h-1 after:border-b after:border-1 after:inline-block"
					>
						<span
							class="rounded-full w-full text-center px-3 py-2 border-color border-solid border"
						>
							{date}
						</span>
					</div>
				</div>
				<div class="p-2 space-y-2 border-b border-color border-solid">
					<div class="py-3 px-6 flex flex-row justify-between align-middle items-center">
						<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
							status
						</p>
						<p class="text-sm uppercase leading-relaxed text-black dark:text-white">
							{status}
						</p>
					</div>
					<div class="py-3 px-6 flex flex-row justify-between align-middle items-center">
						<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
							wallet
						</p>
						<p class="text-sm leading-relaxed text-black dark:text-white">
							{wallet}
						</p>
					</div>
					<div class="py-3 px-6 flex flex-row justify-between align-middle items-center">
						<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
							account name
						</p>
						<p class="text-sm leading-relaxed text-black dark:text-white">
							{name}
						</p>
					</div>
					<div class="py-3 px-6 flex flex-row justify-between align-middle items-center">
						<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
							remark
						</p>
						<p class="text-sm uppercase leading-relaxed text-black dark:text-white">null</p>
					</div>
                    <div class="py-3 px-6 flex flex-row justify-between align-middle items-center">
						<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
							session id
						</p>
						<p class="text-sm uppercase leading-relaxed text-black dark:text-white">
                            {session}
                        </p>
					</div>
				</div>
				<div class="p-6 flex flex-row justify-between align-middle items-center">
					<p class="text-sm uppercase font-mono leading-relaxed text-gray-500 dark:text-gray-400">
						Transaction number
					</p>
					<p class="text-sm leading-relaxed text-black dark:text-white">1234567890</p>
				</div>
				<div
					class="flex justify-center items-center p-6 space-x-2 border-t border-gray-200 rounded-b dark:border-gray-600"
				>
					<button
						type="button"
						class="bg-yellow-100 w-full my-3 px-5 py-2.5 dark:bg-yellow-100/30 hover:ring-1 ring-yellow-300 dark:ring-yellow-100/50 ring-offset-2 theme-text-app rounded-full"
						>Share Receipt</button
					>
				</div>
			</div>
		</div>
	</div>
{/if}
