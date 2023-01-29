<script>
	import App from './app/+page.svelte';
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
</script>

<svelte:head>
	<title>Dashboard | cryptflixinvest.com</title>
</svelte:head>

<div>
	<Header />
</div>
<section>
	<App />
</section>
<div>
	<Footer />
</div>
