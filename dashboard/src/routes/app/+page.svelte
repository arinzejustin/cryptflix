<script lang="ts">
	import { fly } from 'svelte/transition';
	import Icon from '../../components/Icon.svelte';
	import Plan from '../../components/Plan.svelte';
	import Password from '../../components/Password.svelte';
	import Alert from '$lib/Alert.svelte';
	import { onMount } from 'svelte';
	import { getStorage, setStorage } from '$lib/storage';

	let msg: string,
		plan = false,
		err: boolean,
		alert: boolean,
		timeout: any,
		referred: number = 0,
		refer_link: string = 'https://cryptoflixinvest.com/ref/1234567?token=',
		visible = false,
		change = false;

	var copy = (e: Event, { message, text }: any) => {
			e.preventDefault();
			clearTimeout(timeout);
			alert = false;
			navigator.clipboard.writeText(text);
			toast(`${message}`, false);
		},
		toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			alert = true;
			timeout = setTimeout(() => (alert = false), 4400);
		},
		wallet = '19ijqZ22wq7G8oVGQL8i3RxXrVYadsoJPU',
		acct_vis = () => {};
	onMount(() => {
		visible = getStorage('balance_visible') || false;
		acct_vis = () => {
			visible = !visible;
			setStorage('balance_visible', visible);
		};
	});
</script>

