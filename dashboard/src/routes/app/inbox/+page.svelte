<script lang="ts">
	import { fly } from 'svelte/transition';
	import Tab, { Icon, Label } from '@smui/tab';
	import TabBar from '@smui/tab-bar';
	let tabs = [
		{
			icon: 'message',
			label: 'Message',
			target: 'message'
		},
		{
			icon: 'archive',
			label: 'archive',
			target: 'archive'
		}
	];
	let active = tabs[0];
</script>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="container">
	<div class="mb-8">
		<TabBar {tabs} let:tab bind:active class="override relative">
			<Tab {tab} target={tab.target}>
				<Icon class="material-icons">{tab.icon}</Icon>
				<Label class="font-open text-slate-900 dark:text-slate-50">{tab.label}</Label>
			</Tab>
		</TabBar>
		<div class="pt-4 my-6 override">
			{#if active.target == 'message'}
				<div in:fly={{ y: 300, delay: 300 }} out:fly={{ y: -300, duration: 500 }}>
					<p class="font-mono font-medium text-lg pb-4">INBOX</p>
					<div
						class="pt-5 border-dotted border-color border-2 rounded-md dark:bg-black/70 p-4 w-full"
					>
						<div class="text-center p-2 md:p-6">
							<svg
								class="w-10 h-10 mx-auto mb-3"
								xmlns="http://www.w3.org/2000/svg"
								width="1em"
								height="1em"
								viewBox="0 0 24 24"
								><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
									fill="currentColor"
									d="M2 8.994A5.99 5.99 0 0 1 8 3h8c3.313 0 6 2.695 6 5.994V21H8c-3.313 0-6-2.695-6-5.994V8.994zM14 11v2h2v-2h-2zm-6 0v2h2v-2H8z"
								/></svg
							>
							<p class="capitalize py-2 text-lg text-black dark:text-white font-open font-semibold">
								Your inbox is empty
							</p>
							<p class="text-gray-400">
								Deposit, withdrawal, and other important messages will be displayed here.
							</p>
						</div>
					</div>
				</div>
			{:else if active.target == 'archive'}
				<div in:fly={{ y: 300, delay: 300 }} out:fly={{ y: -300, duration: 500 }}>
					<p class="font-mono font-medium text-lg pb-4">ARCHIVE</p>
					<div
						class="pt-5 border-dotted border-color border-2 rounded-md dark:bg-black/70 p-4 w-full"
					>
						<div class="text-center p-2 md:p-6">
							<svg
								class="w-10 h-10 mx-auto mb-3"
								xmlns="http://www.w3.org/2000/svg"
								width="1em"
								height="1em"
								viewBox="0 0 24 24"
								><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
									fill="currentColor"
									><path
										d="M3.375 3C2.339 3 1.5 3.84 1.5 4.875v.75c0 1.036.84 1.875 1.875 1.875h17.25c1.035 0 1.875-.84 1.875-1.875v-.75C22.5 3.839 21.66 3 20.625 3H3.375Z"
									/><path
										fill-rule="evenodd"
										d="m3.087 9l.54 9.176A3 3 0 0 0 6.62 21h10.757a3 3 0 0 0 2.995-2.824L20.913 9H3.087ZM12 10.5a.75.75 0 0 1 .75.75v4.94l1.72-1.72a.75.75 0 1 1 1.06 1.06l-3 3a.75.75 0 0 1-1.06 0l-3-3a.75.75 0 1 1 1.06-1.06l1.72 1.72v-4.94a.75.75 0 0 1 .75-.75Z"
										clip-rule="evenodd"
									/></g
								></svg
							>
							<p class="capitalize py-2 text-lg text-black dark:text-white font-open font-semibold">
								no archived message
							</p>
							<p class="text-gray-400">Your archived messages will appear here</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
</style>
