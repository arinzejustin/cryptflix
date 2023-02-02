<script lang="ts">
	import Loader from '$lib/Loader.svelte';
	import { onMount } from 'svelte';

	export let loading = true,
		src: string,
		open: boolean,
		height: number;

	let shadow = false;

	onMount(() => {
		addEventListener('scroll', () => {
			if (window.scrollY > 50) shadow = true;
			else shadow = false;
		});
		if (window.scrollY > 50) shadow = true;
		//@ts-ignore
		height = document.querySelector('#header')!.offsetHeight;
		onresize = () => {
			//@ts-ignore
			height = document.querySelector('#header')!.offsetHeight;
		};
	});
</script>

<header class="relative">
	<div
	id="header"
		class="fixed bg-white transition-all duration-500 dark:bg-black text-slate-700 dark:text-slate-100 right-0 top-0 border-solid border-b border-slate-300 dark:border-slate-500 {open
			? 'left-[256px]'
			: 'left-0'} {shadow
			? 'shadow-lg dark:shadow-md dark:shadow-slate-600 backdrop-blur-md bg-white/[0.75] dark:bg-black/[0.65]'
			: ''}"
	>
		<div
			class="flex flex-row items-center align-middle justify-between mx-4 py-4 md:py-6"
		>
			<div class="flex flex-row items-center align-middle justify-between">
				<div class="md:hidden">
					<svg
						class="text-slate-700 dark:text-white w-8 h-8"
						xmlns="http://www.w3.org/2000/svg"
						width="1em"
						height="1em"
						viewBox="0 0 24 24"
						><rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
							fill="currentColor"
							d="M4 18q-.425 0-.712-.288Q3 17.425 3 17t.288-.712Q3.575 16 4 16h16q.425 0 .712.288q.288.287.288.712t-.288.712Q20.425 18 20 18Zm0-5q-.425 0-.712-.288Q3 12.425 3 12t.288-.713Q3.575 11 4 11h16q.425 0 .712.287q.288.288.288.713t-.288.712Q20.425 13 20 13Zm0-5q-.425 0-.712-.287Q3 7.425 3 7t.288-.713Q3.575 6 4 6h16q.425 0 .712.287Q21 6.575 21 7t-.288.713Q20.425 8 20 8Z"
						/></svg
					>
				</div>
				<div />
			</div>
			{#if loading}
				<div class="mr-4 md:mr-6">
					<Loader width={'30px'} height={'30px'} />
				</div>
			{:else}
				img> {src}
			{/if}
		</div>
	</div>
</header>