<svelte:head />

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div
		class="bg-yellow-100 w-full dark:bg-yellow-100/30 border border-solid border-yellow-200 shadow-lg rounded-md p-1 md:p-4"
	>
		<p class="font-bold font-open text-2xl md:text-3xl text-center pb-4 text-black dark:text-white">Welcome Arinze Justin</p>
		<div class="flex flex-col md:flex-row justify-between align-middle mx-1 md:mx-4 lg:mx-8">
			<div class="">
				<div class="grid grid-cols-5 gap-1 md:grid-cols-2 md:gap-4 items-center align-middle">
					<p class="font-bold text-black dark:text-white font-open truncate text-lg md:text-2xl col-span-2 md:col-span-1">
						Account Balance
					</p>
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<span class="pt-3 col-span-1" on:click={acct_vis}>
						{#if visible}
							<Icon className={'material-icons cursor-pointer'} name={'visibility'} />
						{:else}
							<Icon className={'material-icons cursor-pointer'} name={'visibility_off'} />
						{/if}
					</span>
					<p class="text-right md:hidden inline col-span-2">
						<a
							href="/app/transaction"
							class="text-sm inline truncate hover:underline transition-all duration-300"
							>Transaction histroy
							<Icon className={'material-icons inline align-middle'} name={'chevron_right'} />
						</a>
					</p>
				</div>
				<div class="py-2">
					{#if visible}
						<p class="text-xl w-1/2 text-center font-open font-medium">$105.5k</p>
					{:else}
						<p class="text-xl w-1/2 text-center font-open font-medium">******</p>
					{/if}
				</div>
				<div class="pt-6 hidden md:block">
					<span class="bg-black/20 dark:bg-black/40 p-1.5 mt-1.5 rounded-md block text-white">
						<Icon className={'material-icons inline align-middle mr-2 theme-text-app'} name={'date_range'} />
						Last Access at
						<b class="align-middle ml-1"> 3/3/2023, 12:05:49 AM </b>
					</span>
				</div>
			</div>
			<div class="">
				<p class="text-right hidden md:block">
					<a
						href="/app/transaction"
						class="text-sm inline truncate hover:underline transition-all duration-300"
						>Transaction histroy
						<Icon className={'material-icons inline align-middle'} name={'chevron_right'} />
					</a>
				</p>
				<div class="pt-3 grid grid-cols-3 gap-0 md:flex md:flex-row align-middle md:justify-evenly">
					<a
						href="/app/transaction/deposit"
						class="m-1.5 shadow-lg text-center text-white md:w-24 border border-solid rounded-md px-4 pt-4 pb-6 align-top border-color bg-black"
					>
						<Icon className={'material-icons mb-2.5 mt-1 text-[40px]'} name={'flight_land'} />
						<p>Deposit Funds</p>
					</a>
					<a
						href="/app/transaction/withdraw"
						class="m-1.5 shadow-lg text-center text-white md:w-24 border border-solid rounded-md px-4 pt-4 pb-6 align-top border-color bg-black"
					>
						<Icon className={'material-icons mb-2.5 mt-1 text-[40px]'} name={'flight_takeoff'} />
						<p>Withdraw Funds</p>
					</a>
					<a on:click={(e) => {(e.preventDefault()), (change = true)}}
						href="/app/settings"
						class="m-1.5 shadow-lg text-center text-white md:w-24 border border-solid rounded-md px-4 pt-4 pb-6 align-top border-color bg-black"
					>
						<Icon className={'material-icons mb-2.5 mt-1 text-[40px]'} name={'settings'} />
						<p>Change Password</p>
					</a>
				</div>
			</div>
		</div>
	</div>
	<div class="my-8 py-4 grid grid-cols-1 md:grid-cols-2 gap-8 align-middle pb-10">
		<div
			class="bg-white dark:bg-black hover:bg-slate-100 border relative my-5 border-solid border-color rounded-md shadow-md hover:shadow-lg dark:shadow-gray-100/50 dark:hover:bg-accent py-4 px-6 md:py-6 md:px-8"
		>
			<Icon className={'icon material-icons'} name={'wallet'} />
			<p class="theme-text-app text-right truncate text-3xl font-bold font-open pt-5">{wallet}</p>
			<p class="font-mono text-right">Your Wallet ID</p>
			<a
				on:click={(e) => {
					copy(e, { message: 'Wallet Copied', text: wallet });
				}}
				href="/app/wallet"
				class="bg-none flex flex-row pt-3 items-center align-middle justify-start text-sm w-full border-t border-solid border-color py-1.5 text-left mt-5 mx-auto mb-0"
			>
				<Icon className={'material-icons text-[30px]'} name={'content_copy'} />
				<span class="text-sm ml-4 font-open">Copy Wallet</span>
			</a>
		</div>
		<div
			class="bg-white dark:bg-black hover:bg-slate-100 border relative my-5 border-solid border-color rounded-md shadow-md hover:shadow-lg dark:shadow-gray-100/50 dark:hover:bg-accent py-4 px-6 md:py-6 md:px-8"
		>
			<Icon className={'icon material-icons'} name={'card_membership'} />
			<p class="theme-text-app text-right truncate text-3xl font-open font-bold pt-5">Plan 2</p>
			<p class="font-mono text-right">Account Type</p>
			<a
				on:click={(e) => {
					e.preventDefault(), (plan = true);
				}}
				href="/app/transaction/deposit"
				class="bg-none flex flex-row pt-3 items-center align-middle justify-start text-sm w-full border-t border-solid border-color py-1.5 text-left mt-5 mx-auto mb-0"
			>
				<Icon className={'material-icons text-[30px]'} name={'rocket'} />
				<span class="text-sm ml-4 font-open">Upgrade Account</span>
			</a>
		</div>
		<div
			class="bg-white dark:bg-black hover:bg-slate-100 border relative my-5 border-solid border-color rounded-md shadow-md hover:shadow-lg dark:shadow-gray-100/50 dark:hover:bg-accent py-4 px-6 md:py-6 md:px-8"
		>
			<Icon className={'icon material-icons'} name={'currency_bitcoin'} />
			<p class="theme-text-app text-right truncate text-3xl font-bold">$100k</p>
			<p class="font-mono text-right">Total Deposit</p>
			<a
				href="/app/transaction/deposit"
				class="bg-none flex flex-row pt-3 items-center align-middle justify-start text-sm w-full border-t border-solid border-color py-1.5 text-left mt-5 mx-auto mb-0"
			>
				<svg
					class="w-6 h-6 mt-1.5"
					xmlns="http://www.w3.org/2000/svg"
					width="1.13em"
					height="1em"
					viewBox="0 0 512 512"
				>
					<rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
						fill="currentColor"
						d="M298.9 24.31c-14.9.3-25.6 3.2-32.7 8.4l-97.3 52.1l-54.1 73.59c-11.4 17.6-3.3 51.6 32.3 29.8l39-51.4c49.5-42.69 150.5-23.1 102.6 62.6c-23.5 49.6-12.5 73.8 17.8 84l13.8-46.4c23.9-53.8 68.5-63.5 66.7-106.9l107.2 7.7l-1-112.09l-194.3-1.4zM244.8 127.7c-17.4-.3-34.5 6.9-46.9 17.3l-39.1 51.4c10.7 8.5 21.5 3.9 32.2-6.4c12.6 6.4 22.4-3.5 30.4-23.3c3.3-13.5 8.2-23 23.4-39zm-79.6 96c-.4 0-.9 0-1.3.1c-3.3.7-7.2 4.2-9.8 12.2c-2.7 8-3.3 19.4-.9 31.6c2.4 12.1 7.4 22.4 13 28.8c5.4 6.3 10.4 8.1 13.7 7.4c3.4-.6 7.2-4.2 9.8-12.1c2.7-8 3.4-19.5 1-31.6c-2.5-12.2-7.5-22.5-13-28.8c-4.8-5.6-9.2-7.6-12.5-7.6zm82.6 106.8c-7.9.1-17.8 2.6-27.5 7.3c-11.1 5.5-19.8 13.1-24.5 20.1c-4.7 6.9-5.1 12.1-3.6 15.2c1.5 3 5.9 5.9 14.3 6.3c8.4.5 19.7-1.8 30.8-7.3c11.1-5.5 19.8-13 24.5-20c4.7-6.9 5.1-12.2 3.6-15.2c-1.5-3.1-5.9-5.9-14.3-6.3c-1.1-.1-2.1-.1-3.3-.1zm-97.6 95.6c-4.7.1-9 .8-12.8 1.9c-8.5 2.5-13.4 7-15 12.3c-1.7 5.4 0 11.8 5.7 18.7c5.8 6.8 15.5 13.3 27.5 16.9c11.9 3.6 23.5 3.5 32.1.9c8.6-2.5 13.5-7 15.1-12.3c1.6-5.4 0-11.8-5.8-18.7c-5.7-6.8-15.4-13.3-27.4-16.9c-6.8-2-13.4-2.9-19.4-2.8z"
					/>
				</svg>
				<span class="text-sm ml-3 font-open">Make New Deposit</span>
			</a>
		</div>
		<div
			class="bg-white dark:bg-black hover:bg-slate-100 border relative my-5 border-solid border-color rounded-md shadow-md hover:shadow-lg dark:shadow-gray-100/50 dark:hover:bg-accent py-4 px-6 md:py-6 md:px-8"
		>
			<Icon className={'icon material-icons'} name={'diversity_3'} />
			<p class="theme-text-app text-right truncate text-3xl font-bold">{referred}</p>
			<p class="font-mono text-right">Referred {referred > 1 ? 'Friends' : 'Friend'}</p>
			<a
				href="#refer"
				class="bg-none flex flex-row pt-3 items-center align-middle justify-start text-sm w-full border-t border-solid border-color py-1.5 text-left mt-5 mx-auto mb-0"
			>
				<Icon className={'material-icons text-[30px]'} name={'link'} />
				<span class="text-sm ml-4 font-open">Refer Friend's</span>
			</a>
		</div>
	</div>
	<div class="pt-7 pb-12 text-center px-0 mt-12 border-t border-solid border-color" id="refer">
		<Icon
			className={'material-icons theme-text-app border-b border-solid border-color mb-6 text-[100px]'}
			name={'link'}
		/>
		<h4 class="mb-3 font-bold uppercase text-xl md:text-3xl">Your Unique Referral Link</h4>
		<p class="mb-7">
			<a
				on:click={(e) => {
					copy(e, { message: 'Referring Link Copied', text: refer_link });
				}}
				href={refer_link}
				class="font-open py-2 my-5 px-5 truncate rounded-md text-sm text-gray-400 border-color hover:border-color lg:border-transparent border-solid border"
				>{refer_link}</a
			>
		</p>
		<span class="mt-7">
			<a
				on:click={(e) => {
					copy(e, { message: 'Referring Link Copied', text: refer_link });
				}}
				href={refer_link}
				class="rounded-md truncate text-xs md:text-sm bg-yellow-100 py-2 px-6 dark:bg-yellow-100/30 theme-text-app"
				>Use these banner tools to promote your referral link in an effective way.</a
			>
		</span>
	</div>
</div>
<Plan active={plan} onClose={() => (plan = false)} />
<Password {change} onClose={() => (change = false)} />
