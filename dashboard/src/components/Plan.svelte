<script lang="ts">
	import { fly } from 'svelte/transition';
	export let active = false,
		onClose: any;
	let plans = [
			{
				name: 'Plan 1',
				duration: '24 Hours',
				profit: '20%',
				minimum: '$50',
				maximum: '$2, 999'
			},
			{
				name: 'Plan 2',
				duration: '48 Hours',
				profit: '50%',
				minimum: '$3, 000',
				maximum: '$9, 999'
			},
			{
				name: 'Plan 3',
				duration: '72 Hours',
				profit: '75%',
				minimum: '$10, 000',
				maximum: 'unlimited'
			},
			{
				name: 'V I P',
				duration: '48 Hours',
				profit: '100%',
				minimum: '$50, 000',
				maximum: 'Unlimited'
			},
			{
				name: 'Share 1',
				duration: 'Daily',
				profit: '30%',
				minimum: '$200',
				maximum: 'Unlimited'
			},
			{
				name: 'Share 2',
				duration: 'Daily',
				profit: '50%',
				minimum: '$2, 000',
				maximum: 'Unlimited'
			}
		],
		choose = (el: string) => {
			var active = document.querySelector('.plan-active')!,
				element = document.querySelector(`#${el}`)!;
			active.classList.remove('plan-active');
			element.classList.add('plan-active');
		};
</script>

{#if active}
	<div
		in:fly={{ y: 600 }}
		out:fly={{ y: -400 }}
		class="bg-white fixed scrollbar transform -translate-x-1/2 z-[10000] w-[95%] overflow-y-auto h-[96%] md:h-3/4 lg:w-2/3 -translate-y-1/2  top-1/2 left-1/2 dark:bg-black border-color border-solid border rounded-lg shadow-md dark:shadow-slate-400 p-2"
	>
		<div class="sticky w-full py-3 flex justify-end">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<svg
				on:click={onClose}
				class="md:w-8 md:h-8 h-6 w-6 cursor-pointer"
				xmlns="http://www.w3.org/2000/svg"
				width="1em"
				height="1em"
				viewBox="0 0 24 24"
				><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
					fill="currentColor"
					d="M13 12q-.425 0-.712-.288Q12 11.425 12 11V5q0-.425.288-.713Q12.575 4 13 4t.713.287Q14 4.575 14 5v3.6l5.9-5.9q.275-.275.7-.275q.425 0 .7.275q.275.275.275.7q0 .425-.275.7L15.4 10H19q.425 0 .712.287q.288.288.288.713t-.288.712Q19.425 12 19 12ZM2.7 21.3q-.275-.275-.275-.7q0-.425.275-.7L8.6 14H5q-.425 0-.713-.288Q4 13.425 4 13t.287-.713Q4.575 12 5 12h6q.425 0 .713.287q.287.288.287.713v6q0 .425-.287.712Q11.425 20 11 20t-.712-.288Q10 19.425 10 19v-3.6l-5.9 5.9q-.275.275-.7.275q-.425 0-.7-.275Z"
				/></svg
			>
		</div>
		<div class="w-full text-center my-4 pb-3">
			<p class="text-lg uppercase font-bold font-open">Our company's investment plan</p>
		</div>
		<div class="grid font-nunito md:grid-cols-2 lg:grid-cols-3 gap-4 my-5 mx-2">
			{#each plans as plan}
				<div
					id={plan.name.split(' ')[0] + plan.name.split(' ')[1]}
					class="{plan.name === 'V I P'
						? 'plan-active'
						: ''} group/item block w-auto border-color border border-solid rounded-lg shadow-lg dark:shadow-sm dark:shadow-slate-400/30"
				>
					<div class="flex flex-row font-open items-center align-middle">
						<div class="text-center w-1/2 inline-flex py-5 px-4">
							<p class="text-lg text-center">{plan.name}</p>
						</div>
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<div
							on:click={(e) => {
								choose(plan.name.split(' ')[0] + plan.name.split(' ')[1]);
							}}
							class="text-center w-1/2 cursor-pointer rounded-tr-lg inline-flex bg-yellow-100 dark:bg-yellow-100/30 theme-text-app py-5 px-4"
						>
							<p class="text-lg text-center w-1/2 mx-auto">Choose</p>
						</div>
					</div>
					<div class="mb-3 mt-5">
						<img src="/logo.png" class="w-28 h-28 mx-auto" alt="" srcset="/logo.png 2x" />
					</div>
					<div class="mb-4">
						<p class="font-semibold text-lg text-center underline uppercase theme-text-app">
							{plan.profit} {plan.name !== 'Share 1' && plan.name !== 'Share 2' ? 'after' : ''} {plan.duration}
						</p>
					</div>
					<div class="mb-2">
						<p class="font-semibold text-lg text-center uppercase">Minimum: {plan.minimum}</p>
					</div>
					<div class="mb-4">
						<p class="font-semibold text-lg text-center uppercase">maximum: {plan.maximum}</p>
					</div>
					<div class="pb-10 lg:pb-16 pt-5 text-center">
						<a
							href="/app/transaction/depoist"
							class="bg-yellow-100 opacity-0 group-hover transition-all duration-500 invest hover:ring-2 ring-offset-1 ring-yellow-200 shadow-md font-semibold dark:bg-yellow-100/30 theme-text-app px-10 py-3 text-base uppercase rounded-full"
							>Invest</a
						>
					</div>
				</div>
			{/each}
		</div>
	</div>
{/if}

<style scoped>
	.plan-active .invest {
		@apply opacity-100;
	}
</style>
