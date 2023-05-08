<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import { cubicIn, cubicOut } from 'svelte/easing';
	import { goto } from '$app/navigation';
	import Alert from '$lib/Alert.svelte';
	import Api from '$lib/api';
	import Checkbox from '@smui/checkbox';
	import { setStorage } from '$lib/storage';
	import { retry } from '../../stores';

	let geneId = Math.random()
		.toString(36)
		.substring(2, 9 + 2);

	let googleGif = false,
		emailGif = false,
		appleGif = false,
		visible = false,
		checked = true;

	var valid: boolean,
		a = true,
		disabled = true,
		e_mail: string = '',
		passcode: string = '',
		pass = false,
		alert = false,
		msg = '',
		err = true,
		value = $retry,
		loggedIn = false;

	var isValid = (email: string) => {
			var regExp =
				/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			return regExp.test(email);
		},
		toast = (message: any, error: boolean) => {
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
		login = async () => {
			if (!checked || passcode == '') {
				toast('Fill all the fields', true);
				return;
			}
			emailGif = true;
			try {
				const req = await Api.post(
					'/login',
					JSON.stringify({
						email: e_mail,
						pass: passcode
					})
				);
				if ('status' in req) {
					toast(req.message, !req.status);
					emailGif = false;
					setStorage('token', req.bearer);
					setStorage('maogic', req.maogic)
					if (req.status) {
						setTimeout(() => {
							loggedIn = true
							goto('/', { replaceState: true })
						}, 3000);
					}
					return;
				}
				emailGif = false;
				toast('An Error Occurred', true);
			} catch (error) {
				emailGif = false;
				//@ts-ignore
				toast(error.message, true);
			}
		},
		toggle = () => {
			const password = document.querySelector(`#p${geneId}`)!,
				type = password.getAttribute('type') === 'password' ? 'text' : 'password';
			password.setAttribute('type', type);
			visible = !visible;
		},
		auth = (e: Event, { google = false, apple = false }) => {
			e.preventDefault();
			googleGif = google;
			appleGif = apple;
			setTimeout(() => {
				toast('Authentication Failed', true);
				setTimeout(() => {
					googleGif = false;
					appleGif = false;
				}, 4000);
			}, 3000);
		};
</script>

<svelte:head>
	<title>Log In | cryptflixinvest.com</title>
</svelte:head>

<cryptflixinvest-login class="md:mx-10">
	<Alert {alert} message={msg} error={err} onClose={() => (alert = false)} />
	<div class="pg9a5nd hak0fbu {loggedIn ? 'hidden' : ''}">
		<div class="jonfdgct mx-4 sm:mx-20 sm:my-5 md:mt-2">
			<div class="lg:w-1/2 xl:w-5/12 px-2 py-6 sm:p-12 flex flex-col justify-center">
				<div class="intro-x mb-6 md:mb-4 flex items-center justify-center">
					<img alt="school" class="w-32 h-32" src="/logo.png" />
				</div>
				<div class="my-6 lg:my-2.5 _0itw21asd">
					<h1 class="text-xl lg:text-2xl xl:text-3xl font-bold text-center">
						SIGN INTO YOUR ACCOUNT
					</h1>
					<div class="hak0fbu flex-1 mt-8">
						<div class="_0itw21asd font-open">
							<button
								on:click={(event) => {
									auth(event, { google: true });
								}}
								class="hak0fbu border border-solid border-slate-300 max-w-xs font-bold shadow-sm rounded-lg py-3 bg-indigo-100 text-gray-800 flex items-center justify-center transition-all duration-300 ease-in-out focus:outline-none hover:shadow focus:shadow-sm focus:shadow-outline"
							>
								<div class="bg-white p-2 rounded-full">
									<svg class="w-6 h-6" viewBox="0 0 533.5 544.3">
										<path
											d="M533.5 278.4c0-18.5-1.5-37.1-4.7-55.3H272.1v104.8h147c-6.1 33.8-25.7 63.7-54.4 82.7v68h87.7c51.5-47.4 81.1-117.4 81.1-200.2z"
											fill="#4285f4"
										/>
										<path
											d="M272.1 544.3c73.4 0 135.3-24.1 180.4-65.7l-87.7-68c-24.4 16.6-55.9 26-92.6 26-71 0-131.2-47.9-152.8-112.3H28.9v70.1c46.2 91.9 140.3 149.9 243.2 149.9z"
											fill="#34a853"
										/>
										<path
											d="M119.3 324.3c-11.4-33.8-11.4-70.4 0-104.2V150H28.9c-38.6 76.9-38.6 167.5 0 244.4l90.4-70.1z"
											fill="#fbbc04"
										/>
										<path
											d="M272.1 107.7c38.8-.6 76.3 14 104.4 40.8l77.7-77.7C405 24.6 339.7-.8 272.1 0 169.2 0 75.1 58 28.9 150l90.4 70.1c21.5-64.5 81.8-112.4 152.8-112.4z"
											fill="#ea4335"
										/>
									</svg>
								</div>
								<span class="ml-4 font-open"> Sign in with Google </span>
								{#if googleGif}
									<div class="ml-3 t-g">
										<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
									</div>
								{/if}
							</button>
							<button
								on:click={(event) => {
									auth(event, { apple: true });
								}}
								class="hak0fbu max-w-xs mt-4 font-bold shadow-sm rounded-lg py-3 bg-black text-gray-50 flex items-center justify-center transition-all duration-300 ease-in-out focus:outline-none hover:shadow focus:shadow-sm focus:shadow-outline"
							>
								<div class="bg-white p-2 rounded-full">
									<svg
										class="w-6 h-6 text-black"
										xmlns="http://www.w3.org/2000/svg"
										width="1em"
										height="1em"
										viewBox="0 0 512 512"
										><path
											fill="currentColor"
											d="M349.13 136.86c-40.32 0-57.36 19.24-85.44 19.24c-28.79 0-50.75-19.1-85.69-19.1c-34.2 0-70.67 20.88-93.83 56.45c-32.52 50.16-27 144.63 25.67 225.11c18.84 28.81 44 61.12 77 61.47h.6c28.68 0 37.2-18.78 76.67-19h.6c38.88 0 46.68 18.89 75.24 18.89h.6c33-.35 59.51-36.15 78.35-64.85c13.56-20.64 18.6-31 29-54.35c-76.19-28.92-88.43-136.93-13.08-178.34c-23-28.8-55.32-45.48-85.79-45.48Z"
										/><path
											fill="currentColor"
											d="M340.25 32c-24 1.63-52 16.91-68.4 36.86c-14.88 18.08-27.12 44.9-22.32 70.91h1.92c25.56 0 51.72-15.39 67-35.11c14.72-18.77 25.88-45.37 21.8-72.66Z"
										/></svg
									>
								</div>
								<span class="ml-4 font-open"> Sign in with Apple </span>
								{#if appleGif}
									<div class="ml-3 t-g">
										<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
									</div>
								{/if}
							</button>
						</div>

						<div class="my-12 mb-8 border-b border-solid text-center">
							<div
								class="leading-none px-2 inline-block text-sm text-gray-600 tracking-wide font-medium bg-white transform translate-y-1/2"
							>
								Or sign in with your e-mail
							</div>
						</div>

						<div class="mb-8 {pass ? 'hidden' : ''}">
							<p class="text-center float-none mb-6 text-[15px] text-slate-600">
								Don't have an account yet ? <a href="/0auth/onboard" class="theme-text-app">
									Register</a
								>
							</p>
						</div>

						<div class="mx-auto max-w-xs">
							{#if a}
								<button
									on:click={(event) => (a = false)}
									transition:fade={{
										delay: 120,
										duration: 900,
										easing: cubicOut
									}}
									class="mt-5 {pass
										? 'hidden'
										: ''} tracking-wide font-semibold bg-black/[0.85] text-gray-50 hak0fbu py-4 rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center focus:shadow-outline focus:outline-none"
								>
									<div class="bg-white p-2 rounded-full">
										<svg
											class="w-5 h-5"
											xmlns="http://www.w3.org/2000/svg"
											aria-hidden="true"
											role="img"
											preserveAspectRatio="xMidYMid meet"
											viewBox="0 0 512 512"
											><rect x="0" y="0" width="512" height="512" fill="none" stroke="none" /><path
												fill="#96A9B2"
												d="M511.824 425.007c1.941-5.245-220.916-173.519-220.916-173.519c-27.9-20.589-42.574-20.913-70.164 0c0 0-222.532 168.138-220.659 173.311l-.045.038c.023.045.06.076.091.117a48.482 48.482 0 0 0 8.119 14.157c1.473 1.786 3.248 3.282 4.955 4.837l-.083.064c.136.121.317.177.453.298c7.235 6.454 16.359 10.634 26.495 11.827c.159.019.287.102.446.121h.612c1.541.147 3.006.517 4.584.517h420.721c20.717 0 38.269-13.028 45.241-31.291c.083-.136.211-.234.287-.374l-.137-.103z"
											/><path
												fill="#B9C5C6"
												d="M256.133 232.176L1.216 423.364V152.515c0-26.4 21.397-47.797 47.797-47.797h414.24c26.4 0 47.797 21.397 47.797 47.797v270.849L256.133 232.176z"
											/><path
												fill="#EDECE6"
												d="m4.189 135.896l217.645 170.949c27.47 20.271 41.918 20.591 69.083 0L508.22 136.167c-3.77-6.834-9.414-12.233-15.869-16.538l2.989-2.342c-7.295-6.641-16.62-10.946-26.971-12.058l-424.455.015c-10.322 1.097-19.662 5.417-26.942 12.043l2.967 2.313c-6.38 4.245-11.972 9.551-15.75 16.296z"
											/><path
												fill="#DCE2E2"
												d="M4.118 136.254C2.207 141.419 221.63 307.099 221.63 307.099c27.47 20.271 41.918 20.591 69.083 0c0 0 219.103-165.546 217.258-170.64l.045-.037c-.022-.045-.059-.074-.089-.115a47.732 47.732 0 0 0-7.994-13.939c-1.45-1.759-3.198-3.231-4.878-4.763l.082-.063c-.134-.119-.312-.175-.446-.294c-7.124-6.354-16.107-10.47-26.086-11.645c-.156-.019-.283-.1-.439-.119h-.602c-1.517-.145-2.96-.509-4.514-.509H48.81c-20.398 0-37.68 12.828-44.543 30.809c-.082.134-.208.231-.283.368l.134.102z"
											/><path
												fill="#597B91"
												d="M291.401 154.645h-38.632a6.155 6.155 0 0 0-6.155 6.155v21.722a6.155 6.155 0 0 0 6.155 6.155h31.415a6.155 6.155 0 0 1 6.155 6.155v11.616a6.155 6.155 0 0 1-6.155 6.155h-31.415a6.155 6.155 0 0 0-6.155 6.155v23.578a6.155 6.155 0 0 0 6.155 6.155h41.316a6.155 6.155 0 0 1 6.155 6.155v12.441a6.155 6.155 0 0 1-6.155 6.155h-75.76a6.155 6.155 0 0 1-6.155-6.155V136.461a6.155 6.155 0 0 1 6.155-6.155h74.81c3.749 0 6.627 3.322 6.092 7.033l-1.733 12.028a6.156 6.156 0 0 1-6.093 5.278z"
											/></svg
										>
									</div>
									<span class="ml-4">Sign in with e-mail</span>
								</button>
							{:else}
								<div>
									<div class="relative">
										<input
											on:keyup={validateEmail}
											transition:fade={{
												delay: 200,
												duration: 1000,
												easing: cubicIn
											}}
											class="hak0fbu transition duration-300 appearance-none block border-solid focus:ring-0 px-8 pl-4 py-4 rounded-lg font-medium bg-gray-50 border-2 border-gray-300 text-sm focus:outline-none focus:bg-white peer"
											type="email"
											aria-describedby="email_help"
											placeholder=" "
											bind:value={e_mail}
											id={geneId}
											spellcheck="false"
										/>
										<label
											for={geneId}
											class=" {a ? 'hidden' : ''} absolute text-sm text-slate-800 {valid
												? 'peer-focus:text-green-600'
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
									on:click={() => (
										(emailGif = true),
										setTimeout(() => {
											emailGif = false;
											a = true;
											pass = true;
										}, 5000)
									)}
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
										class="ml-4 w-6 h-6 inline-block align-middle overflow-hidden {emailGif
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
									{#if emailGif}
										<div class="ml-3">
											<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
										</div>
									{/if}
								</button>
							{/if}
							{#if pass}
								<div
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
													on:keyup={() => (valid = true)}
													class="hak0fbu border-solid px-8 pl-4 py-4 rounded-l-lg font-medium bg-gray-50 border-2 transition duration-300 border-gray-300 placeholder-gray-500 text-sm focus:outline-none focus:bg-white peer appearance-none"
													type="password"
													id={`p${geneId}`}
													placeholder=" "
													bind:value={passcode}
													spellcheck="false"
												/>
												<label
													for={`p${geneId}`}
													class=" {pass ? 'absolute' : 'relative'} text-sm text-slate-800 {valid
														? 'peer-focus:text-green-600'
														: 'peer-focus:text-red-600'} duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-gray-50 px-2 peer-focus:px-2 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1"
													>Passcode</label
												>
											</div>
										</div>
										<!-- svelte-ignore a11y-click-events-have-key-events -->
										<div
											on:click={toggle}
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
									<div class="intro-y flex items-center justify-center mt-5">
										<a
											class="transition p-4 w-full theme-text-app font-medium rounded-lg flex items-center justify-around hover:bg-yellow-100"
											href="/0auth/forgot-password"
											>Forgot Password <svg
												viewBox="0 0 24 24"
												aria-hidden="true"
												focusable="false"
												fill="none"
												xmlns="http://www.w3.org/2000/svg"
												stroke="currentColor"
												stroke-linecap="round"
												stroke-linejoin="round"
												class="inline-block overflow-hidden align-middle w-6 h-6"
												><line x1="5" x2="19" y1="12" y2="12" /><polyline
													points="12 5 19 12 12 19"
												/></svg
											></a
										>
									</div>
									<button
										disabled={emailGif}
										on:click={login}
										class="mt-5 tracking-wide font-semibold bg-black/90 text-gray-100 hak0fbu py-4 shadow rounded-lg hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-300 focus:shadow-outline focus:outline-none"
									>
										<span class="mr-3"> Login </span>
										{#if emailGif}
											<div class="ml-3">
												<img class="w-5 h-5" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
											</div>
										{/if}
									</button>
									<button
										on:click={() => ((pass = false), (a = false))}
										class="mt-5 tracking-wide font-semibold bg-transparent text-gray-800 hak0fbu py-4 shadow rounded-lg hover:text-white hover:bg-black transition-all duration-300 ease-in-out flex items-center justify-center border border-solid border-slate-700 focus:shadow-outline focus:outline-none"
									>
										<svg
											class="mr-3 w-6 h-6 inline-block align-middle overflow-hidden"
											viewBox="0 0 24 24"
											aria-hidden="true"
											focusable="false"
											fill="none"
											xmlns="http://www.w3.org/2000/svg"
											stroke="currentColor"
											stroke-linecap="round"
											stroke-linejoin="round"
											><g transform="rotate(180 12 12)"
												><line x1="5" x2="19" y1="12" y2="12" /><polyline
													points="12 5 19 12 12 19"
												/></g
											></svg
										>
										<span class="ml-3"> Back </span>
									</button>
								</div>
							{/if}
							<div class="flex flex-row justify-start align-middle items-center">
								<Checkbox bind:checked class="mr-1" />
								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<p
									on:click={() => (checked = !checked)}
									class="mt-6 text-sm text-gray-600 text-center ml-4"
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
					class="my-4 mx-10 relative xl:my-6 xl:mx-12  rounded-full hak0fbu bg-contain bg-center bg-no-repeat"
					style="background-image: url('/773m32QMjm9Yg4QxsDxl.png');"
				>
					<div class="absolute top-20 right-[18%]">
						<h1 class="uppercase font-open text-5xl text-slate-700">
							We are
							<div class="inline-block h-[1.5em] overflow-hidden align-middle ms-slider">
								<ul class="ms-slider__words list-none p-0 m-0 inline-block">
									<li
										class="ms-slider__word slider-1 leading-[1.3em] text-left block font-nunito font-black"
									>
										Committed
									</li>
									<li
										class="ms-slider__word slider-3 leading-[1.3em] text-left block font-nunito font-black"
									>
										tested
									</li>
									<li
										class="ms-slider__word slider-2 leading-[1.3em] text-left block font-nunito font-black"
									>
										Trusted
									</li>
									<!-- This last word needs to duplicate the first one to ensure a smooth infinite animation -->
									<li
										class="ms-slider__word slider-1 leading-[1.3em] text-left block font-nunito font-black"
									>
										Committed
									</li>
								</ul>
							</div>
						</h1>
					</div>
				</div>
			</div>
		</div>
	</div>
	<img class="hidden" src="/gif.gif" srcset="/gif.gif 2x" alt="" />
</cryptflixinvest-login>

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

	.slider-1 {
		@apply text-black;
	}

	.slider-2 {
		@apply text-[#daa12f];
	}

	.slider-3 {
		@apply text-teal-600;
	}

	.ms-slider {
		-webkit-mask-image: linear-gradient(transparent, white, white, white, transparent);
		mask-image: linear-gradient(transparent, white, white, white, transparent);
		mask-type: luminance;
		mask-mode: alpha;
	}

	.ms-slider__words {
		-webkit-animation-name: wordSlider;
		animation-name: wordSlider;
		-webkit-animation-timing-function: ease-out;
		animation-timing-function: ease-out;
		-webkit-animation-iteration-count: infinite;
		animation-iteration-count: infinite;
		-webkit-animation-duration: 7s;
		animation-duration: 7s;
	}

	@-webkit-keyframes wordSlider {
		0%,
		27% {
			transform: translateY(0%);
		}

		33%,
		60% {
			transform: translateY(-25%);
		}

		66%,
		93% {
			transform: translateY(-50%);
		}

		100% {
			transform: translateY(-75%);
		}
	}

	@keyframes wordSlider {
		0%,
		27% {
			transform: translateY(0%);
		}

		33%,
		60% {
			transform: translateY(-25%);
		}

		66%,
		93% {
			transform: translateY(-50%);
		}

		100% {
			transform: translateY(-75%);
		}
	}
</style>
