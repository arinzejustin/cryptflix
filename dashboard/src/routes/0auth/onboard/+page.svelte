<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import { cubicIn } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import Alert from '$lib/Alert.svelte';
	import Api from '$lib/api';
	import intlTelInput from 'intl-tel-input';
	import Checkbox from '@smui/checkbox';
	import { onMount } from 'svelte';
	import Textfield from '@smui/textfield';
	import { setStorage } from '$lib/storage';

	let emailId = Math.random()
			.toString(36)
			.substring(2, 9 + 2),
		loading = true,
		visible = false,
		code = 'us',
		first = '',
		last = '',
		tel = '',
		v_code = '',
		register = false,
		verification = false,
		profile = false,
		complete = false,
		resendGif = false,
		ok = true,
		country: string;

	var valid = true,
		checked = false,
		loadGif = false,
		e_mail: string = '',
		alert = false,
		msg = '',
		err = true,
		disabled = true,
		times = 0,
		vis = false,
		pass = '',
		confirm = '',
		uuid: null;

	var isValid = (email: string) => {
			var regExp =
				/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			return regExp.test(email);
		},
		toast = (message: string, error: boolean) => {
			alert = false;
			msg = message;
			err = error;
			alert = true;
			setTimeout(() => (alert = false), 4400);
		},
		validateEmail = () => {
			if (!isValid(e_mail)) {
				disabled = true;
				valid = false;
			} else {
				disabled = false;
				valid = true;
			}
		},
		toggle = (id: string, { v, v2 }: any) => {
			const password = document.querySelector(`#${id}`)!,
				type = password.getAttribute('type') === 'password' ? 'text' : 'password';
			password.setAttribute('type', type);
			visible = v;
			vis = v2;
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
		onboard = async () => {
			if (!checked || first == '' || last == '' || tel == '') {
				toast('Fill all the fields', true);
				loadGif = false;
				return;
			}
			try {
				const req = await Api.post(
					'/onboard',
					JSON.stringify({ email: e_mail, name: `${first} ${last}`, tel: tel, country: country })
				);
				if ('status' in req) {
					register = req.status;
					if (req.double) verification = true;
					toast(req.message, !req.status);
					uuid = req.uuid;
					loadGif = false;
					return;
				}
				loadGif = false;
				toast('An Error Occurred', true);
			} catch (error) {
				loadGif = false;
				//@ts-ignore
				toast(error.message, true);
			}
		},
		verify = async () => {
			if (v_code == '' || !checked) return;
			loadGif = true;
			try {
				const req = await Api.post('/verify', JSON.stringify({ verify: v_code, email: e_mail }));
				if ('status' in req) {
					verification = req.status;
					toast(req.message, !req.status);
					loadGif = false;
					return;
				}
				loadGif = false;
				toast('An Error Occurred', true);
			} catch (error) {
				loadGif = false;
				//@ts-ignore
				toast(error.message, true);
			}
		},
		resend = async () => {
			if (times > 3) {
				toast('Exceeded Number Of Request', true);
				verification = true;
				return;
			}
			resendGif = true;
			try {
				const req = await Api.get('/email', JSON.stringify({ email: e_mail }));
				if ('status' in req) {
					toast(req.message, !req.status);
					resendGif = false;
					return;
				}
				resendGif = false;
				toast('An Error Occurred', true);
			} catch (error) {
				resendGif = false;
				//@ts-ignore
				toast(error.message, true);
			}
			times++;
		},
		check = () => {
			if (pass !== confirm) ok = false;
			else ok = true;
		},
		setup = () => {
			setTimeout(() => {
				complete = true;
				toast('Account Successfully Created', false);
				setTimeout(() => goto('/app', { replaceState: true, noScroll: true }), 4000);
			}, 5000);
		},
		create = async () => {
			if (pass == '' || confirm == '') return;
			loadGif = true;
			try {
				const req = await Api.post(
					'/password',
					JSON.stringify({ passcode: pass, confirm: confirm, uuid: uuid })
				);
				if ('status' in req) {
					profile = req.status;
					toast(req.message, !req.status);
					loadGif = false;
					if (req.status) {
						setStorage('token', req.bearer);
						setStorage('maogic', req.maogic);
					}
					return;
				}
				loadGif = false;
				toast('An Error Occurred', true);
			} catch (error) {
				loadGif = false;
				//@ts-ignore
				toast(error.message, true);
			}
		};

	onMount(() => {
		loading = false;
		setTimeout(() => intl(), 2000);
	});
</script>

<svelte:head>
	<title>Sign Up | cryptflixinvest.com</title>
	<link rel="stylesheet" href="/css/intlTelInput.min.css" />
</svelte:head>

<cryptflixinvest-onboard class="md:mx-10">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div class="pg9a5nd hak0fbu">
		<div class="jonfdgct mx-4 sm:mx-20 sm:my-5 md:mt-2">
			<div class="lg:w-1/2 xl:w-5/12 px-2 py-6 sm:p-12 lg:pt-4 flex flex-col justify-center">
				<div class="intro-x mb-6 md:mb-4 flex items-center justify-center">
					<img alt="school" class="w-32 h-32" src="/logo.png" />
				</div>
				<div class="my-6 lg:my-2.5 _0itw21asd">
					<h1 class="text-xl lg:text-2xl xl:text-3xl font-bold text-center">
						{#if !register}
							CREATE YOUR ACCOUNT
						{:else if register && !verification}
							VERIFY YOUR ACCOUNT
						{:else if register && verification && !profile}
							CREATE YOUR PASSCODE
						{:else}
							ACCOUNT SUCCESSFULLY CREATED
						{/if}
					</h1>
					<ol class="flex items-center w-full align-middle mx-auto my-5">
						<li
							class="flex w-full items-center after:border-solid {register
								? 'text-green-600 after:border-green-100'
								: 'text-gray-600 after:border-gray-100'} after:content-[''] after:w-full after:h-1 after:border-b after:border-4 after:inline-block"
						>
							<span
								class="flex items-center justify-center w-10 h-10 {register
									? 'bg-green-100'
									: 'bg-gray-100'} rounded-full lg:h-12 lg:w-12  shrink-0"
							>
								<svg
									aria-hidden="true"
									class="w-5 h-5 {register ? 'text-green-600' : 'text-gray-600'} lg:w-6 lg:h-6"
									fill="currentColor"
									viewBox="0 0 20 20"
									xmlns="http://www.w3.org/2000/svg"
								>
									{#if register}
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									{:else}
										<path
											fill-rule="evenodd"
											d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
											clip-rule="evenodd"
										/>
									{/if}
								</svg>
							</span>
						</li>
						<li
							class="flex w-full items-center after:border-solid {verification
								? 'text-green-600'
								: 'text-gray-600'} after:content-[''] after:w-full after:h-1 after:border-b {verification
								? 'after:border-green-100'
								: 'after:border-gray-100'} after:border-4 after:inline-block"
						>
							<span
								class="flex items-center justify-center w-10 h-10 {verification
									? 'bg-green-100'
									: 'bg-gray-100'} rounded-full lg:h-12 lg:w-12 shrink-0"
							>
								<svg
									aria-hidden="true"
									class="w-5 h-5 {verification ? 'text-green-600' : 'text-gray-600'} lg:w-6 lg:h-6"
									fill="currentColor"
									viewBox="0 0 {verification ? '20 20' : '32 32'}"
									xmlns="http://www.w3.org/2000/svg"
								>
									{#if verification}
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									{:else}
										<rect x="0" y="0" width="32" height="32" fill="none" stroke="none" /><path
											fill="currentColor"
											d="m11 23.18l-2-2.001l-1.411 1.41L11 26l6-6l-1.41-1.41L11 23.18zM28 30h-4v-2h4V16h-4V8a4.005 4.005 0 0 0-4-4V2a6.007 6.007 0 0 1 6 6v6h2a2.002 2.002 0 0 1 2 2v12a2.002 2.002 0 0 1-2 2z"
										/><path
											fill="currentColor"
											d="M20 14h-2V8A6 6 0 0 0 6 8v6H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V16a2 2 0 0 0-2-2ZM8 8a4 4 0 0 1 8 0v6H8Zm12 20H4V16h16Z"
										/>
									{/if}
								</svg>
							</span>
						</li>
						<li
							class="flex w-full items-center after:border-solid {profile
								? 'text-green-600'
								: 'text-gray-600'} after:content-[''] after:w-full after:h-1 after:border-b {profile
								? 'after:border-green-100'
								: 'after:border-gray-100'} after:border-4 after:inline-block"
						>
							<span
								class="flex items-center justify-center w-10 h-10 {profile
									? 'bg-green-100'
									: 'bg-gray-100'} rounded-full lg:h-12 lg:w-12 dark:bg-gray-700 shrink-0"
							>
								<svg
									aria-hidden="true"
									class="w-5 h-5 {profile ? 'text-green-600' : 'text-gray-600'} lg:w-6 lg:h-6"
									fill="currentColor"
									viewBox="0 0 {profile ? '20 20' : '24 24'}"
									xmlns="http://www.w3.org/2000/svg"
								>
									{#if profile}
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									{:else}
										<rect x="0" y="0" width="24" height="24" fill="none" stroke="none" /><path
											fill="currentColor"
											d="M2 19v-2h20v2Zm1.15-6.05l-1.3-.75l.85-1.5H1V9.2h1.7l-.85-1.45L3.15 7L4 8.45L4.85 7l1.3.75L5.3 9.2H7v1.5H5.3l.85 1.5l-1.3.75l-.85-1.5Zm8 0l-1.3-.75l.85-1.5H9V9.2h1.7l-.85-1.45l1.3-.75l.85 1.45l.85-1.45l1.3.75l-.85 1.45H15v1.5h-1.7l.85 1.5l-1.3.75l-.85-1.5Zm8 0l-1.3-.75l.85-1.5H17V9.2h1.7l-.85-1.45l1.3-.75l.85 1.45l.85-1.45l1.3.75l-.85 1.45H23v1.5h-1.7l.85 1.5l-1.3.75l-.85-1.5Z"
										/>
									{/if}
								</svg>
							</span>
						</li>
						<li
							class="flex items-center w-full before:border-solid before:content-[''] before:w-full before:h-1 before:border-b {profile
								? 'before:border-green-100'
								: 'before:border-gray-100'} before:border-4 before:inline-block"
						>
							<span
								class="flex items-center justify-center w-10 h-10 {complete
									? 'bg-green-100'
									: 'bg-gray-100'} rounded-full lg:h-12 lg:w-12 dark:bg-gray-700 shrink-0"
							>
								<svg
									aria-hidden="true"
									class="w-5 h-5 {complete ? 'text-green-600' : 'text-gray-600'} lg:w-6 lg:h-6"
									fill="currentColor"
									viewBox="0 0 20 20"
									xmlns="http://www.w3.org/2000/svg"
								>
									{#if complete}
										<path
											fill-rule="evenodd"
											d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
											clip-rule="evenodd"
										/>
									{:else}
										<path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" /><path
											fill-rule="evenodd"
											d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
											clip-rule="evenodd"
										/>
									{/if}
								</svg>
							</span>
						</li>
					</ol>
					<div class="hak0fbu flex-1 mt-8 md:mt-5">
						<div class="mx-auto max-w-xs">
							<div class="my-4">
								{#if loading}
									<div class="my-8">
										<span class="css-12hya6r w-20 h-20 border-[black_black_transparent]" />
									</div>
								{:else if !register}
									<div
										transition:slide={{
											delay: 50,
											duration: 1000,
											easing: cubicIn
										}}
									>
										<div class="w-full mt-1 mb-3 py-1">
											<div class="relative">
												<input
													transition:fade={{
														delay: 200,
														duration: 1000,
														easing: cubicIn
													}}
													class="hak0fbu transition duration-300 appearance-none block border-solid focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 text-sm focus:outline-none focus:bg-white peer"
													type="text"
													placeholder=" "
													bind:value={first}
													id="First"
													spellcheck="true"
												/>
												<label
													for="First"
													class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
													>First Name</label
												>
											</div>
										</div>
										<div class="w-full mt-1 mb-3 py-1">
											<div class="relative">
												<input
													transition:fade={{
														delay: 200,
														duration: 1000,
														easing: cubicIn
													}}
													class="hak0fbu transition duration-300 appearance-none block border-solid focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 text-sm focus:outline-none focus:bg-white peer"
													type="text"
													placeholder=" "
													bind:value={last}
													id="Last"
													spellcheck="true"
												/>
												<label
													for="Last"
													class="absolute font-bold font-nunito text-[15px] text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
													>Last Name</label
												>
											</div>
										</div>
										<div class="w-full my-3 py-1">
											<input
												class="hak0fbu font-nunito  border-solid px-8 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 placeholder-gray-500 text-sm focus:outline-none focus:bg-white"
												type="tel"
												id="phone"
												bind:value={tel}
											/>
										</div>
										<div class="w-full my-3 py-1">
											<div class="relative">
												<input
													on:keyup={validateEmail}
													transition:fade={{
														delay: 200,
														duration: 1000,
														easing: cubicIn
													}}
													class="hak0fbu transition duration-300 appearance-none block border-solid focus:ring-0 px-2 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 text-sm focus:outline-none focus:bg-white peer"
													type="email"
													aria-describedby="email_help"
													placeholder=" "
													bind:value={e_mail}
													id={emailId}
													spellcheck="false"
												/>
												<label
													for={emailId}
													class="absolute font-bold text-[15px] font-nunito text-slate-800 {valid
														? 'peer-focus:text-slate-800'
														: 'peer-focus:text-red-600'} duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
													>Your Email</label
												>
											</div>
											{#if !valid}
												<p transition:slide class="text-red-500 text-sm text-center pt-3">
													Ouch !!! Invalid E-mail address
												</p>
											{/if}
										</div>
										<button
											on:click={() => ((loadGif = true), onboard())}
											{disabled}
											transition:fade={{
												delay: 200,
												duration: 1000,
												easing: cubicIn
											}}
											class="mt-5 tracking-wide font-semibold bg-black/90 text-gray-100 hak0fbu py-4 shadow rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-300 focus:shadow-outline focus:outline-none"
										>
											<span class="mr-3"> Next </span>
											<svg
												class="ml-4 w-6 h-6 inline-block align-middle overflow-hidden {loadGif
													? 'hidden'
													: ''}"
												viewBox="0 0 24 24"
												aria-hidden="true"
												focusable="false"
												fill="none"
												xmlns="http://www.w3.org/2000/svg"
												stroke="currentColor"
												stroke-linecap="round"
												stroke-linejoin="round"
												><line x1="5" x2="19" y1="12" y2="12" /><polyline
													points="12 5 19 12 12 19"
												/></svg
											>
											{#if loadGif}
												<div class="ml-3">
													<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
												</div>
											{/if}
										</button>
										<div class="mt-4">
											<p class="text-center float-none mb-6 text-[15px] text-slate-600">
												Already have an account ? <a href="/0auth/login" class="theme-text-app">
													Sign In</a
												>
											</p>
										</div>
									</div>
								{/if}
								{#if register && !verification}
									<div
										class="mx-auto"
										transition:slide={{
											delay: 200,
											duration: 1000,
											easing: cubicIn
										}}
									>
										<!-- svelte-ignore a11y-click-events-have-key-events -->
										<Textfield
											class="rounded-lg items-center w-full mx-auto font-nunito text-[15px]"
											variant="outlined"
											bind:value={v_code}
											label="Verification Code"
											prefix="C-"
											input$pattern={'\\d+(\\.\\d{2})?'}
										/>
										<button
											on:click={verify}
											disabled={loadGif}
											class="mt-5 tracking-wide font-semibold bg-black/90 text-gray-100 hak0fbu py-4 shadow rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-300 focus:shadow-outline focus:outline-none"
										>
											<span class="mr-3"> Verify </span>
											{#if loadGif}
												<div class="ml-3">
													<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
												</div>
											{/if}
										</button>
										<button
											on:click={resend}
											disabled={resendGif}
											class="mt-5 tracking-wide peer font-semibold bg-transparent text-gray-800 hak0fbu py-4 shadow rounded-lg hover:text-white hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-700 focus:shadow-outline focus:outline-none"
										>
											{#if resendGif}
												<span
													class="css-12hya6r w-5 h-5 peer-hover:border-[white_white_transparent] border-[black_black_transparent]"
												/>
											{:else}
												<span class="ml-3"> Resend Code </span>
											{/if}
										</button>
									</div>
								{/if}
								{#if register && verification && !profile}
									<div
										class="md:my-8"
										transition:slide={{
											delay: 200,
											duration: 1000,
											easing: cubicIn
										}}
									>
										<div class="flex items-center justify-center w-full gap-0 mt-4">
											<div class="w-full">
												<div class="relative">
													<input
														class="hak0fbu border-solid px-2 py-4 rounded-l-lg font-medium bg-gray-50 border-2 transition duration-300 border-gray-300 placeholder-gray-500 text-sm focus:outline-none focus:bg-white peer appearance-none"
														type="password"
														id="pass"
														placeholder=" "
														bind:value={pass}
														spellcheck="false"
													/>
													<label
														for="pass"
														class="text-sm absolute text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
														>Passcode</label
													>
												</div>
											</div>
											<!-- svelte-ignore a11y-click-events-have-key-events -->
											<div
												on:click={() => {
													toggle('pass', { v: !visible });
												}}
												class="flex items-center shadow justify-center border-2 border-solid border-slate-300 bg-gray-300 p-3.5 rounded-r-lg"
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
										<div class="flex items-center justify-center w-full gap-0 mt-4">
											<div class="w-full">
												<div class="relative">
													<input
														on:keyup={check}
														class="hak0fbu border-solid px-2 py-4 rounded-l-lg font-medium bg-gray-50 border-2 transition duration-300 border-gray-300 placeholder-gray-500 text-sm focus:outline-none focus:bg-white peer appearance-none"
														type="password"
														id="verify"
														placeholder=" "
														bind:value={confirm}
														spellcheck="false"
													/>
													<label
														for="verify"
														class="text-sm absolute text-slate-800 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
														>Confirm Passcode</label
													>
												</div>
											</div>
											<!-- svelte-ignore a11y-click-events-have-key-events -->
											<div
												on:click={() => {
													toggle('verify', { v2: !vis });
												}}
												class="flex items-center shadow justify-center border-2 border-solid border-slate-300 bg-gray-300 p-3.5 rounded-r-lg"
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
													{#if vis}
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
										{#if !ok}
											<p transition:slide class="my-4 text-center text-sm text-red-500">
												Passcode does not match !!!
											</p>
										{/if}
										<button
											disabled={!ok}
											on:click={create}
											class="mt-5 tracking-wide font-semibold bg-black/90 text-gray-100 hak0fbu py-4 shadow rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-300 focus:shadow-outline focus:outline-none"
										>
											<span class="mr-3"> Create </span>
											{#if loadGif}
												<div class="ml-3">
													<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
												</div>
											{/if}
										</button>
									</div>
								{/if}
								{#if register && verification && profile && !complete}
									<div class="hidden">{setup()}</div>
									<div class="my-8 justify-center align-middle">
										<span class="css-12hya6r w-20 border-4 h-20 border-[black_black_transparent]" />
									</div>
								{/if}
								{#if complete}
									<div class="mx-auto w-full">
										<div class="icon icon--success svg">
											<svg
												class="mx-auto"
												xmlns="http://www.w3.org/2000/svg"
												width="72px"
												height="72px"
											>
												<g fill="none" stroke="rgb(22 163 74)" stroke-width="2">
													<circle
														class="circle text-green-600"
														cx="36"
														cy="36"
														r="35"
														style="stroke-dasharray:240px, 240px; stroke-dashoffset: 480px;"
													/>
													<path
														class="path"
														d="M17.417,37.778l9.93,9.909l25.444-25.393"
														style="stroke-dasharray:50px, 50px; stroke-dashoffset: 0px;"
													/>
												</g>
											</svg>
										</div>
									</div>
								{/if}
							</div>
							<div class="flex flex-row justify-start align-middle items-center">
								<Checkbox bind:checked class="mr-1" disabled={register} />
								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<p
									on:click={() => (checked = !checked)}
									class="{register
										? 'pointer-events-none'
										: ''} mt-6 text-sm text-gray-600 text-center ml-3.5"
								>
									I agree to abide by cryptflixinvest's
									<a href="/" class="border-b border-gray-500 border-dotted"> Terms of Service </a>
									and
									<a href="/" class="border-b border-gray-500 border-dotted"> Privacy Policy </a>
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="flex-1 text-center hidden md:flex rounded-r-xl">
				<div
					class="my-4 mx-10 relative xl:my-6 xl:mx-12 rounded-full hak0fbu bg-contain bg-center bg-no-repeat"
					style="background-image: url('/773m32QMjm9Yg4QxsDxl.png');"
				/>
			</div>
		</div>
	</div>
	<img class="hidden" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
</cryptflixinvest-onboard>

<style>
	:disabled {
		@apply pointer-events-none;
	}
	.pg9a5nd {
		@apply container mx-auto;
	}
	.jonfdgct {
		@apply max-w-screen-xl m-2 bg-white flex justify-center flex-1;
	}
	._0itw21asd {
		@apply flex flex-col items-center;
	}

	.css-12hya6r {
		@apply mx-auto rounded-full border-solid border-2 text-center block bg-transparent;
		border-image: initial;
		animation: 0.8s linear 0s infinite normal both running animation;
	}

	@keyframes animation {
		0% {
			transform: rotate(0deg) scale(1);
		}
		50% {
			transform: rotate(180deg) scale(0.8);
		}
		100% {
			transform: rotate(360deg) scale(1);
		}
	}
	/* animations */

	@-webkit-keyframes checkmark {
		0% {
			stroke-dashoffset: 50px;
		}

		100% {
			stroke-dashoffset: 0;
		}
	}

	@-ms-keyframes checkmark {
		0% {
			stroke-dashoffset: 50px;
		}

		100% {
			stroke-dashoffset: 0;
		}
	}

	@keyframes checkmark {
		0% {
			stroke-dashoffset: 50px;
		}

		100% {
			stroke-dashoffset: 0;
		}
	}

	@-webkit-keyframes checkmarkcircle {
		0% {
			stroke-dashoffset: 240px;
		}

		100% {
			stroke-dashoffset: 480px;
		}
	}

	@-ms-keyframes checkmarkcircle {
		0% {
			stroke-dashoffset: 240px;
		}

		100% {
			stroke-dashoffset: 480px;
		}
	}

	@keyframes checkmarkcircle {
		0% {
			stroke-dashoffset: 240px;
		}

		100% {
			stroke-dashoffset: 480px;
		}
	}

	.path {
		-webkit-animation: checkmark 0.25s ease-in-out 0.7s backwards;
		animation: checkmark 0.25s ease-in-out 0.7s backwards;
		-webkit-animation-delay: 3s;
		animation-delay: 3s;
	}

	.circle {
		-webkit-animation: checkmarkcircle 0.6s ease-in-out backwards;
		animation: checkmarkcircle 0.6s ease-in-out backwards;
		-webkit-animation-delay: 2s;
		animation-delay: 2s;
	}
</style>
