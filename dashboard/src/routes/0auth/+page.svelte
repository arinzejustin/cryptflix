<script>
	import Login from './login/+page.svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	onMount(() => {
		goto('/0auth/login', { replaceState: true, noScroll: true });
	});
</script>

<svelte:head>
	<title>Log In | cryptflixinvest.com</title>
</svelte:head>

<div>
	<Login />
</div>
