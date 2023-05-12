<script lang="ts">
	import { fly, fade } from 'svelte/transition';
	import { onMount } from 'svelte';
	import API from '$lib/api';
	import { getStorage } from '$lib/storage';
	import Alert from '$lib/Alert.svelte';
	import { cubicIn } from 'svelte/easing';
	import intlTelInput from 'intl-tel-input';

	let name = '',
		email = '',
		tel = '',
		country: 'us',
		code = 'us',
		passcode = '',
		deposit = Number('50.00'),
		plan = 'Plan 1',
		balance = Number('50.00'),
		aler: boolean,
		timeout: any,
		err: boolean,
		msg: string,
		visible = false,
		loading = false,
        token: string;
	var toast = (message: any, error: boolean) => {
			msg = message;
			err = error;
			aler = true;
			timeout = setTimeout(() => {
				aler = false;
				clearTimeout(timeout);
			}, 4400);
		},
		intl = () => {
			var input = document.querySelector('#phone')!;
			intlTelInput(input, {
				customPlaceholder: function (selectedCountryPlaceholder: string, selectedCountryData: any) {
					country = selectedCountryData.iso2;
					return 'e.g. ' + selectedCountryPlaceholder;
				},
				initialCountry: 'auto',
				geoIpLookup: (success: any, failure: any) => {
					fetch('https://ipinfo.io/json?token=d0ff16221e0afb')
						.then((response) => response.json())
						.then((resp) => {
							code = resp.country;
							success(code);
							return;
						});
					success(code);
				},
				autoPlaceholder: 'aggressive',
				separateDialCode: true,
				utilsScript: '/js/utils.js'
			});
		},
		toggle = (id: string, { v }: any) => {
			const password = document.querySelector(`#${id}`)!,
				type = password.getAttribute('type') === 'password' ? 'text' : 'password';
			password.setAttribute('type', type);
			visible = v;
		},
		upload = async () => {
            if(email == '' || name == '' || tel == '' || deposit < 50 || balance < 50) {
                toast('Fill all the fields', true)
                return;
            }
            loading = true;
            try {
                const add = await API.post('/admin/add', JSON.stringify({name: name, deposit: deposit, balance: balance, passcode: passcode, country: country, plan: plan, email: email, tel: tel}),
                {
						Authorization: token
					})
                if(add.status) email = '';
                toast(add.message, !add.status);
                loading = false;
            } catch (err: any) {
                loading = false
                toast(err.message, true)
            }
        };
	onMount(() => {
		setTimeout(() => intl(), 2000);
        token = getStorage('token') ?? ''
	});
</script>

<svelte:head>
	<title>Add Client | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>

