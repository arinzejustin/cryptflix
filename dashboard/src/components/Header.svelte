<script lang="ts">
	import Loader from '$lib/Loader.svelte';
	import { onMount } from 'svelte';

	let top: number,
		shadow = false;

	onMount(() => {
		top = window.innerHeight;
		addEventListener('scroll', () => {
			if (window.scrollY > 50) shadow = true;
			else shadow = false;
		});
		addEventListener('DOMContentLoaded', () => {
			if (window.scrollY > 50) shadow = true;
		});
	});
</script>

<header class="mb-[100%] h-screen">
	<div
		class="fixed bg-white transition-all duration-500 dark:bg-black text-slate-700 dark:text-slate-100 right-0 left-0 top-0 w-full border-solid border-b border-slate-300 dark:border-slate-500 {shadow
			? 'shadow-lg dark:shadow-md dark:shadow-slate-100 backdrop-blur-md bg-white/[0.75] dark:bg-black/[0.65]'
			: ''}"
	>
		<div class="flex flex-row items-center align-middle justify-between mx-4 py-4 md:py-6">
			<div class="">
				{top ? top : 0}
			</div>
			<div class="">
				<Loader width={'20px'} height={'20px'} />
			</div>
		</div>
	</div>
</header>
