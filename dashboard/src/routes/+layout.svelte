<script lang="ts">
	import './styles.css';
	import '../../node_modules/svelte-material-ui/bare.css';
	import './animate.css';
	import { beforeNavigate, goto, afterNavigate } from '$app/navigation';
	import API from '$lib/api';
	import {retry} from './stores';
	let num = 0;

	$retry = num;

	beforeNavigate(({ to }) => {
		if (
			to!.route.id == '/0auth/login' ||
			to!.route.id == '/0auth/onboard' ||
			to!.route.id == '/0auth/forget' ||
			to!.route.id == '/0auth/logout' || to!.route.id == '/ref/'
		)
			return;
		else {
			user();
		}
	});

	var user = async () => {
		try {
			const user = await API.post('/user_details', JSON.stringify({ name: '' }), {
				Authorization: ''
			});
		} catch {
			if (num < 1) user();
			else {
				// goto('/0auth/login', { replaceState: true, keepFocus: true });
			}
			num++;
		}
	},
	update = async () => {
		try {
			const settings = await API.post('/user_settings', JSON.stringify({uuid: ''}), {
				Authorization: ''
			});
		} catch {
			
		}
	};
</script>

<div>
	<cryptflixinvest-app class="[--app:100%]">
		<slot />
	</cryptflixinvest-app>
</div>
