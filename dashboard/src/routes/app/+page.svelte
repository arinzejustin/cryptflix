<script>
	import { fly } from 'svelte/transition';
</script>

<svelte:head />

<div in:fly={{ x: 400 }} out:fly={{ x: -400 }} class="flex container">
	div>
</div>