<div in:fly={{ x: 300, delay: 1000 }} out:fly={{ x: -400, duration: 800 }} class="mt-4 pt-5">
	<Alert alert={aler} message={msg} error={err} onClose={() => (aler = false)} />
	<div class="override">
		<p class="py-4 text-center text-xl font-bold font-nunito">Add New Client</p>
		<div
			class="grid grid-cols-1 md:grid-cols-2 gap-8 pb-3 mb-2 justify-between align-middle items-center my-4 py-2"
		>
			<div class="py-0.5">
				<div class="relative">
					<input
						transition:fade={{
							delay: 200,
							duration: 1000,
							easing: cubicIn
						}}
						class="hak0fbu transition duration-300 appearance-none block focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 dark:bg-accent border-solid border-color text-sm focus:outline-none focus:bg-white peer"
						type="text"
						placeholder=" "
						bind:value={name}
						id="name"
						spellcheck="true"
						name="name"
					/>
					<label
						for="name"
						class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 dark:bg-accent dark:text-white px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
						>Client Name</label
					>
				</div>
			</div>
			<div class="py-0.5">
				<div class="relative">
					<input
						transition:fade={{
							delay: 200,
							duration: 1000,
							easing: cubicIn
						}}
						class="hak0fbu transition duration-300 appearance-none block focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 dark:bg-accent border-solid border-color text-sm focus:outline-none focus:bg-white peer"
						type="email"
						placeholder=" "
						bind:value={email}
						id="email"
						spellcheck="true"
						name="email"
					/>
					<label
						for="email"
						class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 dark:bg-accent dark:text-white px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
						>Client Email</label
					>
				</div>
			</div>
			<div class="py-0.5">
				<div class="relative">
					<input
						transition:fade={{
							delay: 200,
							duration: 1000,
							easing: cubicIn
						}}
						class="hak0fbu transition duration-300 appearance-none block focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 dark:bg-accent border-solid border-color text-sm focus:outline-none focus:bg-white peer"
						type="number"
                        step="0.01" min="0"
						placeholder=" "
						bind:value={balance}
						id="balance"
						spellcheck="true"
						name="balance"
					/>
					<label
						for="balance"
						class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 dark:bg-accent dark:text-white px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
						>Client Balance</label
					>
				</div>
			</div>
			<div class="py-0.5">
				<div class="relative">
					<input
						transition:fade={{
							delay: 200,
							duration: 1000,
							easing: cubicIn
						}}
						class="hak0fbu transition duration-300 appearance-none block focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 dark:bg-accent border-solid border-color text-sm focus:outline-none focus:bg-white peer"
						type="number"
						placeholder=" "
                        step="0.01" min="0"
						bind:value={deposit}
						id="deposit"
						spellcheck="true"
						name="deposit"
					/>
					<label
						for="deposit"
						class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 dark:bg-accent dark:text-white px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
						>Client Deposit</label
					>
				</div>
			</div>
			<div class="py-0.5 w-full">
				<input
					class="hak0fbu font-nunito border-solid px-8 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 dark:placeholder-gray-100 placeholder-gray-500 dark:bg-accent border-color text-sm focus:outline-none focus:bg-white"
					type="tel"
					id="phone"
                    name="phone"
					bind:value={tel}
				/>
			</div>
			<div class="flex items-center justify-center w-full gap-0 mt-4">
				<div class="w-full">
					<div class="relative">
						<input
							class="hak0fbu border-solid px-2 py-4 rounded-l-lg font-medium bg-gray-50 border-2 transition duration-300 border-gray-300 dark:placeholder-gray-100 placeholder-gray-500 dark:bg-accent border-color text-sm focus:outline-none focus:bg-white peer appearance-none"
							type="password"
							id="pass"
							placeholder=" "
							bind:value={passcode}
							spellcheck="false"
						/>
						<label
							for="pass"
							class="text-sm absolute text-slate-800 dark:bg-accent dark:text-white duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
							>Passcode</label
						>
					</div>
				</div>
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div
					on:click={() => {
						toggle('pass', { v: !visible });
					}}
					class="flex dark:bg-accent items-center shadow justify-center border-2 border-solid border-color bg-gray-300 p-3.5 rounded-r-lg"
				>
					<svg
						viewBox="0 0 24 24"
						aria-hidden="true"
						focusable="false"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						stroke="currentColor"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="StyledIconBase-sc-ea9ulj-0 bhLQRR w-6 h-6 cursor-pointer"
					>
						{#if visible}
							<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
							<circle cx="12" cy="12" r="3" />
						{:else}
							<path
								d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
							/><line x1="1" x2="23" y1="1" y2="23" />
						{/if}
					</svg>
				</div>
			</div>
			<div class="py-0.5 md:col-span-2">
				<div class="relative">
					<select
						bind:value={plan}
						id="plan"
						name="plan"
						class="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-700 appearance-none dark:text-gray-400 dark:border-gray-300 border-solid focus:outline-none focus:ring-0 focus:border-gray-200 peer"
					>
						<option value="Plan 1">Plan 1</option>
						<option value="Plan 2">Plan 2</option>
						<option value="Plan 3">Plan 3</option>
						<option value="V I P">V I P</option>
						<option value="Share 1">Share 1</option>
						<option value="Share 2">Share 2</option>
					</select>
					<label
						for="plan"
						class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-6 scale-75 top-2 z-10 origin-[0] bg-gray-50 dark:bg-accent dark:text-white px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
						>Client Plan</label
					>
				</div>
			</div>
		</div>
		<button
			disabled={loading}
			on:click={upload}
			class="my-5 tracking-wide font-semibold bg-black/90 text-gray-100 hak0fbu py-4 shadow rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-300 focus:shadow-outline focus:outline-none"
		>
			<span class="mr-3"> Login </span>
			{#if loading}
				<div class="ml-3">
					<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
				</div>
			{/if}
		</button>
	</div>
</div>
