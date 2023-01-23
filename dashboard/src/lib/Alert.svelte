<script lang="ts">
	import { scale, fade } from 'svelte/transition';
	export let alert = false,
		message = '',
		error = false,
		onClose: any;
</script>

{#if alert}
	<div
		in:scale
		out:fade
		class="md:rounded-lg ml-1 right-1 md:ml-0 border border-solid border-slate-200 dark:border-slate-200 bg-white dark:bg-black/60 w-[98%] md:w-1/4 shadow-xl fixed top-4 z-[1000] md:right-4"
	>
		<div class="flex flex-row justify-end align-middle items-center pt-2 mx-4">
			<div class="">
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<svg
					on:click={onClose}
					class="text-slate-400 dark:text-slate-50 w-4 h-4 font-extrabold"
					xmlns="http://www.w3.org/2000/svg"
					width="1em"
					height="1em"
					viewBox="0 0 24 24"
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
		<div class="pt-1 pb-6 pl-7 flex justify-start items-center">
			{#if !error}
			<svg
				fill="rgb(22 163 74 / var(--tw-text-opacity))"
				class="w-6 h-6 inline-block align-middle overflow-hidden text-green-600"
				xmlns="http://www.w3.org/2000/svg"
				width="1.2em"
				height="1.2em"
				viewBox="0 0 24 24"
				><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
					fill="currentColor"
					d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10s10-4.48 10-10S17.52 2 12 2zM9.29 16.29L5.7 12.7a.996.996 0 1 1 1.41-1.41L10 14.17l6.88-6.88a.996.996 0 1 1 1.41 1.41l-7.59 7.59a.996.996 0 0 1-1.41 0z"
				/></svg
			>
			{:else}
			<svg
				fill="rgb(220 38 38 / var(--tw-text-opacity))"
				class="w-5 inline-block h-5 align-middle overflow-hidden text-red-600"
				viewBox="0 0 24 24"
				width="1.2em"
				height="1.2em"
				><path
					d="M11.983 0a12.206 12.206 0 00-8.51 3.653A11.8 11.8 0 000 12.207 11.779 11.779 0 0011.8 24h.214A12.111 12.111 0 0024 11.791 11.766 11.766 0 0011.983 0zM10.5 16.542a1.476 1.476 0 011.449-1.53h.027a1.527 1.527 0 011.523 1.47 1.475 1.475 0 01-1.449 1.53h-.027a1.529 1.529 0 01-1.523-1.47zM11 12.5v-6a1 1 0 012 0v6a1 1 0 11-2 0z"
				/></svg
			>
			{/if}
			<span class="font-nunito text-slate-700 dark:text-slate-50 pl-4">{message}</span>
		</div>
		<div
			class="relative before:absolute md:before:rounded-bl-lg before:left-0 before:right-0 before:bottom-0 before:w-full before:border-[3px] before:border-solid {error
				? 'before:border-red-600'
				: 'before:border-green-600'} animate"
		/>
	</div>
{/if}

<style>
	.animate::before {
		content: '';
		animation: border_anim 4.5s linear forwards;
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
