<script lang="ts">
	import { slide } from 'svelte/transition';
	import { backIn } from 'svelte/easing';
	export let alert: boolean = false,
		message: string = '',
		error = false;
</script>

{#if alert}
	<div
		transition:slide={{
			delay: 200,
			duration: 1000,
			easing: backIn
		}}
		class="rounded-lg border border-solid bg-white dark:border-slate-400 border-slate-200 w-1/4 shadow-md fixed top-4 z-[1000] right-4"
	>
		<div class="flex flex-row justify-between align-middle items-center pt-2 mx-4">
			<div>
				<h1 class="{error ? 'text-red-500' : 'text-green-500'} font-nunito uppercase font-semibold text-lg md:text-xl">{error ? 'error' : 'success'}</h1>
			</div>
			<div class="">
				<svg class="{error ? 'text-red-500' : 'text-green-500'} w-6 h-6" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"
					><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><g
						transform="rotate(180 12 12)"
						><path
							fill="currentColor"
							d="m12 13.4l-4.9 4.9q-.275.275-.7.275q-.425 0-.7-.275q-.275-.275-.275-.7q0-.425.275-.7l4.9-4.9l-4.9-4.9q-.275-.275-.275-.7q0-.425.275-.7q.275-.275.7-.275q.425 0 .7.275l4.9 4.9l4.9-4.9q.275-.275.7-.275q.425 0 .7.275q.275.275.275.7q0 .425-.275.7L13.4 12l4.9 4.9q.275.275.275.7q0 .425-.275.7q-.275.275-.7.275q-.425 0-.7-.275Z"
						/></g
					></svg
				>
			</div>
		</div>
		<div class="pt-3 pb-6">
			<p class="text-center font-nunito">{{ message }}</p>
		</div>
		<div
			class="relative before:absolute before:left-0 before:right-0 before:bottom-0 before:w-full before:border-[3px] before:border-solid {error ? 'before:border-red-500' :'before:border-green-500'} animate"
		/>
	</div>
{/if}

<style>
	.animate::before {
		content: '';
		animation: border_anim 3s linear forwards;
	}
	@keyframes border_anim {
		0% {
			width: 100%;
		}
		100% {
			width: 0%;
		}
	}
</style>
